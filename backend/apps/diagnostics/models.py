import uuid
from django.db import models
from apps.core.models import TenantScopedModel
from apps.appointments.models import PatientProfile, DoctorProfile

class LabReport(TenantScopedModel):
    """
    Pathology & Laboratory Diagnostic Investigation Report.
    """
    CATEGORY_CHOICES = (
        ('HEMATOLOGY', 'Hematology / Complete Blood Count'),
        ('BIOCHEMISTRY', 'Clinical Biochemistry & Metabolic Panel'),
        ('CARDIOLOGY', 'Cardiac Biomarkers & Enzymes'),
        ('MICROBIOLOGY', 'Microbiology & Serology'),
        ('ENDOCRINOLOGY', 'Endocrine & Hormones'),
    )
    STATUS_CHOICES = (
        ('ORDERED', 'Ordered by Physician'),
        ('COLLECTED', 'Specimen Collected'),
        ('ANALYZED', 'Analyzed by Lab Tech'),
        ('APPROVED', 'Approved & Published by Pathologist'),
        ('REJECTED', 'Specimen Hemolyzed / Rejected'),
    )

    report_number = models.CharField(max_length=50, unique=True)
    test_name = models.CharField(max_length=200)
    test_code = models.CharField(max_length=50, default="CBC-85025", help_text="LOINC or CPT code")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='BIOCHEMISTRY')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='lab_reports')
    ordering_doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='ordered_lab_reports')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ORDERED')
    order_date = models.DateField()
    collected_at = models.DateTimeField(null=True, blank=True)
    specimen_type = models.CharField(max_length=100, default="Venous Whole Blood")
    results = models.JSONField(default=list, blank=True, help_text="List of {name, value, unit, reference_range, flag}")
    conclusion = models.TextField(blank=True)
    approved_by = models.CharField(max_length=150, blank=True, default="Dr. Eleanor Vance, Pathologist")
    approved_at = models.DateTimeField(null=True, blank=True)
    document_url = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-order_date', '-created_at']

    def is_published(self):
        return self.status == 'APPROVED'

    def __str__(self):
        return f"Lab #{self.report_number}: {self.test_name} for {self.patient.full_name} ({self.status})"


class RadiologyReport(TenantScopedModel):
    """
    Diagnostic Imaging (X-Ray, MRI, CT Scan, Ultrasound, Echo).
    """
    MODALITY_CHOICES = (
        ('X_RAY', 'Digital Radiography (X-Ray)'),
        ('CT_SCAN', 'Computed Tomography (CT)'),
        ('MRI', 'Magnetic Resonance Imaging (MRI)'),
        ('ULTRASOUND', 'Diagnostic Ultrasound'),
        ('ECHOCARDIOGRAM', 'Transthoracic Echocardiogram'),
    )
    STATUS_CHOICES = (
        ('ORDERED', 'Study Ordered'),
        ('CAPTURED', 'Images Captured'),
        ('APPROVED', 'Report Approved by Radiologist'),
    )

    study_number = models.CharField(max_length=50, unique=True)
    study_name = models.CharField(max_length=200)
    modality = models.CharField(max_length=30, choices=MODALITY_CHOICES, default='X_RAY')
    body_part = models.CharField(max_length=100, default="Chest 2-Views PA & Lateral")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='radiology_reports')
    ordering_doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='ordered_radiology_reports')
    radiologist_name = models.CharField(max_length=150, default="Dr. Arthur Sterling, Chief Radiologist")
    study_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ORDERED')
    clinical_history = models.TextField(blank=True)
    findings = models.TextField(blank=True)
    impression = models.TextField(blank=True)
    key_images = models.JSONField(default=list, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-study_date', '-created_at']

    def is_published(self):
        return self.status == 'APPROVED'

    def __str__(self):
        return f"Imaging #{self.study_number}: {self.study_name} ({self.modality}) for {self.patient.full_name} [{self.status}]"
