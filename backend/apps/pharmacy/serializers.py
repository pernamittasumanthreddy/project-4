from rest_framework import serializers
from apps.pharmacy.models import Medication, DispensingOrder

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'generic_name', 'brand_name', 'dosage_form', 'strength', 'unit_price', 'stock_quantity']


class DispensingOrderSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)

    class Meta:
        model = DispensingOrder
        fields = ['id', 'dispense_number', 'prescription', 'patient', 'patient_name', 'pharmacist_name', 'status', 'dispensed_at', 'total_amount']
