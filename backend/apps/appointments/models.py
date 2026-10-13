import uuid
from django.db import models
from django.conf import settings
from apps.core.models import TenantScopedModel, Tenant, HospitalBranch

class Department(TenantScopedModel):
    """
    Clinical Department (Cardiology, Pulmonology, Neurology, etc.).
    """
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default="Heart", help_text="Lucide icon name")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('tenant', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class DoctorProfile(TenantScopedModel):
    """
    Licensed Physician / Doctor Profile linked to user credentials.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    license_number = models.CharField(max_length=100, unique=True)
    specialization = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=8)
    qualification = models.CharField(max_length=200, default="MD, FACC")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=120.00)
    slot_duration_minutes = models.PositiveIntegerField(default=30)
    is_available_telemedicine = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.9)
    review_count = models.PositiveIntegerField(default=48)
    bio = models.TextField(blank=True)
    office_room = models.CharField(max_length=50, default="Room 304, Tower B")

    class Meta:
        ordering = ['user__first_name']

    @property
    def full_name(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.specialization} [{self.tenant.name}]"


class PatientProfile(TenantScopedModel):
    """
    Hospital Patient Profile and demographic record.
    """
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )
    BLOOD_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    mrn = models.CharField(max_length=50, unique=True, help_text="Medical Record Number")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='FEMALE')
    blood_group = models.CharField(max_length=5, choices=BLOOD_CHOICES, default='O+')
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, default="Family")
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    insurance_provider = models.CharField(max_length=150, blank=True, default="BlueCross Shield")
    insurance_policy_number = models.CharField(max_length=100, blank=True, default="BCS-9842104")

    class Meta:
        ordering = ['-created_at']

    @property
    def full_name(self):
        return self.user.full_name

    def __str__(self):
        return f"{self.full_name} [{self.mrn}] - {self.tenant.name}"


class Appointment(TenantScopedModel):
    """
    Clinical and Telemedicine Appointment booking.
    """
    TYPE_CHOICES = (
        ('IN_PERSON', 'In-Person Consultation'),
        ('TELEMEDICINE', 'Virtual Telemedicine Video Call'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending Confirmation'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Consultation'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'Patient No-Show'),
    )

    appointment_number = models.CharField(max_length=50, unique=True)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='TELEMEDICINE')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    reason_for_visit = models.TextField(help_text="Chief complaint or consultation reason")
    notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['appointment_date', 'start_time']
        indexes = [
            models.Index(fields=['tenant', 'appointment_date']),
            models.Index(fields=['doctor', 'appointment_date', 'start_time']),
            models.Index(fields=['patient', 'appointment_date']),
        ]

    def __str__(self):
        return f"Appt #{self.appointment_number}: {self.patient.full_name} with {self.doctor.full_name} on {self.appointment_date} {self.start_time}"
