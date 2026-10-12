from rest_framework import serializers
from .models import TaxConfiguration, TaxTransaction

class TaxConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxConfiguration
        fields = [
            'id', 'code', 'name', 'rate_percentage', 'cgst_rate', 'sgst_rate',
            'igst_rate', 'hsn_sac_code', 'is_active', 'is_default', 'description'
        ]

class TaxTransactionSerializer(serializers.ModelSerializer):
    tax_name = serializers.CharField(source='tax_config.name', read_only=True)

    class Meta:
        model = TaxTransaction
        fields = [
            'id', 'invoice_number', 'tax_config', 'tax_name', 'taxable_amount',
            'cgst_amount', 'sgst_amount', 'igst_amount', 'total_tax',
            'is_interstate', 'hospital_state', 'customer_state', 'created_at'
        ]
