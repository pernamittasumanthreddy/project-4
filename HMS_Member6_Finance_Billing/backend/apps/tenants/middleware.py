import threading
from django.utils.deprecation import MiddlewareMixin
from .models import Tenant

_thread_locals = threading.local()

def get_current_tenant():
    return getattr(_thread_locals, 'tenant', None)

def set_current_tenant(tenant):
    _thread_locals.tenant = tenant

class TenantHeaderMiddleware(MiddlewareMixin):
    """
    Resolves the active tenant from the 'X-Tenant-ID' request header.
    Falls back gracefully to the first active tenant in development.
    """
    def process_request(self, request):
        tenant_id = request.headers.get('X-Tenant-ID') or request.META.get('HTTP_X_TENANT_ID')
        tenant = None

        if tenant_id:
            tenant = Tenant.objects.filter(id=tenant_id, is_active=True).first()
            if not tenant:
                # Also check slug
                tenant = Tenant.objects.filter(slug=tenant_id, is_active=True).first()

        if not tenant:
            # Development fallback
            tenant = Tenant.objects.filter(is_active=True).first()

        request.tenant = tenant
        set_current_tenant(tenant)

    def process_response(self, request, response):
        set_current_tenant(None)
        return response
