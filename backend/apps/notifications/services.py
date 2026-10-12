"""
Central Notification Dispatcher Service for Member 7.
Connects with Member 1-6 domain events, enforces deduplication, and routes to adapters.
"""

import hashlib
from apps.notifications.models import Notification, DeliveryLog
from apps.notifications.adapters import ConsoleEmailAdapter, ConsoleSMSAdapter

email_adapter = ConsoleEmailAdapter()
sms_adapter = ConsoleSMSAdapter()

class NotificationDispatcher:
    @staticmethod
    def dispatch(tenant, recipient, category, title, message, action_url="", priority="NORMAL", dedup_key=None, channels=('IN_APP', 'EMAIL', 'SMS')):
        """
        Primary dispatching engine. Enforces deduplication and dispatches to configured adapters.
        """
        if not tenant or not recipient:
            return None

        # Automatic dedup key generation if not explicitly provided
        if not dedup_key:
            dedup_raw = f"{recipient.id}:{category}:{title}:{message[:50]}"
            dedup_key = hashlib.md5(dedup_raw.encode()).hexdigest()

        # Check for duplicate event
        existing = Notification.objects.filter(recipient=recipient, event_dedup_key=dedup_key).first()
        if existing:
            return existing

        notification = Notification.objects.create(
            tenant=tenant,
            recipient=recipient,
            category=category,
            priority=priority,
            title=title,
            message=message,
            action_url=action_url,
            event_dedup_key=dedup_key,
        )

        # Log in-app delivery
        DeliveryLog.objects.create(
            notification=notification,
            channel='IN_APP',
            status='DELIVERED',
            destination=f"User #{recipient.username}",
            payload_preview=title,
            attempt_count=1
        )

        # Dispatch via multi-channel adapters
        if 'EMAIL' in channels:
            email_adapter.send(notification, recipient)
        if 'SMS' in channels:
            sms_adapter.send(notification, recipient)

        return notification

    # --- Domain Specific Dispatchers ---

    @classmethod
    def dispatch_appointment_created(cls, appointment):
        # Notify patient
        cls.dispatch(
            tenant=appointment.tenant,
            recipient=appointment.patient.user,
            category='APPOINTMENT',
            priority='HIGH',
            title=f"Appointment Confirmed with {appointment.doctor.full_name}",
            message=f"Your {appointment.get_appointment_type_display().lower()} is scheduled for {appointment.appointment_date} at {appointment.start_time.strftime('%I:%M %p')}.",
            action_url="/patient/appointments",
            dedup_key=f"appt_created_pat_{appointment.id}"
        )
        # Notify doctor
        cls.dispatch(
            tenant=appointment.tenant,
            recipient=appointment.doctor.user,
            category='APPOINTMENT',
            priority='NORMAL',
            title=f"New Patient Consultation Booked: {appointment.patient.full_name}",
            message=f"{appointment.patient.full_name} ({appointment.patient.mrn}) scheduled for {appointment.appointment_date} at {appointment.start_time.strftime('%I:%M %p')}.",
            action_url="/doctor/schedule",
            dedup_key=f"appt_created_doc_{appointment.id}"
        )

    @classmethod
    def dispatch_appointment_cancelled(cls, appointment):
        reason_txt = f" Reason: {appointment.cancellation_reason}" if appointment.cancellation_reason else ""
        cls.dispatch(
            tenant=appointment.tenant,
            recipient=appointment.patient.user,
            category='APPOINTMENT',
            priority='HIGH',
            title=f"Appointment Cancelled: #{appointment.appointment_number}",
            message=f"Your appointment with {appointment.doctor.full_name} on {appointment.appointment_date} has been cancelled.{reason_txt}",
            action_url="/patient/appointments",
            dedup_key=f"appt_cancelled_pat_{appointment.id}"
        )
        cls.dispatch(
            tenant=appointment.tenant,
            recipient=appointment.doctor.user,
            category='APPOINTMENT',
            priority='NORMAL',
            title=f"Appointment Cancelled by Patient: #{appointment.appointment_number}",
            message=f"Appointment for {appointment.patient.full_name} on {appointment.appointment_date} was cancelled.{reason_txt}",
            action_url="/doctor/schedule",
            dedup_key=f"appt_cancelled_doc_{appointment.id}"
        )

    @classmethod
    def dispatch_lab_report_approved(cls, lab_report):
        cls.dispatch(
            tenant=lab_report.tenant,
            recipient=lab_report.patient.user,
            category='LAB_REPORT',
            priority='HIGH',
            title=f"Laboratory Results Released: {lab_report.test_name}",
            message=f"Your laboratory results for {lab_report.test_name} have been verified and approved by the pathologist. Sign in to view findings.",
            action_url="/patient/records",
            dedup_key=f"lab_approved_{lab_report.id}"
        )

    @classmethod
    def dispatch_radiology_report_approved(cls, rad_report):
        cls.dispatch(
            tenant=rad_report.tenant,
            recipient=rad_report.patient.user,
            category='RADIOLOGY',
            priority='HIGH',
            title=f"Diagnostic Imaging Report Ready: {rad_report.study_name}",
            message=f"Your {rad_report.get_modality_display()} report for {rad_report.body_part} is now available in your portal records.",
            action_url="/patient/records",
            dedup_key=f"rad_approved_{rad_report.id}"
        )

    @classmethod
    def dispatch_prescription_issued(cls, prescription):
        cls.dispatch(
            tenant=prescription.tenant,
            recipient=prescription.patient.user,
            category='PRESCRIPTION',
            priority='NORMAL',
            title=f"New Prescription Issued: #{prescription.prescription_number}",
            message=f"Dr. {prescription.doctor.user.last_name} issued a new prescription with medication instructions. View in your medical records.",
            action_url="/patient/records",
            dedup_key=f"rx_issued_{prescription.id}"
        )

    @classmethod
    def dispatch_invoice_created(cls, invoice):
        cls.dispatch(
            tenant=invoice.tenant,
            recipient=invoice.patient.user,
            category='BILLING',
            priority='NORMAL',
            title=f"New Medical Invoice: #{invoice.invoice_number}",
            message=f"An invoice of ${invoice.total_amount:.2f} has been generated. Due date: {invoice.due_date}.",
            action_url="/patient/billing",
            dedup_key=f"inv_created_{invoice.id}"
        )

    @classmethod
    def dispatch_payment_receipt_generated(cls, payment):
        cls.dispatch(
            tenant=payment.tenant,
            recipient=payment.invoice.patient.user,
            category='BILLING',
            priority='NORMAL',
            title=f"Payment Receipt: #{payment.receipt_number}",
            message=f"Payment of ${payment.amount:.2f} for Invoice #{payment.invoice.invoice_number} was successfully recorded.",
            action_url="/patient/billing",
            dedup_key=f"pay_receipt_{payment.id}"
        )

    @classmethod
    def dispatch_telemedicine_invite(cls, session):
        cls.dispatch(
            tenant=session.tenant,
            recipient=session.appointment.patient.user,
            category='TELEMEDICINE',
            priority='URGENT',
            title=f"Virtual Consultation Starting: Dr. {session.appointment.doctor.user.last_name}",
            message=f"Your telemedicine room is open. Click to test audio/video and join your doctor.",
            action_url=f"/telemedicine/room/{session.id}",
            dedup_key=f"tele_invite_{session.id}"
        )

    @classmethod
    def dispatch_clinical_summary_signed(cls, encounter):
        cls.dispatch(
            tenant=encounter.tenant,
            recipient=encounter.patient.user,
            category='CLINICAL',
            priority='NORMAL',
            title=f"Clinical Consultation Summary Available",
            message=f"Dr. {encounter.doctor.user.last_name} finalized your clinical summary. You may review instructions and care plan in your portal.",
            action_url="/patient/records",
            dedup_key=f"enc_signed_{encounter.id}"
        )
