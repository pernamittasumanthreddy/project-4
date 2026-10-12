import uuid
from django.db import models
from apps.core.models import TenantScopedModel
from apps.appointments.models import PatientProfile
from apps.clinical.models import Prescription

class Medication(TenantScopedModel):
    """
    Pharmacy Formulary & Inventory Stock.
    """
    generic_name = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200)
    dosage_form = models.CharField(max_length=100, default="Tablet")
    strength = models.CharField(max_length=50, default="10 mg")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)
    stock_quantity = models.PositiveIntegerField(default=500)
    reorder_level = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ['generic_name']

    def __str__(self):
        return f"{self.generic_name} ({self.brand_name}) {self.strength}"


class DispensingOrder(TenantScopedModel):
    """
    Medication dispensing transaction linked to prescription.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending Dispensing'),
        ('DISPENSED', 'Dispensed to Patient'),
        ('CANCELLED', 'Order Cancelled'),
    )

    dispense_number = models.CharField(max_length=50, unique=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='dispensing_orders')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='dispensed_medications')
    pharmacist_name = models.CharField(max_length=150, default="David Ross, PharmD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPENSED')
    dispensed_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=45.00)

    class Meta:
        ordering = ['-dispensed_at']

    def __str__(self):
        return f"Dispense #{self.dispense_number} for {self.patient.full_name}"
