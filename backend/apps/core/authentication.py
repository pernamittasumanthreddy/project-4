"""
Authentication handlers for HMS Multi-Tenant Platform.
Supports standard Django Session, Token, and Demo Header Authentication for local execution.
"""

from rest_framework import authentication
from apps.core.models import User

class DemonstrationSessionAuthentication(authentication.BaseAuthentication):
    """
    Demonstration & QA Authentication Provider.
    Enables zero-friction local testing and 1-Click Role Switcher across:
    - Super Admin
    - Doctor (Dr. Sophia Chen, Dr. Marcus Vance)
    - Patient (Priya Sharma, David Miller)
    - Staff / Lab / Pharmacy
    without storing hardcoded private tokens in git or requiring external authentication vendors.
    """

    def authenticate(self, request):
        django_request = getattr(request, '_request', request)
        
        # 1. Check HTTP header from META (e.g. HTTP_X_IMPERSONATE_USER)
        impersonate_username = django_request.META.get('HTTP_X_IMPERSONATE_USER')
        
        if impersonate_username:
            user = User.objects.filter(username=impersonate_username, is_active=True).first()
            if user:
                return (user, None)
        
        # 2. Check session user on raw django request without triggering DRF recursion
        raw_user = getattr(django_request, 'user', None)
        if raw_user and raw_user.is_authenticated:
            return (raw_user, None)

        return None
