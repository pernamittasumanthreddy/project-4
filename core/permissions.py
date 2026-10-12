"""HMS Core Permissions & Audit Utilities — Member 1 Foundation"""

from rest_framework import permissions
from core.models import AuditEvent


class HasTenantAccess(permissions.BasePermission):
    """Enforces that authenticated users can only access resources matching their tenant."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.tenant is not None and (
            not request.user.tenant or str(request.user.tenant.id) == str(request.tenant.id)
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if hasattr(obj, 'tenant'):
            return str(obj.tenant.id) == str(request.tenant.id)
        return True


class IsBranchAuthorized(permissions.BasePermission):
    """Enforces branch level access when applicable."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if hasattr(obj, 'branch') and obj.branch and request.branch:
            return str(obj.branch.id) == str(request.branch.id)
        return True


def record_audit_event(tenant, event_type, resource_type, resource_id, actor=None, details=None, branch=None, ip_address=None):
    """Records an immutable audit event."""
    try:
        actor_id = str(actor.id) if actor else 'system'
        actor_email = getattr(actor, 'email', 'system@hms.local') if actor else 'system@hms.local'
        return AuditEvent.objects.create(
            tenant=tenant,
            branch=branch,
            actor_id=actor_id,
            actor_email=actor_email,
            event_type=event_type,
            resource_type=resource_type,
            resource_id=str(resource_id),
            details=details or {},
            ip_address=ip_address
        )
    except Exception:
        return None
