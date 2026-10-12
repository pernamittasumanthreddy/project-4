import uuid
from django.db import models
from django.utils import timezone
from contracts.models import Tenant, HospitalBranch, PatientContract, ClinicalEncounterContract, UserProfile

class ModalityType(models.TextChoices):
    XRAY = 'DX', 'Digital Radiography (X-Ray)'
    CT = 'CT', 'Computed Tomography (CT Scan)'
    MRI = 'MR', 'Magnetic Resonance Imaging (MRI)'
    ULTRASOUND = 'US', 'Diagnostic Ultrasound (US)'
    MAMMOGRAPHY = 'MG', 'Digital Mammography'
    NUCLEAR_MEDICINE = 'NM', 'Nuclear Medicine (SPECT/PET)'

class ImagingModality(models.Model):
    """Radiology Modality Equipment / Department Machine"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100) # e.g. "GE Revolution CT 128-Slice"
    modality_type = models.CharField(max_length=10, choices=ModalityType.choices, default=ModalityType.XRAY)
    room_number = models.CharField(max_length=50, default='Radiology Suite 1')
    ae_title = models.CharField(max_length=50, default='HMS_MODALITY_01', help_text="DICOM Application Entity Title")
    port = models.IntegerField(default=11112)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Imaging Modalities'
        ordering = ['modality_type', 'name']

    def __str__(self):
        return f"{self.name} [{self.modality_type}] - Room {self.room_number}"

class ImagingProcedure(models.Model):
    """Configurable Radiology Procedure Catalogue Item"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='imaging_procedures')
    procedure_code = models.CharField(max_length=50) # e.g. RAD-XR-CHEST, RAD-CT-BRAIN
    cpt_code = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=200)
    modality = models.ForeignKey(ImagingModality, on_delete=models.CASCADE, related_name='procedures')
    body_part = models.CharField(max_length=100, default='Chest')
    prep_instructions = models.TextField(blank=True, default='Remove all metal jewelry and piercings prior to scanning.')
    requires_contrast = models.BooleanField(default=False)
    contrast_type = models.CharField(max_length=100, blank=True, default='None')
    requires_fasting = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=120.00)
    expected_tat_minutes = models.IntegerField(default=180) # 3 hours turnaround
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('tenant', 'procedure_code')
        ordering = ['modality', 'name']

    def __str__(self):
        return f"[{self.procedure_code}] {self.name} ({self.modality.modality_type})"

class ImagingOrderStatus(models.TextChoices):
    ORDERED = 'ORDERED', 'Ordered by Clinician'
    SCHEDULED = 'SCHEDULED', 'Scheduled for Modality Slot'
    ARRIVED = 'ARRIVED', 'Patient Arrived at Radiology Desk'
    IN_PROGRESS = 'IN_PROGRESS', 'Imaging Scan in Progress'
    COMPLETED = 'COMPLETED', 'Acquisition Completed (Study Stored)'
    REPORT_PENDING = 'REPORT_PENDING', 'Awaiting Radiologist Interpretation'
    REPORTING = 'REPORTING', 'Radiologist Drafting Interpretation'
    APPROVED = 'APPROVED', 'Report Approved & Released'
    CANCELLED = 'CANCELLED', 'Order Cancelled'

class ImagingOrder(models.Model):
    """Radiology Examination Order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='imaging_orders')
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='imaging_orders')
    patient = models.ForeignKey(PatientContract, on_delete=models.CASCADE, related_name='imaging_orders')
    encounter = models.ForeignKey(ClinicalEncounterContract, on_delete=models.SET_NULL, null=True, blank=True, related_name='imaging_orders')
    order_number = models.CharField(max_length=50, unique=True)
    accession_number = models.CharField(max_length=50, unique=True, blank=True)
    ordering_clinician = models.CharField(max_length=150)
    priority = models.CharField(max_length=20, default='ROUTINE')
    status = models.CharField(max_length=30, choices=ImagingOrderStatus.choices, default=ImagingOrderStatus.ORDERED)
    clinical_history = models.TextField(blank=True, help_text="Clinical justification and patient symptoms")
    contrast_cleared = models.BooleanField(default=False)
    eGFR_creatinine_check = models.CharField(max_length=100, blank=True, default='eGFR > 60 mL/min (Cleared)')
    scheduled_slot = models.DateTimeField(null=True, blank=True)
    technologist_notes = models.TextField(blank=True)
    ordered_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-ordered_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            date_str = timezone.now().strftime('%Y%m%d')
            rand_code = uuid.uuid4().hex[:6].upper()
            self.order_number = f"ORD-RAD-{date_str}-{rand_code}"
        if not self.accession_number:
            date_str = timezone.now().strftime('%y%m%d')
            short_acc = uuid.uuid4().hex[:5].upper()
            self.accession_number = f"RAD-{date_str}-{short_acc}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} ({self.accession_number}) - {self.patient.full_name} [{self.status}]"

class ImagingOrderItem(models.Model):
    """Specific procedure within an imaging order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(ImagingOrder, on_delete=models.CASCADE, related_name='items')
    procedure = models.ForeignKey(ImagingProcedure, on_delete=models.CASCADE, related_name='order_items')
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order.order_number} -> {self.procedure.name}"

class ImagingStudy(models.Model):
    """DICOM Imaging Study associated with order item and patient"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_item = models.OneToOneField(ImagingOrderItem, on_delete=models.CASCADE, related_name='study')
    patient = models.ForeignKey(PatientContract, on_delete=models.CASCADE, related_name='imaging_studies')
    study_instance_uid = models.CharField(max_length=128, unique=True)
    accession_number = models.CharField(max_length=60)
    modality_type = models.CharField(max_length=10, choices=ModalityType.choices, default=ModalityType.XRAY)
    study_description = models.CharField(max_length=200)
    study_date = models.DateField(default=timezone.now)
    study_time = models.TimeField(default=timezone.now)
    performing_technologist = models.CharField(max_length=150, blank=True, default='Rad Tech Senior')
    series_count = models.PositiveIntegerField(default=1)
    instance_count = models.PositiveIntegerField(default=1)
    dicom_file_path = models.CharField(max_length=255, blank=True)
    is_synthetic_demo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.study_instance_uid:
            # 1.2.840 standard prefix for medical imaging
            rand_uid = '.'.join(str(int(uuid.uuid4().hex[i:i+4], 16)) for i in range(0, 16, 4))
            self.study_instance_uid = f"1.2.840.10008.5.1.4.1.1.{rand_uid}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.study_description} [{self.modality_type}] - {self.study_instance_uid}"

class RadiologyReportStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft Findings'
    IN_REVIEW = 'IN_REVIEW', 'Awaiting Consultant Sign-Off'
    APPROVED = 'APPROVED', 'Signed & Finalized by Radiologist'
    AMENDED = 'AMENDED', 'Amended / Addendum Appended'

class RadiologyReport(models.Model):
    """Diagnostic Interpretation and Report authored by Radiologist"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study = models.OneToOneField(ImagingStudy, on_delete=models.CASCADE, related_name='report')
    report_number = models.CharField(max_length=60, unique=True)
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=RadiologyReportStatus.choices, default=RadiologyReportStatus.DRAFT)
    reporting_radiologist = models.CharField(max_length=150)
    clinical_indication = models.TextField(blank=True)
    examination_technique = models.TextField(blank=True, default='Multi-planar acquisition was obtained. Comparison made with prior studies.')
    findings = models.TextField()
    impression = models.TextField()
    recommendations = models.TextField(blank=True, default='Routine clinical follow-up as clinically warranted.')
    bi_rads_grade = models.CharField(max_length=50, blank=True, help_text="e.g. BI-RADS Category 1: Negative")
    approved_by = models.CharField(max_length=150, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    pdf_filename = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.report_number:
            date_str = timezone.now().strftime('%Y%m%d')
            rand_code = uuid.uuid4().hex[:6].upper()
            self.report_number = f"REP-RAD-{date_str}-{rand_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.report_number} v{self.version} - {self.study.study_description} [{self.status}]"

class RadiologyReportVersion(models.Model):
    """Audit trail for radiology report corrections and addenda"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(RadiologyReport, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    previous_findings = models.TextField()
    previous_impression = models.TextField()
    amended_by = models.CharField(max_length=150)
    amendment_reason = models.TextField()
    amended_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-version_number']

    def __str__(self):
        return f"RAD Addendum v{self.version_number} by {self.amended_by}"
