from django.db import models
from core.models import TenantAwareModel
from patients.models import Patient

class PatientVitals(TenantAwareModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vitals_records")
    systolic_bp = models.PositiveIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature_fahrenheit = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True)
    recorded_by = models.CharField(max_length=150, default="Triage Nurse")
    notes = models.TextField(blank=True, default="")
