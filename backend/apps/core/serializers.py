from rest_framework import serializers
from apps.core.models import Tenant, HospitalBranch, User, AuditLog

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'slug', 'domain', 'tier', 'primary_color', 'contact_email', 'contact_phone', 'is_active', 'created_at']


class HospitalBranchSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = HospitalBranch
        fields = ['id', 'tenant', 'tenant_name', 'name', 'code', 'address', 'city', 'state', 'postal_code', 'phone', 'email', 'is_active']


class UserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone', 'avatar_url', 'tenant', 'tenant_name', 'branch', 'branch_name',
            'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class CurrentUserSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    branch = HospitalBranchSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)
    doctor_profile_id = serializers.SerializerMethodField()
    patient_profile_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone', 'avatar_url', 'tenant', 'branch',
            'doctor_profile_id', 'patient_profile_id', 'is_active'
        ]

    def get_doctor_profile_id(self, obj):
        if hasattr(obj, 'doctor_profile'):
            return str(obj.doctor_profile.id)
        return None

    def get_patient_profile_id(self, obj):
        if hasattr(obj, 'patient_profile'):
            return str(obj.patient_profile.id)
        return None


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'tenant', 'user', 'user_name', 'action', 'resource_type', 'resource_id', 'ip_address', 'details', 'timestamp']
