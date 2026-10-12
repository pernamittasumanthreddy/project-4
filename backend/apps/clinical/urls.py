from django.urls import path
from apps.clinical import views

urlpatterns = [
    path('encounters/', views.EncounterListCreateView.as_view(), name='encounters-list-create'),
    path('encounters/<uuid:pk>/', views.EncounterDetailView.as_view(), name='encounter-detail'),
    path('encounters/<uuid:pk>/sign/', views.EncounterSignView.as_view(), name='encounter-sign'),
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescriptions-list'),
    path('patient/<uuid:patient_id>/summary/', views.PatientEMRSummaryView.as_view(), name='patient-emr-summary'),
]
