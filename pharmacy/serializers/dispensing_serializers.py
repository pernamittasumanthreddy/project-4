"""HMS Pharmacy Dispensing Serializers — Member 5"""

from rest_framework import serializers
from pharmacy.models.dispensing import DispenseRecord, DispensedItem


class DispensedItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.brand_name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    expiry_date = serializers.DateField(source='batch.expiry_date', read_only=True)

    class Meta:
        model = DispensedItem
        fields = [
            'id', 'prescription_item', 'medicine', 'medicine_name',
            'batch', 'batch_number', 'expiry_date', 'quantity_dispensed',
            'unit_price', 'total_price', 'instructions_provided'
        ]
        read_only_fields = ['id', 'total_price']


class DispenseRecordSerializer(serializers.ModelSerializer):
    items = DispensedItemSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='prescription.patient.full_name', read_only=True)
    patient_mrn = serializers.CharField(source='prescription.patient.mrn', read_only=True)
    rx_number = serializers.CharField(source='prescription.prescription_number', read_only=True)
    pharmacist_name = serializers.CharField(source='pharmacist.username', read_only=True)

    class Meta:
        model = DispenseRecord
        fields = [
            'id', 'dispense_number', 'prescription', 'rx_number',
            'patient_name', 'patient_mrn', 'pharmacist', 'pharmacist_name',
            'status', 'total_amount', 'billing_invoice_id', 'items',
            'notes', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'total_amount', 'billing_invoice_id', 'created_at']
