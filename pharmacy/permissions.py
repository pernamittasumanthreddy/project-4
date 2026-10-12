"""HMS Pharmacy Permissions — Member 5
Integrates with Member 1 RBAC system enforcing granular pharmacy operational access.
"""

from rest_framework import permissions
from accounts.models import UserRole


class IsPharmacistOrAdmin(permissions.BasePermission):
    """Permits access to Pharmacists, Hospital Admins, and Super Admins."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in [
            UserRole.PHARMACIST,
            UserRole.HOSPITAL_ADMIN,
            UserRole.SUPER_ADMIN
        ]


class IsInventoryManagerOrAdmin(permissions.BasePermission):
    """Permits access to Inventory Managers, Hospital Admins, and Super Admins."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in [
            UserRole.INVENTORY_MANAGER,
            UserRole.HOSPITAL_ADMIN,
            UserRole.SUPER_ADMIN
        ]


class CanApprovePurchaseOrder(permissions.BasePermission):
    """Only Hospital Admins and Super Admins may authorize purchase orders."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in [UserRole.HOSPITAL_ADMIN, UserRole.SUPER_ADMIN]


class CanDispensePrescription(permissions.BasePermission):
    """Only certified Pharmacists and Admins may dispense clinical prescriptions."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.role in [UserRole.PHARMACIST, UserRole.HOSPITAL_ADMIN]
