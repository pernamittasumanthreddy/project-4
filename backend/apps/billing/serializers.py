from rest_framework import serializers
from apps.billing.models import Invoice, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_reference', 'receipt_number', 'invoice',
            'amount', 'payment_method', 'status', 'transaction_date',
            'is_sandbox_simulation', 'notes'
        ]
        read_only_fields = ['id', 'receipt_number', 'transaction_date']


class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_mrn = serializers.CharField(source='patient.mrn', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'patient', 'patient_name', 'patient_mrn',
            'appointment', 'issue_date', 'due_date', 'status',
            'subtotal', 'tax_amount', 'discount_amount', 'total_amount',
            'paid_amount', 'balance_due', 'line_items', 'payments', 'notes', 'created_at'
        ]
