from django.urls import path
from apps.billing import views

urlpatterns = [
    path('invoices/', views.InvoiceListView.as_view(), name='invoices-list'),
    path('invoices/<uuid:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/<uuid:invoice_id>/pay-sandbox/', views.PaymentSandboxProcessView.as_view(), name='invoice-pay-sandbox'),
]
