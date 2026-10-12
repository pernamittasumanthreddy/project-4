"""HMS Billing Models — Member 6 Contract
Provides Invoicing interface for medications dispensed by the Pharmacy module.
"""

import uuid
from django.db import models
from core.models import BaseTenantModel
from clinical.models import Patient


class InvoiceStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Payment'
    PAID = 'PAID', 'Paid'
    PARTIALLY_PAID = 'PARTIALLY_PAID', 'Partially Paid'
    CANCELLED = 'CANCELLED', 'Cancelled'


class BillingInvoice(BaseTenantModel):
    """Patient billing invoice generated from services, consultations, or pharmacy dispensations."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=60)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING)
    source_module = models.CharField(max_length=50, default='PHARMACY')
    reference_id = models.CharField(max_length=100, blank=True, null=True, help_text="Dispensing ID or encounter ID")

    class Meta:
        db_table = 'billing_invoices'
        unique_together = ('tenant', 'invoice_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.patient.full_name} (${self.total_amount})"


class BillingItem(models.Model):
    """Line item in a billing invoice."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(BillingInvoice, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=50, default='MEDICATION')
    item_code = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = 'billing_invoice_items'

    def __str__(self):
        return f"{self.description} ({self.quantity} @ ${self.unit_price})"
