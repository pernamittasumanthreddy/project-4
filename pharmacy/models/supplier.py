"""HMS Pharmacy Supplier Models — Member 5
Implements pharmaceutical distributor and vendor management.
"""

from django.db import models
from core.models import BaseTenantModel


class Supplier(BaseTenantModel):
    """Pharmaceutical distributor, vendor, or manufacturer entity."""
    code = models.CharField(max_length=60, help_text="Unique vendor code")
    name = models.CharField(max_length=255, db_index=True)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    # Tax & Legal Identifiers
    gstin = models.CharField(max_length=50, blank=True, help_text="GST Identification Number")
    pan_number = models.CharField(max_length=30, blank=True, help_text="Income Tax PAN")
    drug_license_number = models.CharField(max_length=100, blank=True)

    payment_terms = models.CharField(max_length=100, default="Net 30 Days", help_text="e.g. Net 15, Net 30, Cash On Delivery")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_suppliers'
        unique_together = ('tenant', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.code}]"
