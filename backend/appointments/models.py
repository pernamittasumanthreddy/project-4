import uuid
from django.db import models
from django.utils import timezone
from core.models import TenantAwareModel, HospitalBranch, Department
from patients.models import Patient


class DoctorSchedule(TenantAwareModel):
    """
    Weekly recurring or dated availability schedule for physicians/consultants.
    """
    DAY_OF_WEEK_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    doctor_id = models.CharField(max_length=100, db_index=True, help_text="User ID from Auth / Member 1")
    doctor_name = models.CharField(max_length=200)
    doctor_specialty = models.CharField(max_length=150, blank=True, default="General Medicine")
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name="doctor_schedules")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="doctor_schedules")

    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES, db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_minutes = models.PositiveIntegerField(default=15, help_text="Duration per consultation slot")
    buffer_minutes = models.PositiveIntegerField(default=0, help_text="Break buffer between slots")
    max_patients = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hms_doctor_schedules"
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"Dr. {self.doctor_name} ({self.get_day_of_week_display()} {self.start_time}-{self.end_time})"


class DoctorLeave(TenantAwareModel):
    """
    Tracks leaves, conferences, and off-duty periods to block slot booking.
    """
    doctor_id = models.CharField(max_length=100, db_index=True)
    doctor_name = models.CharField(max_length=200)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    reason = models.CharField(max_length=255, blank=True, default="")
    is_approved = models.BooleanField(default=True)

    class Meta:
        db_table = "hms_doctor_leaves"
        ordering = ["-start_date"]

    def __str__(self):
        return f"Dr. {self.doctor_name} Leave ({self.start_date} to {self.end_date})"


class Appointment(TenantAwareModel):
    """
    Core appointment entity supporting OPD, teleconsultation, and walk-in bookings.
    Protected with DB row-locking during creation to eliminate double-booking race conditions.
    """
    TYPE_CHOICES = [
        ("OPD", "Outpatient Consultation"),
        ("TELEMEDICINE", "Video / Teleconsultation"),
        ("FOLLOW_UP", "Follow-up Consultation"),
        ("WALK_IN", "Walk-in Emergency / Urgent Care"),
    ]

    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("CONFIRMED", "Confirmed"),
        ("CHECKED_IN", "Checked In (In Waiting Room)"),
        ("IN_CONSULTATION", "In Consultation"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
        ("NO_SHOW", "No-Show / Missed"),
        ("RESCHEDULED", "Rescheduled"),
    ]

    appointment_number = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unique Appointment Tracking Code, e.g. APT-2026-0001"
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor_id = models.CharField(max_length=100, db_index=True)
    doctor_name = models.CharField(max_length=200)
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name="appointments")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="appointments")

    appointment_date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="OPD")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="SCHEDULED", db_index=True)

    token_number = models.PositiveIntegerField(null=True, blank=True, help_text="Daily sequence queue token number")
    chief_complaint = models.TextField(blank=True, default="")
    cancellation_reason = models.TextField(blank=True, default="")
    cancelled_by_user_id = models.CharField(max_length=100, blank=True, default="")
    cancelled_at = models.DateTimeField(null=True, blank=True)

    checked_in_at = models.DateTimeField(null=True, blank=True)
    consultation_started_at = models.DateTimeField(null=True, blank=True)
    consultation_completed_at = models.DateTimeField(null=True, blank=True)

    # Telemedicine room identifier for Member 7 integration
    telemedicine_room_id = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        db_table = "hms_appointments"
        unique_together = ("tenant", "appointment_number")
        indexes = [
            models.Index(fields=["tenant", "doctor_id", "appointment_date", "start_time"]),
            models.Index(fields=["tenant", "status", "appointment_date"]),
        ]
        ordering = ["appointment_date", "start_time"]

    def __str__(self):
        return f"{self.appointment_number} - {self.patient.full_name} with Dr. {self.doctor_name} ({self.status})"


class OPDQueueToken(TenantAwareModel):
    """
    Real-time OPD queue status and token board.
    """
    QUEUE_STATUS = [
        ("WAITING", "Waiting"),
        ("CALLED", "Called to Room"),
        ("ENGAGED", "Currently with Doctor"),
        ("DONE", "Done"),
        ("SKIPPED", "Skipped / Absent"),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="queue_token")
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name="queue_tokens")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="queue_tokens")
    doctor_id = models.CharField(max_length=100)
    token_number = models.PositiveIntegerField(db_index=True)
    queue_date = models.DateField(default=timezone.now, db_index=True)
    status = models.CharField(max_length=20, choices=QUEUE_STATUS, default="WAITING", db_index=True)
    room_number = models.CharField(max_length=30, blank=True, default="")
    called_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "hms_opd_queue_tokens"
        unique_together = ("tenant", "branch", "doctor_id", "queue_date", "token_number")
        ordering = ["token_number"]

    def __str__(self):
        return f"Token #{self.token_number} [{self.status}] Dr. {self.appointment.doctor_name}"
