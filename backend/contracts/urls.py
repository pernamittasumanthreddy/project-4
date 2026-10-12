from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contracts.views import (
    TenantViewSet, HospitalBranchViewSet, UserProfileViewSet,
    PatientContractViewSet, ClinicalEncounterContractViewSet,
    BillingEventContractViewSet, TeamContractsSummaryView
)

router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenants')
router.register(r'branches', HospitalBranchViewSet, basename='branches')
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'patients', PatientContractViewSet, basename='patients')
router.register(r'encounters', ClinicalEncounterContractViewSet, basename='encounters')
router.register(r'billing-events', BillingEventContractViewSet, basename='billing-events')

urlpatterns = [
    path('summary/', TeamContractsSummaryView.as_view(), name='contracts-summary'),
    path('', include(router.urls)),
]
