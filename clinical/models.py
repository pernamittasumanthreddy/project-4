"""HMS Clinical Models — Member 3 Contract
Defines Patients, Prescriptions, and Prescription Items consumed by Pharmacy & Dispensing.
"""

import uuid
from django.db import models
from core.models import BaseTenantModel
from accounts.models import User


class Patient(BaseTenantModel):
    """Hospital patient entity."""
    mrn = models.CharField(max_length=50, help_text="Medical Record Number")
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')])
    contact_number = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = 'clinical_patients'
        unique_together = ('tenant', 'mrn')
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} [{self.mrn}]"


class PrescriptionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Dispensation'
    PARTIALLY_DISPENSED = 'PARTIALLY_DISPENSED', 'Partially Dispensed'
    DISPENSED = 'DISPENSED', 'Fully Dispensed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Prescription(BaseTenantModel):
    """Clinical prescription issued by a licensed physician."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    prescriber = models.ForeignKey(User, on_delete=models.PROTECT, related_name='prescribed_orders')
    prescription_number = models.CharField(max_length=60)
    diagnosis = models.CharField(max_length=255, blank=True)
    clinical_notes = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=PrescriptionStatus.choices, default=PrescriptionStatus.PENDING)

    class Meta:
        db_table = 'clinical_prescriptions'
        unique_together = ('tenant', 'prescription_number')
        ordering = ['-created_at']

    def __str__(self):
        return f"Rx #{self.prescription_number} for {self.patient.full_name} ({self.get_status_display()})"


class PrescriptionItem(models.Model):
    """Individual line item of prescribed medication."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine_code = models.CharField(max_length=50, blank=True, help_text="Catalogue SKU or reference code")
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, help_text="e.g. 500mg, 1 tablet")
    frequency = models.CharField(max_length=100, help_text="e.g. TID, BID, Once daily")
    duration_days = models.PositiveIntegerField(default=1)
    quantity_prescribed = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_dispensed = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    instructions = models.TextField(blank=True)

    class Meta:
        db_table = 'clinical_prescription_items'

    @property
    def remaining_quantity(self):
        return max(0, self.quantity_prescribed - self.quantity_dispensed)

    def __str__(self):
        return f"{self.medicine_name} ({self.quantity_prescribed} prescribed, {self.quantity_dispensed} dispensed)"
