"""HMS Pharmacy Returns Serializers — Member 5"""

from rest_framework import serializers
from pharmacy.models.returns import PatientReturn, SupplierReturn, StockQuarantine


class PatientReturnSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.brand_name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    receiver_name = serializers.CharField(source='received_by.username', read_only=True)

    class Meta:
        model = PatientReturn
        fields = [
            'id', 'return_number', 'dispense_record', 'patient', 'patient_name',
            'medicine', 'medicine_name', 'batch', 'batch_number', 'quantity_returned',
            'condition', 'reason', 'routed_to_quarantine', 'refund_amount',
            'billing_refund_id', 'received_by', 'receiver_name', 'created_at'
        ]
        read_only_fields = ['id', 'routed_to_quarantine', 'refund_amount', 'created_at']


class SupplierReturnSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.brand_name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)

    class Meta:
        model = SupplierReturn
        fields = [
            'id', 'return_number', 'supplier', 'supplier_name', 'medicine',
            'medicine_name', 'batch', 'batch_number', 'quantity', 'unit_cost',
            'total_credit', 'reason', 'supplier_credit_note', 'authorized_by',
            'created_at'
        ]
        read_only_fields = ['id', 'total_credit', 'created_at']


class StockQuarantineSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.brand_name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.username', read_only=True)

    class Meta:
        model = StockQuarantine
        fields = [
            'id', 'batch', 'batch_number', 'medicine', 'medicine_name',
            'quantity', 'source', 'reason', 'is_resolved', 'resolution',
            'resolution_notes', 'resolved_by', 'resolved_by_name',
            'resolved_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
