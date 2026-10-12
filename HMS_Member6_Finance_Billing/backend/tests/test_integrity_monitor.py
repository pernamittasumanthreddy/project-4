from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.tenants.models import Tenant
from apps.accounting.models import ChartOfAccount, JournalEntry, JournalLine
from apps.payments.models import Payment
from apps.billing.models import BillingEntity, Invoice
from apps.analytics.views import financial_integrity_monitor
from rest_framework.test import APIRequestFactory

class FinancialIntegrityMonitorTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Apex Heart", slug="apex-heart", default_currency="INR")
        self.factory = APIRequestFactory()

    def test_integrity_monitor_detects_unbalanced_journal(self):
        """Verifies that an unbalanced entry flags a CRITICAL severity alert in the integrity monitor."""
        acct_1 = ChartOfAccount.objects.create(tenant=self.tenant, account_code='1010', account_name='Bank', account_type='ASSET')
        acct_2 = ChartOfAccount.objects.create(tenant=self.tenant, account_code='4010', account_name='Rev', account_type='REVENUE')

        # Create an intentionally unbalanced journal entry directly in the DB
        je = JournalEntry.objects.create(
            tenant=self.tenant,
            entry_number="JE-ANOMALY-01",
            entry_date=timezone.now().date(),
            description="Intentionally unbalancing for monitor test",
            total_debit=Decimal('500.00'),
            total_credit=Decimal('400.00'), # Discrepancy ₹100
            status="POSTED"
        )

        request = self.factory.get('/api/v1/analytics/integrity-monitor/')
        request.tenant = self.tenant
        response = financial_integrity_monitor(request)

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertLess(data['integrity_score'], 100)
        self.assertGreaterEqual(data['flagged_issues_count'], 1)
        issue_categories = [i['category'] for i in data['issues']]
        self.assertIn("DOUBLE_ENTRY_UNBALANCED", issue_categories)
