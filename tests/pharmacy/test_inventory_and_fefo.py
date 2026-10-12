"""HMS Pharmacy Inventory & FEFO Allocation Tests — Member 5"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.core.exceptions import ValidationError

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.ledger import MovementType, StockMovement
from pharmacy.services.fefo_service import FEFOService, InsufficientStockError, ExpiredStockError
from pharmacy.services.stock_service import StockService


@pytest.fixture
def setup_inventory():
    tenant = Tenant.objects.create(name="St. Jude Hospital", subdomain="stjude")
    hospital = Hospital.objects.create(tenant=tenant, name="St. Jude Main")
    branch = Branch.objects.create(hospital=hospital, name="Central Pharmacy", code="CP1")
    pharmacist = User.objects.create_user(
        username="test_rph", password="Pass123!", role=UserRole.PHARMACIST, tenant=tenant, branch=branch
    )
    medicine = Medicine.objects.create(
        tenant=tenant, code="MED-CIPRO", brand_name="Cipro", generic_name="Ciprofloxacin", strength="500mg"
    )
    return tenant, branch, pharmacist, medicine


@pytest.mark.django_db
class TestInventoryAndFEFO:

    def test_fefo_earliest_expiry_selected_first(self, setup_inventory):
        """Verifies that the batch expiring earliest is allocated first regardless of creation order."""
        tenant, branch, pharmacist, medicine = setup_inventory
        today = date.today()

        # Batch A: Expiring in 1 year
        batch_late = MedicineBatch.objects.create(
            tenant=tenant, branch=branch, medicine=medicine, batch_number="BATCH-LATE",
            expiry_date=today + timedelta(days=365), purchase_cost=Decimal("1.00"), selling_price=Decimal("2.00"),
            received_quantity=Decimal("100.00"), available_quantity=Decimal("100.00"), status=BatchStatus.ACTIVE
        )
        # Batch B: Expiring in 2 months (Created later, but expires EARLIER)
        batch_early = MedicineBatch.objects.create(
            tenant=tenant, branch=branch, medicine=medicine, batch_number="BATCH-EARLY",
            expiry_date=today + timedelta(days=60), purchase_cost=Decimal("1.00"), selling_price=Decimal("2.00"),
            received_quantity=Decimal("50.00"), available_quantity=Decimal("50.00"), status=BatchStatus.ACTIVE
        )

        allocations = FEFOService.allocate_batches(medicine=medicine, required_quantity=Decimal("30.00"), branch=branch)

        # Must allocate from batch_early first!
        assert len(allocations) == 1
        assert allocations[0]['batch'].batch_number == "BATCH-EARLY"
        assert allocations[0]['allocated_quantity'] == Decimal("30.00")

    def test_fefo_greedy_split_across_batches(self, setup_inventory):
        """Verifies multi-batch greedy allocation when required quantity exceeds single batch."""
        tenant, branch, pharmacist, medicine = setup_inventory
        today = date.today()

        batch_1 = MedicineBatch.objects.create(
            tenant=tenant, branch=branch, medicine=medicine, batch_number="B1",
            expiry_date=today + timedelta(days=60), purchase_cost=Decimal("1.00"), selling_price=Decimal("2.00"),
            received_quantity=Decimal("20.00"), available_quantity=Decimal("20.00"), status=BatchStatus.ACTIVE
        )
        batch_2 = MedicineBatch.objects.create(
            tenant=tenant, branch=branch, medicine=medicine, batch_number="B2",
            expiry_date=today + timedelta(days=120), purchase_cost=Decimal("1.00"), selling_price=Decimal("2.00"),
            received_quantity=Decimal("50.00"), available_quantity=Decimal("50.00"), status=BatchStatus.ACTIVE
        )

        # Request 35 units: 20 from B1, 15 from B2
        allocations = FEFOService.allocate_batches(medicine=medicine, required_quantity=Decimal("35.00"), branch=branch)
        assert len(allocations) == 2
        assert allocations[0]['batch'].batch_number == "B1"
        assert allocations[0]['allocated_quantity'] == Decimal("20.00")
        assert allocations[1]['batch'].batch_number == "B2"
        assert allocations[1]['allocated_quantity'] == Decimal("15.00")

    def test_expired_batches_strictly_excluded(self, setup_inventory):
        """Confirms expired batches are never included in eligible dispensing allocations."""
        tenant, branch, pharmacist, medicine = setup_inventory
        today = date.today()

        MedicineBatch.objects.create(
            tenant=tenant, branch=branch, medicine=medicine, batch_number="EXPIRED-BATCH",
            expiry_date=today - timedelta(days=5), purchase_cost=Decimal("1.00"), selling_price=Decimal("2.00"),
            received_quantity=Decimal("100.00"), available_quantity=Decimal("100.00"), status=BatchStatus.ACTIVE
        )

        with pytest.raises(InsufficientStockError):
            FEFOService.allocate_batches(medicine=medicine, required_quantity=Decimal("10.00"), branch=branch)

    def test_atomic_stock_deduction_and_ledger_entry(self, setup_inventory):
        """Validates StockService row-level locking deduction and immutable movement ledger."""
        tenant, branch, pharmacist, medicine = setup_inventory
        today = date.today()

        batch = MedicineBatch.objects.create(
            tenant=tenant, branch=branch, medicine=medicine, batch_number="STOCK-TEST",
            expiry_date=today + timedelta(days=200), purchase_cost=Decimal("1.00"), selling_price=Decimal("2.00"),
            received_quantity=Decimal("100.00"), available_quantity=Decimal("100.00"), status=BatchStatus.ACTIVE
        )

        movement = StockService.deduct_stock(
            batch_id=batch.id,
            quantity=Decimal("25.00"),
            movement_type=MovementType.PRESCRIPTION_DISPENSE,
            reference_type="DispenseRecord",
            reference_id="TEST-REF-100",
            actor=pharmacist,
            reason="Patient dispensing test"
        )

        batch.refresh_from_db()
        assert batch.available_quantity == Decimal("75.00")
        assert movement.quantity_change == Decimal("-25.00")
        assert movement.quantity_before == Decimal("100.00")
        assert movement.quantity_after == Decimal("75.00")
        assert StockMovement.objects.filter(batch=batch).count() == 1

    def test_prevent_negative_stock(self, setup_inventory):
        """Confirms attempting to deduct more than available quantity raises ValidationError."""
        tenant, branch, pharmacist, medicine = setup_inventory
        today = date.today()

        batch = MedicineBatch.objects.create(
            tenant=tenant, branch=branch, medicine=medicine, batch_number="LOW-BATCH",
            expiry_date=today + timedelta(days=200), purchase_cost=Decimal("1.00"), selling_price=Decimal("2.00"),
            received_quantity=Decimal("10.00"), available_quantity=Decimal("10.00"), status=BatchStatus.ACTIVE
        )

        with pytest.raises(ValidationError):
            StockService.deduct_stock(
                batch_id=batch.id,
                quantity=Decimal("20.00"),
                movement_type=MovementType.PRESCRIPTION_DISPENSE,
                reference_type="Test",
                reference_id="REF-NEG",
                actor=pharmacist
            )
        # Verify batch was not modified
        batch.refresh_from_db()
        assert batch.available_quantity == Decimal("10.00")
