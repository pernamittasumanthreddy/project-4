from django.urls import path
from apps.telemedicine import views

urlpatterns = [
    path('ice-config/', views.TelemedicineIceConfigView.as_view(), name='telemedicine-ice-config'),
    path('appointment/<uuid:appointment_id>/', views.TelemedicineSessionForAppointmentView.as_view(), name='telemedicine-appointment-session'),
    path('sessions/<uuid:pk>/', views.TelemedicineSessionDetailView.as_view(), name='telemedicine-session-detail'),
    path('sessions/<uuid:session_id>/join/', views.TelemedicineJoinRoomView.as_view(), name='telemedicine-session-join'),
    path('sessions/<uuid:session_id>/signaling/', views.TelemedicineSignalingView.as_view(), name='telemedicine-signaling'),
    path('sessions/<uuid:session_id>/leave/', views.TelemedicineLeaveRoomView.as_view(), name='telemedicine-session-leave'),
]
