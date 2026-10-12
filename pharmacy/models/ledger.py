"""HMS Pharmacy Stock Ledger Models — Member 5
Implements auditable, append-only immutable stock movement ledger.
"""

from django.db import models
from core.models import BaseTenantModel
from accounts.models import User
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch


class MovementType(models.TextChoices):
    OPENING_BALANCE = 'OPENING_BALANCE', 'Opening Stock Balance'
    PURCHASE_RECEIPT = 'PURCHASE_RECEIPT', 'Goods Receipt Inward'
    PRESCRIPTION_DISPENSE = 'PRESCRIPTION_DISPENSE', 'Prescription Dispensing Outward'
    PATIENT_RETURN = 'PATIENT_RETURN', 'Patient Medication Return'
    SUPPLIER_RETURN = 'SUPPLIER_RETURN', 'Supplier Return Outward'
    BRANCH_TRANSFER_OUT = 'BRANCH_TRANSFER_OUT', 'Inter-Branch Transfer Out'
    BRANCH_TRANSFER_IN = 'BRANCH_TRANSFER_IN', 'Inter-Branch Transfer In'
    STOCK_ADJUSTMENT = 'STOCK_ADJUSTMENT', 'Physical Count Stock Adjustment'
    EXPIRY_WRITEOFF = 'EXPIRY_WRITEOFF', 'Expired Stock Write-Off'
    DAMAGE_WRITEOFF = 'DAMAGE_WRITEOFF', 'Damaged Stock Write-Off'
    QUARANTINE_MOVE = 'QUARANTINE_MOVE', 'Quarantine Allocation / Release'


class StockMovement(BaseTenantModel):
    """Immutable, append-only transaction ledger entry recording every change to on-hand stock."""
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='movements')
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT, related_name='movements')
    movement_type = models.CharField(max_length=50, choices=MovementType.choices, db_index=True)

    quantity_change = models.DecimalField(max_digits=12, decimal_places=2, help_text="Positive for inward, negative for outward")
    quantity_before = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_after = models.DecimalField(max_digits=12, decimal_places=2)

    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    reference_type = models.CharField(max_length=60, help_text="e.g. GoodsReceipt, DispenseRecord, StockCount")
    reference_id = models.CharField(max_length=100, db_index=True)

    actor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='stock_movements')
    reason = models.TextField(blank=True)
    idempotency_key = models.CharField(max_length=120, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'pharmacy_stock_movements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'branch', 'movement_type', 'created_at']),
            models.Index(fields=['tenant', 'medicine', 'created_at']),
            models.Index(fields=['tenant', 'idempotency_key']),
        ]

    def __str__(self):
        return f"[{self.created_at}] {self.get_movement_type_display()}: {self.medicine.brand_name} ({self.quantity_change}) by {self.actor.username}"
