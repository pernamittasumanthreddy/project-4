from rest_framework import serializers
from appointments.models import DoctorSchedule, DoctorLeave, Appointment, OPDQueueToken


class DoctorScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

    class Meta:
        model = DoctorSchedule
        fields = [
            "id", "doctor_id", "doctor_name", "doctor_specialty",
            "branch", "department", "day_of_week", "day_name",
            "start_time", "end_time", "slot_duration_minutes",
            "buffer_minutes", "max_patients", "is_active"
        ]


class DoctorLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLeave
        fields = ["id", "doctor_id", "doctor_name", "start_date", "end_date", "reason", "is_approved"]


class OPDQueueTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPDQueueToken
        fields = ["id", "appointment", "branch", "department", "doctor_id", "token_number", "queue_date", "status", "room_number", "called_at"]


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    patient_mrn = serializers.CharField(source="patient.mrn", read_only=True)
    patient_phone = serializers.CharField(source="patient.phone", read_only=True)
    queue_token = OPDQueueTokenSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "appointment_number", "patient", "patient_name", "patient_mrn", "patient_phone",
            "doctor_id", "doctor_name", "branch", "department",
            "appointment_date", "start_time", "end_time",
            "appointment_type", "status", "token_number",
            "chief_complaint", "cancellation_reason",
            "checked_in_at", "consultation_started_at", "consultation_completed_at",
            "telemedicine_room_id", "queue_token", "created_at"
        ]
        read_only_fields = ["id", "appointment_number", "token_number", "created_at"]


class BookAppointmentSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField()
    doctor_id = serializers.CharField()
    doctor_name = serializers.CharField()
    branch_id = serializers.UUIDField()
    department_id = serializers.UUIDField()
    appointment_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    appointment_type = serializers.ChoiceField(choices=Appointment.TYPE_CHOICES, default="OPD")
    chief_complaint = serializers.CharField(required=False, allow_blank=True, default="")

