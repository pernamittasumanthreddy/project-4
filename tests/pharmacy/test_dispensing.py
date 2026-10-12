"""HMS Pharmacy Dispensing Integration Tests — Member 5"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.core.exceptions import ValidationError

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from clinical.models import Patient, Prescription, PrescriptionItem, PrescriptionStatus
from billing.models import BillingInvoice
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.dispensing import DispenseRecord
from pharmacy.services.dispensing_service import DispensingService


@pytest.fixture
def setup_dispensing():
    tenant = Tenant.objects.create(name="Hope Medical Network", subdomain="hope")
    hospital = Hospital.objects.create(tenant=tenant, name="Hope Hospital")
    branch = Branch.objects.create(hospital=hospital, name="Main Ward", code="MW1")
    pharmacist = User.objects.create_user(
        username="rx_user", password="Pass123!", role=UserRole.PHARMACIST, tenant=tenant, branch=branch
    )
    doctor = User.objects.create_user(
        username="dr_user", password="Pass123!", role=UserRole.DOCTOR, tenant=tenant, branch=branch
    )
    patient = Patient.objects.create(
        tenant=tenant, branch=branch, mrn="MRN-TEST-100", full_name="Robert Frost", gender="MALE"
    )

    med = Medicine.objects.create(
        tenant=tenant, code="MED-AUG-625", brand_name="Augmentin", generic_name="Amoxicillin Clavulanate",
        strength="625mg", unit_price=Decimal("2.50")
    )
    # Provision batch
    today = date.today()
    batch = MedicineBatch.objects.create(
        tenant=tenant, branch=branch, medicine=med, batch_number="AUG-BATCH-1",
        expiry_date=today + timedelta(days=200), purchase_cost=Decimal("1.50"), selling_price=Decimal("2.50"),
        received_quantity=Decimal("100.00"), available_quantity=Decimal("100.00"), status=BatchStatus.ACTIVE
    )

    rx = Prescription.objects.create(
        tenant=tenant, branch=branch, patient=patient, prescriber=doctor,
        prescription_number="RX-TEST-9001", status=PrescriptionStatus.PENDING
    )
    p_item = PrescriptionItem.objects.create(
        prescription=rx, medicine_code="MED-AUG-625", medicine_name="Augmentin",
        quantity_prescribed=Decimal("10.00"), quantity_dispensed=Decimal("0.00")
    )

    return tenant, branch, pharmacist, patient, med, batch, rx, p_item


@pytest.mark.django_db
class TestDispensingWorkflow:

    def test_dispense_prescription_fefo_and_billing(self, setup_dispensing):
        """Full fulfillment test: stock deduction via FEFO, status update, and billing generation."""
        tenant, branch, pharmacist, patient, med, batch, rx, p_item = setup_dispensing

        dispense_record = DispensingService.dispense_prescription(
            prescription=rx,
            pharmacist=pharmacist,
            notes="Fulfill outpatient course"
        )

        assert dispense_record.id is not None
        assert dispense_record.status == 'COMPLETED'
        assert dispense_record.total_amount == Decimal("25.00")  # 10 * 2.50

        # Verify stock deducted
        batch.refresh_from_db()
        assert batch.available_quantity == Decimal("90.00")

        # Verify prescription status marked DISPENSED
        rx.refresh_from_db()
        assert rx.status == PrescriptionStatus.DISPENSED

        # Verify prescription item quantity updated
        p_item.refresh_from_db()
        assert p_item.quantity_dispensed == Decimal("10.00")

        # Verify Billing invoice generated in Billing module
        invoice = BillingInvoice.objects.filter(tenant=tenant, reference_id=str(dispense_record.id)).first()
        assert invoice is not None
        assert invoice.total_amount == Decimal("25.00")

    def test_prevent_overdispensing(self, setup_dispensing):
        """Confirms system blocks dispensing more than authorized remaining quantity."""
        tenant, branch, pharmacist, patient, med, batch, rx, p_item = setup_dispensing

        payload = [{
            'prescription_item_id': str(p_item.id),
            'quantity_to_dispense': Decimal("50.00")  # Exceeds prescribed 10.00!
        }]

        with pytest.raises(ValidationError):
            DispensingService.dispense_prescription(
                prescription=rx,
                pharmacist=pharmacist,
                dispense_items_payload=payload
            )

    def test_prevent_duplicate_dispensing(self, setup_dispensing):
        """Confirms fulfilled prescriptions cannot be dispensed a second time."""
        tenant, branch, pharmacist, patient, med, batch, rx, p_item = setup_dispensing

        DispensingService.dispense_prescription(prescription=rx, pharmacist=pharmacist)

        # Attempting second time must raise ValidationError
        with pytest.raises(ValidationError):
            DispensingService.dispense_prescription(prescription=rx, pharmacist=pharmacist)
