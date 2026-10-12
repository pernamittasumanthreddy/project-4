from rest_framework import serializers
from .models import (
    LabCategory, LabTest, LabTestPanel, LabOrder, LabOrderItem,
    Specimen, SpecimenEvent, LabResult, LabResultVersion, CriticalResultAlert, LabReport
)
from contracts.serializers import PatientContractSerializer

class LabCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LabCategory
        fields = '__all__'

class LabTestSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = LabTest
        fields = '__all__'

class LabTestPanelSerializer(serializers.ModelSerializer):
    tests = LabTestSerializer(many=True, read_only=True)
    test_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=LabTest.objects.all(), write_only=True, source='tests'
    )
    class Meta:
        model = LabTestPanel
        fields = '__all__'

class SpecimenEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecimenEvent
        fields = '__all__'

class SpecimenSerializer(serializers.ModelSerializer):
    events = SpecimenEventSerializer(many=True, read_only=True)
    class Meta:
        model = Specimen
        fields = '__all__'

class LabResultVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResultVersion
        fields = '__all__'

class LabResultSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    test_code = serializers.CharField(source='test.test_code', read_only=True)
    loinc_code = serializers.CharField(source='test.loinc_code', read_only=True)
    versions = LabResultVersionSerializer(many=True, read_only=True)
    
    class Meta:
        model = LabResult
        fields = '__all__'

class LabOrderItemSerializer(serializers.ModelSerializer):
    test_details = LabTestSerializer(source='test', read_only=True)
    result = LabResultSerializer(read_only=True)

    class Meta:
        model = LabOrderItem
        fields = '__all__'

class LabOrderSerializer(serializers.ModelSerializer):
    items = LabOrderItemSerializer(many=True, read_only=True)
    specimens = SpecimenSerializer(many=True, read_only=True)
    patient_details = PatientContractSerializer(source='patient', read_only=True)

    class Meta:
        model = LabOrder
        fields = '__all__'

class CriticalResultAlertSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    test_name = serializers.CharField(source='result.test.name', read_only=True)
    observed_value = serializers.SerializerMethodField()

    class Meta:
        model = CriticalResultAlert
        fields = '__all__'

    def get_observed_value(self, obj):
        res = obj.result
        return f"{res.numeric_value if res.numeric_value is not None else res.text_value} {res.unit}"

class LabReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='order.patient.full_name', read_only=True)
    accession_number = serializers.CharField(source='order.accession_number', read_only=True)
    
    class Meta:
        model = LabReport
        fields = '__all__'
