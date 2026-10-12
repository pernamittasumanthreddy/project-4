from django.urls import path
from apps.patient_portal import views

urlpatterns = [
    path('dashboard/', views.PatientDashboardView.as_view(), name='patient-dashboard'),
    path('profile/', views.PatientProfileView.as_view(), name='patient-profile'),
    path('medical-records/', views.PatientMedicalRecordsView.as_view(), name='patient-records'),
    path('billing/', views.PatientBillingSummaryView.as_view(), name='patient-billing'),
]
