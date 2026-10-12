"""HMS Pharmacy Purchasing Serializers — Member 5"""

from rest_framework import serializers
from decimal import Decimal
from pharmacy.models.purchasing import (
    PurchaseOrder,
    PurchaseOrderItem,
    GoodsReceipt,
    GoodsReceiptItem,
)


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.brand_name', read_only=True)
    remaining_to_receive = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'medicine', 'medicine_name', 'quantity_ordered',
            'quantity_received', 'remaining_to_receive', 'unit_cost', 'line_total'
        ]
        read_only_fields = ['id', 'quantity_received', 'line_total']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    items = PurchaseOrderItemSerializer(many=True, required=False)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'order_number', 'supplier', 'supplier_name', 'status',
            'order_date', 'expected_delivery_date', 'total_amount', 'items',
            'created_by', 'created_by_name', 'approved_by', 'approved_by_name',
            'approved_at', 'rejection_reason', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'total_amount', 'approved_by', 'approved_at', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        po = PurchaseOrder.objects.create(**validated_data)
        for item_data in items_data:
            PurchaseOrderItem.objects.create(purchase_order=po, **item_data)
        po.recalculate_total()
        return po


class GoodsReceiptItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.brand_name', read_only=True)

    class Meta:
        model = GoodsReceiptItem
        fields = [
            'id', 'po_item', 'medicine', 'medicine_name', 'batch_number',
            'manufacturing_date', 'expiry_date', 'quantity_received',
            'quantity_accepted', 'quantity_rejected', 'rejection_reason',
            'unit_cost', 'batch'
        ]
        read_only_fields = ['id']


class GoodsReceiptSerializer(serializers.ModelSerializer):
    items = GoodsReceiptItemSerializer(many=True, read_only=True)
    received_by_name = serializers.CharField(source='received_by.username', read_only=True)
    po_number = serializers.CharField(source='purchase_order.order_number', read_only=True)

    class Meta:
        model = GoodsReceipt
        fields = [
            'id', 'receipt_number', 'purchase_order', 'po_number',
            'delivery_reference', 'received_date', 'received_by',
            'received_by_name', 'items', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
