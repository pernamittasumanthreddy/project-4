import uuid
from django.db import models
from django.utils import timezone
from contracts.models import Tenant, HospitalBranch, PatientContract, ClinicalEncounterContract, UserProfile

class LabCategory(models.Model):
    """Departmental categories for clinical laboratory"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100) # Hematology, Biochemistry, etc.
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Lab Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

class SpecimenType(models.TextChoices):
    WHOLE_BLOOD = 'WHOLE_BLOOD', 'Whole Blood'
    SERUM = 'SERUM', 'Serum (Gold/Red Top)'
    PLASMA = 'PLASMA', 'Plasma (Lavender/Green Top)'
    URINE_RANDOM = 'URINE_RANDOM', 'Random Clean-Catch Urine'
    URINE_24HR = 'URINE_24HR', '24-Hour Urine'
    CSF = 'CSF', 'Cerebrospinal Fluid'
    SPUTUM = 'SPUTUM', 'Sputum'
    STOOL = 'STOOL', 'Stool'
    SWAB = 'SWAB', 'Nasopharyngeal/Throat Swab'
    BIOPSY = 'BIOPSY', 'Tissue Biopsy'
    PLEURAL_FLUID = 'PLEURAL_FLUID', 'Pleural Fluid'

class LabTest(models.Model):
    """Configurable Laboratory Test Catalogue Item"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='lab_tests')
    category = models.ForeignKey(LabCategory, on_delete=models.CASCADE, related_name='tests')
    test_code = models.CharField(max_length=50) # e.g. CBC-001, GLUC-F
    loinc_code = models.CharField(max_length=30, blank=True, help_text="Logical Observation Identifiers Names and Codes")
    name = models.CharField(max_length=200)
    specimen_type = models.CharField(max_length=40, choices=SpecimenType.choices, default=SpecimenType.SERUM)
    container_type = models.CharField(max_length=100, default='SST Tube (Gold Top)')
    collection_instructions = models.TextField(blank=True, default='Standard venipuncture procedure.')
    processing_method = models.CharField(max_length=100, default='Automated Photometry / Cell Counter')
    unit = models.CharField(max_length=50, blank=True) # mg/dL, g/dL, %, etc.
    ref_min = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    ref_max = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    critical_low = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    critical_high = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    qualitative_normal = models.CharField(max_length=100, blank=True, default='Negative / Non-Reactive')
    expected_tat_minutes = models.IntegerField(default=120, help_text="Turnaround time target in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=25.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'test_code')
        ordering = ['category', 'name']

    def evaluate_numeric_flag(self, val):
        """Calculates clinical abnormal / critical flag from configured rules"""
        if val is None:
            return 'NORMAL'
        val = float(val)
        if self.critical_low is not None and val < float(self.critical_low):
            return 'CRITICAL_LOW'
        if self.critical_high is not None and val > float(self.critical_high):
            return 'CRITICAL_HIGH'
        if self.ref_min is not None and val < float(self.ref_min):
            return 'LOW'
        if self.ref_max is not None and val > float(self.ref_max):
            return 'HIGH'
        return 'NORMAL'

    def __str__(self):
        return f"[{self.test_code}] {self.name} ({self.category.name})"

class LabTestPanel(models.Model):
    """Grouped Diagnostic Profiles (e.g. Complete Blood Count, Comprehensive Metabolic Panel)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='lab_panels')
    panel_code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tests = models.ManyToManyField(LabTest, related_name='panels')
    panel_price = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('tenant', 'panel_code')

    def __str__(self):
        return f"[PANEL] {self.name} ({self.panel_code})"

class OrderPriority(models.TextChoices):
    ROUTINE = 'ROUTINE', 'Routine (Standard TAT)'
    URGENT = 'URGENT', 'Urgent (Priority Processing)'
    STAT = 'STAT', 'STAT (Immediate / Emergency Processing)'

class LabOrderStatus(models.TextChoices):
    ORDERED = 'ORDERED', 'Ordered by Clinician'
    SAMPLE_PENDING = 'SAMPLE_PENDING', 'Awaiting Sample Collection'
    COLLECTED = 'COLLECTED', 'Sample Collected'
    RECEIVED_IN_LAB = 'RECEIVED_IN_LAB', 'Received in Laboratory'
    PROCESSING = 'PROCESSING', 'Processing / In Analysis'
    RESULTS_ENTERED = 'RESULTS_ENTERED', 'Results Entered (Pending Validation)'
    VALIDATED = 'VALIDATED', 'Validated by Lab Senior'
    APPROVED = 'APPROVED', 'Approved by Pathologist'
    CANCELLED = 'CANCELLED', 'Order Cancelled'

class LabOrder(models.Model):
    """Laboratory Investigation Order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='lab_orders')
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='lab_orders')
    patient = models.ForeignKey(PatientContract, on_delete=models.CASCADE, related_name='lab_orders')
    encounter = models.ForeignKey(ClinicalEncounterContract, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_orders')
    order_number = models.CharField(max_length=50, unique=True)
    accession_number = models.CharField(max_length=50, unique=True, blank=True)
    ordering_clinician = models.CharField(max_length=150)
    priority = models.CharField(max_length=20, choices=OrderPriority.choices, default=OrderPriority.ROUTINE)
    status = models.CharField(max_length=30, choices=LabOrderStatus.choices, default=LabOrderStatus.ORDERED)
    clinical_indications = models.TextField(blank=True, help_text="Clinical justification and symptoms")
    fasting_status = models.CharField(max_length=50, default='Not Required', blank=True)
    cancellation_reason = models.TextField(blank=True)
    cancelled_by = models.CharField(max_length=100, blank=True)
    ordered_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-ordered_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            date_str = timezone.now().strftime('%Y%m%d')
            short_id = uuid.uuid4().hex[:6].upper()
            self.order_number = f"ORD-LAB-{date_str}-{short_id}"
        if not self.accession_number:
            date_str = timezone.now().strftime('%y%m%d')
            short_acc = uuid.uuid4().hex[:5].upper()
            self.accession_number = f"ACC-{date_str}-{short_acc}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} ({self.accession_number}) - {self.patient.full_name} [{self.status}]"

class LabOrderItem(models.Model):
    """Specific test or panel item inside a laboratory order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, related_name='items')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='order_items')
    panel = models.ForeignKey(LabTestPanel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=30, choices=LabOrderStatus.choices, default=LabOrderStatus.ORDERED)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order.order_number} -> {self.test.name}"

class SpecimenStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Collection'
    COLLECTED = 'COLLECTED', 'Collected by Phlebotomist'
    RECEIVED = 'RECEIVED', 'Received & Accepted in Lab'
    PROCESSING = 'PROCESSING', 'In Aliquoting / Processing'
    REJECTED = 'REJECTED', 'Rejected (Hemolyzed, Clotted, Insufficient)'
    RECOLLECTION_REQUESTED = 'RECOLLECTION_REQUESTED', 'Recollection Requested'
    DISPOSED = 'DISPOSED', 'Disposed per Biohazard Protocol'

class Specimen(models.Model):
    """Physical biological sample tracking with barcodes and custody events"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, related_name='specimens')
    barcode_id = models.CharField(max_length=60, unique=True)
    specimen_type = models.CharField(max_length=40, choices=SpecimenType.choices)
    container_type = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=SpecimenStatus.choices, default=SpecimenStatus.PENDING)
    collected_by = models.CharField(max_length=100, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    received_by = models.CharField(max_length=100, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.CharField(max_length=150, blank=True)
    rejection_notes = models.TextField(blank=True)
    recollection_needed = models.BooleanField(default=False)
    storage_rack = models.CharField(max_length=50, blank=True, default='Cold Storage Rack B-12')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.barcode_id:
            date_prefix = timezone.now().strftime('%y%m%d')
            rand_code = uuid.uuid4().hex[:6].upper()
            self.barcode_id = f"SPC-{date_prefix}-{rand_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.barcode_id} [{self.specimen_type}] - Status: {self.status}"

class SpecimenEvent(models.Model):
    """Audit log and chain of custody tracking for a specimen"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    specimen = models.ForeignKey(Specimen, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50)
    actor_name = models.CharField(max_length=150)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.specimen.barcode_id}: {self.event_type} by {self.actor_name}"

class ResultStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft Entry'
    ENTERED = 'ENTERED', 'Entered by Technician'
    VALIDATED = 'VALIDATED', 'Validated by Lab Specialist'
    APPROVED = 'APPROVED', 'Approved by Consultant Pathologist'
    AMENDED = 'AMENDED', 'Amended / Corrected Post-Release'

class LabResult(models.Model):
    """Laboratory test diagnostic measurement and findings"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_item = models.OneToOneField(LabOrderItem, on_delete=models.CASCADE, related_name='result')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    numeric_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    text_value = models.TextField(blank=True)
    unit = models.CharField(max_length=50, blank=True)
    ref_range_display = models.CharField(max_length=100, blank=True)
    flag = models.CharField(max_length=30, choices=[
        ('NORMAL', 'Normal'),
        ('LOW', 'Below Reference Range'),
        ('HIGH', 'Above Reference Range'),
        ('CRITICAL_LOW', 'Critically Low Alert'),
        ('CRITICAL_HIGH', 'Critically High Alert'),
        ('POSITIVE', 'Positive / Reactive'),
        ('NEGATIVE', 'Negative / Non-Reactive'),
    ], default='NORMAL')
    is_abnormal = models.BooleanField(default=False)
    is_critical = models.BooleanField(default=False)
    technician_notes = models.TextField(blank=True)
    entered_by = models.CharField(max_length=150, blank=True)
    entered_at = models.DateTimeField(null=True, blank=True)
    validated_by = models.CharField(max_length=150, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=150, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ResultStatus.choices, default=ResultStatus.DRAFT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        val = self.numeric_value if self.numeric_value is not None else self.text_value
        return f"{self.test.name}: {val} {self.unit} [{self.flag}] ({self.status})"

class LabResultVersion(models.Model):
    """Historical audit version for corrected or amended results"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    result = models.ForeignKey(LabResult, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField(default=1)
    previous_numeric_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    previous_text_value = models.TextField(blank=True)
    previous_flag = models.CharField(max_length=30)
    amended_by = models.CharField(max_length=150)
    amendment_reason = models.TextField()
    amended_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-version_number']

    def __str__(self):
        return f"Version {self.version_number} for {self.result.test.name} amended by {self.amended_by}"

class CriticalResultAlert(models.Model):
    """Clinical alert for life-threatening laboratory values requiring documented escalation"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    result = models.ForeignKey(LabResult, on_delete=models.CASCADE, related_name='critical_alerts')
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientContract, on_delete=models.CASCADE)
    clinician_name = models.CharField(max_length=150)
    alert_level = models.CharField(max_length=30, choices=[('URGENT', 'Urgent Alert'), ('LIFE_THREATENING', 'Life-Threatening Value')], default='LIFE_THREATENING')
    alert_status = models.CharField(max_length=30, choices=[
        ('TRIGGERED', 'Alert Triggered (Dispatching)'),
        ('NOTIFIED', 'Clinician Notified via Telephone/In-App'),
        ('ACKNOWLEDGED', 'Clinician Acknowledged Receipt'),
        ('ESCALATED', 'Escalated to Department Head (Unacknowledged > 30m)'),
    ], default='TRIGGERED')
    triggered_at = models.DateTimeField(default=timezone.now)
    notified_at = models.DateTimeField(null=True, blank=True)
    notified_by = models.CharField(max_length=150, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.CharField(max_length=150, blank=True)
    call_log_notes = models.TextField(blank=True)

    def __str__(self):
        return f"CRITICAL: {self.result.test.name} for {self.patient.full_name} [{self.alert_status}]"

class LabReport(models.Model):
    """Final Diagnostic Report issued by Laboratory"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(LabOrder, on_delete=models.CASCADE, related_name='report')
    report_number = models.CharField(max_length=60, unique=True)
    version = models.PositiveIntegerField(default=1)
    is_amended = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=150)
    approved_at = models.DateTimeField(default=timezone.now)
    pdf_filename = models.CharField(max_length=255, blank=True)
    disclaimer = models.TextField(default="Diagnostic laboratory findings are clinical aids and must be correlated with clinical findings and patient history.")

    def save(self, *args, **kwargs):
        if not self.report_number:
            date_str = timezone.now().strftime('%Y%m%d')
            rand_code = uuid.uuid4().hex[:6].upper()
            self.report_number = f"REP-LAB-{date_str}-{rand_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.report_number} v{self.version} - {self.order.patient.full_name}"
