"""
Master API URL Configuration for HMS Multi-Tenant Platform.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # OpenAPI Schema & Interactive Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Admin
    path("admin/", admin.site.urls),

    # Member 2 Modules
    path("api/patients/", include("patients.urls")),
    path("api/appointments/", include("appointments.urls")),
    path("api/admissions/", include("admissions.urls")),

    # Member 3 Modules
    path("api/clinical/", include("clinical.urls")),

    # Member 4 Modules (Laboratory & Radiology)
    path("api/laboratory/", include("lis.urls")),
    path("api/radiology/", include("ris.urls")),
    path("api/dicomweb/", include("ris.dicomweb_urls")),
    path("api/contracts/", include("contracts.urls")),

    # Direct redirects for root and /docs
    path("docs/", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("docs", RedirectView.as_view(url="/api/docs/", permanent=False)),
]
