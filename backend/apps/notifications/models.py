import uuid
from django.db import models
from django.conf import settings
from apps.core.models import TenantScopedModel

class Notification(TenantScopedModel):
    """
    Centralized In-App & Multi-Channel Notification for Patients and Doctors.
    Includes deduplication guardrails and sanitized non-HIPAA-leaking messages.
    """
    CATEGORY_CHOICES = (
        ('APPOINTMENT', 'Appointment Updates & Reminders'),
        ('CLINICAL', 'Clinical Summaries & Encounters'),
        ('LAB_REPORT', 'Laboratory Investigation Results'),
        ('RADIOLOGY', 'Radiology & Imaging Reports'),
        ('PRESCRIPTION', 'Prescription & Pharmacy Updates'),
        ('BILLING', 'Invoices & Payment Confirmations'),
        ('TELEMEDICINE', 'Virtual Consultation Invitations'),
        ('ANNOUNCEMENT', 'Hospital Announcements'),
        ('SYSTEM', 'System & Security Alerts'),
    )

    PRIORITY_CHOICES = (
        ('LOW', 'Low Priority'),
        ('NORMAL', 'Standard Priority'),
        ('HIGH', 'High Priority'),
        ('URGENT', 'Urgent Clinical Alert'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='APPOINTMENT')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='NORMAL')
    title = models.CharField(max_length=255)
    message = models.TextField(help_text="Sanitized, minimal notification body directing user to secure portal")
    action_url = models.CharField(max_length=255, blank=True, help_text="In-app route e.g. /portal/appointments")
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    event_dedup_key = models.CharField(max_length=120, blank=True, null=True, db_index=True, help_text="Unique event hash preventing duplicate notifications")
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['tenant', 'category']),
        ]

    def __str__(self):
        status = "READ" if self.is_read else "UNREAD"
        return f"[{self.get_category_display()}] {self.title} -> {self.recipient.username} ({status})"


class DeliveryLog(models.Model):
    """
    Delivery lifecycle audit for multi-channel notification dispatching.
    Tracks In-App, Email, and SMS simulation states without external credentials.
    """
    CHANNEL_CHOICES = (
        ('IN_APP', 'In-App Portal Notification'),
        ('EMAIL', 'Electronic Mail (Email)'),
        ('SMS', 'Short Message Service (SMS)'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending Delivery'),
        ('DELIVERED', 'Delivered Successfully'),
        ('SIMULATED', 'Simulated via Dev Adapter'),
        ('FAILED', 'Delivery Failed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='delivery_logs')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DELIVERED')
    destination = models.CharField(max_length=200, help_text="Target email or masked phone number")
    attempt_count = models.PositiveIntegerField(default=1)
    payload_preview = models.TextField(blank=True)
    delivered_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-delivered_at']

    def __str__(self):
        return f"{self.channel} -> {self.destination} [{self.status}]"
