from rest_framework import serializers
from .models import InsurancePayer, InsurancePolicy, InsuranceClaim, DenialLog

class InsurancePayerSerializer(serializers.ModelSerializer):
    payer_type_display = serializers.CharField(source='get_payer_type_display', read_only=True)

    class Meta:
        model = InsurancePayer
        fields = [
            'id', 'code', 'name', 'payer_type', 'payer_type_display',
            'tpa_contact_email', 'tpa_contact_phone', 'settlement_tat_days', 'is_active'
        ]

class InsurancePolicySerializer(serializers.ModelSerializer):
    payer_name = serializers.CharField(source='payer.name', read_only=True)

    class Meta:
        model = InsurancePolicy
        fields = [
            'id', 'patient_id', 'patient_name', 'payer', 'payer_name',
            'policy_number', 'card_number', 'sum_insured', 'copay_percentage',
            'valid_from', 'valid_to', 'is_active'
        ]

class DenialLogSerializer(serializers.ModelSerializer):
    denial_code_display = serializers.CharField(source='get_denial_code_display', read_only=True)

    class Meta:
        model = DenialLog
        fields = [
            'id', 'claim', 'denial_code', 'denial_code_display', 'denial_reason',
            'corrective_action_taken', 'resubmitted_claim_reference', 'logged_at', 'resolved'
        ]

class InsuranceClaimSerializer(serializers.ModelSerializer):
    payer_name = serializers.CharField(source='payer.name', read_only=True)
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    patient_name = serializers.CharField(source='invoice.patient_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    denial_logs = DenialLogSerializer(many=True, read_only=True)

    class Meta:
        model = InsuranceClaim
        fields = [
            'id', 'claim_number', 'invoice', 'invoice_number', 'patient_name',
            'payer', 'payer_name', 'policy', 'pre_auth_number',
            'claim_amount', 'approved_amount', 'patient_copay_amount',
            'deductible_amount', 'settled_amount', 'status', 'status_display',
            'submission_date', 'adjudication_date', 'denial_reason',
            'settlement_reference', 'denial_logs', 'created_at'
        ]
        read_only_fields = ['claim_number']
