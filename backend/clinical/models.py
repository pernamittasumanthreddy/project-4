import hashlib
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import TenantAwareModel, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from admissions.models import Admission


class ClinicalEncounter(TenantAwareModel):
    """
    Core electronic clinical consultation / encounter record (SOAP format).
    Includes SHA-256 cryptographic immutability hashing once signed by the physician.
    """
    ENCOUNTER_TYPE_CHOICES = [
        ("OPD", "Outpatient Consultation"),
        ("IPD_ROUND", "Inpatient Ward Round"),
        ("EMERGENCY", "Emergency Triage / Trauma Care"),
        ("TELECONSULT", "Telemedicine Remote Consult"),
    ]

    STATUS_CHOICES = [
        ("IN_PROGRESS", "In Progress (Draft)"),
        ("SIGNED", "Signed & Finalized (Immutable)"),
        ("AMENDED", "Amended with Versioned Addendum"),
        ("CANCELLED", "Cancelled"),
    ]

    encounter_number = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unique Encounter Identifier, e.g. ENC-2026-000001"
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="clinical_encounters"
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clinical_encounters"
    )
    admission = models.ForeignKey(
        Admission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clinical_encounters"
    )
    doctor_id = models.CharField(max_length=100, db_index=True)
    doctor_name = models.CharField(max_length=200)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clinical_encounters"
    )

    encounter_type = models.CharField(
        max_length=30,
        choices=ENCOUNTER_TYPE_CHOICES,
        default="OPD"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="IN_PROGRESS",
        db_index=True
    )
    encounter_datetime = models.DateTimeField(default=timezone.now, db_index=True)

    # SOAP Framework Clinical Notes
    chief_complaint = models.TextField(blank=True, default="")
    subjective_notes = models.TextField(
        blank=True,
        default="",
        help_text="History of Present Illness (HPI), Review of Systems (ROS), patient verbal report"
    )
    objective_findings = models.TextField(
        blank=True,
        default="",
        help_text="Vital signs, physical examination findings, system exam"
    )
    assessment = models.TextField(
        blank=True,
        default="",
        help_text="Clinical reasoning, primary diagnostic hypothesis, differentials"
    )
    plan = models.TextField(
        blank=True,
        default="",
        help_text="Diagnostic orders, medications, patient education, follow-up"
    )

    # Cryptographic Finalization and Immutability Fields
    is_signed = models.BooleanField(default=False)
    signed_at = models.DateTimeField(null=True, blank=True)
    signed_by_doctor_id = models.CharField(max_length=100, blank=True, default="")
    signed_by_doctor_name = models.CharField(max_length=200, blank=True, default="")
    signature_hash = models.CharField(
        max_length=128,
        blank=True,
        default="",
        help_text="SHA-256 cryptographic tamper-evident digest"
    )

    class Meta:
        db_table = "hms_clinical_encounters"
        unique_together = ("tenant", "encounter_number")
        indexes = [
            models.Index(fields=["tenant", "patient", "encounter_datetime"]),
            models.Index(fields=["tenant", "doctor_id", "status"]),
        ]
        ordering = ["-encounter_datetime"]

    def __str__(self):
        return f"{self.encounter_number} - {self.patient.full_name} ({self.status})"

    def can_modify(self) -> bool:
        """Returns True only if the record is still in draft state."""
        return self.status == "IN_PROGRESS" and not self.is_signed

    def compute_signature_hash(self, doctor_id: str, timestamp_str: str) -> str:
        """Computes deterministic SHA-256 checksum over encounter clinical payload."""
        content = (
            f"{self.id}:{self.tenant_id}:{self.patient_id}:"
            f"{self.chief_complaint}:{self.subjective_notes}:"
            f"{self.objective_findings}:{self.assessment}:{self.plan}:"
            f"{doctor_id}:{timestamp_str}"
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def sign_encounter(self, doctor_id: str, doctor_name: str) -> str:
        """
        Signs and finalizes the encounter.
        Once signed, clinical documentation is immutable.
        """
        if self.is_signed or self.status in ["SIGNED", "AMENDED"]:
            raise ValidationError("Clinical encounter is already signed and cannot be re-signed.")

        now = timezone.now()
        timestamp_str = now.isoformat()
        digest = self.compute_signature_hash(doctor_id, timestamp_str)

        self.is_signed = True
        self.status = "SIGNED"
        self.signed_at = now
        self.signed_by_doctor_id = doctor_id
        self.signed_by_doctor_name = doctor_name
        self.signature_hash = digest
        self.save(update_fields=[
            "is_signed", "status", "signed_at",
            "signed_by_doctor_id", "signed_by_doctor_name", "signature_hash", "updated_at"
        ])
        return digest


class ClinicalAmendment(TenantAwareModel):
    """
    Versioned addendum attached to signed encounters.
    Maintains an auditable trail of corrections and late clinical entries.
    """
    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.CASCADE,
        related_name="amendments"
    )
    amendment_sequence = models.PositiveIntegerField(default=1)
    author_id = models.CharField(max_length=100)
    author_name = models.CharField(max_length=200)
    reason = models.TextField(help_text="Clinical justification for addendum")
    addendum_notes = models.TextField(help_text="Supplemental observations or amended clinical data")
    previous_snapshot_hash = models.CharField(max_length=128)
    signature_hash = models.CharField(max_length=128, blank=True, default="")

    class Meta:
        db_table = "hms_clinical_amendments"
        unique_together = ("encounter", "amendment_sequence")
        ordering = ["encounter", "amendment_sequence"]

    def __str__(self):
        return f"Addendum #{self.amendment_sequence} to {self.encounter.encounter_number}"

    def save(self, *args, **kwargs):
        if not self.signature_hash:
            payload = f"{self.encounter_id}:{self.amendment_sequence}:{self.author_id}:{self.reason}:{self.addendum_notes}"
            self.signature_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        super().save(*args, **kwargs)
        # Mark parent encounter status as AMENDED
        if self.encounter.status != "AMENDED":
            self.encounter.status = "AMENDED"
            self.encounter.save(update_fields=["status", "updated_at"])


class ClinicalDiagnosis(TenantAwareModel):
    """
    ICD-10 clinical diagnoses assigned during encounters.
    """
    DIAGNOSIS_TYPE_CHOICES = [
        ("PRIMARY", "Primary Diagnosis"),
        ("SECONDARY", "Secondary / Comorbidity"),
        ("DIFFERENTIAL", "Differential Diagnosis"),
        ("PROVISIONAL", "Provisional Diagnosis"),
    ]

    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.CASCADE,
        related_name="diagnoses"
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="clinical_diagnoses"
    )
    icd10_code = models.CharField(max_length=20, db_index=True)
    diagnosis_name = models.CharField(max_length=255)
    diagnosis_type = models.CharField(
        max_length=30,
        choices=DIAGNOSIS_TYPE_CHOICES,
        default="PRIMARY"
    )
    clinical_notes = models.TextField(blank=True, default="")
    diagnosed_by_doctor_id = models.CharField(max_length=100)
    is_chronic = models.BooleanField(default=False)
    onset_date = models.DateField(null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "hms_clinical_diagnoses"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.icd10_code}] {self.diagnosis_name} ({self.diagnosis_type})"


class PatientAllergy(TenantAwareModel):
    """
    Patient allergy profile with clinical severity grading and reaction profiles.
    Used for automated medication prescription cross-checking.
    """
    ALLERGY_TYPE_CHOICES = [
        ("DRUG", "Drug Allergy"),
        ("FOOD", "Food Allergy"),
        ("ENVIRONMENTAL", "Environmental Allergy"),
        ("LATEX", "Latex / Material Allergy"),
    ]

    SEVERITY_CHOICES = [
        ("MILD", "Mild (Rash, Pruritus, Mild Flushing)"),
        ("MODERATE", "Moderate (Urticaria, Facial Angioedema, Wheezing)"),
        ("SEVERE", "Severe (Bronchospasm, Dyspnea, Hypotension)"),
        ("ANAPHYLAXIS", "Life-Threatening Anaphylaxis (Airway Compromise, Shock)"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="clinical_allergies"
    )
    allergen = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Allergenic agent name, e.g. Penicillin, Sulfa, Aspirin"
    )
    allergy_type = models.CharField(
        max_length=30,
        choices=ALLERGY_TYPE_CHOICES,
        default="DRUG"
    )
    severity = models.CharField(
        max_length=30,
        choices=SEVERITY_CHOICES,
        default="MODERATE"
    )
    reaction_description = models.TextField(blank=True, default="")
    recorded_by_id = models.CharField(max_length=100)
    recorded_by_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hms_patient_allergies"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient.full_name} - {self.allergen} ({self.severity})"


class ElectronicPrescription(TenantAwareModel):
    """
    Electronic Medical Prescription (eRx) header.
    """
    STATUS_CHOICES = [
        ("ACTIVE", "Active / Valid"),
        ("DISPENSED", "Fully Dispensed"),
        ("CANCELLED", "Cancelled"),
        ("EXPIRED", "Expired"),
    ]

    prescription_number = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unique Prescription Tracking ID, e.g. RX-2026-000001"
    )
    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prescriptions"
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="clinical_prescriptions"
    )
    prescriber_id = models.CharField(max_length=100, db_index=True)
    prescriber_name = models.CharField(max_length=200)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="ACTIVE")
    prescribed_date = models.DateTimeField(default=timezone.now, db_index=True)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "hms_electronic_prescriptions"
        unique_together = ("tenant", "prescription_number")
        ordering = ["-prescribed_date"]

    def __str__(self):
        return f"{self.prescription_number} for {self.patient.full_name} ({self.status})"


class PrescriptionItem(TenantAwareModel):
    """
    Individual medication order line item within an Electronic Prescription.
    """
    ROUTE_CHOICES = [
        ("ORAL", "Oral (PO)"),
        ("IV", "Intravenous (IV)"),
        ("IM", "Intramuscular (IM)"),
        ("SUBCUTANEOUS", "Subcutaneous (SC)"),
        ("TOPICAL", "Topical"),
        ("INHALATION", "Inhalation"),
        ("OPHTHALMIC", "Ophthalmic Drops"),
    ]

    prescription = models.ForeignKey(
        ElectronicPrescription,
        on_delete=models.CASCADE,
        related_name="items"
    )
    medication_name = models.CharField(max_length=255, db_index=True)
    generic_name = models.CharField(max_length=255, blank=True, default="")
    dosage = models.CharField(max_length=100, help_text="e.g. 500 mg, 10 ml")
    route = models.CharField(max_length=30, choices=ROUTE_CHOICES, default="ORAL")
    frequency = models.CharField(max_length=50, help_text="e.g. Once Daily (OD), Twice Daily (BID), PRN")
    duration_days = models.PositiveIntegerField(default=5)
    total_quantity = models.PositiveIntegerField(default=10)
    instructions = models.TextField(blank=True, default="Take after food with water")
    is_dispensed = models.BooleanField(default=False)

    class Meta:
        db_table = "hms_prescription_items"
        ordering = ["medication_name"]

    def __str__(self):
        return f"{self.medication_name} {self.dosage} ({self.frequency}) x {self.duration_days}d"


class NursingObservation(TenantAwareModel):
    """
    Inpatient and Triage Nursing Flowsheet with automated MEWS scoring.
    """
    AVPU_CHOICES = [
        ("ALERT", "Alert"),
        ("VOICE", "Responds to Voice"),
        ("PAIN", "Responds to Pain"),
        ("UNRESPONSIVE", "Unresponsive"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="nursing_observations"
    )
    admission = models.ForeignKey(
        Admission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nursing_observations"
    )
    nurse_id = models.CharField(max_length=100)
    nurse_name = models.CharField(max_length=200)
    recorded_at = models.DateTimeField(default=timezone.now, db_index=True)

    # Vital Signs
    systolic_bp = models.PositiveIntegerField(default=120, help_text="Systolic Blood Pressure (mmHg)")
    diastolic_bp = models.PositiveIntegerField(default=80, help_text="Diastolic Blood Pressure (mmHg)")
    heart_rate = models.PositiveIntegerField(default=75, help_text="Heart Rate (beats/min)")
    respiratory_rate = models.PositiveIntegerField(default=16, help_text="Respiratory Rate (breaths/min)")
    temperature_celsius = models.DecimalField(max_digits=4, decimal_places=1, default=36.8, help_text="Body Temp (°C)")
    oxygen_saturation = models.PositiveIntegerField(default=98, help_text="SpO2 percentage (0-100)")
    avpu_score = models.CharField(max_length=20, choices=AVPU_CHOICES, default="ALERT")
    pain_score = models.PositiveIntegerField(default=0, help_text="Wong-Baker Scale (0-10)")

    # Early Warning Calculation
    mews_score = models.PositiveIntegerField(default=0, help_text="Modified Early Warning Score")
    clinical_notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "hms_nursing_observations"
        ordering = ["-recorded_at"]

    def calculate_mews(self) -> int:
        """
        Calculates Modified Early Warning Score (MEWS) based on standardized clinical criteria.
        Scores: 0-2 (Normal), 3-4 (Watch closely), >= 5 (Clinical Trigger / Medical Emergency Team).
        """
        score = 0
        # Systolic BP
        sbp = self.systolic_bp
        if sbp <= 70:
            score += 3
        elif sbp <= 80:
            score += 2
        elif sbp <= 100:
            score += 1
        elif sbp >= 200:
            score += 2

        # Heart Rate
        hr = self.heart_rate
        if hr <= 40:
            score += 2
        elif hr <= 50:
            score += 1
        elif hr >= 130:
            score += 3
        elif hr >= 111:
            score += 2
        elif hr >= 101:
            score += 1

        # Respiratory Rate
        rr = self.respiratory_rate
        if rr <= 8:
            score += 2
        elif rr >= 30:
            score += 3
        elif rr >= 21:
            score += 2
        elif rr >= 15:
            score += 1

        # Temperature
        temp = float(self.temperature_celsius)
        if temp <= 35.0:
            score += 2
        elif temp >= 38.5:
            score += 2

        # AVPU Score
        if self.avpu_score == "VOICE":
            score += 1
        elif self.avpu_score == "PAIN":
            score += 2
        elif self.avpu_score == "UNRESPONSIVE":
            score += 3

        return score

    def save(self, *args, **kwargs):
        self.mews_score = self.calculate_mews()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.full_name} Vitals (MEWS: {self.mews_score}) at {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"


class FluidBalanceRecord(TenantAwareModel):
    """
    Intake and output volume accounting for critically ill or post-op inpatients.
    """
    SHIFT_CHOICES = [
        ("MORNING", "Morning Shift (07:00 - 15:00)"),
        ("EVENING", "Evening Shift (15:00 - 23:00)"),
        ("NIGHT", "Night Shift (23:00 - 07:00)"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="fluid_balances"
    )
    admission = models.ForeignKey(
        Admission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fluid_balances"
    )
    recorded_at = models.DateTimeField(default=timezone.now, db_index=True)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, default="MORNING")

    # Intake
    oral_intake_ml = models.PositiveIntegerField(default=0)
    iv_intake_ml = models.PositiveIntegerField(default=0)

    # Output
    urine_output_ml = models.PositiveIntegerField(default=0)
    drain_output_ml = models.PositiveIntegerField(default=0)

    # Calculated Balance
    net_balance_ml = models.IntegerField(default=0)
    recorded_by_name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "hms_fluid_balances"
        ordering = ["-recorded_at"]

    def save(self, *args, **kwargs):
        total_in = self.oral_intake_ml + self.iv_intake_ml
        total_out = self.urine_output_ml + self.drain_output_ml
        self.net_balance_ml = total_in - total_out
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.full_name} Fluid Net: {self.net_balance_ml} mL ({self.shift})"


class EMARRecord(TenantAwareModel):
    """
    Electronic Medication Administration Record (eMAR) with 5-rights bedside safety verification.
    """
    STATUS_CHOICES = [
        ("PENDING", "Pending Administration"),
        ("GIVEN", "Administered / Given"),
        ("REFUSED", "Refused by Patient"),
        ("HELD", "Clinically Held / Withheld"),
        ("MISSED", "Missed Dose"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="emar_records"
    )
    prescription_item = models.ForeignKey(
        PrescriptionItem,
        on_delete=models.CASCADE,
        related_name="administrations"
    )
    scheduled_time = models.DateTimeField(default=timezone.now)
    administered_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    nurse_id = models.CharField(max_length=100)
    nurse_name = models.CharField(max_length=200)
    five_rights_verified = models.BooleanField(
        default=True,
        help_text="Right Patient, Right Drug, Right Dose, Right Route, Right Time"
    )
    notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "hms_emar_records"
        ordering = ["scheduled_time"]

    def __str__(self):
        return f"{self.prescription_item.medication_name} ({self.status}) for {self.patient.full_name}"


class SBARHandover(TenantAwareModel):
    """
    Clinical Nursing and Physician Shift Handover based on the evidence-based SBAR framework.
    """
    CODE_STATUS_CHOICES = [
        ("FULL_CODE", "Full Code"),
        ("DNR", "Do Not Resuscitate (DNR)"),
        ("DNI", "Do Not Intubate (DNI)"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="sbar_handovers"
    )
    admission = models.ForeignKey(
        Admission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sbar_handovers"
    )
    giving_nurse_id = models.CharField(max_length=100)
    giving_nurse_name = models.CharField(max_length=200)
    receiving_nurse_id = models.CharField(max_length=100)
    receiving_nurse_name = models.CharField(max_length=200)
    handover_time = models.DateTimeField(default=timezone.now, db_index=True)
    shift = models.CharField(max_length=50)

    # SBAR Components
    situation = models.TextField(help_text="Current clinical problem and acuity")
    background = models.TextField(help_text="Admitting diagnosis, surgical history, allergies")
    assessment = models.TextField(help_text="Current vital trends, MEWS score, IV access, lab results")
    recommendation = models.TextField(help_text="Required interventions, pending tests, escalation triggers")
    code_status = models.CharField(max_length=20, choices=CODE_STATUS_CHOICES, default="FULL_CODE")

    class Meta:
        db_table = "hms_sbar_handovers"
        ordering = ["-handover_time"]

    def __str__(self):
        return f"SBAR Handover for {self.patient.full_name} ({self.shift}) - {self.handover_time.strftime('%Y-%m-%d %H:%M')}"


class DischargeSummary(TenantAwareModel):
    """
    Comprehensive Inpatient Discharge Summary with physician signature and warning signs.
    """
    DISCHARGE_CONDITION_CHOICES = [
        ("STABLE", "Stable / Improved"),
        ("CURED", "Cured"),
        ("CRITICAL", "Guarded / Critical"),
        ("LAMA", "Left Against Medical Advice (LAMA)"),
        ("TRANSFERRED", "Transferred to Higher Center"),
        ("DECEASED", "Deceased"),
    ]

    summary_number = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unique Discharge Code, e.g. DCS-2026-000001"
    )
    admission = models.ForeignKey(
        Admission,
        on_delete=models.PROTECT,
        related_name="clinical_discharge_summaries"
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="discharge_summaries"
    )
    author_doctor_id = models.CharField(max_length=100)
    author_doctor_name = models.CharField(max_length=200)
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(default=timezone.now)
    discharge_condition = models.CharField(
        max_length=30,
        choices=DISCHARGE_CONDITION_CHOICES,
        default="STABLE"
    )

    primary_diagnosis = models.TextField()
    hospital_course = models.TextField(help_text="Summary of hospital stay, treatments, surgeries, and clinical response")
    discharge_medications = models.TextField(help_text="Prescribed discharge medications with dosages and duration")
    diet_and_lifestyle = models.TextField(blank=True, default="")
    follow_up_instructions = models.TextField(help_text="Next review date, clinic, and doctor instructions")
    warning_signs_red_flags = models.TextField(help_text="Emergency warning signs requiring immediate hospital return")

    is_signed = models.BooleanField(default=False)
    signed_at = models.DateTimeField(null=True, blank=True)
    signature_hash = models.CharField(max_length=128, blank=True, default="")

    class Meta:
        db_table = "hms_discharge_summaries"
        unique_together = ("tenant", "summary_number")
        ordering = ["-discharge_date"]

    def sign(self, doctor_id: str, doctor_name: str) -> str:
        """Signs and locks the discharge summary."""
        now = timezone.now()
        payload = f"{self.id}:{self.summary_number}:{self.primary_diagnosis}:{self.hospital_course}:{doctor_id}:{now.isoformat()}"
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self.is_signed = True
        self.signed_at = now
        self.signature_hash = digest
        self.save(update_fields=["is_signed", "signed_at", "signature_hash", "updated_at"])
        return digest

    def __str__(self):
        return f"{self.summary_number} - {self.patient.full_name} ({self.discharge_condition})"


class ClinicalReferral(TenantAwareModel):
    """
    Inter-departmental and specialty clinical consult referrals.
    """
    URGENCY_CHOICES = [
        ("ROUTINE", "Routine (Within 3-5 days)"),
        ("URGENT", "Urgent (Within 24-48 hours)"),
        ("STAT", "Immediate / STAT (Emergency)"),
    ]

    STATUS_CHOICES = [
        ("REQUESTED", "Requested"),
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("DECLINED", "Declined"),
    ]

    referral_number = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unique Referral Code, e.g. REF-2026-000001"
    )
    encounter = models.ForeignKey(
        ClinicalEncounter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals"
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="referrals"
    )
    referring_doctor_name = models.CharField(max_length=200)
    target_specialty = models.CharField(max_length=100)
    target_doctor_name = models.CharField(max_length=200, blank=True, default="")
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default="ROUTINE")
    clinical_reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="REQUESTED")
    consultant_reply = models.TextField(blank=True, default="")

    class Meta:
        db_table = "hms_clinical_referrals"
        unique_together = ("tenant", "referral_number")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.referral_number}: {self.patient.full_name} -> {self.target_specialty} ({self.status})"


class ClinicalTemplate(TenantAwareModel):
    """
    Configurable documentation templates for clinical specialties (Cardiology, Surgery, etc.).
    """
    TEMPLATE_TYPE_CHOICES = [
        ("SOAP", "SOAP Clinical Note"),
        ("PROCEDURE", "Procedure / Operative Note"),
        ("DISCHARGE", "Discharge Note"),
        ("HISTORY_PHYSICAL", "Comprehensive History & Physical"),
    ]

    title = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100)
    template_type = models.CharField(
        max_length=30,
        choices=TEMPLATE_TYPE_CHOICES,
        default="SOAP"
    )
    content_json = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hms_clinical_templates"
        ordering = ["specialty", "title"]

    def __str__(self):
        return f"{self.title} ({self.specialty} - {self.template_type})"
