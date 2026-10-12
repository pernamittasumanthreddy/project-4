"""HMS Template Context Processors — Member 1 Foundation"""

def tenant_context(request):
    """Provides current tenant and branch context to UI templates."""
    return {
        'current_tenant': getattr(request, 'tenant', None),
        'current_branch': getattr(request, 'branch', None),
        'user_role': getattr(request.user, 'role', 'GUEST') if request.user.is_authenticated else 'GUEST',
    }
