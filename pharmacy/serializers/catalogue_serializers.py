"""HMS Pharmacy Catalogue Serializers — Member 5"""

from rest_framework import serializers
from pharmacy.models.catalogue import Medicine, MedicineCategory


class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class MedicineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_stock = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = [
            'id', 'code', 'brand_name', 'generic_name', 'active_ingredients',
            'strength', 'dosage_form', 'route', 'manufacturer', 'classification',
            'category', 'category_name', 'requires_prescription', 'storage_instructions',
            'barcode_sku', 'unit_of_measure', 'dispensing_unit', 'reorder_level',
            'reorder_quantity', 'unit_price', 'is_active', 'total_stock', 'is_low_stock',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_stock(self, obj):
        request = self.context.get('request')
        branch = getattr(request, 'branch', None) if request else None
        return obj.get_total_stock(branch=branch)

    def get_is_low_stock(self, obj):
        request = self.context.get('request')
        branch = getattr(request, 'branch', None) if request else None
        return obj.is_low_stock(branch=branch)

    def validate_code(self, value):
        request = self.context.get('request')
        tenant = getattr(request, 'tenant', None)
        qs = Medicine.objects.filter(code__iexact=value, tenant=tenant)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("A medicine with this code already exists for your organization.")
        return value.upper()
