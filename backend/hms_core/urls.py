"""
Master API URL Configuration for HMS.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Direct redirects for root and /docs
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("docs/", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("docs", RedirectView.as_view(url="/api/docs/", permanent=False)),

    # Admin
    path("admin/", admin.site.urls),

    # OpenAPI Schema & Interactive Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Member 2 Modules
    path("api/patients/", include("patients.urls")),
    path("api/appointments/", include("appointments.urls")),
    path("api/admissions/", include("admissions.urls")),
    # Member 3 Modules
    path("api/clinical/", include("clinical.urls")),
]
