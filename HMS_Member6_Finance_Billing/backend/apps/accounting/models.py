from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import TenantScopedModel
from apps.common.decimal_utils import quantize_currency, to_decimal

class ChartOfAccount(TenantScopedModel):
    """
    Standard double-entry chart of accounts.
    Categorized into Assets, Liabilities, Equity, Revenue, and Expenses.
    """
    ACCOUNT_TYPES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('REVENUE', 'Revenue'),
        ('EXPENSE', 'Expense'),
    ]

    account_code = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    is_active = models.BooleanField(default=True)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['account_code']
        unique_together = ('tenant', 'account_code')

    def __str__(self):
        return f"{self.account_code} - {self.account_name} ({self.account_type})"


class JournalEntry(TenantScopedModel):
    """
    Double-entry accounting journal transaction header.
    Invariance: Sum(Debit) must strictly equal Sum(Credit).
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft Entry'),
        ('POSTED', 'Posted to General Ledger'),
        ('REVERSED', 'Reversed / Cancelled'),
    ]

    SOURCE_TYPES = [
        ('MANUAL', 'Manual Journal Voucher'),
        ('INVOICE', 'Invoice Issued (AR / Revenue)'),
        ('PAYMENT', 'Payment Received (Cash/Bank / AR)'),
        ('REFUND', 'Disbursement Refund'),
        ('SETTLEMENT', 'Insurance Settlement Payout'),
        ('PERIOD_CLOSE', 'Year/Period Close Allocation'),
    ]

    entry_number = models.CharField(max_length=100, unique=True, db_index=True)
    entry_date = models.DateField()
    description = models.CharField(max_length=255)
    source_document_type = models.CharField(max_length=30, choices=SOURCE_TYPES, default='MANUAL')
    source_document_id = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='POSTED', db_index=True)
    
    total_debit = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_credit = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    posted_by = models.CharField(max_length=150, default='system_accountant')
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_date', '-created_at']

    def __str__(self):
        return f"{self.entry_number} [{self.entry_date}] - {self.description} (₹{self.total_debit})"

    def verify_balanced(self):
        """
        Validates double-entry balancing invariant.
        Raises ValidationError if debits != credits.
        """
        lines = self.lines.all()
        debit_sum = sum(line.debit_amount for line in lines)
        credit_sum = sum(line.credit_amount for line in lines)
        
        d_val = quantize_currency(debit_sum)
        c_val = quantize_currency(credit_sum)

        if d_val != c_val:
            raise ValidationError(
                f"Double-entry balancing error in Journal Entry {self.entry_number}: "
                f"Total Debit ₹{d_val} does not equal Total Credit ₹{c_val} (Discrepancy: ₹{abs(d_val - c_val)})"
            )
        
        self.total_debit = d_val
        self.total_credit = c_val
        self.save()


class JournalLine(TenantScopedModel):
    """
    Individual debit or credit leg of a journal entry.
    """
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, related_name='journal_lines')
    debit_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    credit_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.account.account_name}: Dr ₹{self.debit_amount} | Cr ₹{self.credit_amount}"

    def clean(self):
        # A single line cannot have both non-zero debit and credit
        if self.debit_amount > Decimal('0.00') and self.credit_amount > Decimal('0.00'):
            raise ValidationError("A journal line must specify either a debit amount or a credit amount, not both.")


class FinancialPeriod(TenantScopedModel):
    """
    Accounting period (monthly/quarterly/yearly) with closing locks.
    """
    period_name = models.CharField(max_length=50) # e.g. FY2026-M10
    start_date = models.DateField()
    end_date = models.DateField()
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.CharField(max_length=150, blank=True, null=True)
    closing_notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-end_date']

    def __str__(self):
        status = "CLOSED" if self.is_closed else "OPEN"
        return f"{self.period_name} ({self.start_date} to {self.end_date}) [{status}]"


class PayableRecord(TenantScopedModel):
    """
    Hospital Accounts Payable - supplier & vendor procurement bills.
    """
    vendor_name = models.CharField(max_length=255)
    bill_number = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='Medical Supplies / Consumables')
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    balance_due = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=30,
        choices=[('PENDING', 'Pending Payment'), ('PARTIALLY_PAID', 'Partially Paid'), ('PAID', 'Paid'), ('OVERDUE', 'Overdue')],
        default='PENDING'
    )

    def __str__(self):
        return f"AP {self.vendor_name} ({self.bill_number}) - ₹{self.balance_due}"
