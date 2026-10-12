"""HMS Pharmacy Returns & Quarantine Models — Member 5
Implements patient returns, supplier returns, and quarantine holding workflows.
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import BaseTenantModel
from accounts.models import User
from clinical.models import Patient
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch
from pharmacy.models.supplier import Supplier
from pharmacy.models.dispensing import DispenseRecord


class ReturnCondition(models.TextChoices):
    SEALED_INTACT = 'SEALED_INTACT', 'Sealed & Intact Original Packaging'
    OPENED_PARTIAL = 'OPENED_PARTIAL', 'Opened / Partially Used'
    DAMAGED = 'DAMAGED', 'Physically Damaged'
    CONTAMINATED = 'CONTAMINATED', 'Suspected Contamination / Adverse Reaction'


class PatientReturn(BaseTenantModel):
    """Controlled patient return of dispensed medication."""
    return_number = models.CharField(max_length=60, help_text="Unique return receipt number")
    dispense_record = models.ForeignKey(DispenseRecord, on_delete=models.PROTECT, related_name='patient_returns')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='pharmacy_returns')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT)

    quantity_returned = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    condition = models.CharField(max_length=50, choices=ReturnCondition.choices, default=ReturnCondition.SEALED_INTACT)
    reason = models.TextField(help_text="Clinical or patient justification for return")

    routed_to_quarantine = models.BooleanField(
        default=True,
        help_text="Returned medicines are strictly routed to quarantine and never added directly to active stock"
    )
    refund_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    billing_refund_id = models.CharField(max_length=100, blank=True, null=True)
    received_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='processed_patient_returns')

    class Meta:
        db_table = 'pharmacy_patient_returns'
        unique_together = ('tenant', 'return_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"Return #{self.return_number} - {self.medicine.brand_name} (Qty: {self.quantity_returned})"


class SupplierReturn(BaseTenantModel):
    """Return of stock back to distributor or manufacturer (e.g., recall, transit damage)."""
    return_number = models.CharField(max_length=60)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='returns')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT)

    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total_credit = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    reason = models.CharField(max_length=255)
    supplier_credit_note = models.CharField(max_length=100, blank=True)
    authorized_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authorized_supplier_returns')

    class Meta:
        db_table = 'pharmacy_supplier_returns'
        unique_together = ('tenant', 'return_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"Supplier Return #{self.return_number} - {self.supplier.name}"


class QuarantineResolution(models.TextChoices):
    DESTROYED = 'DESTROYED', 'Disposed / Biohazard Destruction'
    RETURNED_TO_SUPPLIER = 'RETURNED_TO_SUPPLIER', 'Returned to Supplier'
    RESTORED_TO_STOCK = 'RESTORED_TO_STOCK', 'Inspected & Approved for Active Stock'


class StockQuarantine(BaseTenantModel):
    """Quarantined inventory held in isolation pending inspection, recall, or disposal."""
    batch = models.ForeignKey(MedicineBatch, on_delete=models.CASCADE, related_name='quarantine_records')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    source = models.CharField(max_length=100, help_text="e.g. PATIENT_RETURN, BATCH_RECALL, COLD_CHAIN_FAILURE")
    reason = models.TextField()

    is_resolved = models.BooleanField(default=False)
    resolution = models.CharField(max_length=50, choices=QuarantineResolution.choices, blank=True, null=True)
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_quarantines')
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pharmacy_stock_quarantines'
        ordering = ['-created_at']

    def __str__(self):
        status = f"Resolved: {self.resolution}" if self.is_resolved else "Pending Inspection"
        return f"Quarantine: {self.medicine.brand_name} ({self.quantity}) - {status}"
