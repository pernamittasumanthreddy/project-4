from rest_framework import serializers
from patients.models import Patient, EmergencyContact, PatientConsent, PatientMergeAudit


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = [
            "id", "name", "relationship", "phone", "alternate_phone",
            "email", "address", "is_primary", "created_at"
        ]


class PatientConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientConsent
        fields = [
            "id", "consent_type", "title", "content_text", "is_granted",
            "granted_at", "revoked_at", "signer_name", "signer_relationship", "signature_ip"
        ]


class PatientSerializer(serializers.ModelSerializer):
    emergency_contacts = EmergencyContactSerializer(many=True, read_only=True)
    consents = PatientConsentSerializer(many=True, read_only=True)
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = [
            "id", "mrn", "national_id", "passport_number", "first_name",
            "middle_name", "last_name", "full_name", "date_of_birth", "age",
            "gender", "blood_group", "marital_status", "phone", "alternate_phone",
            "email", "address_line_1", "address_line_2", "city", "state_province",
            "postal_code", "country", "preferred_branch", "status",
            "is_merged", "merged_into", "allergies", "chronic_conditions",
            "emergency_contacts", "consents", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "mrn", "is_merged", "merged_into", "created_at", "updated_at"]


class PatientRegistrationSerializer(serializers.ModelSerializer):
    emergency_contact = EmergencyContactSerializer(required=False, write_only=True)

    class Meta:
        model = Patient
        fields = [
            "first_name", "middle_name", "last_name", "date_of_birth",
            "gender", "blood_group", "marital_status", "phone", "alternate_phone",
            "email", "national_id", "passport_number", "address_line_1",
            "address_line_2", "city", "state_province", "postal_code",
            "country", "preferred_branch", "allergies", "chronic_conditions",
            "emergency_contact"
        ]


class PatientMergeSerializer(serializers.Serializer):
    surviving_patient_id = serializers.UUIDField()
    subsumed_patient_id = serializers.UUIDField()
    reason = serializers.CharField(min_length=10)

