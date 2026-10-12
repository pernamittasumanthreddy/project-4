"""HMS Pharmacy Purchasing Service — Member 5
Implements Purchase Order state transitions and Goods Receipt Note (GRN) inward processing.
"""

from decimal import Decimal
from datetime import date, timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone as dj_timezone

from pharmacy.models.purchasing import (
    PurchaseOrder,
    PurchaseOrderItem,
    POStatus,
    GoodsReceipt,
    GoodsReceiptItem,
)
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.ledger import MovementType
from pharmacy.services.stock_service import StockService
from accounts.models import User
from core.permissions import record_audit_event


class PurchasingService:
    """Manages purchase order workflows and atomic goods receipt processing."""

    @classmethod
    def submit_purchase_order(cls, po: PurchaseOrder, actor: User) -> PurchaseOrder:
        """Transitions DRAFT -> SUBMITTED."""
        if po.status != POStatus.DRAFT:
            raise ValidationError(f"Cannot submit PO in status '{po.get_status_display()}'. Must be in DRAFT.")
        if not po.items.exists():
            raise ValidationError("Cannot submit an empty purchase order with no line items.")

        po.status = POStatus.SUBMITTED
        po.save(update_fields=['status', 'updated_at'])

        record_audit_event(
            tenant=po.tenant,
            branch=po.branch,
            actor=actor,
            event_type='PURCHASE_ORDER_SUBMITTED',
            resource_type='purchase_order',
            resource_id=po.id,
            details={'order_number': po.order_number, 'total': str(po.total_amount)}
        )
        return po

    @classmethod
    def approve_purchase_order(cls, po: PurchaseOrder, approver: User) -> PurchaseOrder:
        """Transitions SUBMITTED -> APPROVED."""
        if po.status != POStatus.SUBMITTED:
            raise ValidationError(f"Cannot approve PO in status '{po.get_status_display()}'. Must be SUBMITTED.")

        po.status = POStatus.APPROVED
        po.approved_by = approver
        po.approved_at = dj_timezone.now()
        po.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])

        record_audit_event(
            tenant=po.tenant,
            branch=po.branch,
            actor=approver,
            event_type='PURCHASE_ORDER_APPROVED',
            resource_type='purchase_order',
            resource_id=po.id,
            details={'order_number': po.order_number}
        )
        return po

    @classmethod
    def reject_purchase_order(cls, po: PurchaseOrder, approver: User, reason: str) -> PurchaseOrder:
        """Transitions SUBMITTED -> REJECTED."""
        if po.status != POStatus.SUBMITTED:
            raise ValidationError(f"Cannot reject PO in status '{po.get_status_display()}'. Must be SUBMITTED.")
        if not reason:
            raise ValidationError("Rejection reason is required.")

        po.status = POStatus.REJECTED
        po.approved_by = approver
        po.rejection_reason = reason
        po.save(update_fields=['status', 'approved_by', 'rejection_reason', 'updated_at'])
        return po

    @classmethod
    @transaction.atomic
    def process_goods_receipt(
        cls,
        po: PurchaseOrder,
        delivery_reference: str,
        items_payload: list,
        receiver: User,
        notes: str = ""
    ) -> GoodsReceipt:
        """Processes goods receipt against an approved PO, creates batches, and increments stock."""
        if po.status not in [POStatus.APPROVED, POStatus.PARTIALLY_RECEIVED]:
            raise ValidationError(
                f"Goods receipt can only be processed against APPROVED or PARTIALLY_RECEIVED orders. Current: {po.status}"
            )
        if not items_payload:
            raise ValidationError("No goods receipt items provided.")

        # Generate unique receipt number
        count = GoodsReceipt.objects.filter(tenant=po.tenant).count() + 1
        receipt_num = f"GRN-{po.branch.code if po.branch else 'HQ'}-{date.today().year}-{count:04d}"

        grn = GoodsReceipt.objects.create(
            tenant=po.tenant,
            branch=po.branch,
            receipt_number=receipt_num,
            purchase_order=po,
            delivery_reference=delivery_reference,
            received_by=receiver,
            notes=notes
        )

        for item_data in items_payload:
            po_item_id = item_data.get('po_item_id')
            po_item = PurchaseOrderItem.objects.select_for_update().get(id=po_item_id, purchase_order=po)

            qty_accepted = Decimal(str(item_data.get('quantity_accepted', '0.00')))
            qty_rejected = Decimal(str(item_data.get('quantity_rejected', '0.00')))
            qty_received = qty_accepted + qty_rejected

            if qty_received <= Decimal('0.00'):
                continue

            batch_number = item_data.get('batch_number')
            expiry_date = item_data.get('expiry_date')
            manufacturing_date = item_data.get('manufacturing_date', None)

            if not batch_number or not expiry_date:
                raise ValidationError("Batch number and expiration date are mandatory for inward stock.")

            # Find or create corresponding batch
            batch, created = MedicineBatch.objects.get_or_create(
                branch=po.branch,
                medicine=po_item.medicine,
                batch_number=batch_number,
                defaults={
                    'tenant': po.tenant,
                    'expiry_date': expiry_date,
                    'manufacturing_date': manufacturing_date,
                    'supplier': po.supplier,
                    'purchase_cost': po_item.unit_cost,
                    'selling_price': po_item.medicine.unit_price or (po_item.unit_cost * Decimal('1.25')),
                    'received_quantity': Decimal('0.00'),
                    'available_quantity': Decimal('0.00'),
                    'status': BatchStatus.ACTIVE
                }
            )

            # Record GoodsReceiptItem
            grn_item = GoodsReceiptItem.objects.create(
                goods_receipt=grn,
                po_item=po_item,
                medicine=po_item.medicine,
                batch_number=batch_number,
                manufacturing_date=manufacturing_date,
                expiry_date=expiry_date,
                quantity_received=qty_received,
                quantity_accepted=qty_accepted,
                quantity_rejected=qty_rejected,
                rejection_reason=item_data.get('rejection_reason', ''),
                unit_cost=po_item.unit_cost,
                batch=batch
            )

            # Update batch received quantity
            batch.received_quantity += qty_accepted
            batch.save(update_fields=['received_quantity'])

            # Add accepted quantity to available stock using StockService
            if qty_accepted > Decimal('0.00'):
                StockService.add_stock(
                    batch_id=batch.id,
                    quantity=qty_accepted,
                    movement_type=MovementType.PURCHASE_RECEIPT,
                    reference_type="GoodsReceipt",
                    reference_id=str(grn.id),
                    actor=receiver,
                    reason=f"Goods Receipt #{receipt_num} for PO #{po.order_number}"
                )

            # Update PO item received balance
            po_item.quantity_received += qty_received
            po_item.save(update_fields=['quantity_received'])

        # Update overall PO status: check if all items are fully received
        all_completed = True
        for item in po.items.all():
            if item.quantity_received < item.quantity_ordered:
                all_completed = False
                break

        po.status = POStatus.RECEIVED if all_completed else POStatus.PARTIALLY_RECEIVED
        po.save(update_fields=['status', 'updated_at'])

        record_audit_event(
            tenant=po.tenant,
            branch=po.branch,
            actor=receiver,
            event_type='GOODS_RECEIPT_PROCESSED',
            resource_type='goods_receipt',
            resource_id=grn.id,
            details={'receipt_number': grn.receipt_number, 'po_number': po.order_number}
        )

        return grn
