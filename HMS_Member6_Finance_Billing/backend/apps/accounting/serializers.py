from decimal import Decimal
from rest_framework import serializers
from .models import ChartOfAccount, JournalEntry, JournalLine, FinancialPeriod, PayableRecord
from apps.common.decimal_utils import quantize_currency

class ChartOfAccountSerializer(serializers.ModelSerializer):
    account_type_display = serializers.CharField(source='get_account_type_display', read_only=True)

    class Meta:
        model = ChartOfAccount
        fields = [
            'id', 'account_code', 'account_name', 'account_type', 'account_type_display',
            'is_active', 'current_balance', 'description'
        ]

class JournalLineSerializer(serializers.ModelSerializer):
    account_code = serializers.CharField(source='account.account_code', read_only=True)
    account_name = serializers.CharField(source='account.account_name', read_only=True)

    class Meta:
        model = JournalLine
        fields = [
            'id', 'account', 'account_code', 'account_name',
            'debit_amount', 'credit_amount', 'description'
        ]

class JournalLineInputSerializer(serializers.Serializer):
    account_id = serializers.CharField(max_length=64)
    debit_amount = serializers.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    credit_amount = serializers.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    description = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')

class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalLineSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    source_type_display = serializers.CharField(source='get_source_document_type_display', read_only=True)

    class Meta:
        model = JournalEntry
        fields = [
            'id', 'entry_number', 'entry_date', 'description',
            'source_document_type', 'source_type_display', 'source_document_id',
            'status', 'status_display', 'total_debit', 'total_credit',
            'posted_by', 'posted_at', 'lines'
        ]
        read_only_fields = ['entry_number', 'total_debit', 'total_credit', 'posted_at']

class CreateJournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalLineInputSerializer(many=True)

    class Meta:
        model = JournalEntry
        fields = ['entry_date', 'description', 'source_document_type', 'source_document_id', 'lines']

    def validate_lines(self, lines):
        if not lines or len(lines) < 2:
            raise serializers.ValidationError("A journal entry requires at least 2 legs (debit and credit).")
        
        tot_debit = sum((quantize_currency(item.get('debit_amount', 0)) for item in lines), Decimal('0.00'))
        tot_credit = sum((quantize_currency(item.get('credit_amount', 0)) for item in lines), Decimal('0.00'))

        if tot_debit != tot_credit:
            raise serializers.ValidationError(
                f"Double-entry balancing violation: Total Debits (₹{tot_debit}) must equal Total Credits (₹{tot_credit}). "
                f"Discrepancy: ₹{abs(tot_debit - tot_credit)}"
            )
        return lines

class FinancialPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialPeriod
        fields = [
            'id', 'period_name', 'start_date', 'end_date', 'is_closed',
            'closed_at', 'closed_by', 'closing_notes'
        ]

class PayableRecordSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PayableRecord
        fields = [
            'id', 'vendor_name', 'bill_number', 'category', 'due_date',
            'total_amount', 'paid_amount', 'balance_due', 'status', 'status_display', 'created_at'
        ]
