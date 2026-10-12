"""HMS Core Models — Member 1 Foundation
Provides multi-tenant data isolation, hospital hierarchy, branch management, and audit trail.
"""

import uuid
from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    """Multi-tenant SaaS root entity representing a healthcare organization."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    subdomain = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_tenants'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.subdomain})"


class Hospital(models.Model):
    """Hospital facility owned by a tenant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='hospitals')
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    tax_identifier = models.CharField(max_length=50, blank=True, null=True, help_text="GSTIN / PAN / Tax Registration")
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_hospitals'
        unique_together = ('tenant', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.tenant.name}"


class Branch(models.Model):
    """Individual hospital branch location."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    is_main_branch = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_branches'
        unique_together = ('hospital', 'code')
        ordering = ['name']

    @property
    def tenant(self):
        return self.hospital.tenant

    def __str__(self):
        return f"{self.name} [{self.code}] - {self.hospital.name}"


class Department(models.Model):
    """Department within a hospital branch (e.g., Pharmacy, Outpatient, ICU)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'core_departments'
        unique_together = ('branch', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.branch.name})"


class TenantQuerySet(models.QuerySet):
    """Custom QuerySet ensuring tenant-scoped access across queries."""
    def for_tenant(self, tenant):
        if not tenant:
            return self.none()
        return self.filter(tenant=tenant)

    def for_branch(self, branch):
        if not branch:
            return self.none()
        return self.filter(branch=branch)


class TenantManager(models.Manager):
    """Manager returning TenantQuerySet."""
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_tenant(self, tenant):
        return self.get_queryset().for_tenant(tenant)

    def for_branch(self, branch):
        return self.get_queryset().for_branch(branch)


class BaseTenantModel(models.Model):
    """Abstract base model implementing tenant and branch scoping."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TenantManager()

    class Meta:
        abstract = True


class AuditEvent(models.Model):
    """Immutable audit trail for security, sensitive modifications, and compliance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    actor_id = models.CharField(max_length=100, null=True, blank=True)
    actor_email = models.CharField(max_length=255, null=True, blank=True)
    event_type = models.CharField(max_length=100, db_index=True)
    resource_type = models.CharField(max_length=100, db_index=True)
    resource_id = models.CharField(max_length=100, db_index=True)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'core_audit_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at}] {self.event_type} on {self.resource_type}:{self.resource_id}"
