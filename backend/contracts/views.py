from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tenant, HospitalBranch, UserProfile, PatientContract, ClinicalEncounterContract, BillingEventContract
from .serializers import (
    TenantSerializer, HospitalBranchSerializer, UserProfileSerializer,
    PatientContractSerializer, ClinicalEncounterContractSerializer, BillingEventContractSerializer
)

class TenantViewSet(viewsets.ReadOnlyModelViewSet):
    """Member 1 Contract: Lists active tenants"""
    queryset = Tenant.objects.filter(is_active=True)
    serializer_class = TenantSerializer

class HospitalBranchViewSet(viewsets.ReadOnlyModelViewSet):
    """Member 1 Contract: Hospital branches scoped by tenant"""
    serializer_class = HospitalBranchSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return HospitalBranch.objects.filter(tenant=tenant, is_active=True)
        return HospitalBranch.objects.filter(is_active=True)

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """Member 1 Contract: User and RBAC profiles"""
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return UserProfile.objects.filter(tenant=tenant)
        return UserProfile.objects.all()

class PatientContractViewSet(viewsets.ModelViewSet):
    """Member 2 Contract: Patient Demographic Registry"""
    serializer_class = PatientContractSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return PatientContract.objects.filter(tenant=tenant)
        return PatientContract.objects.all()

class ClinicalEncounterContractViewSet(viewsets.ModelViewSet):
    """Member 3 Contract: Clinical Encounters"""
    serializer_class = ClinicalEncounterContractSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return ClinicalEncounterContract.objects.filter(tenant=tenant)
        return ClinicalEncounterContract.objects.all()

class BillingEventContractViewSet(viewsets.ReadOnlyModelViewSet):
    """Member 6 Contract: Emitted billing events for lab and radiology procedures"""
    serializer_class = BillingEventContractSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return BillingEventContract.objects.filter(tenant=tenant).order_by('-emitted_at')
        return BillingEventContract.objects.all().order_by('-emitted_at')

class TeamContractsSummaryView(APIView):
    """Provides high-level health and integration state across Members 1, 2, 3, 6"""
    def get(self, request):
        tenant = getattr(request, 'tenant', None)
        tenants = Tenant.objects.all()
        return Response({
            'active_tenant': TenantSerializer(tenant).data if tenant else None,
            'all_tenants': TenantSerializer(tenants, many=True).data,
            'contracts_status': {
                'member_1_auth_tenant': 'READY (Multi-tenant headers active)',
                'member_2_patients': f"{PatientContract.objects.filter(tenant=tenant).count() if tenant else 0} synced records",
                'member_3_clinical': f"{ClinicalEncounterContract.objects.filter(tenant=tenant).count() if tenant else 0} encounters",
                'member_6_billing': f"{BillingEventContract.objects.filter(tenant=tenant).count() if tenant else 0} billable events emitted",
            }
        })
