"""HMS Pharmacy Catalogue Models — Member 5
Implements Medicine Catalogue, Categories, Classifications, and Formulary attributes.
"""

from django.db import models
from core.models import BaseTenantModel


class DosageForm(models.TextChoices):
    TABLET = 'TABLET', 'Tablet'
    CAPSULE = 'CAPSULE', 'Capsule'
    SYRUP = 'SYRUP', 'Syrup / Oral Liquid'
    INJECTION = 'INJECTION', 'Injection / Vial'
    OINTMENT = 'OINTMENT', 'Ointment / Cream'
    INHALER = 'INHALER', 'Inhaler / Aerosol'
    DROPS = 'DROPS', 'Drops (Eye / Ear)'
    IV_FLUID = 'IV_FLUID', 'Intravenous Infusion'
    POWDER = 'POWDER', 'Powder for Suspension'
    OTHER = 'OTHER', 'Other Dosage Form'


class AdministrationRoute(models.TextChoices):
    ORAL = 'ORAL', 'Oral'
    INTRAVENOUS = 'INTRAVENOUS', 'Intravenous (IV)'
    INTRAMUSCULAR = 'INTRAMUSCULAR', 'Intramuscular (IM)'
    SUBCUTANEOUS = 'SUBCUTANEOUS', 'Subcutaneous (SC)'
    TOPICAL = 'TOPICAL', 'Topical / External'
    INHALATION = 'INHALATION', 'Inhalation'
    OPHTHALMIC = 'OPHTHALMIC', 'Ophthalmic (Eye)'
    OTIC = 'OTIC', 'Otic (Ear)'
    NASAL = 'NASAL', 'Nasal'
    RECTAL = 'RECTAL', 'Rectal'


class DrugClassification(models.TextChoices):
    ANTIBIOTIC = 'ANTIBIOTIC', 'Antibiotic / Antimicrobial'
    ANALGESIC = 'ANALGESIC', 'Analgesic / Pain Relief'
    ANTIPYRETIC = 'ANTIPYRETIC', 'Antipyretic / Fever Reducer'
    ANTIHYPERTENSIVE = 'ANTIHYPERTENSIVE', 'Antihypertensive'
    ANTIDIABETIC = 'ANTIDIABETIC', 'Antidiabetic'
    ANTIHISTAMINE = 'ANTIHISTAMINE', 'Antihistamine / Antiallergic'
    CARDIOVASCULAR = 'CARDIOVASCULAR', 'Cardiovascular'
    GASTROINTESTINAL = 'GASTROINTESTINAL', 'Gastrointestinal'
    SEDATIVE = 'SEDATIVE', 'Sedative / Anxiolytic'
    VITAMIN_SUPPLEMENT = 'VITAMIN_SUPPLEMENT', 'Vitamin & Nutritional Supplement'
    OTHER = 'OTHER', 'Other Therapeutic Class'


class MedicineCategory(BaseTenantModel):
    """Categorization for medication formulary."""
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'pharmacy_categories'
        unique_together = ('tenant', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Medicine(BaseTenantModel):
    """Core medicine formulary entity tracked across pharmacy and inventory."""
    code = models.CharField(max_length=60, help_text="Unique product SKU or code")
    brand_name = models.CharField(max_length=200, db_index=True)
    generic_name = models.CharField(max_length=200, db_index=True)
    active_ingredients = models.CharField(max_length=255, blank=True)
    strength = models.CharField(max_length=100, help_text="e.g. 500 mg, 10 mg/ml")
    dosage_form = models.CharField(max_length=50, choices=DosageForm.choices, default=DosageForm.TABLET)
    route = models.CharField(max_length=50, choices=AdministrationRoute.choices, default=AdministrationRoute.ORAL)
    manufacturer = models.CharField(max_length=200, blank=True)
    classification = models.CharField(max_length=50, choices=DrugClassification.choices, default=DrugClassification.OTHER)
    category = models.ForeignKey(MedicineCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicines')

    requires_prescription = models.BooleanField(default=True, help_text="Mandatory clinical prescription for dispensing")
    storage_instructions = models.CharField(max_length=255, default="Store below 25°C in a dry place")
    barcode_sku = models.CharField(max_length=100, blank=True, db_index=True)
    unit_of_measure = models.CharField(max_length=50, default="Strip", help_text="Purchased unit (Box, Bottle, Strip)")
    dispensing_unit = models.CharField(max_length=50, default="Tablet", help_text="Smallest dispensing unit (Tablet, ml, Capsule)")

    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=50.00, help_text="Minimum threshold triggering low-stock alert")
    reorder_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=100.00, help_text="Suggested procurement batch size")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Standard patient retail price per dispensing unit")

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False, help_text="Soft-delete preserving historical dispensing records")

    class Meta:
        db_table = 'pharmacy_medicines'
        unique_together = ('tenant', 'code')
        ordering = ['brand_name']
        indexes = [
            models.Index(fields=['tenant', 'brand_name']),
            models.Index(fields=['tenant', 'generic_name']),
            models.Index(fields=['tenant', 'barcode_sku']),
        ]

    def __str__(self):
        return f"{self.brand_name} ({self.generic_name}) - {self.strength}"

    def get_total_stock(self, branch=None):
        """Calculates total available non-expired stock across active batches."""
        batches = self.batches.filter(
            status='ACTIVE',
            available_quantity__gt=0
        )
        if branch:
            batches = batches.filter(branch=branch)
        from django.db.models import Sum
        total = batches.aggregate(total=Sum('available_quantity'))['total']
        return total or 0.00

    def is_low_stock(self, branch=None):
        """Determines if current available stock is at or below the reorder threshold."""
        return self.get_total_stock(branch) <= self.reorder_level
