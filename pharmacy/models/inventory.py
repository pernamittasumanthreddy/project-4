"""HMS Pharmacy Inventory & Batch Models — Member 5
Implements batch-wise stock tracking, expiry dates, storage locations, and stock constraints.
"""

from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import BaseTenantModel
from accounts.models import User
from pharmacy.models.catalogue import Medicine
from pharmacy.models.supplier import Supplier


class BatchStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active / Eligible for Dispensing'
    QUARANTINED = 'QUARANTINED', 'Quarantined / On Hold'
    RECALLED = 'RECALLED', 'Recalled by Manufacturer'
    EXPIRED = 'EXPIRED', 'Expired'
    DEPLETED = 'DEPLETED', 'Stock Depleted (0 Available)'


class StorageLocation(BaseTenantModel):
    """Storage location within a branch pharmacy (shelves, racks, cold storage)."""
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    is_cold_storage = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'pharmacy_storage_locations'
        unique_together = ('branch', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.code}]"


class MedicineBatch(BaseTenantModel):
    """Physical batch / lot of medicine with discrete expiration date and valuation."""
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=100, db_index=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(db_index=True)

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_batches')
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, blank=True)

    purchase_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Unit purchase cost per dispensing unit"
    )
    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Selling/dispensing price per dispensing unit"
    )

    received_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    available_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        db_index=True,
        help_text="Current usable on-hand quantity"
    )
    reserved_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Quantity allocated to pending unfulfilled dispensations"
    )
    quarantined_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Quantity blocked from dispensing due to inspection, return, or recall"
    )

    status = models.CharField(max_length=30, choices=BatchStatus.choices, default=BatchStatus.ACTIVE, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_batches'
        unique_together = ('branch', 'medicine', 'batch_number')
        ordering = ['expiry_date', 'created_at']
        indexes = [
            models.Index(fields=['tenant', 'branch', 'status', 'expiry_date']),
            models.Index(fields=['tenant', 'medicine', 'status']),
        ]

    def __str__(self):
        return f"{self.medicine.brand_name} - Batch {self.batch_number} (Exp: {self.expiry_date})"

    @property
    def is_expired(self):
        return self.expiry_date <= date.today()

    @property
    def days_until_expiry(self):
        return (self.expiry_date - date.today()).days

    @property
    def is_near_expiry(self):
        """Flags batches within 60 days of expiration."""
        return 0 < self.days_until_expiry <= 60

    def check_and_update_status(self):
        """Refreshes batch state based on date and quantity."""
        if self.status not in [BatchStatus.QUARANTINED, BatchStatus.RECALLED]:
            if self.is_expired:
                self.status = BatchStatus.EXPIRED
            elif self.available_quantity <= Decimal('0.00'):
                self.status = BatchStatus.DEPLETED
            else:
                self.status = BatchStatus.ACTIVE
        return self.status
