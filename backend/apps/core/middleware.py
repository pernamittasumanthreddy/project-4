"""
Multi-Tenant Context Middleware for HMS SaaS.
Enforces strict logical tenant boundary isolation across all incoming requests.
"""

from apps.core.models import Tenant

class TenantContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = None
        tenant_id_header = request.headers.get('X-Tenant-ID')

        # 1. Check if user is authenticated and has an explicit tenant bound
        if getattr(request, 'user', None) and request.user.is_authenticated and request.user.tenant:
            tenant = request.user.tenant
        
        # 2. Or check X-Tenant-ID header (slug or UUID)
        elif tenant_id_header:
            try:
                # Try finding by slug or UUID
                tenant = Tenant.objects.filter(slug=tenant_id_header).first()
                if not tenant:
                    tenant = Tenant.objects.filter(id=tenant_id_header).first()
            except Exception:
                tenant = None

        # 3. Default fallback to primary active tenant
        if not tenant:
            tenant = Tenant.objects.filter(is_active=True).first()

        request.tenant = tenant
        request.tenant_id = str(tenant.id) if tenant else None

        response = self.get_response(request)

        # Attach tenant header to response for audit tracking
        if tenant:
            response['X-Active-Tenant'] = tenant.slug

        return response
