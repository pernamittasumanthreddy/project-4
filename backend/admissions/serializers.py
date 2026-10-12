from rest_framework import serializers
from admissions.models import Ward, Room, Bed, Admission, BedTransferLog


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ["id", "room", "bed_number", "status", "is_active"]


class RoomSerializer(serializers.ModelSerializer):
    beds = BedSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["id", "ward", "room_number", "room_type", "daily_rate", "is_active", "beds"]


class WardSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    ward_type_name = serializers.CharField(source="get_ward_type_display", read_only=True)

    class Meta:
        model = Ward
        fields = ["id", "branch", "name", "ward_type", "ward_type_name", "floor", "total_beds", "is_active", "rooms"]


class BedTransferLogSerializer(serializers.ModelSerializer):
    from_bed_number = serializers.CharField(source="from_bed.bed_number", read_only=True)
    to_bed_number = serializers.CharField(source="to_bed.bed_number", read_only=True)

    class Meta:
        model = BedTransferLog
        fields = ["id", "admission", "from_bed", "from_bed_number", "to_bed", "to_bed_number", "transfer_time", "transferred_by_user_name", "reason"]


class AdmissionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    patient_mrn = serializers.CharField(source="patient.mrn", read_only=True)
    bed_number = serializers.CharField(source="bed.bed_number", read_only=True)
    room_number = serializers.CharField(source="bed.room.room_number", read_only=True)
    ward_name = serializers.CharField(source="bed.room.ward.name", read_only=True)
    transfers = BedTransferLogSerializer(many=True, read_only=True)

    class Meta:
        model = Admission
        fields = [
            "id", "admission_number", "patient", "patient_name", "patient_mrn",
            "branch", "department", "admitting_doctor_id", "admitting_doctor_name",
            "bed", "bed_number", "room_number", "ward_name", "admission_date",
            "discharge_date", "status", "admission_diagnosis", "discharge_diagnosis",
            "discharge_summary", "billing_cleared", "billing_cleared_at", "transfers"
        ]
        read_only_fields = ["id", "admission_number", "billing_cleared", "billing_cleared_at"]


class AdmitPatientSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField()
    branch_id = serializers.UUIDField()
    department_id = serializers.UUIDField()
    admitting_doctor_id = serializers.CharField()
    admitting_doctor_name = serializers.CharField()
    bed_id = serializers.UUIDField()
    admission_diagnosis = serializers.CharField()


class TransferBedSerializer(serializers.Serializer):
    to_bed_id = serializers.UUIDField()
    reason = serializers.CharField()
    transferred_by_user_name = serializers.CharField(default="Ward Nurse")

