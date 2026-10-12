import uuid
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from core.models import Tenant, AuditLog
from patients.models import Patient, EmergencyContact, PatientConsent, PatientMergeAudit
from patients.serializers import (
    PatientSerializer,
    PatientRegistrationSerializer,
    PatientMergeSerializer,
    EmergencyContactSerializer,
    PatientConsentSerializer,
)
from patients.duplicate_engine import PatientDuplicateEngine


class PatientViewSet(viewsets.ModelViewSet):
    """
    CRUD and advanced lifecycle operations for Master Patient Index (MPI).
    Enforces multi-tenant query isolation and provides duplicate resolution.
    """
    serializer_class = PatientSerializer
    filterset_fields = ["gender", "blood_group", "status", "preferred_branch"]
    search_fields = ["mrn", "first_name", "last_name", "phone", "national_id", "email"]
    ordering_fields = ["created_at", "last_name", "mrn"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return Patient.objects.none()
        return Patient.objects.filter(tenant=tenant, is_deleted=False)

    def _generate_mrn(self, tenant: Tenant) -> str:
        prefix = tenant.mrn_prefix or "MRN"
        year = timezone.now().year
        count = Patient.objects.filter(tenant=tenant).count() + 1
        return f"{prefix}-{year}-{count:06d}"

    def create(self, request, *args, **kwargs):
        tenant = getattr(request, "tenant", None)
        if not tenant:
            return Response({"error": "Active tenant context required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PatientRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        emergency_contact_data = data.pop("emergency_contact", None)

        with transaction.atomic():
            mrn = self._generate_mrn(tenant)
            patient = Patient.objects.create(
                tenant=tenant,
                mrn=mrn,
                **data
            )

            if emergency_contact_data:
                EmergencyContact.objects.create(
                    tenant=tenant,
                    patient=patient,
                    **emergency_contact_data
                )

            # Record audit log
            AuditLog.objects.create(
                tenant=tenant,
                actor_id=str(request.user.id) if request.user.is_authenticated else "receptionist",
                action="CREATE",
                entity_name="Patient",
                entity_id=str(patient.id),
                changes={"mrn": mrn, "full_name": patient.full_name}
            )

        return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="check-duplicates")
    def check_duplicates(self, request):
        """
        Scans for potential duplicate patient records prior to registration.
        """
        tenant = getattr(request, "tenant", None)
        if not tenant:
            return Response({"error": "Active tenant required."}, status=status.HTTP_400_BAD_REQUEST)

        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        phone = request.data.get("phone", "")
        date_of_birth = request.data.get("date_of_birth")
        national_id = request.data.get("national_id", "")

        matches = PatientDuplicateEngine.scan_for_duplicates(
            tenant_id=tenant.id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            date_of_birth=date_of_birth,
            national_id=national_id
        )

        return Response({
            "duplicate_count": len(matches),
            "has_high_confidence_match": any(m["confidence_score"] >= 0.85 for m in matches),
            "matches": matches
        })

    @action(detail=False, methods=["post"], url_path="merge-records")
    def merge_records(self, request):
        """
        Safely merges a duplicate patient record into a primary surviving record.
        Preserves complete snapshot for auditability.
        """
        tenant = getattr(request, "tenant", None)
        serializer = PatientMergeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        surviving_id = serializer.validated_data["surviving_patient_id"]
        subsumed_id = serializer.validated_data["subsumed_patient_id"]
        reason = serializer.validated_data["reason"]

        if surviving_id == subsumed_id:
            return Response({"error": "Cannot merge a patient into themselves."}, status=status.HTTP_400_BAD_REQUEST)

        surviving = Patient.objects.filter(id=surviving_id, tenant=tenant).first()
        subsumed = Patient.objects.filter(id=subsumed_id, tenant=tenant).first()

        if not surviving or not subsumed:
            return Response({"error": "Both patient records must exist within this tenant."}, status=status.HTTP_404_NOT_FOUND)

        if subsumed.is_merged:
            return Response({"error": "The secondary record is already merged."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            snapshot = PatientSerializer(subsumed).data

            # Re-link emergency contacts
            EmergencyContact.objects.filter(patient=subsumed).update(patient=surviving)

            # Re-link consents
            PatientConsent.objects.filter(patient=subsumed).update(patient=surviving)

            # Mark subsumed patient
            subsumed.is_merged = True
            subsumed.merged_into = surviving
            subsumed.status = "MERGED"
            subsumed.merged_at = timezone.now()
            subsumed.merged_reason = reason
            subsumed.save()

            # Record audit
            PatientMergeAudit.objects.create(
                tenant=tenant,
                surviving_patient=surviving,
                subsumed_patient=subsumed,
                subsumed_mrn_snapshot=subsumed.mrn,
                merged_by_user_id="reception_admin",
                merged_by_user_email="admin@hospital.com",
                reason=reason,
                snapshot_data=snapshot
            )

        return Response({
            "message": f"Successfully merged {subsumed.mrn} into {surviving.mrn}.",
            "surviving_patient": PatientSerializer(surviving).data
        })
