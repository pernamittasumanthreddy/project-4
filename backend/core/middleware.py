from core.models import Tenant

class TenantHeaderMiddleware:
    """
    Extracts the tenant identifier from request headers (X-Tenant-ID or X-Tenant-Slug).
    Attaches the resolved tenant object to request.tenant.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_id = request.headers.get("X-Tenant-ID")
        tenant_slug = request.headers.get("X-Tenant-Slug")

        request.tenant = None

        if tenant_id:
            try:
                request.tenant = Tenant.objects.filter(id=tenant_id, is_active=True).first()
            except Exception:
                pass
        elif tenant_slug:
            request.tenant = Tenant.objects.filter(slug=tenant_slug, is_active=True).first()
        else:
            # Fallback for development if no header provided
            request.tenant = Tenant.objects.filter(is_active=True).first()

        response = self.get_response(request)
        return response
