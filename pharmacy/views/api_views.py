"""HMS Pharmacy API ViewSets — Member 5
Implements DRF endpoints for Catalogue, Inventory, Purchasing, Dispensing, Returns, and Audits.
"""

from datetime import date
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse


from core.permissions import HasTenantAccess, record_audit_event
from pharmacy.permissions import (
    IsPharmacistOrAdmin,
    IsInventoryManagerOrAdmin,
    CanApprovePurchaseOrder,
    CanDispensePrescription,
)
from pharmacy.models import (
    Medicine,
    MedicineCategory,
    Supplier,
    StorageLocation,
    MedicineBatch,
    PurchaseOrder,
    PurchaseOrderItem,
    GoodsReceipt,
    DispenseRecord,
    PatientReturn,
    SupplierReturn,
    StockQuarantine,
    StockCountSession,
    StockCountItem,
    StockMovement,
)
from pharmacy.serializers import (
    MedicineSerializer,
    MedicineCategorySerializer,
    SupplierSerializer,
    StorageLocationSerializer,
    MedicineBatchSerializer,
    PurchaseOrderSerializer,
    GoodsReceiptSerializer,
    DispenseRecordSerializer,
    PatientReturnSerializer,
    SupplierReturnSerializer,
    StockQuarantineSerializer,
    StockCountSessionSerializer,
)
from pharmacy.services.purchasing_service import PurchasingService
from pharmacy.services.dispensing_service import DispensingService
from pharmacy.services.returns_service import ReturnsService
from pharmacy.services.reconciliation_service import ReconciliationService
from pharmacy.services.alert_service import AlertService
from pharmacy.services.report_service import ReportService
from clinical.models import Prescription


class BaseTenantViewSet(viewsets.ModelViewSet):
    """Base ViewSet automatically scoping queries and mutations to the request tenant."""
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = self.queryset.filter(tenant=tenant)
        branch = getattr(self.request, 'branch', None)
        if branch and hasattr(self.model, 'branch'):
            # Allow branch filtering if model supports branch
            pass
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        branch = getattr(self.request, 'branch', None)
        kwargs = {'tenant': tenant}
        if hasattr(serializer.Meta.model, 'branch'):
            kwargs['branch'] = branch
        serializer.save(**kwargs)


class MedicineCategoryViewSet(BaseTenantViewSet):
    model = MedicineCategory
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsPharmacistOrAdmin]


class MedicineViewSet(BaseTenantViewSet):
    model = Medicine
    queryset = Medicine.objects.filter(is_deleted=False)
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsPharmacistOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                models.Q(brand_name__icontains=search) |
                models.Q(generic_name__icontains=search) |
                models.Q(code__icontains=search)
            )
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category_id=category)
        return qs

    def perform_destroy(self, instance):
        # Soft-delete preserving historical dispensing records
        instance.is_deleted = True
        instance.is_active = False
        instance.save(update_fields=['is_deleted', 'is_active'])


class SupplierViewSet(BaseTenantViewSet):
    model = Supplier
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsInventoryManagerOrAdmin]


class StorageLocationViewSet(BaseTenantViewSet):
    model = StorageLocation
    queryset = StorageLocation.objects.all()
    serializer_class = StorageLocationSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsInventoryManagerOrAdmin]


class MedicineBatchViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only batch inspection viewset with filtering by status and expiration."""
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess]
    serializer_class = MedicineBatchSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        branch = getattr(self.request, 'branch', None)
        qs = MedicineBatch.objects.filter(tenant=tenant)
        if branch:
            qs = qs.filter(branch=branch)
        med_id = self.request.query_params.get('medicine')
        if med_id:
            qs = qs.filter(medicine_id=med_id)
        batch_status = self.request.query_params.get('status')
        if batch_status:
            qs = qs.filter(status=batch_status)
        return qs.order_by('expiry_date')


class PurchaseOrderViewSet(BaseTenantViewSet):
    model = PurchaseOrder
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsInventoryManagerOrAdmin]

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        branch = getattr(self.request, 'branch', None)
        # Generate PO order number
        count = PurchaseOrder.objects.filter(tenant=tenant).count() + 1
        num = f"PO-{branch.code if branch else 'HQ'}-{date.today().year}-{count:04d}"
        serializer.save(tenant=tenant, branch=branch, order_number=num, created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        po = self.get_object()
        updated_po = PurchasingService.submit_purchase_order(po, request.user)
        return Response({'success': True, 'data': PurchaseOrderSerializer(updated_po).data})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, CanApprovePurchaseOrder])
    def approve(self, request, pk=None):
        po = self.get_object()
        updated_po = PurchasingService.approve_purchase_order(po, request.user)
        return Response({'success': True, 'data': PurchaseOrderSerializer(updated_po).data})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, CanApprovePurchaseOrder])
    def reject(self, request, pk=None):
        po = self.get_object()
        reason = request.data.get('reason', '')
        updated_po = PurchasingService.reject_purchase_order(po, request.user, reason)
        return Response({'success': True, 'data': PurchaseOrderSerializer(updated_po).data})

    @action(detail=True, methods=['post'])
    def receive_goods(self, request, pk=None):
        po = self.get_object()
        delivery_ref = request.data.get('delivery_reference', 'DEL-DIRECT')
        items_payload = request.data.get('items', [])
        notes = request.data.get('notes', '')
        grn = PurchasingService.process_goods_receipt(
            po=po,
            delivery_reference=delivery_ref,
            items_payload=items_payload,
            receiver=request.user,
            notes=notes
        )
        return Response({'success': True, 'data': GoodsReceiptSerializer(grn).data})


class GoodsReceiptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GoodsReceiptSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        return GoodsReceipt.objects.filter(tenant=tenant).order_by('-created_at')


class DispenseViewSet(viewsets.ModelViewSet):
    serializer_class = DispenseRecordSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, CanDispensePrescription]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        return DispenseRecord.objects.filter(tenant=tenant).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        prescription_id = request.data.get('prescription_id')
        items_payload = request.data.get('items', None)
        notes = request.data.get('notes', '')

        prescription = Prescription.objects.get(id=prescription_id, tenant=request.tenant)
        dispense_record = DispensingService.dispense_prescription(
            prescription=prescription,
            pharmacist=request.user,
            dispense_items_payload=items_payload,
            notes=notes
        )
        return Response(
            {'success': True, 'data': DispenseRecordSerializer(dispense_record).data},
            status=status.HTTP_201_CREATED
        )


class PatientReturnViewSet(BaseTenantViewSet):
    model = PatientReturn
    queryset = PatientReturn.objects.all()
    serializer_class = PatientReturnSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsPharmacistOrAdmin]

    def create(self, request, *args, **kwargs):
        dispense_id = request.data.get('dispense_record_id')
        dispensed_item_id = request.data.get('dispensed_item_id')
        qty = request.data.get('quantity_returned')
        condition = request.data.get('condition')
        reason = request.data.get('reason')

        dispense_record = DispenseRecord.objects.get(id=dispense_id, tenant=request.tenant)
        ret = ReturnsService.process_patient_return(
            dispense_record=dispense_record,
            dispensed_item_id=dispensed_item_id,
            quantity_returned=qty,
            condition=condition,
            reason=reason,
            received_by=request.user
        )
        return Response(
            {'success': True, 'data': PatientReturnSerializer(ret).data},
            status=status.HTTP_201_CREATED
        )


class SupplierReturnViewSet(BaseTenantViewSet):
    model = SupplierReturn
    queryset = SupplierReturn.objects.all()
    serializer_class = SupplierReturnSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsInventoryManagerOrAdmin]

    def create(self, request, *args, **kwargs):
        batch_id = request.data.get('batch_id')
        supplier_id = request.data.get('supplier_id')
        qty = request.data.get('quantity')
        reason = request.data.get('reason')

        batch = MedicineBatch.objects.get(id=batch_id, tenant=request.tenant)
        supplier = Supplier.objects.get(id=supplier_id, tenant=request.tenant)

        ret = ReturnsService.process_supplier_return(
            batch=batch,
            supplier=supplier,
            quantity=qty,
            reason=reason,
            authorized_by=request.user
        )
        return Response(
            {'success': True, 'data': SupplierReturnSerializer(ret).data},
            status=status.HTTP_201_CREATED
        )


class StockQuarantineViewSet(viewsets.ModelViewSet):
    serializer_class = StockQuarantineSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsPharmacistOrAdmin]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        return StockQuarantine.objects.filter(tenant=tenant).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        quarantine = self.get_object()
        resolution = request.data.get('resolution')
        notes = request.data.get('resolution_notes', '')
        resolved = ReturnsService.resolve_quarantine(
            quarantine=quarantine,
            resolution=resolution,
            resolution_notes=notes,
            resolver=request.user
        )
        return Response({'success': True, 'data': StockQuarantineSerializer(resolved).data})


class StockCountSessionViewSet(BaseTenantViewSet):
    model = StockCountSession
    queryset = StockCountSession.objects.all()
    serializer_class = StockCountSessionSerializer
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess, IsInventoryManagerOrAdmin]

    def create(self, request, *args, **kwargs):
        loc_id = request.data.get('storage_location_id', None)
        loc = StorageLocation.objects.filter(id=loc_id).first() if loc_id else None
        session = ReconciliationService.start_session(
            branch=request.branch,
            location=loc,
            initiated_by=request.user
        )
        return Response(
            {'success': True, 'data': StockCountSessionSerializer(session).data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def update_count(self, request, pk=None):
        session = self.get_object()
        item_id = request.data.get('item_id')
        count_val = request.data.get('counted_quantity')
        reason = request.data.get('reason', '')
        item = StockCountItem.objects.get(id=item_id, session=session)
        updated_item = ReconciliationService.update_item_count(item, count_val, reason)
        return Response({'success': True, 'item_discrepancy': str(updated_item.discrepancy_quantity)})

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        session = self.get_object()
        sub = ReconciliationService.submit_session_for_review(session, request.user)
        return Response({'success': True, 'data': StockCountSessionSerializer(sub).data})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, CanApprovePurchaseOrder])
    def approve(self, request, pk=None):
        session = self.get_object()
        appr = ReconciliationService.approve_session_and_post_adjustments(session, request.user)
        return Response({'success': True, 'data': StockCountSessionSerializer(appr).data})


class AlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess]

    def get(self, request):
        alerts = AlertService.get_alerts_summary(request.tenant, request.branch)
        low_stock = AlertService.get_low_stock_medicines(request.tenant, request.branch)
        return Response({
            'success': True,
            'summary': alerts,
            'low_stock_medicines': low_stock
        })


class ReportsView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantAccess]

    def get(self, request):
        export_type = request.query_params.get('export')
        if export_type == 'csv':
            csv_data = ReportService.generate_stock_csv(request.tenant, request.branch)
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="inventory_audit_{date.today()}.csv"'
            return response
        elif export_type == 'pdf':
            pdf_data = ReportService.generate_stock_pdf(request.tenant, request.branch)
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="inventory_report_{date.today()}.pdf"'
            return response

        valuation = ReportService.get_stock_valuation(request.tenant, request.branch)
        return Response({'success': True, 'valuation': valuation})
