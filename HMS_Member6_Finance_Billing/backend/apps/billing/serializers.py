from decimal import Decimal
from rest_framework import serializers
from .models import BillingEntity, ServicePrice, Invoice, InvoiceLine, CreditNote
from apps.taxes.models import TaxConfiguration

class BillingEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingEntity
        fields = [
            'id', 'name', 'legal_name', 'gstin', 'pan', 'state_code', 'state_name',
            'address', 'contact_phone', 'contact_email', 'invoice_prefix', 'invoice_next_seq', 'is_active'
        ]

class ServicePriceSerializer(serializers.ModelSerializer):
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    tax_rate = serializers.DecimalField(source='tax_config.rate_percentage', max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = ServicePrice
        fields = [
            'id', 'code', 'name', 'department', 'department_display', 'base_amount',
            'hsn_sac_code', 'tax_config', 'tax_rate', 'is_active', 'description'
        ]

class InvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLine
        fields = [
            'id', 'service_code', 'service_name', 'department', 'quantity', 'unit_price',
            'discount_amount', 'hsn_sac_code', 'tax_config', 'tax_rate',
            'gross_amount', 'taxable_amount', 'cgst_amount', 'sgst_amount', 'igst_amount',
            'tax_amount', 'net_amount'
        ]
        read_only_fields = [
            'gross_amount', 'taxable_amount', 'cgst_amount', 'sgst_amount',
            'igst_amount', 'tax_amount', 'net_amount'
        ]

class CreditNoteSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)

    class Meta:
        model = CreditNote
        fields = [
            'id', 'credit_note_number', 'invoice', 'invoice_number', 'amount',
            'reason', 'status', 'approved_by', 'notes', 'created_at'
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True, read_only=True)
    credit_notes = CreditNoteSerializer(many=True, read_only=True)
    billing_entity_name = serializers.CharField(source='billing_entity.name', read_only=True)
    billing_entity_gstin = serializers.CharField(source='billing_entity.gstin', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'billing_entity', 'billing_entity_name', 'billing_entity_gstin',
            'patient_id', 'patient_name', 'patient_mrn', 'patient_state_code',
            'encounter_id', 'encounter_type', 'status', 'issue_date', 'due_date',
            'total_gross', 'total_discount', 'total_taxable', 'total_cgst', 'total_sgst',
            'total_igst', 'total_tax', 'total_net', 'paid_amount', 'balance_due',
            'is_interstate', 'notes', 'terms', 'created_at', 'lines', 'credit_notes'
        ]
        read_only_fields = [
            'total_gross', 'total_discount', 'total_taxable', 'total_cgst', 'total_sgst',
            'total_igst', 'total_tax', 'total_net', 'paid_amount', 'balance_due', 'is_interstate'
        ]

class CreateInvoiceLineInputSerializer(serializers.Serializer):
    service_code = serializers.CharField(max_length=50)
    service_name = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=20, default='OPD')
    quantity = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal('1.00'))
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax_config_id = serializers.CharField(max_length=64, required=False, allow_null=True)
    hsn_sac_code = serializers.CharField(max_length=20, default='999312')

class CreateInvoiceSerializer(serializers.ModelSerializer):
    lines = CreateInvoiceLineInputSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'billing_entity', 'patient_id', 'patient_name', 'patient_mrn', 'patient_state_code',
            'encounter_id', 'encounter_type', 'issue_date', 'due_date', 'notes', 'terms', 'lines'
        ]

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        tenant = validated_data.get('tenant')
        billing_entity = validated_data['billing_entity']
        
        # Generate sequence invoice number
        seq = billing_entity.invoice_next_seq
        billing_entity.invoice_next_seq += 1
        billing_entity.save()
        inv_number = f"{billing_entity.invoice_prefix}-{seq:05d}"

        invoice = Invoice.objects.create(
            invoice_number=inv_number,
            status='ISSUED',
            **validated_data
        )

        for line_item in lines_data:
            tax_id = line_item.pop('tax_config_id', None)
            tax_cfg = TaxConfiguration.objects.filter(id=tax_id).first() if tax_id else None
            InvoiceLine.objects.create(
                tenant=tenant,
                invoice=invoice,
                tax_config=tax_cfg,
                **line_item
            )

        invoice.recalculate_totals()
        return invoice
