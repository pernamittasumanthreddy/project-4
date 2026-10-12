"""HMS Pharmacy Views Package"""
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
from pharmacy.views.ui_views import (
    pharmacy_dashboard,
    medicine_catalogue,
    batch_management,
    dispensing_queue,
    purchasing_management,
    returns_and_quarantine,
    reconciliation_dashboard,
    reports_dashboard,
)
