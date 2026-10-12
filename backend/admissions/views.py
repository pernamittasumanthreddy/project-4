from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import HospitalBranch, Department, AuditLog
from patients.models import Patient
from admissions.models import Ward, Room, Bed, Admission, BedTransferLog
from admissions.serializers import (
    WardSerializer,
    RoomSerializer,
    BedSerializer,
    AdmissionSerializer,
    AdmitPatientSerializer,
    TransferBedSerializer,
)


class WardViewSet(viewsets.ModelViewSet):
    serializer_class = WardSerializer

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return Ward.objects.none()
        return Ward.objects.filter(tenant=tenant).prefetch_related("rooms__beds")


class AdmissionViewSet(viewsets.ModelViewSet):
    """
    Manages Inpatient (IPD) admissions, bed transitions, transfers, and discharge clearances.
    """
    serializer_class = AdmissionSerializer
    filterset_fields = ["status", "branch", "department", "billing_cleared"]
    search_fields = ["admission_number", "patient__first_name", "patient__last_name", "patient__mrn"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return Admission.objects.none()
        return Admission.objects.filter(tenant=tenant).select_related("patient", "bed__room__ward", "branch", "department").prefetch_related("transfers")

    def create(self, request, *args, **kwargs):
        tenant = getattr(request, "tenant", None)
        if not tenant:
            return Response({"error": "Tenant context required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdmitPatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data

        with transaction.atomic():
            # Concurrency check: Lock bed row to ensure it's AVAILABLE
            bed = Bed.objects.select_for_update().filter(id=d["bed_id"], tenant=tenant).first()
            if not bed:
                return Response({"error": "Selected bed does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if bed.status != "AVAILABLE":
                return Response({"error": f"Bed is currently {bed.status}. Please select an available bed."}, status=status.HTTP_409_CONFLICT)

            # Check if patient is already admitted
            already_admitted = Admission.objects.filter(
                tenant=tenant,
                patient_id=d["patient_id"],
                status__in=["ADMITTED", "DISCHARGE_REQUESTED", "BILLING_CLEARED"]
            ).exists()

            if already_admitted:
                return Response({"error": "Patient is already actively admitted in an inpatient ward."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate admission tracking number
            year = timezone.now().year
            adm_count = Admission.objects.filter(tenant=tenant).count() + 1
            adm_number = f"IPD-{year}-{adm_count:06d}"

            patient = Patient.objects.get(id=d["patient_id"], tenant=tenant)
            branch = HospitalBranch.objects.get(id=d["branch_id"], tenant=tenant)
            dept = Department.objects.get(id=d["department_id"], tenant=tenant)

            admission = Admission.objects.create(
                tenant=tenant,
                admission_number=adm_number,
                patient=patient,
                branch=branch,
                department=dept,
                admitting_doctor_id=d["admitting_doctor_id"],
                admitting_doctor_name=d["admitting_doctor_name"],
                bed=bed,
                admission_diagnosis=d["admission_diagnosis"],
                status="ADMITTED"
            )

            # Update Bed Status
            bed.status = "OCCUPIED"
            bed.save()

        return Response(AdmissionSerializer(admission).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="transfer-bed")
    def transfer_bed(self, request, pk=None):
        """
        Transfers an admitted patient to another bed / ward with audit logging.
        """
        admission = self.get_object()
        tenant = admission.tenant

        if admission.status != "ADMITTED":
            return Response({"error": "Only actively admitted patients can be transferred."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransferBedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_bed_id = serializer.validated_data["to_bed_id"]
        reason = serializer.validated_data["reason"]
        transferred_by = serializer.validated_data["transferred_by_user_name"]

        with transaction.atomic():
            new_bed = Bed.objects.select_for_update().filter(id=to_bed_id, tenant=tenant).first()
            if not new_bed:
                return Response({"error": "Target bed does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if new_bed.status != "AVAILABLE":
                return Response({"error": f"Target bed is {new_bed.status}."}, status=status.HTTP_409_CONFLICT)

            old_bed = admission.bed

            # Mark old bed as CLEANING
            old_bed.status = "CLEANING"
            old_bed.save()

            # Mark new bed as OCCUPIED
            new_bed.status = "OCCUPIED"
            new_bed.save()

            # Update admission record
            admission.bed = new_bed
            admission.save()

            # Log transfer history
            BedTransferLog.objects.create(
                tenant=tenant,
                admission=admission,
                from_bed=old_bed,
                to_bed=new_bed,
                transferred_by_user_id="nurse_user",
                transferred_by_user_name=transferred_by,
                reason=reason
            )

        return Response({
            "message": f"Patient transferred from Bed {old_bed.bed_number} to Bed {new_bed.bed_number}.",
            "admission": AdmissionSerializer(admission).data
        })

    @action(detail=True, methods=["post"], url_path="request-discharge")
    def request_discharge(self, request, pk=None):
        """
        Clinician initiates discharge workflow. Awaits billing clearance.
        """
        admission = self.get_object()
        discharge_diag = request.data.get("discharge_diagnosis", "")
        summary = request.data.get("discharge_summary", "")

        admission.status = "DISCHARGE_REQUESTED"
        admission.discharge_diagnosis = discharge_diag
        admission.discharge_summary = summary
        admission.save()

        return Response({"message": "Discharge requested. Pending billing clearance.", "admission": AdmissionSerializer(admission).data})

    @action(detail=True, methods=["post"], url_path="clear-billing")
    def clear_billing(self, request, pk=None):
        """
        Billing department clearance hook (Member 6 integration).
        """
        admission = self.get_object()
        admission.billing_cleared = True
        admission.billing_cleared_at = timezone.now()
        admission.billing_cleared_by = "billing_desk"
        admission.status = "BILLING_CLEARED"
        admission.save()

        return Response({"message": "Billing clearance recorded.", "admission": AdmissionSerializer(admission).data})

    @action(detail=True, methods=["post"], url_path="complete-discharge")
    def complete_discharge(self, request, pk=None):
        """
        Final discharge release. Marks bed as available for sanitization.
        """
        admission = self.get_object()

        if not admission.billing_cleared:
            return Response({"error": "Cannot complete discharge without billing clearance."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            admission.status = "DISCHARGED"
            admission.discharge_date = timezone.now()
            admission.save()

            # Mark bed for cleaning
            bed = admission.bed
            bed.status = "CLEANING"
            bed.save()

        return Response({"message": "Patient discharged successfully. Bed released to cleaning status.", "admission": AdmissionSerializer(admission).data})
