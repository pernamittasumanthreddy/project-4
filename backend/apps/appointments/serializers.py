from rest_framework import serializers
from datetime import datetime, time, timedelta
from apps.appointments.models import Department, DoctorProfile, PatientProfile, Appointment

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'icon_name', 'is_active']


class DoctorProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    avatar_url = serializers.CharField(source='user.avatar_url', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'name', 'license_number', 'specialization', 'experience_years',
            'qualification', 'consultation_fee', 'slot_duration_minutes',
            'is_available_telemedicine', 'rating', 'review_count', 'bio',
            'office_room', 'department', 'department_name', 'avatar_url', 'email'
        ]


class PatientProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            'id', 'mrn', 'full_name', 'email', 'phone', 'username',
            'date_of_birth', 'gender', 'blood_group',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'address_line', 'city', 'state', 'postal_code',
            'insurance_provider', 'insurance_policy_number', 'created_at'
        ]
        read_only_fields = ['id', 'mrn', 'created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_mrn = serializers.CharField(source='patient.mrn', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    doctor_avatar = serializers.CharField(source='doctor.user.avatar_url', read_only=True)
    doctor_fee = serializers.DecimalField(source='doctor.consultation_fee', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'appointment_number', 'patient', 'patient_name', 'patient_mrn',
            'doctor', 'doctor_name', 'doctor_specialization', 'doctor_avatar', 'doctor_fee',
            'appointment_date', 'start_time', 'end_time', 'appointment_type',
            'status', 'reason_for_visit', 'notes', 'cancellation_reason',
            'checked_in_at', 'created_at'
        ]
        read_only_fields = ['id', 'appointment_number', 'created_at']


class AppointmentBookingSerializer(serializers.Serializer):
    doctor_id = serializers.UUIDField()
    appointment_date = serializers.DateField()
    start_time = serializers.TimeField()
    appointment_type = serializers.ChoiceField(choices=['IN_PERSON', 'TELEMEDICINE'], default='TELEMEDICINE')
    reason_for_visit = serializers.CharField(max_length=500)

    def validate(self, data):
        # 1. Verify doctor exists and belongs to active tenant
        request = self.context.get('request')
        doctor = DoctorProfile.objects.filter(id=data['doctor_id']).first()
        if not doctor:
            raise serializers.ValidationError({"doctor_id": "Selected physician was not found."})

        # 2. Check for slot conflict with doctor
        conflicts = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=data['appointment_date'],
            start_time=data['start_time'],
            status__in=['CONFIRMED', 'PENDING', 'IN_PROGRESS']
        )
        if conflicts.exists():
            raise serializers.ValidationError({
                "start_time": f"Doctor {doctor.full_name} is already booked for {data['appointment_date']} at {data['start_time']}. Please select another time slot."
            })

        data['doctor'] = doctor
        return data
