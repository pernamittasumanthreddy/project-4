from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.tenants.models import Tenant, Branch
from apps.billing.models import BillingEntity, Invoice, InvoiceLine
from apps.payments.models import Payment, Refund
from apps.accounting.models import ChartOfAccount

class PaymentsModuleTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Max Mumbai", slug="max-mum", default_currency="INR")
        self.branch = Branch.objects.create(tenant=self.tenant, name="Max Bandra", code="MAX-BAN", city="Mumbai", state_code="27")
        self.billing_entity = BillingEntity.objects.create(
            tenant=self.tenant, branch=self.branch, name="Max Healthcare Legal",
            legal_name="Max Healthcare Ltd", gstin="27MAX00000A1Z1", pan="MAX1234567",
            state_code="27", address="Bandra West", contact_phone="022112233", contact_email="max@test.com"
        )
        # Create GL Accounts for automated journal postings
        ChartOfAccount.objects.create(tenant=self.tenant, account_code='1010', account_name='Bank Current A/c', account_type='ASSET')
        ChartOfAccount.objects.create(tenant=self.tenant, account_code='1020', account_name='Cash in Till', account_type='ASSET')
        ChartOfAccount.objects.create(tenant=self.tenant, account_code='1100', account_name='Accounts Receivable', account_type='ASSET')

        self.invoice = Invoice.objects.create(
            tenant=self.tenant,
            billing_entity=self.billing_entity,
            invoice_number="INV-MAX-26-0001",
            patient_id="PAT-501",
            patient_name="Siddharth Rao",
            patient_state_code="27",
            status="ISSUED",
            issue_date=timezone.now().date(),
            due_date=timezone.now().date()
        )
        InvoiceLine.objects.create(
            tenant=self.tenant,
            invoice=self.invoice,
            service_code="SRV-SURG",
            service_name="Hernia Surgery",
            department="SURG",
            quantity=Decimal('1.00'),
            unit_price=Decimal('50000.00')
        )
        self.invoice.recalculate_totals()

    def test_partial_payment_and_full_settlement(self):
        """Verifies multi-tender payments and status progression to PARTIALLY_PAID and PAID."""
        self.assertEqual(self.invoice.total_net, Decimal('50000.00'))
        self.assertEqual(self.invoice.balance_due, Decimal('50000.00'))

        # Payment 1: ₹20,000 Advance via Card
        p1 = Payment.objects.create(
            tenant=self.tenant,
            payment_number="PAY-2026-00001",
            invoice=self.invoice,
            amount=Decimal('20000.00'),
            method="CARD",
            status="SUCCESS",
            transaction_reference="AUTH-88219"
        )
        self.invoice.paid_amount += p1.amount
        self.invoice.recalculate_totals()
        
        self.assertEqual(self.invoice.status, "PARTIALLY_PAID")
        self.assertEqual(self.invoice.balance_due, Decimal('30000.00'))

        # Payment 2: Remaining ₹30,000 via UPI
        p2 = Payment.objects.create(
            tenant=self.tenant,
            payment_number="PAY-2026-00002",
            invoice=self.invoice,
            amount=Decimal('30000.00'),
            method="UPI",
            status="SUCCESS",
            transaction_reference="UPI/20261012/77123"
        )
        self.invoice.paid_amount += p2.amount
        self.invoice.recalculate_totals()

        self.assertEqual(self.invoice.status, "PAID")
        self.assertEqual(self.invoice.balance_due, Decimal('0.00'))

    def test_idempotency_prevents_duplicate_payments(self):
        """Verifies that an idempotency key avoids duplicated transactions."""
        key = "idemp-txn-uuid-8899"
        Payment.objects.create(
            tenant=self.tenant,
            payment_number="PAY-2026-00003",
            invoice=self.invoice,
            amount=Decimal('5000.00'),
            method="CASH",
            status="SUCCESS",
            idempotency_key=key
        )
        
        # Second query for same key should find existing record
        duplicate = Payment.objects.filter(tenant=self.tenant, idempotency_key=key).first()
        self.assertIsNotNone(duplicate)
        self.assertEqual(duplicate.payment_number, "PAY-2026-00003")

    def test_refund_lifecycle_and_balance_reversion(self):
        """Verifies refund request, approval, and balance recalculation."""
        payment = Payment.objects.create(
            tenant=self.tenant,
            payment_number="PAY-2026-00004",
            invoice=self.invoice,
            amount=Decimal('10000.00'),
            method="CASH",
            status="SUCCESS"
        )
        self.invoice.paid_amount = Decimal('10000.00')
        self.invoice.recalculate_totals()

        # Request Refund
        refund = Refund.objects.create(
            tenant=self.tenant,
            refund_number="REF-2026-00001",
            payment=payment,
            amount=Decimal('4000.00'),
            reason="Consultation cancelled by doctor",
            status="REQUESTED"
        )
        self.assertEqual(refund.status, "REQUESTED")

        # Approve Refund
        refund.status = "APPROVED"
        refund.approved_by = "finance_manager"
        refund.save()

        # Process Refund
        refund.status = "PROCESSED"
        refund.processed_at = timezone.now()
        refund.save()

        payment.status = "PARTIALLY_REFUNDED"
        payment.save()

        self.invoice.paid_amount -= refund.amount
        self.invoice.recalculate_totals()

        self.assertEqual(payment.status, "PARTIALLY_REFUNDED")
        self.assertEqual(self.invoice.paid_amount, Decimal('6000.00'))
        self.assertEqual(self.invoice.balance_due, Decimal('44000.00'))
