from decimal import Decimal
from django.db import models
from apps.common.models import TenantScopedModel
from apps.billing.models import Invoice

class Payment(TenantScopedModel):
    """
    Payment receipt recorded against an invoice.
    Supports Cash, Card, UPI, Wire Transfer, and Insurance Payouts.
    """
    METHOD_CHOICES = [
        ('CASH', 'Cash Counter'),
        ('CARD', 'Credit / Debit Card (POS)'),
        ('UPI', 'UPI / QR Code (Digital)'),
        ('WIRE_TRANSFER', 'Bank Wire / NEFT / RTGS'),
        ('CHEQUE', 'Cheque / Demand Draft'),
        ('INSURANCE_SETTLEMENT', 'Direct Insurer / TPA Settlement'),
    ]

    STATUS_CHOICES = [
        ('SUCCESS', 'Success / Cleared'),
        ('PENDING', 'Pending Clearance'),
        ('FAILED', 'Failed / Declined'),
        ('REFUNDED', 'Fully Refunded'),
        ('PARTIALLY_REFUNDED', 'Partially Refunded'),
    ]

    payment_number = models.CharField(max_length=100, unique=True, db_index=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='CASH')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUCCESS', db_index=True)
    idempotency_key = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    transaction_reference = models.CharField(max_length=100, blank=True, default='', help_text="Bank UTR / POS Auth Code")
    received_by = models.CharField(max_length=150, default='cashier')
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.payment_number} - Invoice {self.invoice.invoice_number} (₹{self.amount} via {self.method})"


class PaymentAttempt(TenantScopedModel):
    """
    Log of payment gateway attempts, retry tokens, and responses.
    """
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='attempts', null=True, blank=True)
    gateway_name = models.CharField(max_length=50, default='INTERNAL_SIMULATOR')
    request_reference = models.CharField(max_length=100, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30, choices=[('INITIATED', 'Initiated'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')])
    response_code = models.CharField(max_length=50, blank=True, default='')
    response_message = models.TextField(blank=True, default='')
    idempotency_key = models.CharField(max_length=128, blank=True, default='')

    def __str__(self):
        return f"Attempt {self.request_reference} - {self.status}"


class Refund(TenantScopedModel):
    """
    Refund request and multi-tier approval workflow.
    """
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('APPROVED', 'Approved by Finance Head'),
        ('PROCESSED', 'Processed & Disbursed'),
        ('REJECTED', 'Rejected'),
    ]

    refund_number = models.CharField(max_length=100, unique=True, db_index=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='REQUESTED', db_index=True)
    requested_by = models.CharField(max_length=150, default='billing_staff')
    approved_by = models.CharField(max_length=150, blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.refund_number} - Payment {self.payment.payment_number} (₹{self.amount}) [{self.status}]"


class ReconciliationRecord(TenantScopedModel):
    """
    Smart Payment Reconciliation batch record for bank statements & gateway payouts.
    """
    STATUS_CHOICES = [
        ('RECONCILED', 'Fully Reconciled'),
        ('DISCREPANCY_DETECTED', 'Discrepancy / Unmatched Items'),
        ('IN_REVIEW', 'Under Financial Review'),
    ]

    batch_number = models.CharField(max_length=100, unique=True, db_index=True)
    statement_date = models.DateField()
    total_records = models.PositiveIntegerField(default=0)
    matched_records = models.PositiveIntegerField(default=0)
    discrepancy_count = models.PositiveIntegerField(default=0)
    total_statement_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_system_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='RECONCILED')
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return f"ReconBatch {self.batch_number} ({self.status}) - Matched: {self.matched_records}/{self.total_records}"
