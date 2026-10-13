"""HMS Accounts Models — Member 1 Foundation
Provides Custom User with Role-Based Access Control (RBAC), tenant & branch assignment.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import Tenant, Branch


class UserRole(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'SaaS Super Administrator'
    HOSPITAL_ADMIN = 'HOSPITAL_ADMIN', 'Hospital Administrator'
    PHARMACIST = 'PHARMACIST', 'Pharmacist'
    INVENTORY_MANAGER = 'INVENTORY_MANAGER', 'Inventory Manager'
    DOCTOR = 'DOCTOR', 'Doctor'
    NURSE = 'NURSE', 'Nurse'
    BILLING_OFFICER = 'BILLING_OFFICER', 'Billing Officer'
    PATIENT = 'PATIENT', 'Patient'


class User(AbstractUser):
    """Custom user model bound to multi-tenant organization and hospital branch."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.PHARMACIST)
    phone = models.CharField(max_length=30, blank=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True, help_text="Professional license number")

    class Meta:
        db_table = 'accounts_users'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()}) - {self.tenant.name if self.tenant else 'Global'}"

    @property
    def is_pharmacist(self):
        return self.role in [UserRole.PHARMACIST, UserRole.HOSPITAL_ADMIN, UserRole.SUPER_ADMIN]

    @property
    def is_inventory_manager(self):
        return self.role in [UserRole.INVENTORY_MANAGER, UserRole.HOSPITAL_ADMIN, UserRole.SUPER_ADMIN]
