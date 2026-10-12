from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ris.views import (
    RadiologyDashboardView, ImagingModalityViewSet, ImagingProcedureViewSet,
    ImagingOrderViewSet, ModalityWorklistView, ImagingStudyViewSet,
    RadiologyReportViewSet
)

router = DefaultRouter()
router.register(r'modalities', ImagingModalityViewSet, basename='ris-modalities')
router.register(r'procedures', ImagingProcedureViewSet, basename='ris-procedures')
router.register(r'orders', ImagingOrderViewSet, basename='ris-orders')
router.register(r'studies', ImagingStudyViewSet, basename='ris-studies')
router.register(r'reports', RadiologyReportViewSet, basename='ris-reports')

urlpatterns = [
    path('dashboard/', RadiologyDashboardView.as_view(), name='ris-dashboard'),
    path('worklist/', ModalityWorklistView.as_view(), name='ris-worklist'),
    path('', include(router.urls)),
]
