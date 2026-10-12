from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointments.views import DoctorScheduleViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r"schedules", DoctorScheduleViewSet, basename="doctor-schedule")
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("", include(router.urls)),
]

