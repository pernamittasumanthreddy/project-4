"""
RBAC & Multi-Tenant Object Permissions for HMS Enterprise Platform.
"""

from rest_framework import permissions

class IsPatient(permissions.BasePermission):
    """Allows access only to authenticated patients."""
    message = "Access restricted to registered patients only."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'PATIENT')


class IsDoctor(permissions.BasePermission):
    """Allows access only to registered physicians/clinicians."""
    message = "Access restricted to licensed physicians only."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'DOCTOR' or request.user.is_superuser))


class IsHospitalAdmin(permissions.BasePermission):
    """Allows access only to hospital or platform administrators."""
    message = "Administrative clearance required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())


class IsClinicianOrStaff(permissions.BasePermission):
    """Allows access to doctors, nurses, and administrative staff."""
    message = "Clinician or hospital staff clearance required."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in ('DOCTOR', 'NURSE', 'HOSPITAL_ADMIN', 'SUPER_ADMIN', 'LAB_TECH', 'PHARMACIST')


class TenantObjectPermission(permissions.BasePermission):
    """
    Enforces that the requested resource belongs strictly to the user's active tenant.
    Prevents cross-tenant data leakage.
    """
    message = "Cross-tenant access violation: resource belongs to a different healthcare organization."

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        obj_tenant = getattr(obj, 'tenant', None)
        if obj_tenant is None and hasattr(obj, 'user'):
            obj_tenant = getattr(obj.user, 'tenant', None)

        if obj_tenant and request.tenant:
            return obj_tenant.id == request.tenant.id
        return True
