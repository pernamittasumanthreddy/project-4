"""HMS Pharmacy Purchasing & Goods Receipt Tests — Member 5"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.core.exceptions import ValidationError

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from pharmacy.models.catalogue import Medicine
from pharmacy.models.supplier import Supplier
from pharmacy.models.purchasing import PurchaseOrder, PurchaseOrderItem, POStatus, GoodsReceipt
from pharmacy.models.inventory import MedicineBatch
from pharmacy.services.purchasing_service import PurchasingService


@pytest.fixture
def setup_purchasing():
    tenant = Tenant.objects.create(name="Mercy Hospital", subdomain="mercy")
    hospital = Hospital.objects.create(tenant=tenant, name="Mercy General")
    branch = Branch.objects.create(hospital=hospital, name="East Clinic", code="EC1")
    manager = User.objects.create_user(
        username="mgr_user", password="Pass123!", role=UserRole.INVENTORY_MANAGER, tenant=tenant, branch=branch
    )
    admin = User.objects.create_user(
        username="admin_user", password="Pass123!", role=UserRole.HOSPITAL_ADMIN, tenant=tenant, branch=branch
    )
    supplier = Supplier.objects.create(
        tenant=tenant, code="SUP-TEST", name="Reliable Meds", phone="+1-555-9999"
    )
    med1 = Medicine.objects.create(
        tenant=tenant, code="MED-1", brand_name="Drug A", generic_name="Gen A", strength="100mg"
    )
    med2 = Medicine.objects.create(
        tenant=tenant, code="MED-2", brand_name="Drug B", generic_name="Gen B", strength="200mg"
    )
    return tenant, branch, manager, admin, supplier, med1, med2


@pytest.mark.django_db
class TestPurchasingAndGRN:

    def test_po_state_machine_flow(self, setup_purchasing):
        """Tests sequential progression DRAFT -> SUBMITTED -> APPROVED."""
        tenant, branch, manager, admin, supplier, med1, _ = setup_purchasing

        po = PurchaseOrder.objects.create(
            tenant=tenant, branch=branch, order_number="PO-TEST-01", supplier=supplier, created_by=manager
        )
        PurchaseOrderItem.objects.create(
            purchase_order=po, medicine=med1, quantity_ordered=Decimal("100.00"), unit_cost=Decimal("2.50")
        )
        po.recalculate_total()
        assert po.status == POStatus.DRAFT

        # 1. Submit PO
        PurchasingService.submit_purchase_order(po, manager)
        assert po.status == POStatus.SUBMITTED

        # 2. Approve PO
        PurchasingService.approve_purchase_order(po, admin)
        assert po.status == POStatus.APPROVED
        assert po.approved_by == admin
        assert po.approved_at is not None

    def test_reject_invalid_state_transition(self, setup_purchasing):
        """Confirms that directly approving a DRAFT order without prior submission is blocked."""
        tenant, branch, manager, admin, supplier, med1, _ = setup_purchasing

        po = PurchaseOrder.objects.create(
            tenant=tenant, branch=branch, order_number="PO-TEST-02", supplier=supplier, created_by=manager
        )
        PurchaseOrderItem.objects.create(
            purchase_order=po, medicine=med1, quantity_ordered=Decimal("50.00"), unit_cost=Decimal("1.00")
        )

        with pytest.raises(ValidationError):
            PurchasingService.approve_purchase_order(po, admin)

    def test_goods_receipt_partial_and_full_delivery(self, setup_purchasing):
        """Tests that goods receipt increments stock only for delivered items and transitions PO appropriately."""
        tenant, branch, manager, admin, supplier, med1, med2 = setup_purchasing
        today = date.today()

        po = PurchaseOrder.objects.create(
            tenant=tenant, branch=branch, order_number="PO-TEST-03", supplier=supplier,
            status=POStatus.APPROVED, created_by=manager
        )
        item1 = PurchaseOrderItem.objects.create(
            purchase_order=po, medicine=med1, quantity_ordered=Decimal("100.00"), unit_cost=Decimal("2.00")
        )
        item2 = PurchaseOrderItem.objects.create(
            purchase_order=po, medicine=med2, quantity_ordered=Decimal("50.00"), unit_cost=Decimal("5.00")
        )
        po.recalculate_total()

        # Step 1: Deliver partial delivery (only 40 units of Item 1)
        items_payload = [{
            'po_item_id': str(item1.id),
            'batch_number': 'BATCH-REC-01',
            'expiry_date': today + timedelta(days=365),
            'quantity_accepted': Decimal("40.00"),
            'quantity_rejected': Decimal("0.00")
        }]

        grn = PurchasingService.process_goods_receipt(
            po=po,
            delivery_reference="CHALLAN-991",
            items_payload=items_payload,
            receiver=manager
        )

        assert grn.id is not None
        po.refresh_from_db()
        assert po.status == POStatus.PARTIALLY_RECEIVED

        # Verify stock increased ONLY for med1
        assert med1.get_total_stock(branch) == Decimal("40.00")
        assert med2.get_total_stock(branch) == Decimal("0.00")
