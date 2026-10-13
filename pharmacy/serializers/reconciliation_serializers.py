"""HMS Pharmacy Reconciliation Serializers — Member 5"""

from rest_framework import serializers
from pharmacy.models.reconciliation import StockCountSession, StockCountItem


class StockCountItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='batch.medicine.brand_name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    expiry_date = serializers.DateField(source='batch.expiry_date', read_only=True)

    class Meta:
        model = StockCountItem
        fields = [
            'id', 'batch', 'medicine_name', 'batch_number', 'expiry_date',
            'expected_quantity', 'counted_quantity', 'discrepancy_quantity',
            'unit_cost', 'discrepancy_value', 'discrepancy_reason'
        ]
        read_only_fields = ['id', 'expected_quantity', 'discrepancy_quantity', 'discrepancy_value']


class StockCountSessionSerializer(serializers.ModelSerializer):
    items = StockCountItemSerializer(many=True, read_only=True)
    location_name = serializers.CharField(source='storage_location.name', read_only=True)
    initiated_by_name = serializers.CharField(source='initiated_by.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = StockCountSession
        fields = [
            'id', 'session_number', 'storage_location', 'location_name',
            'status', 'initiated_by', 'initiated_by_name', 'approved_by',
            'approved_by_name', 'approved_at', 'total_discrepancy_value',
            'items', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'approved_by', 'approved_at', 'total_discrepancy_value', 'created_at']
