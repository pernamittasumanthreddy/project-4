from django.urls import path
from apps.doctor_portal import views

urlpatterns = [
    path('dashboard/', views.DoctorDashboardView.as_view(), name='doctor-dashboard'),
    path('schedule/', views.DoctorScheduleAgendaView.as_view(), name='doctor-schedule'),
    path('consultation/<uuid:appointment_id>/', views.DoctorConsultationWorkspaceView.as_view(), name='doctor-consultation'),
]
