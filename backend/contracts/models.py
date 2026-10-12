import uuid
from django.db import models
from django.utils import timezone

class Tenant(models.Model):
    """Member 1 Contract: Multi-tenant healthcare organization"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=50, unique=True)
    domain = models.CharField(max_length=150, blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class HospitalBranch(models.Model):
    """Member 1 Contract: Branch or site within a tenant hospital"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    branch_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_main_branch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'branch_code')

    def __str__(self):
        return f"{self.tenant.code} - {self.name} ({self.branch_code})"

class UserRole(models.TextChoices):
    HOSPITAL_ADMIN = 'HOSPITAL_ADMIN', 'Hospital Administrator'
    LAB_MANAGER = 'LAB_MANAGER', 'Laboratory Manager'
    LAB_TECHNICIAN = 'LAB_TECHNICIAN', 'Laboratory Technician'
    PATHOLOGIST_APPROVER = 'PATHOLOGIST_APPROVER', 'Pathologist / Lab Approver'
    RADIOLOGY_TECHNICIAN = 'RADIOLOGY_TECHNICIAN', 'Radiology Technologist'
    RADIOLOGIST = 'RADIOLOGIST', 'Consultant Radiologist'
    TREATING_CLINICIAN = 'TREATING_CLINICIAN', 'Treating Clinician / Physician'
    NURSE = 'NURSE', 'Clinical Staff / Nurse'
    AUDITOR = 'AUDITOR', 'Healthcare Compliance Auditor'

class UserProfile(models.Model):
    """Member 1 Contract: User representation with tenant, branch and RBAC role"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users')
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='users')
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    role = models.CharField(max_length=40, choices=UserRole.choices, default=UserRole.LAB_TECHNICIAN)
    license_number = models.CharField(max_length=100, blank=True)
    digital_signature_hash = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('tenant', 'username')

    def __str__(self):
        return f"{self.full_name} [{self.role}] - {self.tenant.code}"

class PatientContract(models.Model):
    """Member 2 Contract: Patient Demographic Reference"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='patients')
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='patients')
    uhid = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group = models.CharField(max_length=10, blank=True, default='O+')
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    allergies = models.TextField(blank=True, default='None reported')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'uhid')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.uhid} - {self.full_name}"

class EncounterType(models.TextChoices):
    OPD = 'OPD', 'Outpatient Department'
    IPD = 'IPD', 'Inpatient Admission'
    EMERGENCY = 'EMERGENCY', 'Emergency & Trauma'
    ICU = 'ICU', 'Intensive Care Unit'
    DAYCARE = 'DAYCARE', 'Day Care Surgery'

class ClinicalEncounterContract(models.Model):
    """Member 3 Contract: Clinical Consultation & Encounter Reference"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='encounters')
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='encounters')
    patient = models.ForeignKey(PatientContract, on_delete=models.CASCADE, related_name='encounters')
    encounter_id = models.CharField(max_length=50)
    encounter_type = models.CharField(max_length=20, choices=EncounterType.choices, default=EncounterType.OPD)
    attending_doctor = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    chief_complaint = models.TextField(blank=True)
    provisional_diagnosis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'encounter_id')

    def __str__(self):
        return f"{self.encounter_id} ({self.encounter_type}) - {self.patient.full_name}"

class BillingEventContract(models.Model):
    """Member 6 Contract: Billable investigation event emitter"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='billing_events')
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='billing_events')
    patient = models.ForeignKey(PatientContract, on_delete=models.CASCADE)
    encounter = models.ForeignKey(ClinicalEncounterContract, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.CharField(max_length=10, choices=[('LIS', 'Laboratory'), ('RIS', 'Radiology')])
    order_id = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    service_code = models.CharField(max_length=50)
    service_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending Bill Generation'),
        ('EMITTED', 'Charge Event Emitted'),
        ('BILLED', 'Added to Patient Invoice'),
    ], default='EMITTED')
    emitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"BILL-[{self.module}] {self.service_code}: ${self.amount} ({self.status})"
