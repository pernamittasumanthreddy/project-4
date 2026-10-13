"""
Enterprise Multi-Tenant Data Seeder for CareTrust HMS Platform.
Populates Core Tenants, Branches, Departments, Patients (MPI), Schedules, Appointments, and Clinical Records.
Zero external API keys required. 100% local database seeding.
"""
import os
import sys
import django
from datetime import date, datetime, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_core.settings')
django.setup()

from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import DoctorSchedule, Appointment, OPDQueueToken
from admissions.models import Ward, Room, Bed, Admission
from clinical.models import ClinicalEncounter, ClinicalDiagnosis, ElectronicPrescription, PrescriptionItem

def run_seeder():
    print("=" * 70)
    print("SEEDING CARETRUST HMS ENTERPRISE DATA")
    print("=" * 70)

    # 1. Tenants
    tenant1, _ = Tenant.objects.get_or_create(
        slug="caretrust-health",
        defaults={
            "name": "CareTrust Health System",
            "mrn_prefix": "CTH",
            "is_active": True,
        }
    )
    tenant2, _ = Tenant.objects.get_or_create(
        slug="apex-health",
        defaults={
            "name": "Apex Healthcare Specialty Network",
            "mrn_prefix": "APX",
            "is_active": True,
        }
    )

    # 2. Branches
    branch_main, _ = HospitalBranch.objects.get_or_create(
        tenant=tenant1,
        code="MAIN",
        defaults={
            "name": "CareTrust Metro General & Trauma Center",
            "address": "100 Medical Center Boulevard, New York, NY",
            "phone": "+1 (212) 555-0100",
            "email": "metro.admin@caretrust.health",
            "is_active": True,
        }
    )
    branch_sub, _ = HospitalBranch.objects.get_or_create(
        tenant=tenant1,
        code="WEST",
        defaults={
            "name": "CareTrust Westside Ambulatory Pavilion",
            "address": "450 West 57th Street, New York, NY",
            "phone": "+1 (212) 555-0199",
            "email": "westside@caretrust.health",
            "is_active": True,
        }
    )

    # 3. Departments
    dept_cardio, _ = Department.objects.get_or_create(
        tenant=tenant1,
        branch=branch_main,
        code="CARD",
        defaults={"name": "Cardiology & Interventional Suite", "is_active": True}
    )
    dept_neuro, _ = Department.objects.get_or_create(
        tenant=tenant1,
        branch=branch_main,
        code="NEUR",
        defaults={"name": "Neurology & Stroke Center", "is_active": True}
    )
    dept_gen, _ = Department.objects.get_or_create(
        tenant=tenant1,
        branch=branch_main,
        code="GENM",
        defaults={"name": "General Internal Medicine", "is_active": True}
    )
    dept_emrg, _ = Department.objects.get_or_create(
        tenant=tenant1,
        branch=branch_main,
        code="EMRG",
        defaults={"name": "Emergency & Level 1 Trauma", "is_active": True}
    )

    # 4. Patients (MPI)
    sample_patients = [
        {"first_name": "Eleanor", "last_name": "Vance", "mrn": "CTH-2026-0001", "gender": "FEMALE", "dob": date(1982, 4, 15), "blood": "O+", "phone": "+1 (555) 234-5678"},
        {"first_name": "Marcus", "last_name": "Aurelius", "mrn": "CTH-2026-0002", "gender": "MALE", "dob": date(1965, 8, 23), "blood": "A+", "phone": "+1 (555) 345-6789"},
        {"first_name": "Sarah", "last_name": "Connor", "mrn": "CTH-2026-0003", "gender": "FEMALE", "dob": date(1990, 11, 3), "blood": "B-", "phone": "+1 (555) 456-7890"},
        {"first_name": "David", "last_name": "Chen", "mrn": "CTH-2026-0004", "gender": "MALE", "dob": date(1978, 2, 19), "blood": "AB+", "phone": "+1 (555) 567-8901"},
        {"first_name": "Priya", "last_name": "Sharma", "mrn": "CTH-2026-0005", "gender": "FEMALE", "dob": date(1995, 6, 30), "blood": "A-", "phone": "+1 (555) 678-9012"},
    ]

    created_patients = []
    for sp in sample_patients:
        pat, _ = Patient.objects.get_or_create(
            tenant=tenant1,
            mrn=sp["mrn"],
            defaults={
                "first_name": sp["first_name"],
                "last_name": sp["last_name"],
                "date_of_birth": sp["dob"],
                "gender": sp["gender"],
                "blood_group": sp["blood"],
                "phone": sp["phone"],
                "email": f"{sp['first_name'].lower()}.{sp['last_name'].lower()}@example.com",
                "preferred_branch": branch_main,
                "status": "ACTIVE",
            }
        )
        created_patients.append(pat)

    # 5. Doctor Schedules & Appointments
    sched_doc1, _ = DoctorSchedule.objects.get_or_create(
        tenant=tenant1,
        branch=branch_main,
        department=dept_cardio,
        doctor_id="DOC-CARD-01",
        day_of_week=0,
        defaults={
            "doctor_name": "Dr. Sophia Patel, MD, FACC",
            "doctor_specialty": "Interventional Cardiology",
            "start_time": time(9, 0),
            "end_time": time(17, 0),
            "slot_duration_minutes": 20,
            "max_patients": 24,
            "is_active": True,
        }
    )

    today = date.today()
    if created_patients:
        app1, _ = Appointment.objects.get_or_create(
            tenant=tenant1,
            appointment_number="APT-2026-0001",
            defaults={
                "branch": branch_main,
                "patient": created_patients[0],
                "appointment_date": today,
                "start_time": time(9, 20),
                "end_time": time(9, 40),
                "doctor_id": "DOC-CARD-01",
                "doctor_name": "Dr. Sophia Patel, MD, FACC",
                "department": dept_cardio,
                "chief_complaint": "Exertional chest tightness and dyspnea on exertion",
                "status": "CONFIRMED",
            }
        )

        app2, _ = Appointment.objects.get_or_create(
            tenant=tenant1,
            appointment_number="APT-2026-0002",
            defaults={
                "branch": branch_main,
                "patient": created_patients[1],
                "appointment_date": today,
                "start_time": time(10, 0),
                "end_time": time(10, 20),
                "doctor_id": "DOC-CARD-01",
                "doctor_name": "Dr. Sophia Patel, MD, FACC",
                "department": dept_cardio,
                "chief_complaint": "Post-angioplasty routine follow-up checkup",
                "status": "COMPLETED",
            }
        )

    # 6. Wards & Beds
    ward_icu, _ = Ward.objects.get_or_create(
        tenant=tenant1,
        branch=branch_main,
        name="Intensive Cardiac Care Unit (ICCU)",
        defaults={"ward_type": "ICU", "floor": "3", "total_beds": 12, "is_active": True}
    )
    room_101, _ = Room.objects.get_or_create(
        tenant=tenant1,
        ward=ward_icu,
        room_number="ICU-101",
        defaults={"room_type": "SINGLE", "daily_rate": 500.00, "is_active": True}
    )
    bed_1, _ = Bed.objects.get_or_create(
        tenant=tenant1,
        room=room_101,
        bed_number="BED-01",
        defaults={"status": "OCCUPIED", "is_active": True}
    )
    bed_2, _ = Bed.objects.get_or_create(
        tenant=tenant1,
        room=room_101,
        bed_number="BED-02",
        defaults={"status": "AVAILABLE", "is_active": True}
    )

    # 7. Clinical Encounter
    if created_patients:
        enc1, _ = ClinicalEncounter.objects.get_or_create(
            tenant=tenant1,
            encounter_number="ENC-2026-0001",
            defaults={
                "patient": created_patients[0],
                "appointment": app1 if 'app1' in locals() else None,
                "encounter_type": "OPD",
                "doctor_id": "DOC-CARD-01",
                "doctor_name": "Dr. Sophia Patel, MD, FACC",
                "department": dept_cardio,
                "chief_complaint": "Retrosternal chest discomfort radiating to left arm",
                "subjective_notes": "Patient reports 2-week history of pressure-like chest pain with exertion.",
                "objective_findings": "BP 138/86 mmHg, HR 74 bpm, regular. ECG reveals sinus rhythm with non-specific ST changes.",
                "assessment": "Suspected Stable Angina Pectoris; Primary Essential Hypertension.",
                "plan": "Order diagnostic cardiac profile, 12-lead ECG, and treadmill stress test. Prescribe beta-blocker.",
                "status": "FINALIZED",
                "is_signed": True,
                "signed_by_doctor_name": "Dr. Sophia Patel, MD, FACC",
            }
        )

    print(f"SUCCESS: Seeded {Tenant.objects.count()} Tenants, {HospitalBranch.objects.count()} Branches, {Department.objects.count()} Departments, {Patient.objects.count()} Patients, {Appointment.objects.count()} Appointments.")

if __name__ == "__main__":
    run_seeder()
