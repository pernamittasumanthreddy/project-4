from django.urls import path, include
from rest_framework.routers import DefaultRouter
from admissions.views import WardViewSet, AdmissionViewSet

router = DefaultRouter()
router.register(r"wards", WardViewSet, basename="ward")
router.register(r"admissions", AdmissionViewSet, basename="admission")

urlpatterns = [
    path("", include(router.urls)),
]
