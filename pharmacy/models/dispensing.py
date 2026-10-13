"""HMS Pharmacy Dispensing Models — Member 5
Implements prescription review, batch allocation, and patient dispensing records.
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import BaseTenantModel
from accounts.models import User
from clinical.models import Prescription, PrescriptionItem
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch


class DispenseStatus(models.TextChoices):
    COMPLETED = 'COMPLETED', 'Dispensation Completed'
    CANCELLED = 'CANCELLED', 'Dispensation Cancelled / Reversed'


class DispenseRecord(BaseTenantModel):
    """Pharmacy dispensing order fulfilling an authorized physician prescription."""
    dispense_number = models.CharField(max_length=60, help_text="Unique dispensation receipt number")
    prescription = models.ForeignKey(Prescription, on_delete=models.PROTECT, related_name='dispensations')
    pharmacist = models.ForeignKey(User, on_delete=models.PROTECT, related_name='dispensed_orders')
    status = models.CharField(max_length=30, choices=DispenseStatus.choices, default=DispenseStatus.COMPLETED)

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    billing_invoice_id = models.CharField(max_length=100, blank=True, null=True, help_text="Integrated billing invoice ID")
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_dispense_records'
        unique_together = ('tenant', 'dispense_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"Dispense #{self.dispense_number} for Rx #{self.prescription.prescription_number}"

    def recalculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = Decimal(str(total))
        self.save(update_fields=['total_amount'])
        return self.total_amount


class DispensedItem(models.Model):
    """Line item detailing specific medicine and batch allocated to patient."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dispense_record = models.ForeignKey(DispenseRecord, on_delete=models.CASCADE, related_name='items')
    prescription_item = models.ForeignKey(PrescriptionItem, on_delete=models.PROTECT, related_name='dispensed_allocations')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT, related_name='dispensed_lines')

    quantity_dispensed = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    instructions_provided = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_dispensed_items'

    def save(self, *args, **kwargs):
        self.total_price = Decimal(str(self.quantity_dispensed)) * Decimal(str(self.unit_price))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.brand_name} (Batch: {self.batch.batch_number}) - Qty: {self.quantity_dispensed}"
