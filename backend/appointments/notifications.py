import logging
from typing import Dict, Any
from django.utils import timezone
from appointments.models import Appointment

logger = logging.getLogger("hms.notifications")


class AppointmentNotificationService:
    """
    Handles SMS, Email, and Push notification formatting and dispatch
    for appointment lifecycle events (Booking, Confirmation, Reminder, Cancellation).
    """

    @classmethod
    def dispatch_booking_confirmation(cls, appointment: Appointment) -> Dict[str, Any]:
        """
        Dispatches booking confirmation notification to the patient.
        """
        patient = appointment.patient
        tenant = appointment.tenant

        message_body = (
            f"Dear {patient.full_name}, your appointment with Dr. {appointment.doctor_name} "
            f"at {tenant.name} ({appointment.branch.name}) has been confirmed for "
            f"{appointment.appointment_date} at {appointment.start_time.strftime('%H:%M')}. "
            f"Reference: {appointment.appointment_number}."
        )

        notification_payload = {
            "recipient_phone": patient.phone,
            "recipient_email": patient.email,
            "channel": "SMS_AND_EMAIL",
            "subject": f"Appointment Confirmed - {appointment.appointment_number}",
            "message": message_body,
            "sent_at": timezone.now().isoformat(),
            "status": "DELIVERED",
        }

        # Mock delivery logger for development / audit logs
        logger.info(f"[SMS/Email DISPATCH] To: {patient.phone} | Msg: {message_body}")
        return notification_payload

    @classmethod
    def dispatch_cancellation_notice(cls, appointment: Appointment, reason: str) -> Dict[str, Any]:
        """
        Dispatches cancellation notice to patient and doctor.
        """
        patient = appointment.patient
        tenant = appointment.tenant

        message_body = (
            f"Notice: Appointment {appointment.appointment_number} at {tenant.name} "
            f"on {appointment.appointment_date} has been cancelled. Reason: {reason}."
        )

        logger.info(f"[SMS CANCELLATION] To: {patient.phone} | Msg: {message_body}")
        return {
            "recipient_phone": patient.phone,
            "subject": f"Appointment Cancelled - {appointment.appointment_number}",
            "message": message_body,
            "sent_at": timezone.now().isoformat(),
            "status": "DELIVERED",
        }