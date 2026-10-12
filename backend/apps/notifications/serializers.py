from rest_framework import serializers
from apps.notifications.models import Notification, DeliveryLog

class DeliveryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLog
        fields = ['id', 'channel', 'status', 'destination', 'attempt_count', 'payload_preview', 'delivered_at', 'error_message']


class NotificationSerializer(serializers.ModelSerializer):
    delivery_logs = DeliveryLogSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'category', 'category_display',
            'priority', 'priority_display', 'title', 'message',
            'action_url', 'is_read', 'read_at', 'event_dedup_key',
            'metadata', 'delivery_logs', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
