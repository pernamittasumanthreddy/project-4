from django.urls import path
from apps.notifications import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications-list'),
    path('unread-count/', views.NotificationUnreadCountView.as_view(), name='notifications-unread-count'),
    path('<uuid:pk>/read/', views.NotificationMarkReadView.as_view(), name='notifications-mark-read'),
    path('mark-all-read/', views.NotificationMarkAllReadView.as_view(), name='notifications-mark-all-read'),
    path('delivery-logs/', views.DeliveryLogListView.as_view(), name='notifications-delivery-logs'),
]
