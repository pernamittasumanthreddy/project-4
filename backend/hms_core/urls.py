import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from contracts.views import (
    TenantViewSet, HospitalBranchViewSet, UserProfileViewSet,
    PatientContractViewSet, ClinicalEncounterContractViewSet,
    BillingEventContractViewSet, TeamContractsSummaryView
)
from lis.views import (
    LabDashboardView, LabCatalogueViewSet, LabCategoryViewSet,
    LabTestPanelViewSet, LabOrderViewSet, SpecimenViewSet,
    LabResultViewSet, CriticalAlertViewSet, LabReportViewSet, TATAnalyticsView
)
from ris.views import (
    RadiologyDashboardView, ImagingModalityViewSet, ImagingProcedureViewSet,
    ImagingOrderViewSet, ModalityWorklistView, ImagingStudyViewSet,
    RadiologyReportViewSet, DICOMWebView
)

router = DefaultRouter()
# Contracts
router.register(r'contracts/tenants', TenantViewSet, basename='tenants')
router.register(r'contracts/branches', HospitalBranchViewSet, basename='branches')
router.register(r'contracts/users', UserProfileViewSet, basename='users')
router.register(r'contracts/patients', PatientContractViewSet, basename='patients')
router.register(r'contracts/encounters', ClinicalEncounterContractViewSet, basename='encounters')
router.register(r'contracts/billing-events', BillingEventContractViewSet, basename='billing-events')

# LIS
router.register(r'laboratory/catalogue', LabCatalogueViewSet, basename='lab-catalogue')
router.register(r'laboratory/categories', LabCategoryViewSet, basename='lab-categories')
router.register(r'laboratory/panels', LabTestPanelViewSet, basename='lab-panels')
router.register(r'laboratory/orders', LabOrderViewSet, basename='lab-orders')
router.register(r'laboratory/specimens', SpecimenViewSet, basename='lab-specimens')
router.register(r'laboratory/results', LabResultViewSet, basename='lab-results')
router.register(r'laboratory/critical-alerts', CriticalAlertViewSet, basename='lab-critical-alerts')
router.register(r'laboratory/reports', LabReportViewSet, basename='lab-reports')

# RIS
router.register(r'radiology/modalities', ImagingModalityViewSet, basename='ris-modalities')
router.register(r'radiology/procedures', ImagingProcedureViewSet, basename='ris-procedures')
router.register(r'radiology/orders', ImagingOrderViewSet, basename='ris-orders')
router.register(r'radiology/studies', ImagingStudyViewSet, basename='ris-studies')
router.register(r'radiology/reports', RadiologyReportViewSet, basename='ris-reports')

urlpatterns = [
    # OpenAPI Specification & Interactive Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Custom Dashboard & Analytics Endpoints
    path('api/contracts/summary/', TeamContractsSummaryView.as_view(), name='contracts-summary'),
    path('api/laboratory/dashboard/', LabDashboardView.as_view(), name='lab-dashboard'),
    path('api/laboratory/tat-analytics/', TATAnalyticsView.as_view(), name='lab-tat-analytics'),
    path('api/radiology/dashboard/', RadiologyDashboardView.as_view(), name='ris-dashboard'),
    path('api/radiology/worklist/', ModalityWorklistView.as_view(), name='ris-worklist'),

    # DICOMweb Standard PS3.18 REST Services
    path('api/dicomweb/studies/', DICOMWebView.as_view(), name='dicomweb-studies'),
    path('api/dicomweb/studies/<str:study_uid>/metadata/', DICOMWebView.as_view(), {'action': 'metadata'}, name='dicomweb-metadata'),
    path('api/dicomweb/studies/<str:study_uid>/metadata', DICOMWebView.as_view(), {'action': 'metadata'}),
    path('api/dicomweb/studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>/', DICOMWebView.as_view(), name='dicomweb-instance'),
    path('api/dicomweb/studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>', DICOMWebView.as_view()),
    path('api/dicomweb/studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>/<str:action>/', DICOMWebView.as_view(), name='dicomweb-instance-action'),
    path('api/dicomweb/studies/<str:study_uid>/series/<str:series_uid>/instances/<str:instance_uid>/<str:action>', DICOMWebView.as_view()),

    # Router APIs
    path('api/', include(router.urls)),

    # Frontend Single-Page App Static Fallback
    re_path(r'^(?!api|static|media|dicom).*$', serve, {
        'document_root': settings.BASE_DIR.parent / 'frontend',
        'path': 'index.html',
    }),
]
