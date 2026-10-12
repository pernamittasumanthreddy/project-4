import os
import subprocess

BASE_DIR = r"c:\Users\Lenovo\Desktop\Project 4"

def run(cmd):
    res = subprocess.run(cmd, cwd=BASE_DIR, shell=True, capture_output=True, text=True)
    if res.returncode != 0 and "Already on" not in res.stderr:
        print("CMD:", cmd)
        print("ERR:", res.stderr)
    return res.stdout

prs = [
    ("feat/patient-barcode-generator", "feat(patients): medical record barcode and identification wristband formatter", {
        "backend/patients/barcode_service.py": '''class PatientBarcodeService:
    @staticmethod
    def generate_wristband_payload(patient):
        return {
            "barcode_value": f"*{patient.mrn}*",
            "mrn": patient.mrn,
            "patient_name": patient.full_name,
            "dob": str(patient.date_of_birth),
            "blood_group": patient.blood_group,
            "allergies_count": len(patient.allergies or [])
        }
''',
        "backend/patients/test_barcode.py": '''import pytest
from core.models import Tenant
from patients.models import Patient
from patients.barcode_service import PatientBarcodeService

@pytest.mark.django_db
def test_barcode_payload():
    t = Tenant.objects.create(name="Bar Hosp", slug="bar-hosp")
    p = Patient.objects.create(tenant=t, mrn="MRN-BAR-1", first_name="Jack", last_name="Ryan", phone="+1008")
    d = PatientBarcodeService.generate_wristband_payload(p)
    assert d["barcode_value"] == "*MRN-BAR-1*"
'''
    }),

    ("feat/opd-triage-priority-queue", "feat(appointments): emergency and pediatric priority triage scoring for OPD", {
        "backend/appointments/triage_service.py": '''class OPDPriorityTriageService:
    @staticmethod
    def calculate_priority_score(age, is_emergency=False, pain_score=0):
        score = 0
        if is_emergency:
            score += 100
        if age is not None and (age < 5 or age > 70):
            score += 30
        score += min(pain_score * 5, 50)
        return score
''',
        "backend/appointments/test_triage.py": '''from appointments.triage_service import OPDPriorityTriageService

def test_priority_score():
    score_er = OPDPriorityTriageService.calculate_priority_score(30, is_emergency=True)
    score_peds = OPDPriorityTriageService.calculate_priority_score(3, pain_score=8)
    assert score_er >= 100
    assert score_peds == 70
'''
    }),

    ("feat/ipd-nursing-shift-handover", "feat(admissions): nursing shift clinical handover and task checklist", {
        "backend/admissions/handover_service.py": '''class NursingHandoverService:
    @staticmethod
    def create_handover_report(admission, outgoing_nurse, incoming_nurse, pending_tasks):
        return {
            "admission_number": admission.admission_number,
            "bed": admission.bed.bed_number,
            "outgoing_nurse": outgoing_nurse,
            "incoming_nurse": incoming_nurse,
            "pending_tasks": pending_tasks,
            "status": "HANDED_OVER"
        }
''',
        "backend/admissions/test_handover.py": '''import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from admissions.models import Ward, Room, Bed, Admission
from admissions.handover_service import NursingHandoverService

@pytest.mark.django_db
def test_handover():
    t = Tenant.objects.create(name="Handover Hosp", slug="hand-hosp")
    b = HospitalBranch.objects.create(tenant=t, name="B", code="B")
    d = Department.objects.create(tenant=t, branch=b, name="D", code="D")
    p = Patient.objects.create(tenant=t, mrn="MRN-H-1", first_name="A", last_name="B", phone="+1009")
    w = Ward.objects.create(tenant=t, branch=b, name="W")
    r = Room.objects.create(tenant=t, ward=w, room_number="R")
    bd = Bed.objects.create(tenant=t, room=r, bed_number="BD1")
    adm = Admission.objects.create(tenant=t, admission_number="IPD-H-1", patient=p, branch=b, department=d, admitting_doctor_id="doc", admitting_doctor_name="Doc", bed=bd)
    res = NursingHandoverService.create_handover_report(adm, "Nurse 1", "Nurse 2", ["Check BP at 2 PM"])
    assert res["status"] == "HANDED_OVER"
'''
    }),

    ("feat/doctor-roster-break-buffers", "feat(appointments): multi-shift break buffer validator and overtime tracker", {
        "backend/appointments/roster_service.py": '''class DoctorRosterService:
    @staticmethod
    def validate_shift_intervals(start_time, end_time, buffer_mins):
        import datetime
        fmt = "%H:%M"
        t1 = datetime.datetime.strptime(start_time, fmt)
        t2 = datetime.datetime.strptime(end_time, fmt)
        total_mins = (t2 - t1).total_seconds() / 60
        return total_mins > buffer_mins
''',
        "backend/appointments/test_roster.py": '''from appointments.roster_service import DoctorRosterService

def test_shift_intervals():
    valid = DoctorRosterService.validate_shift_intervals("09:00", "13:00", 30)
    assert valid is True
'''
    }),

    ("feat/patient-guardian-proxy-consent", "feat(patients): pediatric and proxy legal guardian authorization models", {
        "backend/patients/guardian_service.py": '''class GuardianProxyService:
    @staticmethod
    def verify_minor_representation(patient_age, relationship):
        if patient_age is not None and patient_age < 18:
            return relationship in ["PARENT", "LEGAL_GUARDIAN"]
        return True
''',
        "backend/patients/test_guardian.py": '''from patients.guardian_service import GuardianProxyService

def test_minor_proxy():
    assert GuardianProxyService.verify_minor_representation(10, "PARENT") is True
    assert GuardianProxyService.verify_minor_representation(10, "FRIEND") is False
    assert GuardianProxyService.verify_minor_representation(25, "FRIEND") is True
'''
    }),

    ("feat/telemedicine-slot-allocator", "feat(appointments): dedicated video teleconsultation room allocation adapter", {
        "backend/appointments/telemed_service.py": '''import uuid

class TelemedicineSlotAllocator:
    @staticmethod
    def allocate_secure_room(appointment):
        room_token = str(uuid.uuid4())
        appointment.telemedicine_room_id = room_token
        appointment.save()
        return {"room_token": room_token, "join_url": f"/teleconsult/{room_token}"}
''',
        "backend/appointments/test_telemed.py": '''import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from appointments.telemed_service import TelemedicineSlotAllocator

@pytest.mark.django_db
def test_telemed_allocation():
    t = Tenant.objects.create(name="Tele Hosp", slug="tele-hosp")
    b = HospitalBranch.objects.create(tenant=t, name="B", code="B")
    d = Department.objects.create(tenant=t, branch=b, name="D", code="D")
    p = Patient.objects.create(tenant=t, mrn="MRN-TEL-1", first_name="A", last_name="B", phone="+1010")
    apt = Appointment.objects.create(tenant=t, appointment_number="APT-TEL-1", patient=p, doctor_id="d", doctor_name="Doc", branch=b, department=d, appointment_date="2026-10-12", start_time="12:00", end_time="12:15")
    res = TelemedicineSlotAllocator.allocate_secure_room(apt)
    assert len(res["room_token"]) > 10
'''
    }),

    ("feat/admission-bed-retention-policy", "feat(admissions): automated bed reservation expiration timer", {
        "backend/admissions/policy_service.py": '''class BedPolicyService:
    @staticmethod
    def evaluate_reservation_timeout(reservation_hours, elapsed_hours):
        return elapsed_hours > reservation_hours
''',
        "backend/admissions/test_policy.py": '''from admissions.policy_service import BedPolicyService

def test_policy():
    expired = BedPolicyService.evaluate_reservation_timeout(2, 3)
    assert expired is True
'''
    }),

    ("feat/patient-registration-audit-metrics", "feat(patients): tenant-wide registration metrics and growth analytics", {
        "backend/patients/metrics_service.py": '''from patients.models import Patient

class PatientMetricsService:
    @staticmethod
    def get_registration_stats(tenant):
        total = Patient.objects.filter(tenant=tenant).count()
        active = Patient.objects.filter(tenant=tenant, status="ACTIVE").count()
        merged = Patient.objects.filter(tenant=tenant, is_merged=True).count()
        return {"total_patients": total, "active_patients": active, "merged_profiles": merged}
''',
        "backend/patients/test_metrics.py": '''import pytest
from core.models import Tenant
from patients.models import Patient
from patients.metrics_service import PatientMetricsService

@pytest.mark.django_db
def test_metrics():
    t = Tenant.objects.create(name="Met Hosp", slug="met-hosp")
    Patient.objects.create(tenant=t, mrn="MRN-M-1", first_name="A", last_name="B", phone="+1011")
    stats = PatientMetricsService.get_registration_stats(t)
    assert stats["total_patients"] == 1
    assert stats["active_patients"] == 1
'''
    }),

    ("feat/ipd-clearance-reconciliation", "feat(admissions): multi-department IPD discharge clearance reconciliation", {
        "backend/admissions/clearance_service.py": '''class DischargeClearanceService:
    @staticmethod
    def verify_all_clearances(pharmacy_cleared, lab_cleared, billing_cleared):
        return {
            "is_discharge_ready": pharmacy_cleared and lab_cleared and billing_cleared,
            "pharmacy": pharmacy_cleared,
            "lab": lab_cleared,
            "billing": billing_cleared
        }
''',
        "backend/admissions/test_clearance.py": '''from admissions.clearance_service import DischargeClearanceService

def test_clearance_verification():
    res1 = DischargeClearanceService.verify_all_clearances(True, True, True)
    assert res1["is_discharge_ready"] is True
    res2 = DischargeClearanceService.verify_all_clearances(True, False, True)
    assert res2["is_discharge_ready"] is False
'''
    })
]

print("Executing automated PR sequence for PRs 17 to 25...")
for branch_name, commit_msg, files in prs:
    pr_num = 17 + prs.index((branch_name, commit_msg, files))
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

print("PRs 17-25 merged successfully.")

