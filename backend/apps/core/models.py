import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Tenant(models.Model):
    """
    Hospital Network / Healthcare Organization Tenant.
    Provides complete logical isolation across multi-tenant SaaS deployments.
    """
    TIER_CHOICES = (
        ('COMMUNITY', 'Community Hospital'),
        ('REGIONAL', 'Regional Medical Center'),
        ('ENTERPRISE', 'Enterprise Academic Health System'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    domain = models.CharField(max_length=255, unique=True, help_text="e.g. caretrust.hms.health")
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='ENTERPRISE')
    license_key = models.CharField(max_length=128, blank=True, default="LIC-CARETRUST-ENT-2026")
    primary_color = models.CharField(max_length=20, default="#0F766E")
    contact_email = models.EmailField(default="admin@caretrust.health")
    contact_phone = models.CharField(max_length=30, default="+1 (800) 555-CARE")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

    def __str__(self):
        return f"{self.name} ({self.slug})"


class HospitalBranch(models.Model):
    """
    Physical Hospital Campus or Clinic facility belonging to a Tenant.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, help_text="e.g. MAIN, NORTH, AMBULATORY")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'code')
        ordering = ['name']
        verbose_name = 'Hospital Branch'
        verbose_name_plural = 'Hospital Branches'

    def __str__(self):
        return f"{self.name} - {self.tenant.name} [{self.code}]"


class User(AbstractUser):
    """
    Unified User model across all roles in the multi-tenant HMS platform.
    """
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Platform Super Administrator'),
        ('HOSPITAL_ADMIN', 'Hospital Administrator'),
        ('DOCTOR', 'Physician / Clinician'),
        ('PATIENT', 'Patient'),
        ('NURSE', 'Registered Nurse'),
        ('PHARMACIST', 'Pharmacist'),
        ('LAB_TECH', 'Laboratory Technologist'),
        ('RECEPTIONIST', 'Front Desk / Registrar'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    branch = models.ForeignKey(HospitalBranch, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='PATIENT')
    phone = models.CharField(max_length=30, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.username

    def is_doctor(self):
        return self.role == 'DOCTOR'

    def is_patient(self):
        return self.role == 'PATIENT'

    def is_admin(self):
        return self.role in ('SUPER_ADMIN', 'HOSPITAL_ADMIN') or self.is_superuser

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()}) [{self.username}]"


class TenantScopedModel(models.Model):
    """
    Abstract base class enforcing multi-tenant isolation on all subordinate models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    branch = models.ForeignKey(HospitalBranch, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditLog(models.Model):
    """
    Immutable HIPAA/HITECH Audit Trail capturing sensitive medical and administrative actions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='audit_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100, help_text="e.g. VIEW_RECORDS, SIGN_ENCOUNTER, JOIN_TELEMEDICINE")
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {user_name} -> {self.action} on {self.resource_type}:{self.resource_id}"
