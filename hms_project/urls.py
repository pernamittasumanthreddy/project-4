"""HMS Project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/pharmacy/', include('pharmacy.urls')),
    path('pharmacy/', include('pharmacy.ui_urls')),
    path('', lambda req: redirect('pharmacy_dashboard')),
]
