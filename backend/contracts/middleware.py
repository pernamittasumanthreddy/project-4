from .models import Tenant, HospitalBranch, UserProfile

class TenantHeaderMiddleware:
    """
    Multi-tenant request resolution middleware:
    Resolves tenant and branch from HTTP headers:
    - X-Tenant-Code / X-Tenant-ID
    - X-Branch-ID
    - X-User-Role / X-User-ID
    Enforces tenant context on request object.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_code = request.headers.get('X-Tenant-Code')
        tenant_id = request.headers.get('X-Tenant-ID')
        branch_id = request.headers.get('X-Branch-ID')

        tenant = None
        branch = None

        if tenant_code:
            tenant = Tenant.objects.filter(code=tenant_code, is_active=True).first()
        elif tenant_id:
            tenant = Tenant.objects.filter(id=tenant_id, is_active=True).first()
        
        if not tenant:
            tenant = Tenant.objects.filter(is_active=True).first()

        if tenant and branch_id:
            branch = HospitalBranch.objects.filter(id=branch_id, tenant=tenant).first()
        elif tenant:
            branch = HospitalBranch.objects.filter(tenant=tenant).first()

        request.tenant = tenant
        request.branch = branch

        # User profile resolution
        role_header = request.headers.get('X-User-Role')
        username_header = request.headers.get('X-Username', 'system_tech')
        if tenant:
            user_profile = UserProfile.objects.filter(tenant=tenant, username=username_header).first()
            if not user_profile and role_header:
                user_profile = UserProfile.objects.filter(tenant=tenant, role=role_header).first()
            request.user_profile = user_profile
        else:
            request.user_profile = None

        response = self.get_response(request)
        if tenant:
            response['X-Tenant-Code'] = tenant.code
        return response
