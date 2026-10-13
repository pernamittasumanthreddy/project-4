from rest_framework import serializers
from .models import (
    ImagingModality, ImagingProcedure, ImagingOrder, ImagingOrderItem,
    ImagingStudy, RadiologyReport, RadiologyReportVersion
)
from contracts.serializers import PatientContractSerializer

class ImagingModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagingModality
        fields = '__all__'

class ImagingProcedureSerializer(serializers.ModelSerializer):
    modality_details = ImagingModalitySerializer(source='modality', read_only=True)
    class Meta:
        model = ImagingProcedure
        fields = '__all__'

class RadiologyReportVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyReportVersion
        fields = '__all__'

class RadiologyReportSerializer(serializers.ModelSerializer):
    versions = RadiologyReportVersionSerializer(many=True, read_only=True)
    study_description = serializers.CharField(source='study.study_description', read_only=True)
    patient_name = serializers.CharField(source='study.patient.full_name', read_only=True)

    class Meta:
        model = RadiologyReport
        fields = '__all__'

class ImagingStudySerializer(serializers.ModelSerializer):
    report = RadiologyReportSerializer(read_only=True)
    patient_details = PatientContractSerializer(source='patient', read_only=True)

    class Meta:
        model = ImagingStudy
        fields = '__all__'

class ImagingOrderItemSerializer(serializers.ModelSerializer):
    procedure_details = ImagingProcedureSerializer(source='procedure', read_only=True)
    study = ImagingStudySerializer(read_only=True)

    class Meta:
        model = ImagingOrderItem
        fields = '__all__'

class ImagingOrderSerializer(serializers.ModelSerializer):
    items = ImagingOrderItemSerializer(many=True, read_only=True)
    patient_details = PatientContractSerializer(source='patient', read_only=True)

    class Meta:
        model = ImagingOrder
        fields = '__all__'
