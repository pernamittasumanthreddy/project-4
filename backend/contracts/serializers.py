from rest_framework import serializers
from .models import Tenant, HospitalBranch, UserProfile, PatientContract, ClinicalEncounterContract, BillingEventContract

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class HospitalBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalBranch
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class PatientContractSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model = PatientContract
        fields = '__all__'

class ClinicalEncounterContractSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_uhid = serializers.CharField(source='patient.uhid', read_only=True)
    class Meta:
        model = ClinicalEncounterContract
        fields = '__all__'

class BillingEventContractSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    class Meta:
        model = BillingEventContract
        fields = '__all__'
