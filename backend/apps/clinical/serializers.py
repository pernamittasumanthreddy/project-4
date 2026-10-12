from rest_framework import serializers
from apps.clinical.models import Encounter, Diagnosis, Prescription, PrescriptionItem, Allergy, MedicalHistory

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['id', 'patient', 'allergen', 'reaction', 'severity', 'identified_date']


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['id', 'patient', 'condition_name', 'onset_year', 'status', 'notes']


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ['id', 'encounter', 'patient', 'icd10_code', 'description', 'severity', 'is_primary', 'diagnosed_date']


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medication_name', 'dosage', 'route', 'frequency', 'duration_days', 'quantity', 'instructions']


class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'prescription_number', 'encounter', 'patient', 'patient_name',
            'doctor', 'doctor_name', 'status', 'issued_date', 'valid_until',
            'special_instructions', 'items', 'created_at'
        ]


class EncounterSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_mrn = serializers.CharField(source='patient.mrn', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    diagnoses = DiagnosisSerializer(many=True, read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    signed_by_name = serializers.CharField(source='signed_by.full_name', read_only=True)

    class Meta:
        model = Encounter
        fields = [
            'id', 'encounter_number', 'appointment', 'patient', 'patient_name', 'patient_mrn',
            'doctor', 'doctor_name', 'doctor_specialization', 'encounter_date', 'encounter_type',
            'status', 'chief_complaint', 'vitals', 'subjective_notes', 'physical_examination',
            'assessment', 'clinical_plan', 'signed_by', 'signed_by_name', 'signed_at',
            'diagnoses', 'prescriptions', 'created_at'
        ]
