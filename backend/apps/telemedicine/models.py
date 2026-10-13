import uuid
import secrets
from django.db import models
from apps.core.models import TenantScopedModel
from apps.appointments.models import Appointment

class TelemedicineSession(TenantScopedModel):
    """
    Secure Virtual Consultation Session linking Appointment, Doctor, and Patient.
    Manages WebRTC room authorization, tokens, waiting room, and lifecycle states.
    """
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled / Ready for Activation'),
        ('WAITING_ROOM', 'Patient in Virtual Waiting Room'),
        ('IN_PROGRESS', 'Live WebRTC Consultation'),
        ('ENDED', 'Consultation Concluded'),
        ('EXPIRED', 'Session Expired'),
        ('CANCELLED', 'Session Cancelled'),
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='telemedicine_session')
    room_code = models.CharField(max_length=64, unique=True)
    doctor_token = models.CharField(max_length=64, default=secrets.token_urlsafe)
    patient_token = models.CharField(max_length=64, default=secrets.token_urlsafe)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')

    # Participant presence tracking
    doctor_present = models.BooleanField(default=False)
    patient_present = models.BooleanField(default=False)
    doctor_joined_at = models.DateTimeField(null=True, blank=True)
    patient_joined_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)

    # Security & compliance
    recording_enabled = models.BooleanField(default=False, help_text="HIPAA compliant: false by default")
    clinical_quick_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Room {self.room_code} for Appt #{self.appointment.appointment_number} [{self.status}]"


class SignalingMessage(models.Model):
    """
    High-Speed WebRTC Session Signaling Message store.
    Exchanges SDP Offers, Answers, and ICE Candidates securely between doctor and patient.
    Requires ZERO external paid vendors (Twilio/Agora/Vonage).
    """
    MESSAGE_TYPES = (
        ('OFFER', 'WebRTC SDP Offer'),
        ('ANSWER', 'WebRTC SDP Answer'),
        ('ICE_CANDIDATE', 'Interactive Connectivity ICE Candidate'),
        ('WAITING_PING', 'Waiting Room Presence Ping'),
        ('CALL_STATUS', 'Call State Update'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(TelemedicineSession, on_delete=models.CASCADE, related_name='signaling_messages')
    sender_role = models.CharField(max_length=20, choices=(('DOCTOR', 'Doctor'), ('PATIENT', 'Patient')))
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    payload = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['session', 'sender_role', 'is_delivered']),
        ]

    def __str__(self):
        return f"[{self.sender_role} -> {self.message_type}] in {self.session.room_code}"
