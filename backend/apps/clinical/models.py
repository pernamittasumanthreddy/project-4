import uuid
from django.db import models
from django.conf import settings
from apps.core.models import TenantScopedModel
from apps.appointments.models import PatientProfile, DoctorProfile, Appointment

class Encounter(TenantScopedModel):
    """
    Clinical Patient Encounter / Consultation Record.
    """
    TYPE_CHOICES = (
        ('OUTPATIENT', 'Outpatient Consultation'),
        ('TELEMEDICINE', 'Telemedicine Virtual Encounter'),
        ('INPATIENT', 'Inpatient Ward Round'),
        ('EMERGENCY', 'Emergency Evaluation'),
    )
    STATUS_CHOICES = (
        ('DRAFT', 'Clinical Draft'),
        ('SIGNED', 'Signed & Finalized'),
        ('AMENDED', 'Clinically Amended'),
    )

    encounter_number = models.CharField(max_length=50, unique=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='encounter')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='encounters')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='encounters')
    encounter_date = models.DateField()
    encounter_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='TELEMEDICINE')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')

    # Clinical SOAP notes
    chief_complaint = models.TextField()
    vitals = models.JSONField(default=dict, blank=True, help_text="bp, heart_rate, temp_c, spo2, weight_kg, height_cm")
    subjective_notes = models.TextField(blank=True)
    physical_examination = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    clinical_plan = models.TextField(blank=True)

    # Signature lock
    signed_by = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='signed_encounters')
    signed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-encounter_date', '-created_at']

    def __str__(self):
        return f"Encounter #{self.encounter_number} - {self.patient.full_name} ({self.status})"


class Diagnosis(TenantScopedModel):
    """
    Standardized ICD-10 Diagnosis assigned to a patient during an encounter.
    """
    SEVERITY_CHOICES = (
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe / Acute'),
        ('CHRONIC', 'Chronic / Ongoing'),
    )

    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='diagnoses')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='diagnoses')
    icd10_code = models.CharField(max_length=20, help_text="e.g. I10, E11.9, J45.909")
    description = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MODERATE')
    is_primary = models.BooleanField(default=False)
    diagnosed_date = models.DateField()

    class Meta:
        ordering = ['-is_primary', 'icd10_code']

    def __str__(self):
        return f"[{self.icd10_code}] {self.description} ({self.patient.full_name})"


class Prescription(TenantScopedModel):
    """
    Physician medication prescription.
    """
    STATUS_CHOICES = (
        ('ACTIVE', 'Active Medication'),
        ('COMPLETED', 'Completed Course'),
        ('DISPENSED', 'Dispensed by Pharmacy'),
        ('DISCONTINUED', 'Discontinued'),
    )

    prescription_number = models.CharField(max_length=50, unique=True)
    encounter = models.ForeignKey(Encounter, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='prescriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    issued_date = models.DateField()
    valid_until = models.DateField()
    special_instructions = models.TextField(blank=True)

    class Meta:
        ordering = ['-issued_date']

    def __str__(self):
        return f"Rx #{self.prescription_number} for {self.patient.full_name} by {self.doctor.full_name}"


class PrescriptionItem(models.Model):
    """
    Individual medication item in a prescription.
    """
    ROUTE_CHOICES = (
        ('ORAL', 'Oral (PO)'),
        ('INHALATION', 'Inhalation'),
        ('TOPICAL', 'Topical'),
        ('IV', 'Intravenous (IV)'),
        ('SC', 'Subcutaneous'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text="e.g. 50mg, 10ml, 2 puffs")
    route = models.CharField(max_length=20, choices=ROUTE_CHOICES, default='ORAL')
    frequency = models.CharField(max_length=100, help_text="e.g. Once daily with meals, BID, PRN")
    duration_days = models.PositiveIntegerField(default=30)
    quantity = models.PositiveIntegerField(default=30)
    instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.medication_name} {self.dosage} - {self.frequency}"


class Allergy(TenantScopedModel):
    """
    Patient allergy and adverse drug reaction alert.
    """
    SEVERITY_CHOICES = (
        ('MILD', 'Mild rash / itchiness'),
        ('MODERATE', 'Moderate urticaria / wheezing'),
        ('SEVERE', 'Severe Anaphylaxis risk'),
    )

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='allergies')
    allergen = models.CharField(max_length=150, help_text="e.g. Penicillin, Peanuts, Sulfa Drugs")
    reaction = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MODERATE')
    identified_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-severity']

    def __str__(self):
        return f"Allergy: {self.allergen} ({self.severity}) - {self.patient.full_name}"


class MedicalHistory(TenantScopedModel):
    """
    Chronic conditions and past surgical/medical history.
    """
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_history')
    condition_name = models.CharField(max_length=200)
    onset_year = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default="Active Management")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-onset_year']

    def __str__(self):
        return f"{self.condition_name} ({self.onset_year}) - {self.patient.full_name}"
