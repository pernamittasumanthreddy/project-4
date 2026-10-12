from rest_framework import serializers
from .models import Tenant, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'code', 'city', 'state_code', 'gstin', 'address', 'phone', 'email', 'is_active']

class TenantSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'slug', 'domain', 'subscription_tier', 'is_active', 'default_currency', 'created_at', 'branches']
