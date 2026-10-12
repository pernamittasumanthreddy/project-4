"""HMS Pharmacy Django Admin Registration — Member 5"""

from django.contrib import admin
from pharmacy.models import (
    Medicine,
    MedicineCategory,
    Supplier,
    StorageLocation,
    MedicineBatch,
    PurchaseOrder,
    PurchaseOrderItem,
    GoodsReceipt,
    GoodsReceiptItem,
    DispenseRecord,
    DispensedItem,
    PatientReturn,
    SupplierReturn,
    StockQuarantine,
    StockCountSession,
    StockCountItem,
    StockMovement,
)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('code', 'brand_name', 'generic_name', 'strength', 'dosage_form', 'reorder_level', 'tenant')
    search_fields = ('code', 'brand_name', 'generic_name', 'barcode_sku')
    list_filter = ('dosage_form', 'classification', 'requires_prescription', 'tenant')


@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'batch_number', 'expiry_date', 'available_quantity', 'status', 'branch')
    list_filter = ('status', 'expiry_date', 'branch')
    search_fields = ('batch_number', 'medicine__brand_name')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'contact_person', 'phone', 'email', 'tenant')
    search_fields = ('code', 'name', 'contact_person')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'status', 'total_amount', 'order_date', 'branch')
    list_filter = ('status', 'order_date', 'branch')


@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'purchase_order', 'delivery_reference', 'received_date', 'received_by')


@admin.register(DispenseRecord)
class DispenseRecordAdmin(admin.ModelAdmin):
    list_display = ('dispense_number', 'prescription', 'pharmacist', 'total_amount', 'created_at')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'medicine', 'batch', 'movement_type', 'quantity_change', 'quantity_after', 'actor')
    list_filter = ('movement_type', 'created_at')


admin.site.register(MedicineCategory)
admin.site.register(StorageLocation)
admin.site.register(PatientReturn)
admin.site.register(SupplierReturn)
admin.site.register(StockQuarantine)
admin.site.register(StockCountSession)
