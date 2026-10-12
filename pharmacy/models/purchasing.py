"""HMS Pharmacy Purchasing & Inward Models — Member 5
Implements Purchase Order lifecycle and Goods Receipt Note (GRN) inward processing.
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import BaseTenantModel
from accounts.models import User
from pharmacy.models.catalogue import Medicine
from pharmacy.models.supplier import Supplier
from pharmacy.models.inventory import MedicineBatch


class POStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    SUBMITTED = 'SUBMITTED', 'Submitted for Approval'
    APPROVED = 'APPROVED', 'Approved'
    PARTIALLY_RECEIVED = 'PARTIALLY_RECEIVED', 'Partially Received'
    RECEIVED = 'RECEIVED', 'Fully Received'
    REJECTED = 'REJECTED', 'Rejected'
    CANCELLED = 'CANCELLED', 'Cancelled'


class PurchaseOrder(BaseTenantModel):
    """Procurement order placed with an authorized pharmaceutical supplier."""
    order_number = models.CharField(max_length=60, help_text="PO tracking reference")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    status = models.CharField(max_length=30, choices=POStatus.choices, default=POStatus.DRAFT, db_index=True)
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_purchase_orders')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_purchase_orders')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_purchase_orders'
        unique_together = ('tenant', 'order_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"PO #{self.order_number} - {self.supplier.name} ({self.get_status_display()})"

    def recalculate_total(self):
        """Computes server-side order total from line items."""
        total = sum(item.line_total for item in self.items.all())
        self.total_amount = Decimal(str(total))
        self.save(update_fields=['total_amount'])
        return self.total_amount


class PurchaseOrderItem(models.Model):
    """Line item in a purchase order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='po_items')

    quantity_ordered = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    quantity_received = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    line_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    class Meta:
        db_table = 'pharmacy_purchase_order_items'

    def save(self, *args, **kwargs):
        self.line_total = Decimal(str(self.quantity_ordered)) * Decimal(str(self.unit_cost))
        super().save(*args, **kwargs)

    @property
    def remaining_to_receive(self):
        return max(Decimal('0.00'), self.quantity_ordered - self.quantity_received)


class GoodsReceipt(BaseTenantModel):
    """Stock Inward Goods Receipt Note (GRN) received against an approved purchase order."""
    receipt_number = models.CharField(max_length=60, help_text="GRN unique identifier")
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='goods_receipts')
    delivery_reference = models.CharField(max_length=100, help_text="Supplier delivery challan or invoice number")
    received_date = models.DateField(auto_now_add=True)
    received_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_goods_receipts')
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_goods_receipts'
        unique_together = ('tenant', 'receipt_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"GRN #{self.receipt_number} (PO: {self.purchase_order.order_number})"


class GoodsReceiptItem(models.Model):
    """Line item in a goods receipt recording verified batches and delivered quantities."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='items')
    po_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.PROTECT, related_name='receipt_items')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)

    batch_number = models.CharField(max_length=100)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField()

    quantity_received = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantity_accepted = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    quantity_rejected = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    rejection_reason = models.CharField(max_length=255, blank=True)

    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    batch = models.ForeignKey(MedicineBatch, on_delete=models.SET_NULL, null=True, blank=True, related_name='receipt_origins')

    class Meta:
        db_table = 'pharmacy_goods_receipt_items'

    def __str__(self):
        return f"{self.medicine.brand_name} Batch {self.batch_number} - Accepted: {self.quantity_accepted}"
