from decimal import Decimal
from rest_framework import serializers
from .models import Payment, PaymentAttempt, Refund, ReconciliationRecord
from apps.billing.models import Invoice

class PaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    patient_name = serializers.CharField(source='invoice.patient_name', read_only=True)
    method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'payment_number', 'invoice', 'invoice_number', 'patient_name',
            'amount', 'method', 'method_display', 'status', 'idempotency_key',
            'transaction_reference', 'received_by', 'notes', 'created_at'
        ]
        read_only_fields = ['payment_number', 'status']

class RefundSerializer(serializers.ModelSerializer):
    payment_number = serializers.CharField(source='payment.payment_number', read_only=True)
    invoice_number = serializers.CharField(source='payment.invoice.invoice_number', read_only=True)

    class Meta:
        model = Refund
        fields = [
            'id', 'refund_number', 'payment', 'payment_number', 'invoice_number',
            'amount', 'reason', 'status', 'requested_by', 'approved_by',
            'processed_at', 'rejection_reason', 'created_at'
        ]
        read_only_fields = ['refund_number']

class ReconciliationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationRecord
        fields = [
            'id', 'batch_number', 'statement_date', 'total_records', 'matched_records',
            'discrepancy_count', 'total_statement_amount', 'total_system_amount',
            'status', 'notes', 'created_at'
        ]
