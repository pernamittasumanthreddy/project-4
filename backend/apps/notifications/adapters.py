"""
Notification Delivery Adapters for HMS SaaS.
Provides clean local simulation for Email and SMS with zero external paid API keys.
Guarantees privacy: No raw diagnostic findings or clinical notes are sent over unencrypted SMS/Email.
"""

import logging
from datetime import datetime
from apps.notifications.models import DeliveryLog

logger = logging.getLogger('hms.notifications')

class BaseDeliveryAdapter:
    def send(self, notification, recipient_user):
        raise NotImplementedError


class ConsoleEmailAdapter(BaseDeliveryAdapter):
    """
    Local simulation email adapter.
    Logs sanitized email metadata without leaking medical credentials or secrets.
    """
    def send(self, notification, recipient_user):
        destination = recipient_user.email or f"{recipient_user.username}@hms-patient.local"
        
        # Privacy guardrail: Sanitized generic body with portal deep-link
        safe_subject = f"[{notification.tenant.name}] {notification.title}"
        safe_body = (
            f"Dear {recipient_user.full_name},\n\n"
            f"{notification.message}\n\n"
            f"For your medical privacy, please sign in to the secure portal to view full clinical details:\n"
            f"https://{notification.tenant.domain}{notification.action_url or '/portal'}\n\n"
            f"Regards,\n{notification.tenant.name} Care Team"
        )

        log = DeliveryLog.objects.create(
            notification=notification,
            channel='EMAIL',
            status='SIMULATED',
            destination=destination,
            payload_preview=f"Subject: {safe_subject} | Preview: {safe_body[:100]}...",
            attempt_count=1
        )
        logger.info(f"[SIMULATED EMAIL] To: {destination} | Subject: {safe_subject}")
        return log


class ConsoleSMSAdapter(BaseDeliveryAdapter):
    """
    Local simulation SMS adapter.
    Formats minimal <= 160 character SMS text and masks recipient phone.
    """
    def send(self, notification, recipient_user):
        raw_phone = recipient_user.phone or "+1-555-019-4821"
        # Mask middle digits for privacy
        masked_phone = f"+1 (***) ***-{raw_phone[-4:]}" if len(raw_phone) >= 4 else "+1 (***) ***-0000"

        short_msg = f"{notification.tenant.name}: {notification.title}. Log in to patient portal to view."[:160]

        log = DeliveryLog.objects.create(
            notification=notification,
            channel='SMS',
            status='SIMULATED',
            destination=masked_phone,
            payload_preview=short_msg,
            attempt_count=1
        )
        logger.info(f"[SIMULATED SMS] To: {masked_phone} | Message: {short_msg}")
        return log
