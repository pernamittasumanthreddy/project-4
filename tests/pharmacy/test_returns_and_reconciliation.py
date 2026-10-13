"""HMS Pharmacy Returns & Reconciliation Tests — Member 5"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.core.exceptions import ValidationError

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from clinical.models import Patient, Prescription, PrescriptionItem
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.dispensing import DispenseRecord, DispensedItem
from pharmacy.models.returns import PatientReturn, ReturnCondition, StockQuarantine, QuarantineResolution
from pharmacy.models.reconciliation import CountSessionStatus
from pharmacy.services.returns_service import ReturnsService
from pharmacy.services.reconciliation_service import ReconciliationService


@pytest.fixture
def setup_returns():
    tenant = Tenant.objects.create(name="Metro Clinic", subdomain="metro")
    hospital = Hospital.objects.create(tenant=tenant, name="Metro Hospital")
    branch = Branch.objects.create(hospital=hospital, name="Day Clinic", code="DC1")
    pharmacist = User.objects.create_user(
        username="metro_rph", password="Pass123!", role=UserRole.PHARMACIST, tenant=tenant, branch=branch
    )
    admin = User.objects.create_user(
        username="metro_admin", password="Pass123!", role=UserRole.HOSPITAL_ADMIN, tenant=tenant, branch=branch
    )
    patient = Patient.objects.create(
        tenant=tenant, branch=branch, mrn="MRN-RET-1", full_name="Alice Brown", gender="FEMALE"
    )

    med = Medicine.objects.create(
        tenant=tenant, code="MED-RET-1", brand_name="Med R", generic_name="Gen R", strength="10mg", unit_price=Decimal("1.00")
    )
    today = date.today()
    batch = MedicineBatch.objects.create(
        tenant=tenant, branch=branch, medicine=med, batch_number="B-RET-1",
        expiry_date=today + timedelta(days=150), purchase_cost=Decimal("0.50"), selling_price=Decimal("1.00"),
        received_quantity=Decimal("50.00"), available_quantity=Decimal("50.00"), status=BatchStatus.ACTIVE
    )
    rx = Prescription.objects.create(
        tenant=tenant, branch=branch, patient=patient, prescriber=pharmacist, prescription_number="RX-RET-1"
    )
    p_item = PrescriptionItem.objects.create(
        prescription=rx, medicine_code="MED-RET-1", medicine_name="Med R",
        quantity_prescribed=Decimal("20.00"), quantity_dispensed=Decimal("20.00")
    )

    dispense = DispenseRecord.objects.create(
        tenant=tenant, branch=branch, dispense_number="DSP-RET-1", prescription=rx,
        pharmacist=pharmacist, total_amount=Decimal("20.00")
    )
    dispensed_item = DispensedItem.objects.create(
        dispense_record=dispense, prescription_item=p_item, medicine=med, batch=batch,
        quantity_dispensed=Decimal("20.00"), unit_price=Decimal("1.00")
    )

    return tenant, branch, pharmacist, admin, patient, med, batch, dispense, dispensed_item


@pytest.mark.django_db
class TestReturnsAndReconciliation:

    def test_patient_return_routes_strictly_to_quarantine(self, setup_returns):
        """Verifies patient returns are routed to quarantine and never directly into usable inventory."""
        tenant, branch, pharmacist, admin, patient, med, batch, dispense, dispensed_item = setup_returns

        init_available = batch.available_quantity

        p_return = ReturnsService.process_patient_return(
            dispense_record=dispense,
            dispensed_item_id=str(dispensed_item.id),
            quantity_returned=Decimal("5.00"),
            condition=ReturnCondition.SEALED_INTACT,
            reason="Adverse mild nausea",
            received_by=pharmacist
        )

        assert p_return.id is not None
        assert p_return.routed_to_quarantine is True
        assert p_return.refund_amount == Decimal("5.00")

        # Crucial check: Available stock must NOT have increased!
        batch.refresh_from_db()
        assert batch.available_quantity == init_available
        assert batch.quarantined_quantity == Decimal("5.00")

        # Verify quarantine record created
        quarantine = StockQuarantine.objects.filter(batch=batch).first()
        assert quarantine is not None
        assert quarantine.quantity == Decimal("5.00")

    def test_stock_count_session_reconciliation_workflow(self, setup_returns):
        """Tests physical stock audit, variance computation, and compensating adjustments."""
        tenant, branch, pharmacist, admin, patient, med, batch, _, _ = setup_returns

        # 1. Start audit session
        session = ReconciliationService.start_session(branch=branch, initiated_by=pharmacist)
        assert session.status == CountSessionStatus.IN_PROGRESS

        item = session.items.first()
        assert item.expected_quantity == batch.available_quantity

        # 2. Record physical count (Found 52 instead of 50 -> +2 surplus)
        ReconciliationService.update_item_count(
            item=item,
            physical_count=Decimal("52.00"),
            reason="Unrecorded sample pack recovered"
        )
        item.refresh_from_db()
        assert item.discrepancy_quantity == Decimal("2.00")

        # 3. Submit session
        ReconciliationService.submit_session_for_review(session, pharmacist)
        assert session.status == CountSessionStatus.SUBMITTED

        # 4. Approve session & post compensating ledger adjustment
        ReconciliationService.approve_session_and_post_adjustments(session, admin)
        assert session.status == CountSessionStatus.APPROVED

        # Verify stock adjusted to match physical count (52.00)
        batch.refresh_from_db()
        assert batch.available_quantity == Decimal("52.00")
