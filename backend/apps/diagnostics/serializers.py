from rest_framework import serializers
from apps.diagnostics.models import LabReport, RadiologyReport

class LabReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_mrn = serializers.CharField(source='patient.mrn', read_only=True)
    ordering_doctor_name = serializers.CharField(source='ordering_doctor.full_name', read_only=True)

    class Meta:
        model = LabReport
        fields = [
            'id', 'report_number', 'test_name', 'test_code', 'category',
            'patient', 'patient_name', 'patient_mrn',
            'ordering_doctor', 'ordering_doctor_name',
            'status', 'order_date', 'collected_at', 'specimen_type',
            'results', 'conclusion', 'approved_by', 'approved_at', 'document_url'
        ]


class RadiologyReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_mrn = serializers.CharField(source='patient.mrn', read_only=True)
    ordering_doctor_name = serializers.CharField(source='ordering_doctor.full_name', read_only=True)

    class Meta:
        model = RadiologyReport
        fields = [
            'id', 'study_number', 'study_name', 'modality', 'body_part',
            'patient', 'patient_name', 'patient_mrn',
            'ordering_doctor', 'ordering_doctor_name', 'radiologist_name',
            'study_date', 'status', 'clinical_history', 'findings', 'impression',
            'key_images', 'approved_at'
        ]
