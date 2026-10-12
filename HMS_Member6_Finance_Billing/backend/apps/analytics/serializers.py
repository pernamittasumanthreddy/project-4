from rest_framework import serializers
from .models import FinancialAuditEvent

class FinancialAuditEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAuditEvent
        fields = [
            'id', 'actor_username', 'action_type', 'entity_name', 'entity_id',
            'summary', 'changes_json', 'ip_address', 'created_at'
        ]
