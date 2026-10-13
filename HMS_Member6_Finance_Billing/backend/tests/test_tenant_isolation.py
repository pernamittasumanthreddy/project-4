from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.tenants.models import Tenant, Branch
from apps.billing.models import BillingEntity, Invoice
from apps.payments.models import Payment

class MultiTenantIsolationTests(TestCase):
    def setUp(self):
        # Hospital A
        self.tenant_a = Tenant.objects.create(name="Hospital Alpha", slug="hosp-alpha")
        self.branch_a = Branch.objects.create(tenant=self.tenant_a, name="Alpha Main", code="ALP-01", city="Delhi", state_code="07")
        self.entity_a = BillingEntity.objects.create(
            tenant=self.tenant_a, branch=self.branch_a, name="Alpha Legal", legal_name="Alpha Ltd",
            gstin="07ALPHA0000A1Z1", pan="ALPHA1234", state_code="07"
        )
        self.invoice_a = Invoice.objects.create(
            tenant=self.tenant_a, billing_entity=self.entity_a,
            invoice_number="INV-ALPHA-01", patient_id="PAT-A1", patient_name="Patient Alpha",
            patient_state_code="07", status="ISSUED", issue_date=timezone.now().date(), due_date=timezone.now().date(),
            total_net=Decimal('5000.00'), balance_due=Decimal('5000.00')
        )
        self.payment_a = Payment.objects.create(
            tenant=self.tenant_a, payment_number="PAY-ALPHA-01", invoice=self.invoice_a,
            amount=Decimal('5000.00'), method="CASH", status="SUCCESS"
        )

        # Hospital B
        self.tenant_b = Tenant.objects.create(name="Hospital Beta", slug="hosp-beta")
        self.branch_b = Branch.objects.create(tenant=self.tenant_b, name="Beta Main", code="BET-01", city="Mumbai", state_code="27")
        self.entity_b = BillingEntity.objects.create(
            tenant=self.tenant_b, branch=self.branch_b, name="Beta Legal", legal_name="Beta Ltd",
            gstin="27BETA0000B1Z1", pan="BETA1234", state_code="27"
        )
        self.invoice_b = Invoice.objects.create(
            tenant=self.tenant_b, billing_entity=self.entity_b,
            invoice_number="INV-BETA-01", patient_id="PAT-B1", patient_name="Patient Beta",
            patient_state_code="27", status="ISSUED", issue_date=timezone.now().date(), due_date=timezone.now().date(),
            total_net=Decimal('12000.00'), balance_due=Decimal('12000.00')
        )

    def test_tenant_a_query_cannot_retrieve_tenant_b_invoices(self):
        """Proves Hospital A cannot enumerate or view Hospital B's financial records."""
        invoices_for_a = Invoice.objects.for_tenant(self.tenant_a)
        
        self.assertEqual(invoices_for_a.count(), 1)
        self.assertEqual(invoices_for_a.first().invoice_number, "INV-ALPHA-01")
        # Ensure Hospital B invoice is NOT in queryset
        self.assertFalse(invoices_for_a.filter(invoice_number="INV-BETA-01").exists())

    def test_tenant_b_query_cannot_retrieve_tenant_a_payments(self):
        """Proves Hospital B cannot view Hospital A's payment receipts."""
        payments_for_b = Payment.objects.for_tenant(self.tenant_b)
        self.assertEqual(payments_for_b.count(), 0)
        self.assertFalse(payments_for_b.filter(payment_number="PAY-ALPHA-01").exists())
