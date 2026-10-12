from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.core.models import Tenant, HospitalBranch, User, AuditLog

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tier', 'domain', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'domain')
    list_filter = ('tier', 'is_active')

@admin.register(HospitalBranch)
class HospitalBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'tenant', 'city', 'is_active')
    search_fields = ('name', 'code', 'city')
    list_filter = ('tenant', 'is_active')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'tenant', 'is_active')
    list_filter = ('role', 'tenant', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Healthcare SaaS Profile', {'fields': ('tenant', 'branch', 'role', 'phone', 'avatar_url')}),
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'tenant', 'user', 'action', 'resource_type', 'resource_id', 'ip_address')
    list_filter = ('action', 'resource_type', 'tenant')
    search_fields = ('action', 'resource_id', 'user__username')
    readonly_fields = ('timestamp',)
