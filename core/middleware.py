"""HMS Core Middleware — Member 1 Foundation
Resolves tenant context and active branch on incoming requests.
"""

import sys
from django.conf import settings
from core.models import Tenant, Branch
from accounts.models import User


class TenantMiddleware:
    """Extracts and verifies tenant context for the current request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        request.branch = None

        # 0. Dev environment auto-login fallback (seamless UI exploration outside pytest)
        if getattr(settings, 'DEBUG', False) and 'pytest' not in sys.modules:
            if hasattr(request, 'user') and not request.user.is_authenticated:
                dev_user = User.objects.filter(username='pharmacist').first()
                if dev_user:
                    request.user = dev_user

        # 1. Resolve from authenticated user
        if hasattr(request, 'user') and request.user.is_authenticated:
            request.tenant = getattr(request.user, 'tenant', None)
            request.branch = getattr(request.user, 'branch', None)


        # 2. Allow X-Tenant-ID header override if authorized or in dev
        header_tenant_id = request.headers.get('X-Tenant-ID')
        if header_tenant_id:
            try:
                found_tenant = Tenant.objects.filter(id=header_tenant_id, is_active=True).first()
                if found_tenant:
                    # If user is superuser or belongs to that tenant
                    if not request.tenant or request.user.is_superuser or str(request.tenant.id) == str(found_tenant.id):
                        request.tenant = found_tenant
            except Exception:
                pass

        header_branch_id = request.headers.get('X-Branch-ID')
        if header_branch_id:
            try:
                found_branch = Branch.objects.filter(id=header_branch_id, is_active=True).first()
                if found_branch:
                    if not request.tenant or str(found_branch.tenant.id) == str(request.tenant.id):
                        request.branch = found_branch
                        request.tenant = found_branch.tenant
            except Exception:
                pass

        # 3. Fallback for public development sessions
        if not request.tenant:
            request.tenant = Tenant.objects.filter(is_active=True).first()
            if request.tenant and not request.branch:
                request.branch = Branch.objects.filter(hospital__tenant=request.tenant, is_active=True).first()

        response = self.get_response(request)
        return response
