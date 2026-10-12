from rest_framework import serializers
from apps.telemedicine.models import TelemedicineSession, SignalingMessage
from apps.appointments.serializers import AppointmentSerializer

class SignalingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalingMessage
        fields = ['id', 'session', 'sender_role', 'message_type', 'payload', 'timestamp', 'is_delivered']
        read_only_fields = ['id', 'timestamp']


class TelemedicineSessionSerializer(serializers.ModelSerializer):
    appointment_details = AppointmentSerializer(source='appointment', read_only=True)
    patient_name = serializers.CharField(source='appointment.patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='appointment.doctor.full_name', read_only=True)

    class Meta:
        model = TelemedicineSession
        fields = [
            'id', 'room_code', 'appointment', 'appointment_details',
            'patient_name', 'doctor_name', 'status',
            'doctor_present', 'patient_present',
            'doctor_joined_at', 'patient_joined_at',
            'started_at', 'ended_at', 'duration_seconds',
            'recording_enabled', 'clinical_quick_notes', 'created_at'
        ]
        read_only_fields = ['id', 'room_code', 'doctor_token', 'patient_token', 'created_at']
