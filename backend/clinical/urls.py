from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clinical.views import (
    ClinicalEncounterViewSet,
    ClinicalDiagnosisViewSet,
    PatientAllergyViewSet,
    ElectronicPrescriptionViewSet,
    PrescriptionItemViewSet,
    NursingObservationViewSet,
    FluidBalanceRecordViewSet,
    EMARRecordViewSet,
    SBARHandoverViewSet,
    DischargeSummaryViewSet,
    ClinicalReferralViewSet,
    ClinicalTemplateViewSet,
)

from clinical.rag_views import RAGQueryAPIView, RAGEvaluateAPIView

router = DefaultRouter()
router.register(r"encounters", ClinicalEncounterViewSet, basename="clinical-encounter")
router.register(r"diagnoses", ClinicalDiagnosisViewSet, basename="clinical-diagnosis")
router.register(r"allergies", PatientAllergyViewSet, basename="patient-allergy")
router.register(r"prescriptions", ElectronicPrescriptionViewSet, basename="electronic-prescription")
router.register(r"prescription-items", PrescriptionItemViewSet, basename="prescription-item")
router.register(r"nursing-observations", NursingObservationViewSet, basename="nursing-observation")
router.register(r"fluid-balances", FluidBalanceRecordViewSet, basename="fluid-balance")
router.register(r"emar", EMARRecordViewSet, basename="emar-record")
router.register(r"sbar-handovers", SBARHandoverViewSet, basename="sbar-handover")
router.register(r"discharge-summaries", DischargeSummaryViewSet, basename="discharge-summary")
router.register(r"referrals", ClinicalReferralViewSet, basename="clinical-referral")
router.register(r"templates", ClinicalTemplateViewSet, basename="clinical-template")

urlpatterns = [
    path("rag/query", RAGQueryAPIView.as_view(), name="clinical-rag-query"),
    path("rag/query/", RAGQueryAPIView.as_view(), name="clinical-rag-query-slash"),
    path("rag/evaluate", RAGEvaluateAPIView.as_view(), name="clinical-rag-evaluate"),
    path("rag/evaluate/", RAGEvaluateAPIView.as_view(), name="clinical-rag-evaluate-slash"),
    path("", include(router.urls)),
]
