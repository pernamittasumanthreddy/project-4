import uuid
from decimal import Decimal
from django.db import models
from apps.common.models import TenantScopedModel
from apps.common.decimal_utils import quantize_currency, to_decimal, calculate_tax
from apps.taxes.models import TaxConfiguration

class BillingEntity(TenantScopedModel):
    """
    Hospital Legal & Tax Entity for invoicing and GST compliance.
    """
    name = models.CharField(max_length=200, help_text="Hospital Entity Name")
    legal_name = models.CharField(max_length=255)
    gstin = models.CharField(max_length=15, help_text="15-digit GST Identification Number")
    pan = models.CharField(max_length=10)
    state_code = models.CharField(max_length=10, default='07', help_text="e.g. 07 for Delhi")
    state_name = models.CharField(max_length=100, default='Delhi')
    address = models.TextField()
    contact_phone = models.CharField(max_length=30)
    contact_email = models.EmailField()
    invoice_prefix = models.CharField(max_length=10, default='INV')
    invoice_next_seq = models.PositiveIntegerField(default=1001)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.gstin})"


class ServicePrice(TenantScopedModel):
    """
    Hospital Charge Master / Service Price Catalogue across all clinical departments.
    """
    DEPARTMENT_CHOICES = [
        ('OPD', 'Outpatient Consultation'),
        ('IPD', 'Inpatient Ward / Bed'),
        ('LAB', 'Laboratory Pathology'),
        ('RAD', 'Radiology & Imaging'),
        ('PHARM', 'Pharmacy Medication'),
        ('SURG', 'Surgical / Operation Theatre'),
        ('PROC', 'Clinical Procedure'),
    ]

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='OPD')
    base_amount = models.DecimalField(max_digits=12, decimal_places=2)
    hsn_sac_code = models.CharField(max_length=20, default='999312')
    tax_config = models.ForeignKey(TaxConfiguration, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['department', 'name']

    def __str__(self):
        return f"[{self.department}] {self.name} - ₹{self.base_amount}"


class Invoice(TenantScopedModel):
    """
    Hospital Bill / Itemized Patient Invoice.
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ISSUED', 'Issued'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Fully Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]

    ENCOUNTER_TYPE_CHOICES = [
        ('OPD', 'Outpatient'),
        ('IPD', 'Inpatient Admission'),
        ('EMERGENCY', 'Emergency / Trauma'),
        ('DAYCARE', 'Day Care Procedure'),
    ]

    invoice_number = models.CharField(max_length=100, unique=True, db_index=True)
    billing_entity = models.ForeignKey(BillingEntity, on_delete=models.PROTECT, related_name='invoices')
    patient_id = models.CharField(max_length=64, db_index=True, help_text="M1 Patient Identifier Reference")
    patient_name = models.CharField(max_length=255)
    patient_mrn = models.CharField(max_length=100, blank=True, default='')
    patient_state_code = models.CharField(max_length=10, default='07')
    encounter_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    encounter_type = models.CharField(max_length=20, choices=ENCOUNTER_TYPE_CHOICES, default='OPD')
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT', db_index=True)
    issue_date = models.DateField()
    due_date = models.DateField()

    # Calculations (All decimal safe)
    total_gross = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_taxable = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_cgst = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_sgst = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_igst = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_net = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    is_interstate = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')
    terms = models.TextField(blank=True, default='Payment due upon receipt or discharge.')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.invoice_number} - {self.patient_name} (₹{self.total_net})"

    def recalculate_totals(self):
        """
        Recalculates invoice header totals from associated lines.
        Guarantees zero-floating point errors with quantize_currency.
        """
        hospital_state = self.billing_entity.state_code if self.billing_entity else '07'
        self.is_interstate = (hospital_state != self.patient_state_code)

        lines = self.lines.all()
        gross = Decimal('0.00')
        disc = Decimal('0.00')
        cgst = Decimal('0.00')
        sgst = Decimal('0.00')
        igst = Decimal('0.00')
        tax_total = Decimal('0.00')
        net = Decimal('0.00')

        for line in lines:
            gross += line.gross_amount
            disc += line.discount_amount
            
            # Ensure line tax splits reflect current interstate status
            if line.tax_amount > Decimal('0.00'):
                if self.is_interstate:
                    line.igst_amount = line.tax_amount
                    line.cgst_amount = Decimal('0.00')
                    line.sgst_amount = Decimal('0.00')
                else:
                    half = quantize_currency(line.tax_amount / Decimal('2.00'))
                    line.cgst_amount = half
                    line.sgst_amount = quantize_currency(line.tax_amount - half)
                    line.igst_amount = Decimal('0.00')
                line.save(update_fields=['cgst_amount', 'sgst_amount', 'igst_amount'])

            cgst += line.cgst_amount
            sgst += line.sgst_amount
            igst += line.igst_amount
            tax_total += line.tax_amount
            net += line.net_amount

        self.total_gross = quantize_currency(gross)
        self.total_discount = quantize_currency(disc)
        self.total_taxable = quantize_currency(gross - disc)
        self.total_cgst = quantize_currency(cgst)
        self.total_sgst = quantize_currency(sgst)
        self.total_igst = quantize_currency(igst)
        self.total_tax = quantize_currency(tax_total)
        self.total_net = quantize_currency(net)
        
        # Calculate balance due
        self.balance_due = quantize_currency(self.total_net - self.paid_amount)
        
        # Update status based on paid amount
        if self.status not in ['CANCELLED', 'DRAFT']:
            if self.balance_due <= Decimal('0.00') and self.total_net > Decimal('0.00'):
                self.status = 'PAID'
            elif self.paid_amount > Decimal('0.00') and self.balance_due > Decimal('0.00'):
                self.status = 'PARTIALLY_PAID'
            elif self.paid_amount == Decimal('0.00'):
                self.status = 'ISSUED'

        self.save()


class InvoiceLine(TenantScopedModel):
    """
    Individual billable service or supply charged to an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lines')
    service_code = models.CharField(max_length=50)
    service_name = models.CharField(max_length=255)
    department = models.CharField(max_length=20, default='OPD')
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    hsn_sac_code = models.CharField(max_length=20, default='999312')
    
    tax_config = models.ForeignKey(TaxConfiguration, on_delete=models.SET_NULL, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        # Guarantee line math correctness
        q = to_decimal(self.quantity)
        u = to_decimal(self.unit_price)
        d = to_decimal(self.discount_amount)
        self.gross_amount = quantize_currency(q * u)
        self.taxable_amount = quantize_currency(self.gross_amount - d)

        # Tax calculation
        if self.tax_config and self.tax_config.rate_percentage > Decimal('0.00'):
            self.tax_rate = self.tax_config.rate_percentage
            rate = self.tax_rate
            total_tax = calculate_tax(self.taxable_amount, rate)
            self.tax_amount = total_tax

            # Check if invoice is interstate
            is_interstate = self.invoice.is_interstate if self.invoice else False
            if is_interstate:
                self.igst_amount = total_tax
                self.cgst_amount = Decimal('0.00')
                self.sgst_amount = Decimal('0.00')
            else:
                half = quantize_currency(total_tax / Decimal('2.00'))
                self.cgst_amount = half
                self.sgst_amount = quantize_currency(total_tax - half)
                self.igst_amount = Decimal('0.00')
        else:
            self.tax_rate = Decimal('0.00')
            self.tax_amount = Decimal('0.00')
            self.cgst_amount = Decimal('0.00')
            self.sgst_amount = Decimal('0.00')
            self.igst_amount = Decimal('0.00')

        self.net_amount = quantize_currency(self.taxable_amount + self.tax_amount)
        super().save(*args, **kwargs)


class CreditNote(TenantScopedModel):
    """
    Auditable concession or correction against an issued invoice.
    """
    credit_note_number = models.CharField(max_length=100, unique=True, db_index=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='credit_notes')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=255)
    status = models.CharField(
        max_length=30,
        choices=[('DRAFT', 'Draft'), ('APPROVED', 'Approved'), ('APPLIED', 'Applied'), ('VOID', 'Void')],
        default='APPROVED'
    )
    approved_by = models.CharField(max_length=150, default='finance_head')
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.credit_note_number} - Invoice {self.invoice.invoice_number} (₹{self.amount})"
