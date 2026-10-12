import uuid
from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    """
    Represents an independent Healthcare Organization/Hospital Tenant.
    Maintained collaboratively with Member 1 (Platform & SaaS Admin).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, help_text="Full registered hospital name")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL safe unique identifier")
    mrn_prefix = models.CharField(max_length=10, default="MRN", help_text="Prefix used in patient MRN numbers")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hms_tenants"
        ordering = ["name"]

    def __str__(self):
        return self.name


class HospitalBranch(models.Model):
    """
    Represents physical branches of a Hospital Tenant.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, help_text="Branch code, e.g. MAIN, DWTN")
    address = models.TextField(blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hms_branches"
        unique_together = ("tenant", "code")
        ordering = ["tenant", "name"]

    def __str__(self):
        return f"{self.tenant.name} - {self.name} ({self.code})"


class Department(models.Model):
    """
    Represents clinical & operational departments (e.g. Cardiology, OPD, Orthopedics).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="departments")
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name="departments", null=True, blank=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    is_clinical = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "hms_departments"
        unique_together = ("tenant", "code")

    def __str__(self):
        return f"{self.name} ({self.code})"


class TenantAwareModel(models.Model):
    """
    Abstract base model that enforces mandatory tenant scoping,
    UUID primary keys, audit timestamps, and soft-delete capabilities.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_records",
        help_text="Tenant boundary to guarantee multi-tenant data isolation."
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])


class AuditLog(models.Model):
    """
    Immutable security and data modification audit log for compliance.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="audit_logs")
    actor_id = models.CharField(max_length=100, default="system")
    actor_email = models.CharField(max_length=255, blank=True, default="")
    action = models.CharField(max_length=50, help_text="CREATE, UPDATE, DELETE, VIEW, MERGE, EXPORT")
    entity_name = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "hms_audit_logs"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"[{self.action}] {self.entity_name}:{self.entity_id} by {self.actor_email} at {self.timestamp}"
