from rest_framework import serializers
from clinical.models import (
    ClinicalEncounter,
    ClinicalAmendment,
    ClinicalDiagnosis,
    PatientAllergy,
    ElectronicPrescription,
    PrescriptionItem,
    NursingObservation,
    FluidBalanceRecord,
    EMARRecord,
    SBARHandover,
    DischargeSummary,
    ClinicalReferral,
    ClinicalTemplate,
)


class ClinicalAmendmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalAmendment
        fields = [
            "id", "encounter", "amendment_sequence", "author_id",
            "author_name", "reason", "addendum_notes",
            "previous_snapshot_hash", "signature_hash", "created_at"
        ]
        read_only_fields = ["id", "amendment_sequence", "signature_hash", "created_at"]


class ClinicalDiagnosisSerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")

    class Meta:
        model = ClinicalDiagnosis
        fields = [
            "id", "encounter", "patient", "patient_mrn", "patient_name",
            "icd10_code", "diagnosis_name", "diagnosis_type",
            "clinical_notes", "diagnosed_by_doctor_id", "is_chronic",
            "onset_date", "resolved_date", "created_at"
        ]
        read_only_fields = ["id", "created_at"]


class PatientAllergySerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")

    class Meta:
        model = PatientAllergy
        fields = [
            "id", "patient", "patient_mrn", "patient_name",
            "allergen", "allergy_type", "severity",
            "reaction_description", "recorded_by_id",
            "recorded_by_name", "is_active", "created_at"
        ]
        read_only_fields = ["id", "created_at"]


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = [
            "id", "prescription", "medication_name", "generic_name",
            "dosage", "route", "frequency", "duration_days",
            "total_quantity", "instructions", "is_dispensed"
        ]
        read_only_fields = ["id"]


class ElectronicPrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, required=False)
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")

    class Meta:
        model = ElectronicPrescription
        fields = [
            "id", "prescription_number", "encounter", "patient",
            "patient_mrn", "patient_name", "prescriber_id",
            "prescriber_name", "status", "prescribed_date",
            "expiry_date", "notes", "items", "created_at"
        ]
        read_only_fields = ["id", "prescription_number", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        prescription = ElectronicPrescription.objects.create(**validated_data)
        for item_data in items_data:
            item_data.pop("prescription", None)
            PrescriptionItem.objects.create(
                tenant=prescription.tenant,
                prescription=prescription,
                **item_data
            )
        return prescription


class ClinicalEncounterSerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")
    diagnoses = ClinicalDiagnosisSerializer(many=True, read_only=True)
    amendments = ClinicalAmendmentSerializer(many=True, read_only=True)
    prescriptions = ElectronicPrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = ClinicalEncounter
        fields = [
            "id", "encounter_number", "patient", "patient_mrn", "patient_name",
            "appointment", "admission", "doctor_id", "doctor_name", "department",
            "encounter_type", "status", "encounter_datetime",
            "chief_complaint", "subjective_notes", "objective_findings",
            "assessment", "plan", "is_signed", "signed_at",
            "signed_by_doctor_id", "signed_by_doctor_name", "signature_hash",
            "diagnoses", "amendments", "prescriptions", "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "encounter_number", "is_signed", "signed_at",
            "signed_by_doctor_id", "signed_by_doctor_name",
            "signature_hash", "created_at", "updated_at"
        ]


class SignEncounterSerializer(serializers.Serializer):
    doctor_id = serializers.CharField(max_length=100)
    doctor_name = serializers.CharField(max_length=200)


class AddAmendmentSerializer(serializers.Serializer):
    author_id = serializers.CharField(max_length=100)
    author_name = serializers.CharField(max_length=200)
    reason = serializers.CharField()
    addendum_notes = serializers.CharField()


class NursingObservationSerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")
    mews_score = serializers.ReadOnlyField()

    class Meta:
        model = NursingObservation
        fields = [
            "id", "patient", "patient_mrn", "patient_name", "admission",
            "nurse_id", "nurse_name", "recorded_at",
            "systolic_bp", "diastolic_bp", "heart_rate", "respiratory_rate",
            "temperature_celsius", "oxygen_saturation", "avpu_score",
            "pain_score", "mews_score", "clinical_notes", "created_at"
        ]
        read_only_fields = ["id", "mews_score", "created_at"]


class FluidBalanceRecordSerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")
    net_balance_ml = serializers.ReadOnlyField()

    class Meta:
        model = FluidBalanceRecord
        fields = [
            "id", "patient", "patient_mrn", "patient_name", "admission",
            "recorded_at", "shift", "oral_intake_ml", "iv_intake_ml",
            "urine_output_ml", "drain_output_ml", "net_balance_ml",
            "recorded_by_name", "notes", "created_at"
        ]
        read_only_fields = ["id", "net_balance_ml", "created_at"]


class EMARRecordSerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")
    medication_name = serializers.ReadOnlyField(source="prescription_item.medication_name")
    dosage = serializers.ReadOnlyField(source="prescription_item.dosage")
    route = serializers.ReadOnlyField(source="prescription_item.route")

    class Meta:
        model = EMARRecord
        fields = [
            "id", "patient", "patient_mrn", "patient_name",
            "prescription_item", "medication_name", "dosage", "route",
            "scheduled_time", "administered_time", "status",
            "nurse_id", "nurse_name", "five_rights_verified",
            "notes", "created_at"
        ]
        read_only_fields = ["id", "created_at"]


class SBARHandoverSerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")

    class Meta:
        model = SBARHandover
        fields = [
            "id", "patient", "patient_mrn", "patient_name", "admission",
            "giving_nurse_id", "giving_nurse_name", "receiving_nurse_id",
            "receiving_nurse_name", "handover_time", "shift",
            "situation", "background", "assessment", "recommendation",
            "code_status", "created_at"
        ]
        read_only_fields = ["id", "created_at"]


class DischargeSummarySerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")
    admission_number = serializers.ReadOnlyField(source="admission.admission_number")

    class Meta:
        model = DischargeSummary
        fields = [
            "id", "summary_number", "admission", "admission_number",
            "patient", "patient_mrn", "patient_name",
            "author_doctor_id", "author_doctor_name",
            "admission_date", "discharge_date", "discharge_condition",
            "primary_diagnosis", "hospital_course", "discharge_medications",
            "diet_and_lifestyle", "follow_up_instructions",
            "warning_signs_red_flags", "is_signed", "signed_at",
            "signature_hash", "created_at"
        ]
        read_only_fields = [
            "id", "summary_number", "is_signed", "signed_at",
            "signature_hash", "created_at"
        ]


class SignDischargeSummarySerializer(serializers.Serializer):
    doctor_id = serializers.CharField(max_length=100)
    doctor_name = serializers.CharField(max_length=200)


class ClinicalReferralSerializer(serializers.ModelSerializer):
    patient_mrn = serializers.ReadOnlyField(source="patient.mrn")
    patient_name = serializers.ReadOnlyField(source="patient.full_name")

    class Meta:
        model = ClinicalReferral
        fields = [
            "id", "referral_number", "encounter", "patient",
            "patient_mrn", "patient_name", "referring_doctor_name",
            "target_specialty", "target_doctor_name", "urgency",
            "clinical_reason", "status", "consultant_reply", "created_at"
        ]
        read_only_fields = ["id", "referral_number", "created_at"]


class ClinicalTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalTemplate
        fields = [
            "id", "title", "specialty", "template_type",
            "content_json", "is_active", "created_at"
        ]
        read_only_fields = ["id", "created_at"]
