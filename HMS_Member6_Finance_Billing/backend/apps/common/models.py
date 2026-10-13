import uuid
from django.db import models
from apps.tenants.models import Tenant, Branch
from apps.tenants.middleware import get_current_tenant

def generate_entity_id():
    return f"ent-{uuid.uuid4().hex[:12]}"

class TenantScopedQuerySet(models.QuerySet):
    def for_tenant(self, tenant):
        if not tenant:
            return self
        return self.filter(tenant=tenant)

class TenantScopedManager(models.Manager):
    def get_queryset(self):
        return TenantScopedQuerySet(self.model, using=self._db)

    def for_tenant(self, tenant):
        return self.get_queryset().for_tenant(tenant)

class TenantScopedModel(models.Model):
    """
    Abstract base model guaranteeing tenant and branch partitioning for all financial entities.
    """
    id = models.CharField(max_length=64, primary_key=True, default=generate_entity_id)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=150, default='system')

    objects = TenantScopedManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Auto-assign active tenant if not set
        if not hasattr(self, 'tenant') or self.tenant_id is None:
            current_tenant = get_current_tenant()
            if current_tenant:
                self.tenant = current_tenant
        super().save(*args, **kwargs)
