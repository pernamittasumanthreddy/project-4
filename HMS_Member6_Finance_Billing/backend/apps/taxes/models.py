from decimal import Decimal
from django.db import models
from apps.common.models import TenantScopedModel
from apps.common.decimal_utils import quantize_currency, to_decimal

class TaxConfiguration(TenantScopedModel):
    """
    Configurable GST Tax rates and classification slabs.
    Supports Indian GST: Exempt, 5%, 12%, 18%, 28%.
    """
    code = models.CharField(max_length=50, help_text="e.g. GST_18, GST_EXEMPT, GST_12")
    name = models.CharField(max_length=150, help_text="e.g. Standard Healthcare Tech 18%")
    rate_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    hsn_sac_code = models.CharField(max_length=20, default='999312', help_text="HSN/SAC code")
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.rate_percentage}%)"

    def save(self, *args, **kwargs):
        # Auto-compute split if total rate is given and splits are zero
        total = to_decimal(self.rate_percentage)
        if total > 0:
            if self.cgst_rate == Decimal('0.00') and self.sgst_rate == Decimal('0.00'):
                half = quantize_currency(total / Decimal('2.00'))
                self.cgst_rate = half
                self.sgst_rate = half
            if self.igst_rate == Decimal('0.00'):
                self.igst_rate = total
        super().save(*args, **kwargs)


class TaxTransaction(TenantScopedModel):
    """
    Audit log of tax charged on invoices for GSTR reporting.
    """
    invoice_number = models.CharField(max_length=100, db_index=True)
    tax_config = models.ForeignKey(TaxConfiguration, on_delete=models.PROTECT)
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_tax = models.DecimalField(max_digits=12, decimal_places=2)
    is_interstate = models.BooleanField(default=False)
    hospital_state = models.CharField(max_length=10)
    customer_state = models.CharField(max_length=10)

    def __str__(self):
        return f"TaxTx {self.invoice_number} - Total ₹{self.total_tax}"
