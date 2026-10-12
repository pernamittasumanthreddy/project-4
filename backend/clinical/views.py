import hashlib
import uuid
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from core.models import Tenant, AuditLog
from patients.models import Patient
from clinical.models import (
    ClinicalEncounter,
    ClinicalAmendment,
    ClinicalDiagnosis,
    PatientAllergy,
    ElectronicPrescription,
    PrescriptionItem,
    NursingObservation,
    FluidBalanceRecord,
    EMARRecord,
    SBARHandover,
    DischargeSummary,
    ClinicalReferral,
    ClinicalTemplate,
)
from clinical.serializers import (
    ClinicalEncounterSerializer,
    SignEncounterSerializer,
    AddAmendmentSerializer,
    ClinicalAmendmentSerializer,
    ClinicalDiagnosisSerializer,
    PatientAllergySerializer,
    ElectronicPrescriptionSerializer,
    PrescriptionItemSerializer,
    NursingObservationSerializer,
    FluidBalanceRecordSerializer,
    EMARRecordSerializer,
    SBARHandoverSerializer,
    DischargeSummarySerializer,
    SignDischargeSummarySerializer,
    ClinicalReferralSerializer,
    ClinicalTemplateSerializer,
)


class ClinicalEncounterViewSet(viewsets.ModelViewSet):
    """
    Electronic Medical Record (EMR) Consultation Encounters.
    Guarantees tenant isolation, SOAP documentation, cryptographic sign-off, and addendum trail.
    """
    serializer_class = ClinicalEncounterSerializer
    filterset_fields = ["patient", "doctor_id", "status", "encounter_type"]
    search_fields = [
        "encounter_number", "patient__mrn", "patient__first_name",
        "patient__last_name", "chief_complaint", "assessment"
    ]
    ordering_fields = ["encounter_datetime", "created_at"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return ClinicalEncounter.objects.none()
        return ClinicalEncounter.objects.filter(
            tenant=tenant,
            is_deleted=False
        ).select_related("patient", "department").prefetch_related("diagnoses", "amendments", "prescriptions__items")

    def _generate_encounter_number(self, tenant: Tenant) -> str:
        year = timezone.now().year
        count = ClinicalEncounter.objects.filter(tenant=tenant).count() + 1
        return f"ENC-{year}-{count:06d}"

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            raise ValueError("Active tenant context is required.")
        enc_num = self._generate_encounter_number(tenant)
        serializer.save(tenant=tenant, encounter_number=enc_num)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.can_modify():
            return Response(
                {
                    "error": "Clinical record is finalized and immutable. "
                             "Direct modifications are forbidden. Please append a clinical addendum instead."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def sign(self, request, pk=None):
        """Cryptographically sign and finalize encounter."""
        encounter = self.get_object()
        serializer = SignEncounterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            digest = encounter.sign_encounter(
                doctor_id=serializer.validated_data["doctor_id"],
                doctor_name=serializer.validated_data["doctor_name"]
            )
            return Response({
                "message": "Encounter successfully signed and locked.",
                "encounter_number": encounter.encounter_number,
                "signature_hash": digest,
                "signed_at": encounter.signed_at
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def amend(self, request, pk=None):
        """Append a versioned addendum to a signed encounter."""
        encounter = self.get_object()
        if encounter.status not in ["SIGNED", "AMENDED"]:
            return Response(
                {"error": "Only signed encounters can be amended. Edit the draft encounter directly."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AddAmendmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        seq = encounter.amendments.count() + 1
        prev_hash = encounter.signature_hash

        amendment = ClinicalAmendment.objects.create(
            tenant=encounter.tenant,
            encounter=encounter,
            amendment_sequence=seq,
            author_id=data["author_id"],
            author_name=data["author_name"],
            reason=data["reason"],
            addendum_notes=data["addendum_notes"],
            previous_snapshot_hash=prev_hash
        )

        return Response(ClinicalAmendmentSerializer(amendment).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def patient_timeline(self, request):
        """Returns longitudinal chronological clinical timeline for a patient."""
        patient_id = request.query_params.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id parameter required"}, status=status.HTTP_400_BAD_REQUEST)

        tenant = getattr(request, "tenant", None)
        encounters = ClinicalEncounter.objects.filter(
            tenant=tenant,
            patient_id=patient_id,
            is_deleted=False
        ).order_by("-encounter_datetime")

        return Response(ClinicalEncounterSerializer(encounters, many=True).data)


class ClinicalDiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalDiagnosisSerializer
    filterset_fields = ["patient", "encounter", "diagnosis_type", "icd10_code"]
    search_fields = ["icd10_code", "diagnosis_name"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return ClinicalDiagnosis.objects.none()
        return ClinicalDiagnosis.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)


class PatientAllergyViewSet(viewsets.ModelViewSet):
    serializer_class = PatientAllergySerializer
    filterset_fields = ["patient", "allergy_type", "severity", "is_active"]
    search_fields = ["allergen", "reaction_description"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return PatientAllergy.objects.none()
        return PatientAllergy.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)

    @action(detail=False, methods=["post"])
    def check_conflict(self, request):
        """Cross-checks an ordered drug name against patient's active allergies."""
        patient_id = request.data.get("patient_id")
        drug_name = request.data.get("drug_name", "").strip().lower()

        if not patient_id or not drug_name:
            return Response({"error": "patient_id and drug_name are required."}, status=status.HTTP_400_BAD_REQUEST)

        tenant = getattr(request, "tenant", None)
        allergies = PatientAllergy.objects.filter(tenant=tenant, patient_id=patient_id, is_active=True)

        conflicts = []
        for allergy in allergies:
            allergen_clean = allergy.allergen.strip().lower()
            if allergen_clean in drug_name or drug_name in allergen_clean:
                conflicts.append({
                    "allergen": allergy.allergen,
                    "severity": allergy.severity,
                    "reaction": allergy.reaction_description,
                    "warning": f"ALERT: Patient has recorded {allergy.severity} allergy to {allergy.allergen}!"
                })

        return Response({
            "has_conflict": len(conflicts) > 0,
            "conflicts": conflicts
        })


class ElectronicPrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = ElectronicPrescriptionSerializer
    filterset_fields = ["patient", "encounter", "prescriber_id", "status"]
    search_fields = ["prescription_number", "patient__mrn", "patient__first_name", "patient__last_name"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return ElectronicPrescription.objects.none()
        return ElectronicPrescription.objects.filter(
            tenant=tenant,
            is_deleted=False
        ).prefetch_related("items")

    def _generate_prescription_number(self, tenant: Tenant) -> str:
        year = timezone.now().year
        count = ElectronicPrescription.objects.filter(tenant=tenant).count() + 1
        return f"RX-{year}-{count:06d}"

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        rx_num = self._generate_prescription_number(tenant)
        serializer.save(tenant=tenant, prescription_number=rx_num)


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionItemSerializer
    filterset_fields = ["prescription", "is_dispensed"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return PrescriptionItem.objects.none()
        return PrescriptionItem.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)


class NursingObservationViewSet(viewsets.ModelViewSet):
    serializer_class = NursingObservationSerializer
    filterset_fields = ["patient", "admission", "nurse_id"]
    ordering_fields = ["recorded_at", "mews_score"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return NursingObservation.objects.none()
        return NursingObservation.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)


class FluidBalanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FluidBalanceRecordSerializer
    filterset_fields = ["patient", "admission", "shift"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return FluidBalanceRecord.objects.none()
        return FluidBalanceRecord.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)


class EMARRecordViewSet(viewsets.ModelViewSet):
    serializer_class = EMARRecordSerializer
    filterset_fields = ["patient", "prescription_item", "status"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return EMARRecord.objects.none()
        return EMARRecord.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)

    @action(detail=True, methods=["post"])
    def administer(self, request, pk=None):
        emar = self.get_object()
        emar.status = "GIVEN"
        emar.administered_time = timezone.now()
        emar.nurse_id = request.data.get("nurse_id", emar.nurse_id)
        emar.nurse_name = request.data.get("nurse_name", emar.nurse_name)
        emar.notes = request.data.get("notes", emar.notes)
        emar.save()
        return Response(EMARRecordSerializer(emar).data)


class SBARHandoverViewSet(viewsets.ModelViewSet):
    serializer_class = SBARHandoverSerializer
    filterset_fields = ["patient", "admission", "shift"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return SBARHandover.objects.none()
        return SBARHandover.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)


class DischargeSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = DischargeSummarySerializer
    filterset_fields = ["patient", "admission", "is_signed", "discharge_condition"]
    search_fields = ["summary_number", "primary_diagnosis", "hospital_course"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return DischargeSummary.objects.none()
        return DischargeSummary.objects.filter(tenant=tenant, is_deleted=False)

    def _generate_summary_number(self, tenant: Tenant) -> str:
        year = timezone.now().year
        count = DischargeSummary.objects.filter(tenant=tenant).count() + 1
        return f"DCS-{year}-{count:06d}"

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        dcs_num = self._generate_summary_number(tenant)
        serializer.save(tenant=tenant, summary_number=dcs_num)

    @action(detail=True, methods=["post"])
    def sign(self, request, pk=None):
        dcs = self.get_object()
        serializer = SignDischargeSummarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        digest = dcs.sign(
            doctor_id=serializer.validated_data["doctor_id"],
            doctor_name=serializer.validated_data["doctor_name"]
        )
        return Response({
            "message": "Discharge summary signed and locked.",
            "summary_number": dcs.summary_number,
            "signature_hash": digest,
            "signed_at": dcs.signed_at
        })


class ClinicalReferralViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalReferralSerializer
    filterset_fields = ["patient", "target_specialty", "urgency", "status"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return ClinicalReferral.objects.none()
        return ClinicalReferral.objects.filter(tenant=tenant, is_deleted=False)

    def _generate_referral_number(self, tenant: Tenant) -> str:
        year = timezone.now().year
        count = ClinicalReferral.objects.filter(tenant=tenant).count() + 1
        return f"REF-{year}-{count:06d}"

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        ref_num = self._generate_referral_number(tenant)
        serializer.save(tenant=tenant, referral_number=ref_num)


class ClinicalTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicalTemplateSerializer
    filterset_fields = ["specialty", "template_type", "is_active"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return ClinicalTemplate.objects.none()
        return ClinicalTemplate.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        serializer.save(tenant=tenant)
