"""HMS Pharmacy UI URLs — Member 5"""

from django.urls import path
from pharmacy.views.ui_views import (
    pharmacy_dashboard,
    medicine_catalogue,
    batch_management,
    dispensing_queue,
    purchasing_management,
    returns_and_quarantine,
    reconciliation_dashboard,
    reports_dashboard,
)

urlpatterns = [
    path('', pharmacy_dashboard, name='pharmacy_dashboard'),
    path('catalogue/', medicine_catalogue, name='pharmacy_catalogue'),
    path('batches/', batch_management, name='pharmacy_batches'),
    path('dispensing/', dispensing_queue, name='pharmacy_dispensing'),
    path('purchasing/', purchasing_management, name='pharmacy_purchasing'),
    path('returns/', returns_and_quarantine, name='pharmacy_returns'),
    path('reconciliation/', reconciliation_dashboard, name='pharmacy_reconciliation'),
    path('reports/', reports_dashboard, name='pharmacy_reports'),
]
