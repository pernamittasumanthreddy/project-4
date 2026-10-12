"""HMS Pharmacy Supplier Serializers — Member 5"""

from rest_framework import serializers
from pharmacy.models.supplier import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'code', 'name', 'contact_person', 'phone', 'email',
            'address', 'gstin', 'pan_number', 'drug_license_number',
            'payment_terms', 'is_active', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_code(self, value):
        request = self.context.get('request')
        tenant = getattr(request, 'tenant', None)
        qs = Supplier.objects.filter(code__iexact=value, tenant=tenant)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("A supplier with this code already exists for your organization.")
        return value.upper()
