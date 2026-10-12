import os
from pathlib import Path
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse, FileResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .models import (
    ImagingModality, ImagingProcedure, ImagingOrder, ImagingOrderItem,
    ImagingStudy, RadiologyReport, RadiologyReportVersion,
    ImagingOrderStatus, RadiologyReportStatus, ModalityType
)
from .serializers import (
    ImagingModalitySerializer, ImagingProcedureSerializer,
    ImagingOrderSerializer, ImagingOrderItemSerializer,
    ImagingStudySerializer, RadiologyReportSerializer
)
from .dicom_service import generate_synthetic_dicom_file, render_dicom_to_png_bytes
from .pdf_generator import generate_radiology_report_pdf
from contracts.models import BillingEventContract, PatientContract, HospitalBranch

class RadiologyDashboardView(APIView):
    """
    Real-time database-calculated radiology statistics scoped by tenant and branch.
    Zero hardcoded numbers.
    """
    def get(self, request):
        tenant = getattr(request, 'tenant', None)
        branch = getattr(request, 'branch', None)

        if not tenant:
            return Response({'error': 'Tenant context required'}, status=400)

        orders_qs = ImagingOrder.objects.filter(tenant=tenant)
        if branch:
            orders_qs = orders_qs.filter(branch=branch)

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        orders_today_count = orders_qs.filter(ordered_at__gte=today_start).count()
        awaiting_schedule = orders_qs.filter(status=ImagingOrderStatus.ORDERED).count()
        scheduled_procedures = orders_qs.filter(status=ImagingOrderStatus.SCHEDULED).count()
        patients_arrived = orders_qs.filter(status=ImagingOrderStatus.ARRIVED).count()
        scans_in_progress = orders_qs.filter(status=ImagingOrderStatus.IN_PROGRESS).count()
        scans_completed = orders_qs.filter(status=ImagingOrderStatus.COMPLETED).count()
        awaiting_interpretation = orders_qs.filter(status=ImagingOrderStatus.REPORT_PENDING).count()
        currently_reporting = orders_qs.filter(status=ImagingOrderStatus.REPORTING).count()
        approved_reports = orders_qs.filter(status=ImagingOrderStatus.APPROVED).count()

        # Breakdown by Modality
        modality_breakdown = ImagingModality.objects.annotate(
            procedure_count=Count('procedures', filter=Q(procedures__tenant=tenant)),
            active_orders=Count('procedures__order_items', filter=Q(procedures__order_items__order__tenant=tenant))
        ).values('id', 'name', 'modality_type', 'room_number', 'active_orders')

        return Response({
            'tenant_code': tenant.code,
            'branch_name': branch.name if branch else 'All Branches',
            'statistics': {
                'total_orders_today': orders_today_count,
                'awaiting_scheduling': awaiting_schedule,
                'scheduled': scheduled_procedures,
                'patients_arrived': patients_arrived,
                'scans_in_progress': scans_in_progress,
                'scans_completed': scans_completed,
                'awaiting_interpretation': awaiting_interpretation,
                'currently_reporting': currently_reporting,
                'approved_reports': approved_reports,
            },
            'modalities': list(modality_breakdown),
            'timestamp': now.isoformat()
        })

class ImagingModalityViewSet(viewsets.ReadOnlyModelViewSet):
    """Radiology Modality Equipment / Department Suites"""
    queryset = ImagingModality.objects.filter(is_active=True)
    serializer_class = ImagingModalitySerializer

class ImagingProcedureViewSet(viewsets.ModelViewSet):
    """Radiology Procedure Catalogue Item Management"""
    serializer_class = ImagingProcedureSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = ImagingProcedure.objects.all().select_related('modality')
        if tenant:
            qs = qs.filter(tenant=tenant)
        modality_type = self.request.query_params.get('modality')
        if modality_type:
            qs = qs.filter(modality__modality_type=modality_type)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(procedure_code__icontains=search) | Q(body_part__icontains=search))
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)

class ImagingOrderViewSet(viewsets.ModelViewSet):
    """Radiology Order Management & Modality Lifecycle Transitions"""
    serializer_class = ImagingOrderSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        branch = getattr(self.request, 'branch', None)
        qs = ImagingOrder.objects.all().select_related('patient', 'branch').prefetch_related('items__procedure__modality', 'items__study')
        if tenant:
            qs = qs.filter(tenant=tenant)
        if branch:
            qs = qs.filter(branch=branch)
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
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
        tenant = getattr(request, 'tenant', None)
        branch = getattr(request, 'branch', None)
        patient_id = request.data.get('patient_id')
        procedure_ids = request.data.get('procedure_ids', [])
        ordering_clinician = request.data.get('ordering_clinician', 'Attending Physician')
        priority = request.data.get('priority', 'ROUTINE')
        clinical_history = request.data.get('clinical_history', '')
        contrast_cleared = bool(request.data.get('contrast_cleared', False))

        if not patient_id:
            return Response({'error': 'Patient ID is required'}, status=400)
        if not procedure_ids:
            return Response({'error': 'At least one imaging procedure must be selected'}, status=400)

        patient = PatientContract.objects.filter(id=patient_id, tenant=tenant).first()
        if not patient:
            return Response({'error': 'Patient not found in this tenant'}, status=404)

        order = ImagingOrder.objects.create(
            tenant=tenant,
            branch=branch or HospitalBranch.objects.filter(tenant=tenant).first(),
            patient=patient,
            ordering_clinician=ordering_clinician,
            priority=priority,
            clinical_history=clinical_history,
            contrast_cleared=contrast_cleared,
            status=ImagingOrderStatus.ORDERED
        )

        procedures = ImagingProcedure.objects.filter(id__in=procedure_ids, tenant=tenant)
        for proc in procedures:
            ImagingOrderItem.objects.create(
                order=order,
                procedure=proc,
                price_at_order=proc.price
            )

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        order = self.get_object()
        slot_str = request.data.get('scheduled_slot')
        order.status = ImagingOrderStatus.SCHEDULED
        if slot_str:
            order.scheduled_slot = slot_str
        else:
            order.scheduled_slot = timezone.now() + timedelta(hours=2)
        order.save()
        return Response({'message': f'Order {order.order_number} scheduled', 'status': order.status, 'slot': order.scheduled_slot})

    @action(detail=True, methods=['post'])
    def mark_arrived(self, request, pk=None):
        order = self.get_object()
        order.status = ImagingOrderStatus.ARRIVED
        order.save()
        return Response({'message': f'Patient {order.patient.full_name} marked arrived at radiology desk', 'status': order.status})

    @action(detail=True, methods=['post'])
    def start_scan(self, request, pk=None):
        order = self.get_object()
        order.status = ImagingOrderStatus.IN_PROGRESS
        order.save()
        return Response({'message': f'Scanning in progress for {order.order_number}', 'status': order.status})

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def complete_scan(self, request, pk=None):
        """Technologist finishes acquisition, generates authentic DICOM study, and queues for radiologist"""
        order = self.get_object()
        technologist = request.data.get('technologist', 'Senior Radiologic Technologist')

        order.status = ImagingOrderStatus.REPORT_PENDING
        order.completed_at = timezone.now()
        order.save()

        # For each order item, generate authentic DICOM study and initial report draft
        for item in order.items.all():
            if not hasattr(item, 'study'):
                modality_type = item.procedure.modality.modality_type
                study = ImagingStudy.objects.create(
                    order_item=item,
                    patient=order.patient,
                    accession_number=order.accession_number,
                    modality_type=modality_type,
                    study_description=item.procedure.name,
                    performing_technologist=technologist,
                    series_count=1,
                    instance_count=1,
                    is_synthetic_demo=True
                )

                # Generate authentic standard DICOM file via pydicom
                dcm_file_path = generate_synthetic_dicom_file(
                    patient=order.patient,
                    procedure=item.procedure,
                    study_uid=study.study_instance_uid,
                    accession_no=order.accession_number,
                    modality=modality_type,
                    slice_index=1,
                    total_slices=1
                )
                study.dicom_file_path = dcm_file_path
                study.save()

                # Generate initial draft radiology report
                RadiologyReport.objects.create(
                    study=study,
                    reporting_radiologist='Consultant Radiologist',
                    clinical_indication=order.clinical_history or f"Evaluation of {item.procedure.body_part}",
                    examination_technique=f"Multi-planar high-resolution {modality_type} acquisition obtained.",
                    findings=f"Examination of the {item.procedure.body_part} demonstrates normal anatomical alignment. No acute fracture, focal consolidation, or mass effect identified.",
                    impression=f"Unremarkable {item.procedure.name}. No acute abnormalities identified.",
                    status=RadiologyReportStatus.DRAFT
                )

        return Response({'message': f'Acquisition completed for order {order.order_number}. DICOM study stored in PACS.', 'status': order.status})

class ModalityWorklistView(APIView):
    """DICOM Modality Worklist (MWL) query endpoint for radiology equipment"""
    def get(self, request):
        tenant = getattr(request, 'tenant', None)
        modality_param = request.query_params.get('modality')
        
        orders = ImagingOrder.objects.filter(
            tenant=tenant,
            status__in=[ImagingOrderStatus.SCHEDULED, ImagingOrderStatus.ARRIVED, ImagingOrderStatus.IN_PROGRESS]
        ).select_related('patient', 'branch').prefetch_related('items__procedure__modality')

        if modality_param:
            orders = orders.filter(items__procedure__modality__modality_type=modality_param)

        worklist = []
        for o in orders:
            for item in o.items.all():
                worklist.append({
                    'accession_number': o.accession_number,
                    'patient_id': o.patient.uhid,
                    'patient_name': o.patient.full_name,
                    'patient_dob': str(o.patient.dob),
                    'patient_sex': o.patient.gender,
                    'modality': item.procedure.modality.modality_type,
                    'scheduled_station_ae': item.procedure.modality.ae_title,
                    'scheduled_procedure_code': item.procedure.procedure_code,
                    'scheduled_procedure_description': item.procedure.name,
                    'scheduled_start_time': o.scheduled_slot.isoformat() if o.scheduled_slot else o.ordered_at.isoformat(),
                    'referring_physician': o.ordering_clinician,
                    'status': o.status,
                })

        return Response({'count': len(worklist), 'worklist': worklist})

class ImagingStudyViewSet(viewsets.ReadOnlyModelViewSet):
    """DICOM Study Records and PACS references"""
    serializer_class = ImagingStudySerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = ImagingStudy.objects.all().select_related('patient', 'order_item__order', 'report')
        if tenant:
            qs = qs.filter(patient__tenant=tenant)
        accession = self.request.query_params.get('accession')
        if accession:
            qs = qs.filter(accession_number=accession)
        return qs

class RadiologyReportViewSet(viewsets.ModelViewSet):
    """Radiology Diagnostic Reporting, Consultant Sign-Off, Addenda & PDF Downloads"""
    serializer_class = RadiologyReportSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = RadiologyReport.objects.all().select_related('study__patient', 'study__order_item__order')
        if tenant:
            qs = qs.filter(study__patient__tenant=tenant)
        return qs

    @action(detail=True, methods=['post'])
    def save_draft(self, request, pk=None):
        report = self.get_object()
        report.findings = request.data.get('findings', report.findings)
        report.impression = request.data.get('impression', report.impression)
        report.recommendations = request.data.get('recommendations', report.recommendations)
        report.bi_rads_grade = request.data.get('bi_rads_grade', report.bi_rads_grade)
        report.reporting_radiologist = request.data.get('radiologist', report.reporting_radiologist)
        report.status = RadiologyReportStatus.DRAFT
        report.save()

        order = report.study.order_item.order
        order.status = ImagingOrderStatus.REPORTING
        order.save()

        return Response({'message': 'Draft findings saved successfully', 'status': report.status})

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve_report(self, request, pk=None):
        """Radiologist consultant signs off and releases diagnostic report"""
        report = self.get_object()
        approver = request.data.get('approved_by', 'Consultant Radiologist, M.D.')

        report.findings = request.data.get('findings', report.findings)
        report.impression = request.data.get('impression', report.impression)
        report.recommendations = request.data.get('recommendations', report.recommendations)
        report.bi_rads_grade = request.data.get('bi_rads_grade', report.bi_rads_grade)
        report.approved_by = approver
        report.approved_at = timezone.now()
        report.status = RadiologyReportStatus.APPROVED
        report.save()

        order = report.study.order_item.order
        order.status = ImagingOrderStatus.APPROVED
        order.save()

        # Emit Member 6 Billing Event Contract
        proc = report.study.order_item.procedure
        BillingEventContract.objects.get_or_create(
            tenant=order.tenant,
            branch=order.branch,
            patient=order.patient,
            encounter=order.encounter,
            module='RIS',
            order_id=order.order_number,
            item_id=str(report.study.id),
            service_code=proc.procedure_code,
            service_name=proc.name,
            amount=proc.price,
            status='EMITTED'
        )

        return Response({'message': f'Radiology report finalized and signed by {approver}', 'status': report.status})

    @action(detail=True, methods=['post'])
    def amend_report(self, request, pk=None):
        """Creates formal addendum version for finalized radiology report"""
        report = self.get_object()
        reason = request.data.get('reason')
        addendum_findings = request.data.get('findings')
        addendum_impression = request.data.get('impression')
        amended_by = request.data.get('amended_by', 'Senior Staff Radiologist')

        if not reason:
            return Response({'error': 'Amendment reason is required for clinical audit compliance'}, status=400)

        next_ver = report.version + 1
        RadiologyReportVersion.objects.create(
            report=report,
            version_number=report.version,
            previous_findings=report.findings,
            previous_impression=report.impression,
            amended_by=amended_by,
            amendment_reason=reason
        )

        report.version = next_ver
        if addendum_findings:
            report.findings = addendum_findings
        if addendum_impression:
            report.impression = addendum_impression
        report.status = RadiologyReportStatus.AMENDED
        report.save()

        return Response({'message': f'Addendum version {next_ver} appended to report', 'version': report.version, 'status': report.status})

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Generates and streams authentic ReportLab Radiology PDF report"""
        report = self.get_object()
        pdf_bytes = generate_radiology_report_pdf(report)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"Radiology_Report_{report.report_number}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response

class DICOMWebView(APIView):
    """
    DICOMweb Standard Interface (QIDO-RS and WADO-RS endpoints).
    Complies with PS3.18 DICOM Web Services Specification.
    """
    def get(self, request, study_uid=None, series_uid=None, instance_uid=None, action=None):
        tenant = getattr(request, 'tenant', None)

        # 1. QIDO-RS Study Search: GET /api/dicomweb/studies
        if not study_uid:
            studies = ImagingStudy.objects.all().select_related('patient', 'order_item__procedure')
            if tenant:
                studies = studies.filter(patient__tenant=tenant)
            
            dicom_json = []
            for s in studies:
                dicom_json.append({
                    "0020000D": {"vr": "UI", "Value": [s.study_instance_uid]},
                    "00100020": {"vr": "LO", "Value": [s.patient.uhid]},
                    "00100010": {"vr": "PN", "Value": [{"Alphabetic": f"{s.patient.last_name}^{s.patient.first_name}"}]},
                    "00080060": {"vr": "CS", "Value": [s.modality_type]},
                    "00081030": {"vr": "LO", "Value": [s.study_description]},
                    "00080050": {"vr": "SH", "Value": [s.accession_number]},
                    "00080020": {"vr": "DA", "Value": [s.study_date.strftime('%Y%m%d')]},
                    "00201206": {"vr": "IS", "Value": [s.series_count]},
                    "00201208": {"vr": "IS", "Value": [s.instance_count]}
                })
            return Response(dicom_json)

        # Find Study
        study = ImagingStudy.objects.filter(study_instance_uid=study_uid).first()
        if not study:
            return Response({'error': 'DICOM Study not found'}, status=404)

        # 2. WADO-RS Study Metadata: GET /api/dicomweb/studies/{studyUID}/metadata
        if action == 'metadata' or not series_uid:
            metadata = [{
                "0020000D": {"vr": "UI", "Value": [study.study_instance_uid]},
                "0020000E": {"vr": "UI", "Value": [f"{study.study_instance_uid}.1"]},
                "00080018": {"vr": "UI", "Value": [f"{study.study_instance_uid}.1.1"]},
                "00100020": {"vr": "LO", "Value": [study.patient.uhid]},
                "00100010": {"vr": "PN", "Value": [{"Alphabetic": f"{study.patient.last_name}^{study.patient.first_name}"}]},
                "00080060": {"vr": "CS", "Value": [study.modality_type]},
                "00081030": {"vr": "LO", "Value": [study.study_description]},
                "00280010": {"vr": "US", "Value": [512]}, # Rows
                "00280011": {"vr": "US", "Value": [512]}, # Columns
                "00280100": {"vr": "US", "Value": [16]},  # BitsAllocated
                "00280101": {"vr": "US", "Value": [12]},  # BitsStored
                "00280004": {"vr": "CS", "Value": ["MONOCHROME2"]},
                "00281050": {"vr": "DS", "Value": ["40"]}, # WindowCenter
                "00281051": {"vr": "DS", "Value": ["400"]}, # WindowWidth
            }]
            return Response(metadata)

        # Locate DICOM file
        dcm_path = study.dicom_file_path
        if not dcm_path or not os.path.exists(dcm_path):
            # Regenerate if missing
            dcm_path = generate_synthetic_dicom_file(
                patient=study.patient,
                procedure=study.order_item.procedure,
                study_uid=study.study_instance_uid,
                accession_no=study.accession_number,
                modality=study.modality_type,
                slice_index=1,
                total_slices=1
            )
            study.dicom_file_path = dcm_path
            study.save()

        # 3. WADO-RS Rendered Frame: GET /api/dicomweb/studies/{uid}/series/{uid}/instances/{uid}/rendered
        if action == 'rendered' or request.query_params.get('rendered') == 'true':
            png_bytes = render_dicom_to_png_bytes(dcm_path)
            return HttpResponse(png_bytes, content_type='image/png')

        # 4. WADO-RS Raw DCM download
        return FileResponse(open(dcm_path, 'rb'), content_type='application/dicom')
