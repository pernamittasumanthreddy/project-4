from django.urls import path
from apps.diagnostics import views

urlpatterns = [
    path('lab-reports/', views.LabReportListView.as_view(), name='lab-reports-list'),
    path('lab-reports/<uuid:pk>/', views.LabReportDetailView.as_view(), name='lab-report-detail'),
    path('lab-reports/<uuid:pk>/approve/', views.LabReportApproveView.as_view(), name='lab-report-approve'),
    path('radiology-reports/', views.RadiologyReportListView.as_view(), name='radiology-reports-list'),
    path('radiology-reports/<uuid:pk>/', views.RadiologyReportDetailView.as_view(), name='radiology-report-detail'),
]
