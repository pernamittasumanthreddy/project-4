from django.urls import path
from apps.core import views

urlpatterns = [
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('switch-role/', views.DemoRoleSwitcherView.as_view(), name='demo-switch-role'),
    path('demo-personas/', views.AvailableDemoUsersView.as_view(), name='demo-personas'),
    path('tenants/', views.TenantListView.as_view(), name='tenants-list'),
    path('branches/', views.HospitalBranchListView.as_view(), name='branches-list'),
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit-logs-list'),
]
