"""
Test Suite: Notification Center & Delivery Adapters (Member 7).
Covers in-app inbox, unread badges, deduplication, and safe email/SMS adapters.
"""

from django.test import TestCase, Client
from apps.core.models import Tenant, User
from apps.notifications.models import Notification, DeliveryLog
from apps.notifications.services import NotificationDispatcher

class NotificationsTestCase(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="CareTrust", slug="caretrust", domain="caretrust.local")
        self.user = User.objects.create(username="patient_priya", tenant=self.tenant, role="PATIENT", email="priya@test.local", phone="+1-617-555-8834")
        self.client = Client()

    def test_notification_dispatch_and_inbox_retrieval(self):
        """NotificationDispatcher dispatches in-app and delivery logs."""
        notif = NotificationDispatcher.dispatch(
            tenant=self.tenant,
            recipient=self.user,
            category='APPOINTMENT',
            title='Appointment Confirmed',
            message='Your appointment with Dr. Sophia Chen is scheduled.',
            action_url='/patient/appointments'
        )
        self.assertIsNotNone(notif)
        self.assertEqual(notif.is_read, False)

        # Check in-app inbox
        resp = self.client.get('/api/v1/notifications/', HTTP_X_IMPERSONATE_USER='patient_priya')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['unread_count'], 1)
        self.assertEqual(len(resp.data['notifications']), 1)
        self.assertEqual(resp.data['notifications'][0]['title'], 'Appointment Confirmed')

        # Check multi-channel delivery logs (IN_APP, EMAIL, SMS)
        logs = DeliveryLog.objects.filter(notification=notif)
        self.assertTrue(logs.filter(channel='IN_APP').exists())
        self.assertTrue(logs.filter(channel='EMAIL').exists())
        self.assertTrue(logs.filter(channel='SMS').exists())

    def test_deduplication_prevents_duplicate_notifications(self):
        """Dispatches with identical dedup_key return existing notification without duplicating."""
        key = "unique_event_hash_12345"
        notif1 = NotificationDispatcher.dispatch(
            tenant=self.tenant,
            recipient=self.user,
            category='BILLING',
            title='Invoice Created',
            message='Invoice #INV-001 has been generated.',
            dedup_key=key
        )
        notif2 = NotificationDispatcher.dispatch(
            tenant=self.tenant,
            recipient=self.user,
            category='BILLING',
            title='Invoice Created',
            message='Invoice #INV-001 has been generated.',
            dedup_key=key
        )
        self.assertEqual(notif1.id, notif2.id)
        self.assertEqual(Notification.objects.filter(recipient=self.user).count(), 1)

    def test_mark_as_read_and_mark_all_read(self):
        """Verifies state updates for reading notifications."""
        n1 = NotificationDispatcher.dispatch(self.tenant, self.user, 'SYSTEM', 'Notice 1', 'Msg 1', dedup_key="n1")
        n2 = NotificationDispatcher.dispatch(self.tenant, self.user, 'SYSTEM', 'Notice 2', 'Msg 2', dedup_key="n2")

        # Mark n1 read
        resp1 = self.client.post(f'/api/v1/notifications/{n1.id}/read/')
        self.assertEqual(resp1.status_code, 200)
        n1.refresh_from_db()
        self.assertTrue(n1.is_read)

        # Check unread count
        count_resp = self.client.get('/api/v1/notifications/unread-count/', HTTP_X_IMPERSONATE_USER='patient_priya')
        self.assertEqual(count_resp.data['unread_count'], 1)

        # Mark all read
        resp_all = self.client.post('/api/v1/notifications/mark-all-read/', HTTP_X_IMPERSONATE_USER='patient_priya')
        self.assertEqual(resp_all.status_code, 200)
        self.assertEqual(Notification.objects.filter(recipient=self.user, is_read=False).count(), 0)
