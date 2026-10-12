from django.db import models
from apps.common.models import TenantScopedModel

class FinancialAuditEvent(TenantScopedModel):
    """
    Append-only immutable financial audit trail.
    Tracks every invoice change, payment received, refund approval, and manual journal edit.
    """
    actor_username = models.CharField(max_length=150)
    action_type = models.CharField(max_length=60, help_text="e.g. INVOICE_ISSUED, PAYMENT_RECEIVED, REFUND_APPROVED, PERIOD_CLOSED")
    entity_name = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100)
    summary = models.TextField()
    changes_json = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at}] {self.actor_username}: {self.action_type} on {self.entity_name} ({self.entity_id})"
