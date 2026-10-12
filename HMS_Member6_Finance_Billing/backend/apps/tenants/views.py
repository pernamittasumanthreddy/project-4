from rest_framework import viewsets, permissions
from .models import Tenant, Branch
from .serializers import TenantSerializer, BranchSerializer

class TenantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Tenant Organization read endpoints for multi-tenant switching.
    """
    queryset = Tenant.objects.filter(is_active=True)
    serializer_class = TenantSerializer
    permission_classes = [permissions.AllowAny]

class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Hospital Branch list and details.
    """
    queryset = Branch.objects.filter(is_active=True)
    serializer_class = BranchSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return qs.filter(tenant=self.request.tenant)
        return qs
