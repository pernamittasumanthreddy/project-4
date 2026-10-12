"""
Notification Center Views (Member 7).
Provides in-app notification inbox, real-time unread count badges, and mark-as-read state.
"""

from datetime import datetime
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.notifications.models import Notification, DeliveryLog
from apps.notifications.serializers import NotificationSerializer, DeliveryLogSerializer
from apps.core.models import User

class NotificationListView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            # Fall back to user specified by query or default patient for demo
            username = request.query_params.get('username')
            if username:
                user = User.objects.filter(username=username).first()
            if not user:
                user = User.objects.filter(role='PATIENT').first()

        qs = Notification.objects.filter(recipient=user).select_related('recipient').prefetch_related('delivery_logs')

        category = request.query_params.get('category')
        if category:
            qs = qs.filter(category=category.upper())

        is_read_param = request.query_params.get('is_read')
        if is_read_param is not None:
            is_read_bool = is_read_param.lower() in ('true', '1')
            qs = qs.filter(is_read=is_read_bool)

        unread_count = Notification.objects.filter(recipient=user, is_read=False).count()

        serializer = NotificationSerializer(qs[:50], many=True)
        return Response({
            "recipient_id": str(user.id) if user else None,
            "recipient_username": user.username if user else "anonymous",
            "unread_count": unread_count,
            "total_count": qs.count(),
            "notifications": serializer.data
        })


class NotificationUnreadCountView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            username = request.query_params.get('username')
            user = User.objects.filter(username=username).first() if username else User.objects.filter(role='PATIENT').first()

        unread_count = Notification.objects.filter(recipient=user, is_read=False).count() if user else 0
        return Response({"unread_count": unread_count})


class NotificationMarkReadView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        notification = Notification.objects.filter(id=pk).first()
        if not notification:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        from django.utils import timezone
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

        return Response({
            "success": True,
            "message": "Notification marked as read.",
            "notification": NotificationSerializer(notification).data
        })


class NotificationMarkAllReadView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.utils import timezone
        user = request.user
        if not user or not user.is_authenticated:
            username = request.data.get('username')
            user = User.objects.filter(username=username).first() if username else User.objects.filter(role='PATIENT').first()

        if user:
            updated_count = Notification.objects.filter(recipient=user, is_read=False).update(
                is_read=True,
                read_at=timezone.now()
            )

        else:
            updated_count = 0

        return Response({
            "success": True,
            "message": f"{updated_count} notifications marked as read.",
            "updated_count": updated_count
        })


class DeliveryLogListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DeliveryLogSerializer
    queryset = DeliveryLog.objects.all()[:100]
