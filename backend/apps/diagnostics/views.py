"""
Diagnostics Views (Member 4 integration contract).
Provides laboratory blood/urine panels and radiology reports with clinical approval states.
"""

from datetime import datetime
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.diagnostics.models import LabReport, RadiologyReport
from apps.diagnostics.serializers import LabReportSerializer, RadiologyReportSerializer

class LabReportListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LabReportSerializer

    def get_queryset(self):
        qs = LabReport.objects.all().select_related('patient__user', 'ordering_doctor__user', 'tenant')
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)

        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)

        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param.upper())

        # If accessed by a patient persona, only return APPROVED reports!
        user = self.request.user
        if user and user.is_authenticated and user.role == 'PATIENT':
            qs = qs.filter(status='APPROVED')

        return qs


class LabReportDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer


class LabReportApproveView(views.APIView):
    """
    Approve lab report and notify the patient.
    """
    permission_classes = [AllowAny]

    def post(self, request, pk):
        report = LabReport.objects.filter(id=pk).first()
        if not report:
            return Response({"error": "Lab report not found"}, status=status.HTTP_404_NOT_FOUND)

        from django.utils import timezone
        report.status = 'APPROVED'
        report.approved_at = timezone.now()
        report.approved_by = request.data.get('approved_by', 'Dr. Eleanor Vance, Pathologist')
        report.save()

        # Trigger notification
        try:
            from apps.notifications.services import NotificationDispatcher
            NotificationDispatcher.dispatch_lab_report_approved(report)
        except Exception:
            pass

        return Response({
            "success": True,
            "message": f"Lab report #{report.report_number} approved and released to patient portal.",
            "report": LabReportSerializer(report).data
        })


class RadiologyReportListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RadiologyReportSerializer

    def get_queryset(self):
        qs = RadiologyReport.objects.all().select_related('patient__user', 'ordering_doctor__user', 'tenant')
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)

        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)

        user = self.request.user
        if user and user.is_authenticated and user.role == 'PATIENT':
            qs = qs.filter(status='APPROVED')

        return qs


class RadiologyReportDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = RadiologyReport.objects.all()
    serializer_class = RadiologyReportSerializer
