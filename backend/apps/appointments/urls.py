from django.urls import path
from apps.appointments import views

urlpatterns = [
    path('departments/', views.DepartmentListView.as_view(), name='departments-list'),
    path('doctors/', views.DoctorDirectoryView.as_view(), name='doctors-list'),
    path('doctors/<uuid:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctors/<uuid:doctor_id>/available-slots/', views.DoctorAvailableSlotsView.as_view(), name='doctor-slots'),
    path('', views.AppointmentListCreateView.as_view(), name='appointments-list-create'),
    path('<uuid:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<uuid:pk>/cancel/', views.AppointmentCancelView.as_view(), name='appointment-cancel'),
]
