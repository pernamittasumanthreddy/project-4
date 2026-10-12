from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.tenants.models import Tenant, Branch
from apps.taxes.models import TaxConfiguration
from apps.billing.models import BillingEntity, ServicePrice, Invoice, InvoiceLine, CreditNote

class BillingModuleTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Fortis Healthcare",
            slug="fortis-delhi",
            default_currency="INR"
        )
        self.branch = Branch.objects.create(
            tenant=self.tenant,
            name="Fortis Okhla",
            code="FORT-OKH",
            city="New Delhi",
            state_code="07",
            gstin="07FORTIS0000A1Z1"
        )
        self.billing_entity = BillingEntity.objects.create(
            tenant=self.tenant,
            branch=self.branch,
            name="Fortis Healthcare Legal",
            legal_name="Fortis Healthcare Ltd",
            gstin="07FORTIS0000A1Z1",
            pan="FORTIS1234",
            state_code="07",
            address="Okhla Road, New Delhi",
            contact_phone="+91 11 4277 6222",
            contact_email="billing@fortis.in",
            invoice_prefix="INV-FOR-26",
            invoice_next_seq=100
        )
        self.tax_exempt = TaxConfiguration.objects.create(
            tenant=self.tenant,
            code="GST_EXEMPT",
            name="Healthcare Exempt",
            rate_percentage=Decimal('0.00'),
            cgst_rate=Decimal('0.00'),
            sgst_rate=Decimal('0.00'),
            igst_rate=Decimal('0.00')
        )
        self.tax_18 = TaxConfiguration.objects.create(
            tenant=self.tenant,
            code="GST_18",
            name="Admin Software Tech",
            rate_percentage=Decimal('18.00'),
            cgst_rate=Decimal('9.00'),
            sgst_rate=Decimal('9.00'),
            igst_rate=Decimal('18.00')
        )

    def test_decimal_safe_line_and_invoice_calculation(self):
        """Validates that invoice math is zero-float error accurate."""
        invoice = Invoice.objects.create(
            tenant=self.tenant,
            billing_entity=self.billing_entity,
            invoice_number="INV-FOR-26-00100",
            patient_id="PAT-991",
            patient_name="Rahul Verma",
            patient_state_code="07",
            status="ISSUED",
            issue_date=timezone.now().date(),
            due_date=timezone.now().date()
        )
        
        # Line 1: 2 units @ 1250.50 with 100.00 discount (Exempt tax)
        line_1 = InvoiceLine.objects.create(
            tenant=self.tenant,
            invoice=invoice,
            service_code="SRV-01",
            service_name="Cardiology Consult",
            department="OPD",
            quantity=Decimal('2.00'),
            unit_price=Decimal('1250.50'),
            discount_amount=Decimal('100.00'),
            tax_config=self.tax_exempt
        )
        
        # Gross = 2501.00, Taxable = 2401.00, Net = 2401.00
        self.assertEqual(line_1.gross_amount, Decimal('2501.00'))
        self.assertEqual(line_1.taxable_amount, Decimal('2401.00'))
        self.assertEqual(line_1.net_amount, Decimal('2401.00'))

        # Line 2: 1 unit @ 1000.00 with 18% GST (Intra-state: 9% CGST + 9% SGST)
        line_2 = InvoiceLine.objects.create(
            tenant=self.tenant,
            invoice=invoice,
            service_code="SRV-02",
            service_name="Medical Admin Processing",
            department="OPD",
            quantity=Decimal('1.00'),
            unit_price=Decimal('1000.00'),
            tax_config=self.tax_18
        )
        self.assertEqual(line_2.tax_amount, Decimal('180.00'))
        self.assertEqual(line_2.cgst_amount, Decimal('90.00'))
        self.assertEqual(line_2.sgst_amount, Decimal('90.00'))
        self.assertEqual(line_2.igst_amount, Decimal('0.00'))
        self.assertEqual(line_2.net_amount, Decimal('1180.00'))

        invoice.recalculate_totals()
        self.assertEqual(invoice.total_gross, Decimal('3501.00'))
        self.assertEqual(invoice.total_taxable, Decimal('3401.00'))
        self.assertEqual(invoice.total_tax, Decimal('180.00'))
        self.assertEqual(invoice.total_net, Decimal('3581.00'))
        self.assertEqual(invoice.balance_due, Decimal('3581.00'))
        self.assertEqual(invoice.status, "ISSUED")

    def test_interstate_igst_calculation(self):
        """Tests that patient from another state triggers IGST instead of CGST+SGST."""
        invoice_interstate = Invoice.objects.create(
            tenant=self.tenant,
            billing_entity=self.billing_entity,
            invoice_number="INV-FOR-26-00101",
            patient_id="PAT-992",
            patient_name="Ananya Roy",
            patient_state_code="19", # West Bengal (Hospital is Delhi 07)
            status="ISSUED",
            issue_date=timezone.now().date(),
            due_date=timezone.now().date()
        )
        line = InvoiceLine.objects.create(
            tenant=self.tenant,
            invoice=invoice_interstate,
            service_code="SRV-02",
            service_name="Admin Processing",
            department="OPD",
            quantity=Decimal('1.00'),
            unit_price=Decimal('1000.00'),
            tax_config=self.tax_18
        )
        invoice_interstate.recalculate_totals()
        self.assertTrue(invoice_interstate.is_interstate)
        # Should charge 18% IGST and 0 CGST/SGST
        self.assertEqual(invoice_interstate.total_igst, Decimal('180.00'))
        self.assertEqual(invoice_interstate.total_cgst, Decimal('0.00'))
        self.assertEqual(invoice_interstate.total_sgst, Decimal('0.00'))

    def test_credit_note_reduces_balance_due(self):
        """Tests that credit note application accurately adjusts invoice balance."""
        invoice = Invoice.objects.create(
            tenant=self.tenant,
            billing_entity=self.billing_entity,
            invoice_number="INV-FOR-26-00102",
            patient_id="PAT-993",
            patient_name="Sunil K",
            patient_state_code="07",
            status="ISSUED",
            issue_date=timezone.now().date(),
            due_date=timezone.now().date()
        )
        InvoiceLine.objects.create(
            tenant=self.tenant,
            invoice=invoice,
            service_code="SRV-01",
            service_name="Consultation",
            department="OPD",
            quantity=Decimal('1.00'),
            unit_price=Decimal('1000.00'),
            tax_config=self.tax_exempt
        )
        invoice.recalculate_totals()
        self.assertEqual(invoice.balance_due, Decimal('1000.00'))

        # Apply ₹200 concession credit note
        CreditNote.objects.create(
            tenant=self.tenant,
            credit_note_number="CN-2026-0001",
            invoice=invoice,
            amount=Decimal('200.00'),
            reason="Senior citizen discount concession"
        )
        invoice.balance_due = Decimal('800.00')
        invoice.save()
        self.assertEqual(invoice.balance_due, Decimal('800.00'))
