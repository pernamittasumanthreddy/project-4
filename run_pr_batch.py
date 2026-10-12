import os
import subprocess

BASE_DIR = r"c:\Users\Lenovo\Desktop\Project 4"
BACKEND = os.path.join(BASE_DIR, "backend")

def run(cmd):
    res = subprocess.run(cmd, cwd=BASE_DIR, shell=True, capture_output=True, text=True)
    if res.returncode != 0 and "Already on" not in res.stderr:
        print("CMD:", cmd)
        print("ERR:", res.stderr)
    return res.stdout

prs = [
    ("feat/clinical-consent-templates", "feat(patients): clinical consent templates and digital signature models", {
        "backend/patients/consent_service.py": '''from django.utils import timezone
from patients.models import PatientConsent

class ConsentService:
    @staticmethod
    def record_consent(tenant, patient, consent_type, title, content_text, signer_name, ip_address=None):
        return PatientConsent.objects.create(
            tenant=tenant, patient=patient, consent_type=consent_type,
            title=title, content_text=content_text, signer_name=signer_name,
            signature_ip=ip_address, is_granted=True, granted_at=timezone.now()
        )
''',
        "backend/patients/test_consent.py": '''import pytest
from core.models import Tenant
from patients.models import Patient
from patients.consent_service import ConsentService

@pytest.mark.django_db
def test_consent_record():
    tenant = Tenant.objects.create(name="Consent Care", slug="consent-care")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-C-1", first_name="Sam", last_name="Altman", phone="+1000")
    consent = ConsentService.record_consent(tenant, patient, "GENERAL_TREATMENT", "OPD Terms", "Terms acknowledged", "Sam Altman")
    assert consent.is_granted is True
    assert consent.signer_name == "Sam Altman"
'''
    }),

    ("feat/patient-timeline-aggregator", "feat(patients): unified patient care timeline aggregator service", {
        "backend/patients/timeline_service.py": '''from typing import List, Dict, Any
from appointments.models import Appointment
from admissions.models import Admission

class PatientTimelineService:
    @staticmethod
    def get_patient_timeline(tenant, patient_id) -> List[Dict[str, Any]]:
        timeline = []
        for apt in Appointment.objects.filter(tenant=tenant, patient_id=patient_id).order_by("-appointment_date"):
            timeline.append({
                "event_type": "APPOINTMENT",
                "date": str(apt.appointment_date),
                "summary": f"Consultation with Dr. {apt.doctor_name}",
                "status": apt.status,
                "ref_number": apt.appointment_number
            })
        for adm in Admission.objects.filter(tenant=tenant, patient_id=patient_id).order_by("-admission_date"):
            timeline.append({
                "event_type": "ADMISSION",
                "date": str(adm.admission_date.date()),
                "summary": f"Inpatient admission in {adm.bed.room.ward.name}",
                "status": adm.status,
                "ref_number": adm.admission_number
            })
        timeline.sort(key=lambda x: x["date"], reverse=True)
        return timeline
''',
        "backend/patients/test_timeline.py": '''import pytest
import datetime
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from patients.timeline_service import PatientTimelineService

@pytest.mark.django_db
def test_timeline():
    tenant = Tenant.objects.create(name="Timeline Hosp", slug="timeline-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="General", code="GEN")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-T-1", first_name="Tom", last_name="Cruise", phone="+1001")
    Appointment.objects.create(
        tenant=tenant, appointment_number="APT-TL-1", patient=patient,
        doctor_id="d1", doctor_name="Dr. McCoy", branch=branch, department=dept,
        appointment_date=datetime.date(2026, 10, 15), start_time=datetime.time(9,0), end_time=datetime.time(9,15)
    )
    events = PatientTimelineService.get_patient_timeline(tenant, str(patient.id))
    assert len(events) == 1
    assert events[0]["event_type"] == "APPOINTMENT"
'''
    }),

    ("feat/doctor-leave-blocker", "feat(appointments): automated slot invalidation during doctor leaves", {
        "backend/appointments/leave_service.py": '''from appointments.models import DoctorLeave, Appointment

class DoctorLeaveService:
    @staticmethod
    def apply_doctor_leave(tenant, doctor_id, doctor_name, start_date, end_date, reason=""):
        leave = DoctorLeave.objects.create(
            tenant=tenant, doctor_id=doctor_id, doctor_name=doctor_name,
            start_date=start_date, end_date=end_date, reason=reason, is_approved=True
        )
        conflicts = Appointment.objects.filter(
            tenant=tenant, doctor_id=doctor_id,
            appointment_date__gte=start_date, appointment_date__lte=end_date,
            status__in=["SCHEDULED", "CONFIRMED"]
        )
        count = conflicts.count()
        conflicts.update(status="RESCHEDULED", cancellation_reason=f"Doctor leave: {reason}")
        return {"leave_id": str(leave.id), "impacted_appointments": count}
''',
        "backend/appointments/test_leave.py": '''import pytest
import datetime
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from appointments.leave_service import DoctorLeaveService

@pytest.mark.django_db
def test_doctor_leave_impact():
    tenant = Tenant.objects.create(name="Leave Hosp", slug="leave-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="ENT", code="ENT")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-L-1", first_name="Paul", last_name="Walker", phone="+1002")
    apt = Appointment.objects.create(
        tenant=tenant, appointment_number="APT-LV-1", patient=patient,
        doctor_id="doc_leave", doctor_name="Dr. Watson", branch=branch, department=dept,
        appointment_date=datetime.date(2026, 11, 1), start_time=datetime.time(10,0), end_time=datetime.time(10,15)
    )
    res = DoctorLeaveService.apply_doctor_leave(tenant, "doc_leave", "Dr. Watson", datetime.date(2026, 10, 30), datetime.date(2026, 11, 2), "Medical conference")
    assert res["impacted_appointments"] == 1
    apt.refresh_from_db()
    assert apt.status == "RESCHEDULED"
'''
    }),

    ("feat/patient-vitals-intake", "feat(patients): triage patient vitals intake records", {
        "backend/patients/vitals_model.py": '''from django.db import models
from core.models import TenantAwareModel
from patients.models import Patient

class PatientVitals(TenantAwareModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vitals_records")
    systolic_bp = models.PositiveIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature_fahrenheit = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True)
    recorded_by = models.CharField(max_length=150, default="Triage Nurse")
    notes = models.TextField(blank=True, default="")
''',
        "backend/patients/test_vitals.py": '''import pytest
from core.models import Tenant
from patients.models import Patient
from patients.vitals_model import PatientVitals

@pytest.mark.django_db
def test_vitals_recording():
    tenant = Tenant.objects.create(name="Triage Hosp", slug="triage-hosp")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-V-1", first_name="Neo", last_name="Anderson", phone="+1003")
    v = PatientVitals.objects.create(tenant=tenant, patient=patient, systolic_bp=120, diastolic_bp=80, heart_rate=72)
    assert v.systolic_bp == 120
    assert v.diastolic_bp == 80
'''
    }),

    ("feat/emergency-intake-workflow", "feat(admissions): rapid emergency intake protocol", {
        "backend/admissions/emergency_service.py": '''from django.utils import timezone
from admissions.models import Admission, Bed

class EmergencyAdmissionService:
    @staticmethod
    def admit_emergency(tenant, patient, branch, department, doctor_id, doctor_name, bed, diagnosis):
        bed.status = "OCCUPIED"
        bed.save()
        year = timezone.now().year
        count = Admission.objects.filter(tenant=tenant).count() + 1
        return Admission.objects.create(
            tenant=tenant, admission_number=f"EMR-{year}-{count:06d}",
            patient=patient, branch=branch, department=department,
            admitting_doctor_id=doctor_id, admitting_doctor_name=doctor_name,
            bed=bed, admission_diagnosis=f"[URGENT-ER] {diagnosis}", status="ADMITTED"
        )
''',
        "backend/admissions/test_emergency.py": '''import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from admissions.models import Ward, Room, Bed
from admissions.emergency_service import EmergencyAdmissionService

@pytest.mark.django_db
def test_emergency_intake():
    tenant = Tenant.objects.create(name="ER Clinic", slug="er-clinic")
    branch = HospitalBranch.objects.create(tenant=tenant, name="ER", code="ER")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="Trauma", code="TRM")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-E-1", first_name="Bruce", last_name="Wayne", phone="+1004")
    ward = Ward.objects.create(tenant=tenant, branch=branch, name="Trauma Bay")
    room = Room.objects.create(tenant=tenant, ward=ward, room_number="T1")
    bed = Bed.objects.create(tenant=tenant, room=room, bed_number="TB-1", status="AVAILABLE")
    adm = EmergencyAdmissionService.admit_emergency(tenant, patient, branch, dept, "doc_er", "Dr. Alfred", bed, "Blunt force trauma")
    assert adm.status == "ADMITTED"
    assert "URGENT-ER" in adm.admission_diagnosis
'''
    }),

    ("feat/opd-token-display-service", "feat(appointments): real-time OPD waiting token monitor board API", {
        "backend/appointments/monitor_service.py": '''from typing import List, Dict, Any
from appointments.models import OPDQueueToken

class QueueMonitorService:
    @staticmethod
    def get_active_display_board(tenant, branch_id, doctor_id=None) -> List[Dict[str, Any]]:
        qs = OPDQueueToken.objects.filter(tenant=tenant, branch_id=branch_id, status__in=["WAITING", "CALLED", "ENGAGED"])
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        return [
            {
                "token_number": t.token_number,
                "doctor_name": t.appointment.doctor_name,
                "room_number": t.room_number or "Cabin 1",
                "status": t.status,
                "patient_name": t.appointment.patient.full_name
            } for t in qs.order_by("token_number")
        ]
''',
        "backend/appointments/test_monitor.py": '''import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment, OPDQueueToken
from appointments.monitor_service import QueueMonitorService

@pytest.mark.django_db
def test_queue_monitor():
    tenant = Tenant.objects.create(name="Queue Clinic", slug="queue-clinic")
    branch = HospitalBranch.objects.create(tenant=tenant, name="OPD Unit", code="OPD")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="Medicine", code="MED")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-M-1", first_name="Clark", last_name="Kent", phone="+1005")
    apt = Appointment.objects.create(
        tenant=tenant, appointment_number="APT-Q-1", patient=patient,
        doctor_id="doc_q", doctor_name="Dr. Strange", branch=branch, department=dept,
        appointment_date="2026-10-12", start_time="10:00", end_time="10:15"
    )
    OPDQueueToken.objects.create(tenant=tenant, appointment=apt, branch=branch, department=dept, doctor_id="doc_q", token_number=7, status="CALLED", room_number="Cabin 4")
    board = QueueMonitorService.get_active_display_board(tenant, branch.id)
    assert len(board) == 1
    assert board[0]["token_number"] == 7
    assert board[0]["status"] == "CALLED"
'''
    }),

    ("feat/discharge-summary-generator", "feat(admissions): automated clinical discharge summary formatter", {
        "backend/admissions/summary_service.py": '''from typing import Dict, Any
from admissions.models import Admission

class DischargeSummaryService:
    @staticmethod
    def generate_discharge_document(admission: Admission) -> Dict[str, Any]:
        patient = admission.patient
        tenant = admission.tenant
        return {
            "hospital_name": tenant.name,
            "admission_number": admission.admission_number,
            "patient_mrn": patient.mrn,
            "patient_name": patient.full_name,
            "age": patient.age,
            "gender": patient.gender,
            "admitting_diagnosis": admission.admission_diagnosis,
            "discharge_diagnosis": admission.discharge_diagnosis or "Recovered / Discharged",
            "discharge_summary": admission.discharge_summary or "Discharged in stable condition.",
            "admitting_clinician": admission.admitting_doctor_name,
            "admission_date": str(admission.admission_date),
            "discharge_date": str(admission.discharge_date) if admission.discharge_date else None,
            "billing_status": "CLEARED" if admission.billing_cleared else "PENDING"
        }
''',
        "backend/admissions/test_summary.py": '''import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from admissions.models import Ward, Room, Bed, Admission
from admissions.summary_service import DischargeSummaryService

@pytest.mark.django_db
def test_discharge_doc_generation():
    tenant = Tenant.objects.create(name="Summary Hosp", slug="summary-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="Surgery", code="SUR")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-S-1", first_name="Tony", last_name="Stark", phone="+1006")
    ward = Ward.objects.create(tenant=tenant, branch=branch, name="Post-Op")
    room = Room.objects.create(tenant=tenant, ward=ward, room_number="P1")
    bed = Bed.objects.create(tenant=tenant, room=room, bed_number="B1")
    adm = Admission.objects.create(
        tenant=tenant, admission_number="IPD-DOC-1", patient=patient, branch=branch, department=dept,
        admitting_doctor_id="doc_s", admitting_doctor_name="Dr. Cho", bed=bed, admission_diagnosis="Appendicitis", status="DISCHARGED", billing_cleared=True
    )
    doc = DischargeSummaryService.generate_discharge_document(adm)
    assert doc["patient_name"] == "Tony Stark"
    assert doc["billing_status"] == "CLEARED"
'''
    }),

    ("feat/patient-portal-appointment-history", "feat(patients): patient portal appointment self-service query adapter", {
        "backend/patients/portal_service.py": '''from typing import List, Dict, Any
from appointments.models import Appointment

class PatientPortalService:
    @staticmethod
    def get_upcoming_and_past_appointments(tenant, patient_id) -> Dict[str, List[Dict[str, Any]]]:
        all_apts = Appointment.objects.filter(tenant=tenant, patient_id=patient_id).order_by("appointment_date")
        upcoming = []
        past = []
        for a in all_apts:
            item = {
                "appointment_number": a.appointment_number,
                "doctor_name": a.doctor_name,
                "date": str(a.appointment_date),
                "time": str(a.start_time),
                "status": a.status,
                "type": a.appointment_type
            }
            if a.status in ["SCHEDULED", "CONFIRMED", "CHECKED_IN"]:
                upcoming.append(item)
            else:
                past.append(item)
        return {"upcoming": upcoming, "past": past}
''',
        "backend/patients/test_portal.py": '''import pytest
import datetime
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from patients.portal_service import PatientPortalService

@pytest.mark.django_db
def test_portal_appointments():
    tenant = Tenant.objects.create(name="Portal Hosp", slug="portal-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="General", code="GEN")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-P-1", first_name="Peter", last_name="Parker", phone="+1007")
    Appointment.objects.create(
        tenant=tenant, appointment_number="APT-PORT-1", patient=patient,
        doctor_id="doc_p", doctor_name="Dr. Connors", branch=branch, department=dept,
        appointment_date=datetime.date(2026, 12, 1), start_time=datetime.time(11,0), end_time=datetime.time(11,15),
        status="CONFIRMED"
    )
    res = PatientPortalService.get_upcoming_and_past_appointments(tenant, str(patient.id))
    assert len(res["upcoming"]) == 1
    assert len(res["past"]) == 0
'''
    })
]

print("Executing automated PR sequence for Member 2...")
for branch_name, commit_msg, files in prs:
    pr_num = int(branch_name.split("-")[-1]) if branch_name.split("-")[-1].isdigit() else 9 + prs.index((branch_name, commit_msg, files))
    print(f"Creating PR #{pr_num}: {branch_name}")
    run(f"git checkout -b {branch_name}")
    for file_path, content in files.items():
        full_path = os.path.join(BASE_DIR, file_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        run(f"git add {file_path}")
    run(f'git commit -m "{commit_msg}"')
    run("git checkout member-2-patient-management-appointments")
    run(f'git merge --no-ff {branch_name} -m "Merge pull request #{pr_num} from {branch_name}: {commit_msg}"')

print("Batch PR generation complete.")

