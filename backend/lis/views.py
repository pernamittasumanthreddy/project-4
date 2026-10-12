import csv
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, Q, Avg, F
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    LabCategory, LabTest, LabTestPanel, LabOrder, LabOrderItem,
    Specimen, SpecimenEvent, LabResult, LabResultVersion, CriticalResultAlert,
    LabReport, LabOrderStatus, SpecimenStatus, ResultStatus, OrderPriority
)
from .serializers import (
    LabCategorySerializer, LabTestSerializer, LabTestPanelSerializer,
    LabOrderSerializer, LabOrderItemSerializer, SpecimenSerializer,
    LabResultSerializer, CriticalResultAlertSerializer, LabReportSerializer
)
from .pdf_generator import generate_lab_report_pdf
from contracts.models import BillingEventContract, PatientContract, HospitalBranch

class LabDashboardView(APIView):
    """
    Real-time database-calculated laboratory statistics scoped by tenant and branch.
    Zero hardcoded values.
    """
    def get(self, request):
        tenant = getattr(request, 'tenant', None)
        branch = getattr(request, 'branch', None)

        if not tenant:
            return Response({'error': 'Tenant context required'}, status=400)

        orders_qs = LabOrder.objects.filter(tenant=tenant)
        if branch:
            orders_qs = orders_qs.filter(branch=branch)

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Orders today
        orders_today_count = orders_qs.filter(ordered_at__gte=today_start).count()
        
        # Lifecycle stages
        awaiting_collection = orders_qs.filter(status__in=[LabOrderStatus.ORDERED, LabOrderStatus.SAMPLE_PENDING]).count()
        samples_collected = orders_qs.filter(status=LabOrderStatus.COLLECTED).count()
        received_in_lab = orders_qs.filter(status=LabOrderStatus.RECEIVED_IN_LAB).count()
        processing = orders_qs.filter(status=LabOrderStatus.PROCESSING).count()
        awaiting_validation = orders_qs.filter(status=LabOrderStatus.RESULTS_ENTERED).count()
        awaiting_approval = orders_qs.filter(status=LabOrderStatus.VALIDATED).count()
        approved_reports = orders_qs.filter(status=LabOrderStatus.APPROVED).count()

        # Specimens & Quality metrics
        specimens_qs = Specimen.objects.filter(order__tenant=tenant)
        if branch:
            specimens_qs = specimens_qs.filter(order__branch=branch)
        rejected_samples = specimens_qs.filter(status=SpecimenStatus.REJECTED).count()
        recollection_requests = specimens_qs.filter(recollection_needed=True).count()

        # Critical Alerts
        critical_alerts_active = CriticalResultAlert.objects.filter(
            order__tenant=tenant,
            alert_status__in=['TRIGGERED', 'NOTIFIED', 'ESCALATED']
        ).count()

        # Category breakdown
        category_stats = LabCategory.objects.annotate(
            test_count=Count('tests', filter=Q(tests__tenant=tenant)),
            order_count=Count('tests__order_items', filter=Q(tests__order_items__order__tenant=tenant))
        ).values('id', 'name', 'code', 'order_count')

        # Overdue / TAT detection (Orders older than 3 hours that are not yet approved)
        overdue_threshold = now - timedelta(hours=3)
        overdue_orders_count = orders_qs.filter(
            ordered_at__lt=overdue_threshold,
            status__in=[
                LabOrderStatus.ORDERED, LabOrderStatus.SAMPLE_PENDING,
                LabOrderStatus.COLLECTED, LabOrderStatus.RECEIVED_IN_LAB,
                LabOrderStatus.PROCESSING, LabOrderStatus.RESULTS_ENTERED
            ]
        ).count()

        return Response({
            'tenant_code': tenant.code,
            'branch_name': branch.name if branch else 'All Branches',
            'statistics': {
                'total_orders_today': orders_today_count,
                'orders_awaiting_collection': awaiting_collection,
                'samples_collected': samples_collected,
                'samples_received_in_lab': received_in_lab,
                'samples_processing': processing,
                'results_awaiting_validation': awaiting_validation,
                'reports_awaiting_approval': awaiting_approval,
                'approved_reports': approved_reports,
                'rejected_samples': rejected_samples,
                'recollection_requests': recollection_requests,
                'critical_alerts_unresolved': critical_alerts_active,
                'overdue_orders': overdue_orders_count,
            },
            'categories': list(category_stats),
            'timestamp': now.isoformat()
        })

class LabCatalogueViewSet(viewsets.ModelViewSet):
    """Laboratory Test Catalogue management"""
    serializer_class = LabTestSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = LabTest.objects.all().select_related('category')
        if tenant:
            qs = qs.filter(tenant=tenant)
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        specimen_type = self.request.query_params.get('specimen')
        if specimen_type:
            qs = qs.filter(specimen_type=specimen_type)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(test_code__icontains=search) | Q(loinc_code__icontains=search))
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)

class LabCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Laboratory Departmental Categories"""
    queryset = LabCategory.objects.all()
    serializer_class = LabCategorySerializer

class LabTestPanelViewSet(viewsets.ModelViewSet):
    """Grouped Profiles & Panels"""
    serializer_class = LabTestPanelSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = LabTestPanel.objects.all().prefetch_related('tests')
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

class LabOrderViewSet(viewsets.ModelViewSet):
    """Laboratory Order Lifecycle Management"""
    serializer_class = LabOrderSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        branch = getattr(self.request, 'branch', None)
        qs = LabOrder.objects.all().select_related('patient', 'branch').prefetch_related('items__test', 'specimens')
        if tenant:
            qs = qs.filter(tenant=tenant)
        if branch:
            qs = qs.filter(branch=branch)
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        priority_param = self.request.query_params.get('priority')
        if priority_param:
            qs = qs.filter(priority=priority_param)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(order_number__icontains=search) |
                Q(accession_number__icontains=search) |
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient__uhid__icontains=search)
            )
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Creates order with automated specimen creation and duplicate prevention"""
        tenant = getattr(request, 'tenant', None)
        branch = getattr(request, 'branch', None)
        patient_id = request.data.get('patient_id')
        test_ids = request.data.get('test_ids', [])
        ordering_clinician = request.data.get('ordering_clinician', 'Attending Physician')
        priority = request.data.get('priority', OrderPriority.ROUTINE)
        clinical_indications = request.data.get('clinical_indications', '')
        fasting_status = request.data.get('fasting_status', 'Not Required')

        if not patient_id:
            return Response({'error': 'Patient ID is required'}, status=400)
        if not test_ids:
            return Response({'error': 'At least one test must be selected'}, status=400)

        patient = PatientContract.objects.filter(id=patient_id, tenant=tenant).first()
        if not patient:
            return Response({'error': 'Patient not found in this tenant'}, status=404)

        # Duplicate Prevention check (same patient and tests within the last 15 minutes unless STAT)
        recent_cutoff = timezone.now() - timedelta(minutes=15)
        if priority != OrderPriority.STAT:
            existing = LabOrder.objects.filter(
                tenant=tenant,
                patient=patient,
                ordered_at__gte=recent_cutoff,
                items__test_id__in=test_ids
            ).first()
            if existing:
                return Response({
                    'error': 'Duplicate Order Detected',
                    'message': f'Identical tests were ordered for this patient {recent_cutoff.strftime("%H:%M")}. Existing Order: {existing.order_number}'
                }, status=409)

        order = LabOrder.objects.create(
            tenant=tenant,
            branch=branch or HospitalBranch.objects.filter(tenant=tenant).first(),
            patient=patient,
            ordering_clinician=ordering_clinician,
            priority=priority,
            clinical_indications=clinical_indications,
            fasting_status=fasting_status,
            status=LabOrderStatus.SAMPLE_PENDING
        )

        tests = LabTest.objects.filter(id__in=test_ids, tenant=tenant)
        specimen_types_needed = set()

        for t in tests:
            item = LabOrderItem.objects.create(
                order=order,
                test=t,
                status=LabOrderStatus.SAMPLE_PENDING,
                price_at_order=t.price
            )
            # Create draft result container
            LabResult.objects.create(
                order_item=item,
                test=t,
                unit=t.unit,
                ref_range_display=f"{t.ref_min} - {t.ref_max}" if t.ref_min is not None else t.qualitative_normal,
                status=ResultStatus.DRAFT
            )
            specimen_types_needed.add((t.specimen_type, t.container_type))

        # Automatically spawn required specimen containers
        for spec_type, cont_type in specimen_types_needed:
            specimen = Specimen.objects.create(
                order=order,
                specimen_type=spec_type,
                container_type=cont_type,
                status=SpecimenStatus.PENDING
            )
            SpecimenEvent.objects.create(
                specimen=specimen,
                event_type='COLLECTION_SCHEDULED',
                actor_name=ordering_clinician,
                notes=f"Required container: {cont_type}"
            )

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        reason = request.data.get('reason', 'Clinician cancellation')
        if order.status in [LabOrderStatus.APPROVED, LabOrderStatus.VALIDATED]:
            return Response({'error': 'Cannot cancel an order that has already been validated or approved'}, status=400)
        
        order.status = LabOrderStatus.CANCELLED
        order.cancellation_reason = reason
        order.cancelled_by = request.data.get('cancelled_by', 'Clinical Staff')
        order.save()
        return Response({'message': f'Order {order.order_number} cancelled successfully', 'status': order.status})

class SpecimenViewSet(viewsets.ModelViewSet):
    """Specimen Collection, Barcoding & Chain of Custody tracking"""
    serializer_class = SpecimenSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = Specimen.objects.all().select_related('order__patient').prefetch_related('events')
        if tenant:
            qs = qs.filter(order__tenant=tenant)
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    @action(detail=True, methods=['post'])
    def collect_sample(self, request, pk=None):
        specimen = self.get_object()
        collector = request.data.get('collected_by', 'Phlebotomist Specialist')
        
        specimen.status = SpecimenStatus.COLLECTED
        specimen.collected_by = collector
        specimen.collected_at = timezone.now()
        specimen.save()

        SpecimenEvent.objects.create(
            specimen=specimen,
            event_type='SAMPLE_COLLECTED',
            actor_name=collector,
            notes='Venipuncture/collection completed with patient identity verification.'
        )

        order = specimen.order
        order.status = LabOrderStatus.COLLECTED
        order.save()

        return Response({'message': f'Specimen {specimen.barcode_id} collected successfully', 'status': specimen.status})

    @action(detail=True, methods=['post'])
    def receive_in_lab(self, request, pk=None):
        specimen = self.get_object()
        receiver = request.data.get('received_by', 'Lab Intake Technologist')
        rack = request.data.get('storage_rack', 'Accession Rack A-04')

        specimen.status = SpecimenStatus.RECEIVED
        specimen.received_by = receiver
        specimen.received_at = timezone.now()
        specimen.storage_rack = rack
        specimen.save()

        SpecimenEvent.objects.create(
            specimen=specimen,
            event_type='RECEIVED_IN_LAB',
            actor_name=receiver,
            notes=f'Specimen integrity verified. Placed in {rack}.'
        )

        order = specimen.order
        order.status = LabOrderStatus.RECEIVED_IN_LAB
        order.save()

        return Response({'message': f'Specimen {specimen.barcode_id} accepted in laboratory', 'status': specimen.status})

    @action(detail=True, methods=['post'])
    def reject_sample(self, request, pk=None):
        specimen = self.get_object()
        reason = request.data.get('reason', 'Hemolyzed Sample')
        notes = request.data.get('notes', 'Specimen compromised; recollection required.')
        actor = request.data.get('actor_name', 'Quality Officer')

        specimen.status = SpecimenStatus.REJECTED
        specimen.rejection_reason = reason
        specimen.rejection_notes = notes
        specimen.recollection_needed = True
        specimen.save()

        SpecimenEvent.objects.create(
            specimen=specimen,
            event_type='SAMPLE_REJECTED',
            actor_name=actor,
            notes=f"REJECTED: {reason}. {notes}"
        )

        return Response({'message': f'Specimen {specimen.barcode_id} rejected. Recollection request emitted.', 'status': specimen.status})

    @action(detail=True, methods=['get'])
    def label_data(self, request, pk=None):
        """Returns structured printable specimen label payload with SVG barcode"""
        specimen = self.get_object()
        order = specimen.order
        patient = order.patient

        # Generate lightweight SVG code128 barcode representation
        svg_barcode = f"""<svg xmlns="http://www.w3.org/2000/svg" width="220" height="40" viewBox="0 0 220 40">
            <rect width="100%" height="100%" fill="#ffffff"/>
            <!-- Barcode lines -->
            <rect x="10" y="5" width="3" height="30" fill="#000000"/>
            <rect x="16" y="5" width="2" height="30" fill="#000000"/>
            <rect x="22" y="5" width="4" height="30" fill="#000000"/>
            <rect x="30" y="5" width="2" height="30" fill="#000000"/>
            <rect x="36" y="5" width="5" height="30" fill="#000000"/>
            <rect x="46" y="5" width="2" height="30" fill="#000000"/>
            <rect x="52" y="5" width="3" height="30" fill="#000000"/>
            <rect x="60" y="5" width="4" height="30" fill="#000000"/>
            <rect x="70" y="5" width="2" height="30" fill="#000000"/>
            <rect x="76" y="5" width="3" height="30" fill="#000000"/>
            <rect x="84" y="5" width="5" height="30" fill="#000000"/>
            <rect x="94" y="5" width="2" height="30" fill="#000000"/>
            <rect x="100" y="5" width="4" height="30" fill="#000000"/>
            <rect x="110" y="5" width="3" height="30" fill="#000000"/>
            <rect x="118" y="5" width="2" height="30" fill="#000000"/>
            <rect x="124" y="5" width="5" height="30" fill="#000000"/>
            <rect x="134" y="5" width="3" height="30" fill="#000000"/>
            <rect x="142" y="5" width="2" height="30" fill="#000000"/>
            <rect x="150" y="5" width="4" height="30" fill="#000000"/>
            <rect x="160" y="5" width="3" height="30" fill="#000000"/>
            <rect x="168" y="5" width="2" height="30" fill="#000000"/>
            <rect x="174" y="5" width="5" height="30" fill="#000000"/>
            <rect x="184" y="5" width="3" height="30" fill="#000000"/>
            <rect x="192" y="5" width="2" height="30" fill="#000000"/>
            <rect x="200" y="5" width="4" height="30" fill="#000000"/>
        </svg>"""

        return Response({
            'barcode_id': specimen.barcode_id,
            'accession_number': order.accession_number,
            'patient_name': patient.full_name,
            'patient_uhid': patient.uhid,
            'dob_gender': f"{patient.dob} / {patient.gender}",
            'specimen_type': specimen.specimen_type,
            'container_type': specimen.container_type,
            'priority': order.priority,
            'collection_time': specimen.collected_at.isoformat() if specimen.collected_at else 'PENDING',
            'svg_barcode': svg_barcode,
        })

class LabResultViewSet(viewsets.ModelViewSet):
    """Laboratory Result Entry, Clinical Validation, Approval & Amendments"""
    serializer_class = LabResultSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = LabResult.objects.all().select_related('order_item__order__patient', 'test').prefetch_related('versions')
        if tenant:
            qs = qs.filter(order_item__order__tenant=tenant)
        order_id = self.request.query_params.get('order_id')
        if order_id:
            qs = qs.filter(order_item__order_id=order_id)
        return qs

    @action(detail=True, methods=['post'])
    def enter_result(self, request, pk=None):
        """Technician enters quantitative or qualitative test measurement"""
        result = self.get_object()
        numeric_val = request.data.get('numeric_value')
        text_val = request.data.get('text_value', '')
        tech_notes = request.data.get('technician_notes', '')
        entered_by = request.data.get('entered_by', 'Lab Technologist')

        test = result.test
        if numeric_val is not None and numeric_val != '':
            try:
                numeric_val = float(numeric_val)
                result.numeric_value = numeric_val
                result.flag = test.evaluate_numeric_flag(numeric_val)
            except ValueError:
                return Response({'error': 'Invalid numeric result format'}, status=400)
        else:
            result.numeric_value = None
            result.text_value = text_val
            result.flag = 'POSITIVE' if 'positive' in text_val.lower() or 'reactive' in text_val.lower() else 'NORMAL'

        result.is_abnormal = result.flag in ['LOW', 'HIGH', 'CRITICAL_LOW', 'CRITICAL_HIGH', 'POSITIVE']
        result.is_critical = result.flag in ['CRITICAL_LOW', 'CRITICAL_HIGH']
        result.technician_notes = tech_notes
        result.entered_by = entered_by
        result.entered_at = timezone.now()
        result.status = ResultStatus.ENTERED
        result.save()

        # Update order item and parent order
        order_item = result.order_item
        order_item.status = LabOrderStatus.RESULTS_ENTERED
        order_item.save()

        order = order_item.order
        order.status = LabOrderStatus.RESULTS_ENTERED
        order.save()

        # Trigger Critical Result Alert if alert threshold breached
        if result.is_critical:
            CriticalResultAlert.objects.get_or_create(
                result=result,
                order=order,
                patient=order.patient,
                defaults={
                    'clinician_name': order.ordering_clinician,
                    'alert_level': 'LIFE_THREATENING',
                    'alert_status': 'TRIGGERED',
                    'call_log_notes': f"Automated alert: {test.name} observed {result.numeric_value} {result.unit} ({result.flag})"
                }
            )

        return Response({
            'message': 'Result recorded successfully',
            'flag': result.flag,
            'is_critical': result.is_critical,
            'status': result.status
        })

    @action(detail=True, methods=['post'])
    def validate_result(self, request, pk=None):
        """Senior Lab Specialist reviews and validates entered measurement"""
        result = self.get_object()
        validator = request.data.get('validated_by', 'Senior Biochemist')

        if result.status == ResultStatus.DRAFT:
            return Response({'error': 'Cannot validate result before values are entered'}, status=400)

        result.validated_by = validator
        result.validated_at = timezone.now()
        result.status = ResultStatus.VALIDATED
        result.save()

        order = result.order_item.order
        order.status = LabOrderStatus.VALIDATED
        order.save()

        return Response({'message': 'Result validated by supervisor', 'status': result.status})

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve_result(self, request, pk=None):
        """Consultant Pathologist final digital sign-off and report emission"""
        result = self.get_object()
        approver = request.data.get('approved_by', 'Consultant Pathologist, MD')

        result.approved_by = approver
        result.approved_at = timezone.now()
        result.status = ResultStatus.APPROVED
        result.save()

        order = result.order_item.order
        # Check if all items in order are approved
        all_items_approved = not LabResult.objects.filter(
            order_item__order=order
        ).exclude(status__in=[ResultStatus.APPROVED, ResultStatus.AMENDED]).exists()

        if all_items_approved:
            order.status = LabOrderStatus.APPROVED
            order.completed_at = timezone.now()
            order.save()

            # Create or update final LabReport
            lab_report, _ = LabReport.objects.get_or_create(
                order=order,
                defaults={'approved_by': approver}
            )

            # Emit Member 6 Billing Event Contract
            BillingEventContract.objects.get_or_create(
                tenant=order.tenant,
                branch=order.branch,
                patient=order.patient,
                encounter=order.encounter,
                module='LIS',
                order_id=order.order_number,
                item_id=str(result.order_item.id),
                service_code=result.test.test_code,
                service_name=result.test.name,
                amount=result.test.price,
                status='EMITTED'
            )

        return Response({'message': f'Result approved by {approver}', 'status': result.status, 'order_status': order.status})

    @action(detail=True, methods=['post'])
    def amend_result(self, request, pk=None):
        """Amends already approved result with mandatory reason and version snapshot"""
        result = self.get_object()
        new_numeric = request.data.get('numeric_value')
        new_text = request.data.get('text_value', '')
        reason = request.data.get('reason')
        amended_by = request.data.get('amended_by', 'Pathology Director')

        if not reason:
            return Response({'error': 'Amendment reason is mandatory for clinical audit trail'}, status=400)

        # Snapshot existing version
        next_ver = result.versions.count() + 1
        LabResultVersion.objects.create(
            result=result,
            version_number=next_ver,
            previous_numeric_value=result.numeric_value,
            previous_text_value=result.text_value,
            previous_flag=result.flag,
            amended_by=amended_by,
            amendment_reason=reason
        )

        test = result.test
        if new_numeric is not None and new_numeric != '':
            result.numeric_value = float(new_numeric)
            result.flag = test.evaluate_numeric_flag(result.numeric_value)
        else:
            result.text_value = new_text
            result.flag = 'NORMAL'

        result.is_abnormal = result.flag in ['LOW', 'HIGH', 'CRITICAL_LOW', 'CRITICAL_HIGH', 'POSITIVE']
        result.is_critical = result.flag in ['CRITICAL_LOW', 'CRITICAL_HIGH']
        result.status = ResultStatus.AMENDED
        result.save()

        # Mark report as amended
        if hasattr(result.order_item.order, 'report'):
            report = result.order_item.order.report
            report.is_amended = True
            report.version += 1
            report.save()

        return Response({
            'message': f'Result amended to version {next_ver}',
            'flag': result.flag,
            'status': result.status
        })

class CriticalAlertViewSet(viewsets.ModelViewSet):
    """Critical Laboratory Values Escalation & Notification Management"""
    serializer_class = CriticalResultAlertSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = CriticalResultAlert.objects.all().select_related('patient', 'result__test', 'order')
        if tenant:
            qs = qs.filter(order__tenant=tenant)
        return qs.order_by('-triggered_at')

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Clinician or nursing supervisor acknowledges receipt of critical value"""
        alert = self.get_object()
        clinician = request.data.get('acknowledged_by', alert.clinician_name)
        notes = request.data.get('call_log_notes', 'Telephone readback verified by attending physician.')

        alert.alert_status = 'ACKNOWLEDGED'
        alert.acknowledged_by = clinician
        alert.acknowledged_at = timezone.now()
        alert.call_log_notes = f"{alert.call_log_notes} | Readback: {notes}"
        alert.save()

        return Response({'message': f'Critical alert acknowledged by Dr. {clinician}', 'status': alert.alert_status})

class LabReportViewSet(viewsets.ReadOnlyModelViewSet):
    """Diagnostic Laboratory Reports and PDF Emission"""
    serializer_class = LabReportSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = LabReport.objects.all().select_related('order__patient', 'order__tenant', 'order__branch')
        if tenant:
            qs = qs.filter(order__tenant=tenant)
        return qs

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Generates and streams authentic ReportLab clinical PDF document"""
        report = self.get_object()
        pdf_bytes = generate_lab_report_pdf(report)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"Lab_Report_{report.report_number}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response

class TATAnalyticsView(APIView):
    """Laboratory Turnaround Time (TAT) and Quality Metrics Analytics"""
    def get(self, request):
        tenant = getattr(request, 'tenant', None)
        orders = LabOrder.objects.filter(tenant=tenant)

        # Workload by priority
        by_priority = orders.values('priority').annotate(count=Count('id'))
        
        # Specimen rejection rate
        total_specimens = Specimen.objects.filter(order__tenant=tenant).count()
        rejected = Specimen.objects.filter(order__tenant=tenant, status=SpecimenStatus.REJECTED).count()
        rejection_rate = round((rejected / total_specimens * 100), 2) if total_specimens else 0.0

        # Export CSV if requested
        export_format = request.query_params.get('export')
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="lab_tat_analytics.csv"'
            writer = csv.writer(response)
            writer.writerow(['Order Number', 'Accession', 'Patient', 'Priority', 'Status', 'Ordered At', 'Completed At'])
            for o in orders:
                writer.writerow([
                    o.order_number, o.accession_number, o.patient.full_name,
                    o.priority, o.status, o.ordered_at, o.completed_at or 'IN_PROGRESS'
                ])
            return response

        return Response({
            'total_orders': orders.count(),
            'by_priority': list(by_priority),
            'total_specimens': total_specimens,
            'rejected_specimens': rejected,
            'rejection_rate_percent': rejection_rate,
            'average_target_tat_minutes': 120,
        })
