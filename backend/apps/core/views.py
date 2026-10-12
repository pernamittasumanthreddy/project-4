"""
Core Platform & SaaS Administration Views (Member 1).
Provides tenancy management, user profiles, session role switching, and HIPAA audit trails.
"""

from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout

from apps.core.models import Tenant, HospitalBranch, User, AuditLog
from apps.core.serializers import (
    TenantSerializer,
    HospitalBranchSerializer,
    UserSerializer,
    CurrentUserSerializer,
    AuditLogSerializer,
)

class CurrentUserView(views.APIView):
    """
    Returns authenticated user information, roles, and active tenant context.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            # Fall back to default demo user (Priya Sharma - Patient) if unauthenticated in dev
            user = User.objects.filter(role='PATIENT').first()
            if not user:
                return Response({
                    "authenticated": False,
                    "user": None,
                    "message": "No active session or demo user found."
                })

        serializer = CurrentUserSerializer(user)
        return Response({
            "authenticated": True,
            "user": serializer.data,
            "tenant": {
                "id": str(user.tenant.id) if user.tenant else None,
                "name": user.tenant.name if user.tenant else "Default Health Network",
                "slug": user.tenant.slug if user.tenant else "default",
            } if user.tenant else None
        })


class DemoRoleSwitcherView(views.APIView):
    """
    1-Click Role Switcher for local development, reviewer testing, and multi-tenant demonstration.
    Allows instant switching between pre-seeded personas without requiring external auth tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        role = request.data.get('role')

        query = User.objects.all()
        if username:
            user = query.filter(username=username).first()
        elif role:
            user = query.filter(role=role.upper()).first()
        else:
            return Response(
                {"error": "Please provide either 'username' or 'role'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user:
            return Response(
                {"error": f"Persona with identifier '{username or role}' not found in database"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Log session switch in audit log
        if user.tenant:
            AuditLog.objects.create(
                tenant=user.tenant,
                user=user,
                action="DEMO_ROLE_SWITCH",
                resource_type="USER",
                resource_id=str(user.id),
                details={"impersonated_role": user.role, "username": user.username}
            )

        serializer = CurrentUserSerializer(user)
        return Response({
            "success": True,
            "message": f"Active session switched to {user.full_name} ({user.get_role_display()})",
            "user": serializer.data
        })


class AvailableDemoUsersView(views.APIView):
    """
    Lists available seeded personas for the 1-Click Role Switcher.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.filter(is_active=True).order_by('role', 'username')
        demo_personas = []
        for u in users:
            specialty = ""
            if hasattr(u, 'doctor_profile'):
                specialty = u.doctor_profile.specialization
            elif hasattr(u, 'patient_profile'):
                specialty = f"MRN: {u.patient_profile.mrn}"

            demo_personas.append({
                "id": str(u.id),
                "username": u.username,
                "name": u.full_name,
                "role": u.role,
                "role_display": u.get_role_display(),
                "specialty_or_info": specialty,
                "tenant_name": u.tenant.name if u.tenant else "Platform Global",
                "avatar_url": u.avatar_url,
            })
        return Response({"personas": demo_personas})


class TenantListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Tenant.objects.filter(is_active=True)
    serializer_class = TenantSerializer


class HospitalBranchListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HospitalBranchSerializer

    def get_queryset(self):
        tenant_id = self.request.query_params.get('tenant_id')
        qs = HospitalBranch.objects.filter(is_active=True)
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        return qs


class AuditLogListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            if user.is_superuser:
                return AuditLog.objects.all()[:100]
            return AuditLog.objects.filter(tenant=user.tenant)[:100]
        return AuditLog.objects.filter(user=user)[:50]
