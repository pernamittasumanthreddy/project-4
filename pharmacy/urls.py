"""HMS Pharmacy REST API URLs — Member 5"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pharmacy.views.api_views import (
    MedicineCategoryViewSet,
    MedicineViewSet,
    SupplierViewSet,
    StorageLocationViewSet,
    MedicineBatchViewSet,
    PurchaseOrderViewSet,
    GoodsReceiptViewSet,
    DispenseViewSet,
    PatientReturnViewSet,
    SupplierReturnViewSet,
    StockQuarantineViewSet,
    StockCountSessionViewSet,
    AlertsView,
    ReportsView,
)

router = DefaultRouter()
router.register('categories', MedicineCategoryViewSet, basename='pharmacy_categories')
router.register('medicines', MedicineViewSet, basename='pharmacy_medicines')
router.register('suppliers', SupplierViewSet, basename='pharmacy_suppliers')
router.register('storage-locations', StorageLocationViewSet, basename='pharmacy_locations')
router.register('batches', MedicineBatchViewSet, basename='pharmacy_batches')
router.register('purchase-orders', PurchaseOrderViewSet, basename='pharmacy_orders')
router.register('goods-receipts', GoodsReceiptViewSet, basename='pharmacy_receipts')
router.register('dispensations', DispenseViewSet, basename='pharmacy_dispensations')
router.register('patient-returns', PatientReturnViewSet, basename='pharmacy_patient_returns')
router.register('supplier-returns', SupplierReturnViewSet, basename='pharmacy_supplier_returns')
router.register('quarantines', StockQuarantineViewSet, basename='pharmacy_quarantines')
router.register('reconciliations', StockCountSessionViewSet, basename='pharmacy_reconciliations')

urlpatterns = [
    path('', include(router.urls)),
    path('alerts/', AlertsView.as_view(), name='pharmacy_api_alerts'),
    path('reports/', ReportsView.as_view(), name='pharmacy_api_reports'),
]
