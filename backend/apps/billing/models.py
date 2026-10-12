import uuid
from decimal import Decimal
from django.db import models
from apps.core.models import TenantScopedModel
from apps.appointments.models import PatientProfile, Appointment

class Invoice(TenantScopedModel):
    """
    Patient Medical Invoice containing itemized clinical, laboratory, and pharmacy charges.
    """
    STATUS_CHOICES = (
        ('UNPAID', 'Unpaid / Pending Payment'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid in Full'),
        ('VOID', 'Void / Cancelled'),
    )

    invoice_number = models.CharField(max_length=50, unique=True)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='invoices')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    line_items = models.JSONField(default=list, blank=True, help_text="List of {description, quantity, unit_price, total}")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-issue_date', '-created_at']

    def update_totals(self):
        """Calculates accurate invoice totals from line items."""
        sub = Decimal('0.00')
        for item in self.line_items:
            qty = Decimal(str(item.get('quantity', 1)))
            rate = Decimal(str(item.get('unit_price', 0)))
            sub += (qty * rate)
        self.subtotal = sub
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.balance_due = max(Decimal('0.00'), self.total_amount - self.paid_amount)
        if self.paid_amount >= self.total_amount and self.total_amount > Decimal('0.00'):
            self.status = 'PAID'
        elif self.paid_amount > Decimal('0.00'):
            self.status = 'PARTIALLY_PAID'
        else:
            self.status = 'UNPAID'

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.patient.full_name} (${self.total_amount}) [{self.status}]"


class Payment(TenantScopedModel):
    """
    Patient settlement transaction record.
    """
    METHOD_CHOICES = (
        ('CREDIT_CARD', 'Credit / Debit Card'),
        ('UPI', 'Unified Payments Interface (UPI)'),
        ('NET_BANKING', 'Electronic Funds Transfer'),
        ('INSURANCE', 'Direct Insurance Claim'),
        ('CASH', 'Cash / Counter Deposit'),
    )
    STATUS_CHOICES = (
        ('SUCCESS', 'Transaction Successful'),
        ('PENDING', 'Processing / Verification'),
        ('FAILED', 'Transaction Declined'),
    )

    payment_reference = models.CharField(max_length=100, unique=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='CREDIT_CARD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUCCESS')
    transaction_date = models.DateTimeField(auto_now_add=True)
    is_sandbox_simulation = models.BooleanField(default=True, help_text="True for zero-key local demo mode")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f"Receipt #{self.receipt_number} (${self.amount}) for Invoice #{self.invoice.invoice_number}"
