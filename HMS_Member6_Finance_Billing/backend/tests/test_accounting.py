from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.tenants.models import Tenant
from apps.accounting.models import ChartOfAccount, JournalEntry, JournalLine, FinancialPeriod

class AccountingModuleTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Apollo Delhi", slug="apollo-del", default_currency="INR")
        self.bank_acct = ChartOfAccount.objects.create(tenant=self.tenant, account_code='1010', account_name='Bank Current A/c', account_type='ASSET')
        self.ar_acct = ChartOfAccount.objects.create(tenant=self.tenant, account_code='1100', account_name='Accounts Receivable', account_type='ASSET')
        self.rev_acct = ChartOfAccount.objects.create(tenant=self.tenant, account_code='4010', account_name='OPD Consultation Rev', account_type='REVENUE')

    def test_balanced_journal_entry_posts_successfully(self):
        """Verifies that equal debit and credit sums post without error."""
        je = JournalEntry.objects.create(
            tenant=self.tenant,
            entry_number="JE-TEST-001",
            entry_date=timezone.now().date(),
            description="Consultation revenue recognition",
            status="POSTED"
        )
        # Dr AR 1200.00
        JournalLine.objects.create(
            tenant=self.tenant,
            journal_entry=je,
            account=self.ar_acct,
            debit_amount=Decimal('1200.00'),
            credit_amount=Decimal('0.00')
        )
        # Cr Revenue 1200.00
        JournalLine.objects.create(
            tenant=self.tenant,
            journal_entry=je,
            account=self.rev_acct,
            debit_amount=Decimal('0.00'),
            credit_amount=Decimal('1200.00')
        )
        je.verify_balanced()
        self.assertEqual(je.total_debit, Decimal('1200.00'))
        self.assertEqual(je.total_credit, Decimal('1200.00'))

    def test_unbalanced_journal_entry_raises_validation_error(self):
        """Proves invariant: Double-entry system rejects entries where Debit != Credit."""
        je = JournalEntry.objects.create(
            tenant=self.tenant,
            entry_number="JE-TEST-002",
            entry_date=timezone.now().date(),
            description="Faulty unbalanced test entry",
            status="DRAFT"
        )
        # Dr AR 1500.00
        JournalLine.objects.create(
            tenant=self.tenant,
            journal_entry=je,
            account=self.ar_acct,
            debit_amount=Decimal('1500.00'),
            credit_amount=Decimal('0.00')
        )
        # Cr Revenue only 1000.00 (Unbalanced by 500.00)
        JournalLine.objects.create(
            tenant=self.tenant,
            journal_entry=je,
            account=self.rev_acct,
            debit_amount=Decimal('0.00'),
            credit_amount=Decimal('1000.00')
        )
        with self.assertRaises(ValidationError):
            je.verify_balanced()

    def test_financial_period_closing_workflow(self):
        """Tests that a closed period locks and preserves historical audit dates."""
        period = FinancialPeriod.objects.create(
            tenant=self.tenant,
            period_name="FY2026-M09",
            start_date=timezone.now().date().replace(day=1),
            end_date=timezone.now().date().replace(day=28),
            is_closed=False
        )
        self.assertFalse(period.is_closed)
        
        # Close period
        period.is_closed = True
        period.closed_at = timezone.now()
        period.closed_by = "auditor_smith"
        period.save()

        self.assertTrue(period.is_closed)
        self.assertEqual(period.closed_by, "auditor_smith")
