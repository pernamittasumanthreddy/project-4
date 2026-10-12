from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'tenant', 'branch', 'is_staff')
    list_filter = ('role', 'tenant', 'branch', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Tenant & HMS Role', {'fields': ('tenant', 'branch', 'role', 'phone', 'employee_id', 'license_number')}),
    )
