from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Tenants
from apps.tenants.views import TenantViewSet, BranchViewSet

# Taxes
from apps.taxes.views import TaxConfigurationViewSet, TaxTransactionViewSet, tax_summary_report

# Billing
from apps.billing.views import BillingEntityViewSet, ServicePriceViewSet, InvoiceViewSet, CreditNoteViewSet

# Payments
from apps.payments.views import PaymentViewSet, RefundViewSet, ReconciliationViewSet

# Insurance
from apps.insurance.views import InsurancePayerViewSet, InsurancePolicyViewSet, InsuranceClaimViewSet, denial_workbench

# Accounting
from apps.accounting.views import (
    ChartOfAccountViewSet, JournalEntryViewSet, FinancialPeriodViewSet,
    PayableRecordViewSet, accounts_receivable_aging
)

# Analytics
from apps.analytics.views import (
    FinancialAuditEventViewSet, finance_dashboard_kpis, financial_integrity_monitor
)

router = DefaultRouter()
# Tenants
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'branches', BranchViewSet, basename='branch')

# Taxes
router.register(r'taxes/configurations', TaxConfigurationViewSet, basename='tax-config')
router.register(r'taxes/transactions', TaxTransactionViewSet, basename='tax-transaction')

# Billing
router.register(r'billing/entities', BillingEntityViewSet, basename='billing-entity')
router.register(r'billing/services', ServicePriceViewSet, basename='billing-service')
router.register(r'billing/invoices', InvoiceViewSet, basename='invoice')
router.register(r'billing/credit-notes', CreditNoteViewSet, basename='credit-note')

# Payments
router.register(r'payments/records', PaymentViewSet, basename='payment')
router.register(r'payments/refunds', RefundViewSet, basename='refund')
router.register(r'payments/reconciliation', ReconciliationViewSet, basename='reconciliation')

# Insurance
router.register(r'insurance/payers', InsurancePayerViewSet, basename='insurance-payer')
router.register(r'insurance/policies', InsurancePolicyViewSet, basename='insurance-policy')
router.register(r'insurance/claims', InsuranceClaimViewSet, basename='insurance-claim')

# Accounting
router.register(r'accounting/accounts', ChartOfAccountViewSet, basename='chart-of-account')
router.register(r'accounting/journals', JournalEntryViewSet, basename='journal-entry')
router.register(r'accounting/periods', FinancialPeriodViewSet, basename='financial-period')
router.register(r'accounting/payables', PayableRecordViewSet, basename='payable')

# Analytics
router.register(r'analytics/audit-events', FinancialAuditEventViewSet, basename='audit-event')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Custom Functional Endpoints
    path('api/v1/taxes/summary/', tax_summary_report, name='tax-summary'),
    path('api/v1/insurance/denial-workbench/', denial_workbench, name='denial-workbench'),
    path('api/v1/accounting/receivables/', accounts_receivable_aging, name='ar-aging'),
    path('api/v1/analytics/dashboard/', finance_dashboard_kpis, name='finance-dashboard-kpis'),
    path('api/v1/analytics/integrity-monitor/', financial_integrity_monitor, name='financial-integrity-monitor'),

    # REST Router
    path('api/v1/', include(router.urls)),
]
