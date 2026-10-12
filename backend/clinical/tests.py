import uuid
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from admissions.models import Ward, Room, Bed, Admission
from appointments.models import Appointment
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


class ClinicalManagementTests(TestCase):
    """
    Automated test suite verifying Member 3 Clinical Management:
    - Multi-tenant query isolation
    - SOAP clinical notes & auto-numbering
    - Cryptographic signing & immutability enforcement
    - Versioned amendments/addenda
    - Allergy conflict interception
    - Automated MEWS calculation
    - Inpatient discharge summaries
    """

    def setUp(self):
        self.client = APIClient()

        # Tenant A (Apollo General)
        self.tenant_a = Tenant.objects.create(
            name="Apollo General Hospital",
            slug="apollo-general",
            mrn_prefix="APL"
        )
        self.branch_a = HospitalBranch.objects.create(
            tenant=self.tenant_a,
            name="Apollo Main Campus",
            code="MAIN"
        )
        self.dept_cardio_a = Department.objects.create(
            tenant=self.tenant_a,
            branch=self.branch_a,
            name="Cardiology",
            code="CARD",
            is_clinical=True
        )

        # Tenant B (Fortis Care)
        self.tenant_b = Tenant.objects.create(
            name="Fortis Care Hospital",
            slug="fortis-care",
            mrn_prefix="FTC"
        )
        self.branch_b = HospitalBranch.objects.create(
            tenant=self.tenant_b,
            name="Fortis North",
            code="NORTH"
        )

        # Patients
        self.patient_a = Patient.objects.create(
            tenant=self.tenant_a,
            mrn="APL-2026-000001",
            first_name="Ramesh",
            last_name="Sharma",
            gender="MALE",
            blood_group="O+"
        )
        self.patient_b = Patient.objects.create(
            tenant=self.tenant_b,
            mrn="FTC-2026-000001",
            first_name="Pooja",
            last_name="Patel",
            gender="FEMALE",
            blood_group="B+"
        )

    def test_clinical_encounter_creation(self):
        """Tests encounter creation with auto-generated tracking code."""
        encounter = ClinicalEncounter.objects.create(
            tenant=self.tenant_a,
            encounter_number="ENC-2026-000001",
            patient=self.patient_a,
            doctor_id="DOC-101",
            doctor_name="Dr. Anil Mehta",
            department=self.dept_cardio_a,
            encounter_type="OPD",
            chief_complaint="Chest tightness upon exertion for 3 days",
            subjective_notes="Patient reports dull retrosternal pain radiating to left jaw.",
            objective_findings="BP 145/92 mmHg, Pulse 88 bpm. Heart sounds regular, no S3/S4 gallop.",
            assessment="Suspected Unstable Angina. Rule out NSTEMI.",
            plan="Perform urgent 12-lead ECG, Troponin-I assay. Start Aspirin 75mg."
        )
        self.assertEqual(encounter.status, "IN_PROGRESS")
        self.assertFalse(encounter.is_signed)
        self.assertTrue(encounter.can_modify())

    def test_encounter_cryptographic_signing_and_immutability(self):
        """Tests that signing generates a SHA-256 hash and prevents direct modifications."""
        encounter = ClinicalEncounter.objects.create(
            tenant=self.tenant_a,
            encounter_number="ENC-2026-000002",
            patient=self.patient_a,
            doctor_id="DOC-101",
            doctor_name="Dr. Anil Mehta",
            chief_complaint="Routine hypertensive follow-up",
            subjective_notes="Adherent to medications. No headaches or visual changes.",
            objective_findings="BP 128/82 mmHg, HR 72 bpm.",
            assessment="Essential Hypertension, well controlled.",
            plan="Continue Telmisartan 40mg OD. Review in 3 months."
        )

        # Sign encounter
        digest = encounter.sign_encounter(doctor_id="DOC-101", doctor_name="Dr. Anil Mehta")
        self.assertTrue(encounter.is_signed)
        self.assertEqual(encounter.status, "SIGNED")
        self.assertIsNotNone(encounter.signed_at)
        self.assertEqual(len(digest), 64) # Valid SHA-256 64-char hex string
        self.assertFalse(encounter.can_modify())

        # API update attempt must be rejected
        self.client.defaults["HTTP_X_TENANT_ID"] = str(self.tenant_a.id)
        response = self.client.patch(
            f"/api/clinical/encounters/{encounter.id}/",
            {"chief_complaint": "Unauthorized alteration"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("immutable", response.data["error"])

    def test_clinical_amendment_versioning(self):
        """Tests appending versioned addendum to an already finalized encounter."""
        encounter = ClinicalEncounter.objects.create(
            tenant=self.tenant_a,
            encounter_number="ENC-2026-000003",
            patient=self.patient_a,
            doctor_id="DOC-101",
            doctor_name="Dr. Anil Mehta",
            chief_complaint="Post-op assessment"
        )
        encounter.sign_encounter(doctor_id="DOC-101", doctor_name="Dr. Anil Mehta")

        # Amend via API
        self.client.defaults["HTTP_X_TENANT_ID"] = str(self.tenant_a.id)
        response = self.client.post(
            f"/api/clinical/encounters/{encounter.id}/amend/",
            {
                "author_id": "DOC-101",
                "author_name": "Dr. Anil Mehta",
                "reason": "Late lab report reconciliation",
                "addendum_notes": "Troponin-I returned negative at 0.01 ng/mL. Patient discharged safely."
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        encounter.refresh_from_db()
        self.assertEqual(encounter.status, "AMENDED")
        self.assertEqual(encounter.amendments.count(), 1)
        self.assertEqual(encounter.amendments.first().amendment_sequence, 1)

    def test_multi_tenant_isolation(self):
        """Proves Hospital B cannot view or access Hospital A's clinical records."""
        encounter_a = ClinicalEncounter.objects.create(
            tenant=self.tenant_a,
            encounter_number="ENC-APL-001",
            patient=self.patient_a,
            doctor_id="DOC-A",
            doctor_name="Dr. Apollo",
            chief_complaint="Confidential record"
        )

        # Hospital B attempts to fetch Tenant A encounter
        self.client.defaults["HTTP_X_TENANT_ID"] = str(self.tenant_b.id)
        response = self.client.get(f"/api/clinical/encounters/{encounter_a.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Hospital B list encounters
        list_response = self.client.get("/api/clinical/encounters/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        # Should be empty or only contain Tenant B encounters
        results = list_response.data.get("results", list_response.data)
        self.assertEqual(len(results), 0)

    def test_allergy_conflict_interception(self):
        """Tests drug-allergy conflict checking."""
        # Patient A has severe Penicillin allergy
        PatientAllergy.objects.create(
            tenant=self.tenant_a,
            patient=self.patient_a,
            allergen="Penicillin",
            allergy_type="DRUG",
            severity="ANAPHYLAXIS",
            reaction_description="Laryngeal edema and severe hypotension in 2021",
            recorded_by_id="NURSE-01",
            recorded_by_name="Nurse Sarah"
        )

        self.client.defaults["HTTP_X_TENANT_ID"] = str(self.tenant_a.id)
        conflict_check = self.client.post(
            "/api/clinical/allergies/check_conflict/",
            {
                "patient_id": str(self.patient_a.id),
                "drug_name": "Amoxicillin-Penicillin 500mg"
            }
        )
        self.assertEqual(conflict_check.status_code, status.HTTP_200_OK)
        self.assertTrue(conflict_check.data["has_conflict"])
        self.assertEqual(len(conflict_check.data["conflicts"]), 1)
        self.assertEqual(conflict_check.data["conflicts"][0]["severity"], "ANAPHYLAXIS")

    def test_automated_mews_calculation(self):
        """Tests that Nursing Observation automatically calculates correct MEWS score."""
        # Normal observation
        obs_normal = NursingObservation.objects.create(
            tenant=self.tenant_a,
            patient=self.patient_a,
            nurse_id="NUR-50",
            nurse_name="Nurse Brenda",
            systolic_bp=120,
            heart_rate=72,
            respiratory_rate=16,
            temperature_celsius=36.8,
            oxygen_saturation=98,
            avpu_score="ALERT"
        )
        self.assertEqual(obs_normal.mews_score, 1) # RR 16 contributes +1

        # High-risk critical observation
        obs_critical = NursingObservation.objects.create(
            tenant=self.tenant_a,
            patient=self.patient_a,
            nurse_id="NUR-50",
            nurse_name="Nurse Brenda",
            systolic_bp=65,       # +3 (SBP <= 70)
            heart_rate=135,       # +3 (HR >= 130)
            respiratory_rate=32,  # +3 (RR >= 30)
            temperature_celsius=39.1, # +2 (Temp >= 38.5)
            oxygen_saturation=86,
            avpu_score="PAIN"     # +2 (Responds to pain)
        )
        # Expected score: 3 + 3 + 3 + 2 + 2 = 13
        self.assertEqual(obs_critical.mews_score, 13)

    def test_fluid_balance_calculation(self):
        """Tests intake vs output volume balancing."""
        fb = FluidBalanceRecord.objects.create(
            tenant=self.tenant_a,
            patient=self.patient_a,
            shift="MORNING",
            oral_intake_ml=500,
            iv_intake_ml=1000,     # Total intake = 1500
            urine_output_ml=800,
            drain_output_ml=200,    # Total output = 1000
            recorded_by_name="Nurse Brenda"
        )
        self.assertEqual(fb.net_balance_ml, 500)

    def test_discharge_summary_lifecycle(self):
        """Tests creating and digitally signing an inpatient discharge summary."""
        ward = Ward.objects.create(tenant=self.tenant_a, branch=self.branch_a, name="Cardiology Ward")
        room = Room.objects.create(tenant=self.tenant_a, ward=ward, room_number="301")
        bed = Bed.objects.create(tenant=self.tenant_a, room=room, bed_number="301-A", status="OCCUPIED")
        admission = Admission.objects.create(
            tenant=self.tenant_a,
            admission_number="IPD-2026-0001",
            patient=self.patient_a,
            branch=self.branch_a,
            department=self.dept_cardio_a,
            admitting_doctor_id="DOC-101",
            admitting_doctor_name="Dr. Anil Mehta",
            bed=bed,
            admission_diagnosis="Acute Coronary Syndrome"
        )

        summary = DischargeSummary.objects.create(
            tenant=self.tenant_a,
            summary_number="DCS-2026-000001",
            admission=admission,
            patient=self.patient_a,
            author_doctor_id="DOC-101",
            author_doctor_name="Dr. Anil Mehta",
            admission_date=timezone.now(),
            discharge_condition="STABLE",
            primary_diagnosis="NSTEMI - Successfully revascularized with DES to LAD",
            hospital_course="Coronary angiography performed on Day 1. Uncomplicated stay. Echocardiogram LVEF 55%.",
            discharge_medications="Aspirin 75mg OD, Clopidogrel 75mg OD, Atorvastatin 80mg ON, Metoprolol 25mg BD",
            diet_and_lifestyle="Low sodium, cardiac rehabilitation exercise program",
            follow_up_instructions="Cardiology OPD in 2 weeks with repeat ECG and renal panel",
            warning_signs_red_flags="Recurrent chest pain, diaphoresis, shortness of breath -> Call Emergency"
        )

        self.assertFalse(summary.is_signed)
        digest = summary.sign(doctor_id="DOC-101", doctor_name="Dr. Anil Mehta")
        self.assertTrue(summary.is_signed)
        self.assertIsNotNone(summary.signed_at)
        self.assertEqual(len(digest), 64)
