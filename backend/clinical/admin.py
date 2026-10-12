from django.contrib import admin
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


@admin.register(ClinicalEncounter)
class ClinicalEncounterAdmin(admin.ModelAdmin):
    list_display = ["encounter_number", "patient", "doctor_name", "encounter_type", "status", "is_signed", "encounter_datetime"]
    list_filter = ["status", "encounter_type", "is_signed"]
    search_fields = ["encounter_number", "doctor_name", "patient__mrn", "patient__first_name", "patient__last_name"]


@admin.register(ClinicalAmendment)
class ClinicalAmendmentAdmin(admin.ModelAdmin):
    list_display = ["encounter", "amendment_sequence", "author_name", "created_at"]
    search_fields = ["encounter__encounter_number", "author_name", "reason"]


@admin.register(ClinicalDiagnosis)
class ClinicalDiagnosisAdmin(admin.ModelAdmin):
    list_display = ["icd10_code", "diagnosis_name", "diagnosis_type", "patient", "is_chronic"]
    list_filter = ["diagnosis_type", "is_chronic"]
    search_fields = ["icd10_code", "diagnosis_name", "patient__mrn"]


@admin.register(PatientAllergy)
class PatientAllergyAdmin(admin.ModelAdmin):
    list_display = ["patient", "allergen", "allergy_type", "severity", "is_active"]
    list_filter = ["allergy_type", "severity", "is_active"]
    search_fields = ["allergen", "patient__mrn"]


@admin.register(ElectronicPrescription)
class ElectronicPrescriptionAdmin(admin.ModelAdmin):
    list_display = ["prescription_number", "patient", "prescriber_name", "status", "prescribed_date"]
    list_filter = ["status"]
    search_fields = ["prescription_number", "patient__mrn", "prescriber_name"]


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ["medication_name", "dosage", "frequency", "duration_days", "prescription", "is_dispensed"]
    search_fields = ["medication_name", "generic_name"]


@admin.register(NursingObservation)
class NursingObservationAdmin(admin.ModelAdmin):
    list_display = ["patient", "nurse_name", "recorded_at", "systolic_bp", "heart_rate", "mews_score"]
    list_filter = ["avpu_score"]
    search_fields = ["patient__mrn", "nurse_name"]


@admin.register(FluidBalanceRecord)
class FluidBalanceRecordAdmin(admin.ModelAdmin):
    list_display = ["patient", "shift", "recorded_at", "oral_intake_ml", "iv_intake_ml", "urine_output_ml", "net_balance_ml"]
    list_filter = ["shift"]
    search_fields = ["patient__mrn"]


@admin.register(EMARRecord)
class EMARRecordAdmin(admin.ModelAdmin):
    list_display = ["patient", "prescription_item", "status", "scheduled_time", "administered_time", "nurse_name"]
    list_filter = ["status"]
    search_fields = ["patient__mrn", "nurse_name"]


@admin.register(SBARHandover)
class SBARHandoverAdmin(admin.ModelAdmin):
    list_display = ["patient", "shift", "giving_nurse_name", "receiving_nurse_name", "code_status", "handover_time"]
    list_filter = ["shift", "code_status"]
    search_fields = ["patient__mrn", "giving_nurse_name", "receiving_nurse_name"]


@admin.register(DischargeSummary)
class DischargeSummaryAdmin(admin.ModelAdmin):
    list_display = ["summary_number", "patient", "author_doctor_name", "discharge_condition", "is_signed", "discharge_date"]
    list_filter = ["discharge_condition", "is_signed"]
    search_fields = ["summary_number", "patient__mrn", "author_doctor_name"]


@admin.register(ClinicalReferral)
class ClinicalReferralAdmin(admin.ModelAdmin):
    list_display = ["referral_number", "patient", "referring_doctor_name", "target_specialty", "urgency", "status"]
    list_filter = ["urgency", "status"]
    search_fields = ["referral_number", "patient__mrn", "target_specialty"]


@admin.register(ClinicalTemplate)
class ClinicalTemplateAdmin(admin.ModelAdmin):
    list_display = ["title", "specialty", "template_type", "is_active"]
    list_filter = ["specialty", "template_type", "is_active"]
    search_fields = ["title", "specialty"]
