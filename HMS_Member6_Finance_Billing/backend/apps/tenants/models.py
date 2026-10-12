import uuid
from django.db import models

def generate_tenant_id():
    return f"tenant-{uuid.uuid4().hex[:12]}"

def generate_branch_id():
    return f"branch-{uuid.uuid4().hex[:12]}"

class Tenant(models.Model):
    """
    Hospital Organization / Multi-tenant entity.
    """
    id = models.CharField(max_length=64, primary_key=True, default=generate_tenant_id)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    subscription_tier = models.CharField(
        max_length=50,
        choices=[('STARTER', 'Starter'), ('PRO', 'Professional'), ('ENTERPRISE', 'Enterprise')],
        default='ENTERPRISE'
    )
    is_active = models.BooleanField(default=True)
    default_currency = models.CharField(max_length=3, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Branch(models.Model):
    """
    Hospital Branch under a Tenant Organization.
    """
    id = models.CharField(max_length=64, primary_key=True, default=generate_branch_id)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state_code = models.CharField(max_length=10, help_text="e.g. '07' for Delhi, '27' for Maharashtra")
    gstin = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'code')

    def __str__(self):
        return f"{self.name} [{self.code}] - {self.tenant.name}"
