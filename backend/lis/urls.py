from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lis.views import (
    LabDashboardView, LabCatalogueViewSet, LabCategoryViewSet,
    LabTestPanelViewSet, LabOrderViewSet, SpecimenViewSet,
    LabResultViewSet, CriticalAlertViewSet, LabReportViewSet, TATAnalyticsView
)

router = DefaultRouter()
router.register(r'catalogue', LabCatalogueViewSet, basename='lab-catalogue')
router.register(r'categories', LabCategoryViewSet, basename='lab-categories')
router.register(r'panels', LabTestPanelViewSet, basename='lab-panels')
router.register(r'orders', LabOrderViewSet, basename='lab-orders')
router.register(r'specimens', SpecimenViewSet, basename='lab-specimens')
router.register(r'results', LabResultViewSet, basename='lab-results')
router.register(r'critical-alerts', CriticalAlertViewSet, basename='lab-critical-alerts')
router.register(r'reports', LabReportViewSet, basename='lab-reports')

urlpatterns = [
    path('dashboard/', LabDashboardView.as_view(), name='lab-dashboard'),
    path('tat-analytics/', TATAnalyticsView.as_view(), name='lab-tat-analytics'),
    path('', include(router.urls)),
]
