"""HMS Pharmacy Reconciliation Models — Member 5
Implements physical stock count sessions, variance calculations, and adjustment authorizations.
"""

import uuid
from django.db import models
from decimal import Decimal
from core.models import BaseTenantModel
from accounts.models import User
from pharmacy.models.inventory import MedicineBatch, StorageLocation


class CountSessionStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft / Initializing'
    IN_PROGRESS = 'IN_PROGRESS', 'Counting In Progress'
    SUBMITTED = 'SUBMITTED', 'Submitted for Review'
    APPROVED = 'APPROVED', 'Approved & Stock Adjusted'
    CANCELLED = 'CANCELLED', 'Cancelled'


class StockCountSession(BaseTenantModel):
    """Physical audit and reconciliation session for a branch inventory location."""
    session_number = models.CharField(max_length=60, help_text="Audit session identifier")
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=30, choices=CountSessionStatus.choices, default=CountSessionStatus.IN_PROGRESS, db_index=True)

    initiated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='initiated_stock_counts')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_stock_counts')
    approved_at = models.DateTimeField(null=True, blank=True)

    total_discrepancy_value = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_stock_count_sessions'
        unique_together = ('tenant', 'session_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"Audit Session #{self.session_number} ({self.get_status_display()})"

    def recalculate_variance(self):
        variance = sum(item.discrepancy_value for item in self.items.all())
        self.total_discrepancy_value = Decimal(str(variance))
        self.save(update_fields=['total_discrepancy_value'])
        return self.total_discrepancy_value


class StockCountItem(models.Model):
    """Physical count recorded against a specific tracked medicine batch."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(StockCountSession, on_delete=models.CASCADE, related_name='items')
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT)

    expected_quantity = models.DecimalField(max_digits=12, decimal_places=2, help_text="Recorded system balance at count initiation")
    counted_quantity = models.DecimalField(max_digits=12, decimal_places=2, help_text="Physically verified quantity on shelf")
    discrepancy_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text="counted - expected")

    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discrepancy_value = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'), help_text="discrepancy * unit_cost")
    discrepancy_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'pharmacy_stock_count_items'

    def save(self, *args, **kwargs):
        self.discrepancy_quantity = Decimal(str(self.counted_quantity)) - Decimal(str(self.expected_quantity))
        self.discrepancy_value = self.discrepancy_quantity * Decimal(str(self.unit_cost))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.batch.medicine.brand_name} (Batch {self.batch.batch_number}): Diff {self.discrepancy_quantity}"
