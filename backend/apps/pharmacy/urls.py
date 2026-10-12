from django.urls import path
from apps.pharmacy import views

urlpatterns = [
    path('medications/', views.MedicationListView.as_view(), name='medications-list'),
    path('dispenses/', views.DispensingOrderListView.as_view(), name='dispenses-list'),
    path('dispensing-orders/', views.DispensingOrderListView.as_view(), name='dispensing-orders-list'),
]
