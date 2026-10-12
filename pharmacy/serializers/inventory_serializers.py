"""HMS Pharmacy Inventory Serializers — Member 5"""

from rest_framework import serializers
from pharmacy.models.inventory import MedicineBatch, StorageLocation


class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = ['id', 'code', 'name', 'is_cold_storage', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class MedicineBatchSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.brand_name', read_only=True)
    medicine_generic = serializers.CharField(source='medicine.generic_name', read_only=True)
    medicine_strength = serializers.CharField(source='medicine.strength', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    location_name = serializers.CharField(source='storage_location.name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_near_expiry = serializers.BooleanField(read_only=True)
    days_until_expiry = serializers.IntegerField(read_only=True)

    class Meta:
        model = MedicineBatch
        fields = [
            'id', 'medicine', 'medicine_name', 'medicine_generic', 'medicine_strength',
            'batch_number', 'manufacturer', 'manufacturing_date', 'expiry_date',
            'supplier', 'supplier_name', 'storage_location', 'location_name',
            'purchase_cost', 'selling_price', 'received_quantity', 'available_quantity',
            'reserved_quantity', 'quarantined_quantity', 'status', 'is_expired',
            'is_near_expiry', 'days_until_expiry', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
