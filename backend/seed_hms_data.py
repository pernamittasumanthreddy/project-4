"""
Enterprise Multi-Tenant Seed Data Generator for HMS Platform.
Populates realistic hospital tenants, doctors, patients, appointments, encounters,
diagnostic investigations, billing records, and telemedicine rooms.
Zero external paid APIs required. 100% local database seeding.
"""

import os
import sys
import django
from datetime import date, datetime, time, timedelta
from decimal import Decimal

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_core.settings')
django.setup()

from apps.core.models import Tenant, HospitalBranch, User, AuditLog
from apps.appointments.models import Department, DoctorProfile, PatientProfile, Appointment
from apps.clinical.models import Encounter, Diagnosis, Prescription, PrescriptionItem, Allergy, MedicalHistory
from apps.diagnostics.models import LabReport, RadiologyReport
from apps.pharmacy.models import Medication, DispensingOrder
from apps.billing.models import Invoice, Payment
from apps.telemedicine.models import TelemedicineSession
from apps.notifications.services import NotificationDispatcher

def seed_hms_database():
    print("=" * 70)
    print("STARTING HMS MULTI-TENANT ENTERPRISE DATABASE SEEDING")
    print("=" * 70)

    # 1. Create Multi-Tenant Organizations
    tenant_caretrust, _ = Tenant.objects.get_or_create(
        slug="caretrust-health",
        defaults={
            "name": "CareTrust Health System",
            "domain": "caretrust.hms.health",
            "tier": "ENTERPRISE",
            "license_key": "LIC-CARETRUST-ENT-2026",
            "primary_color": "#0F766E",
            "contact_email": "admin@caretrust.health",
            "contact_phone": "+1 (800) 555-CARE",
            "is_active": True,
        }
    )

    tenant_metro, _ = Tenant.objects.get_or_create(
        slug="metrohealth-hms",
        defaults={
            "name": "MetroHealth Regional Medical Center",
            "domain": "metrohealth.hms.health",
            "tier": "REGIONAL",
            "license_key": "LIC-METRO-REG-2026",
            "primary_color": "#1E40AF",
            "contact_email": "operations@metrohealth.health",
            "contact_phone": "+1 (888) 555-METRO",
            "is_active": True,
        }
    )
    print(f"[+] Multi-Tenant Organizations Verified: {tenant_caretrust.name}, {tenant_metro.name}")

    # 2. Create Hospital Campuses / Branches
    branch_main, _ = HospitalBranch.objects.get_or_create(
        tenant=tenant_caretrust,
        code="MAIN",
        defaults={
            "name": "CareTrust University Medical Center",
            "address": "742 Evergreen Terrace, Medical District",
            "city": "Metro Boston",
            "state": "MA",
            "postal_code": "02115",
            "phone": "+1 (617) 555-0100",
            "email": "main@caretrust.health",
            "is_active": True,
        }
    )

    branch_north, _ = HospitalBranch.objects.get_or_create(
        tenant=tenant_caretrust,
        code="NORTH",
        defaults={
            "name": "North Wing Outpatient & Specialty Pavilion",
            "address": "1200 North Parkway, Suite 400",
            "city": "Cambridge",
            "state": "MA",
            "postal_code": "02138",
            "phone": "+1 (617) 555-0199",
            "email": "north@caretrust.health",
            "is_active": True,
        }
    )
    print(f"[+] Hospital Branches Configured: {branch_main.name}, {branch_north.name}")

    # 3. Create Clinical Departments
    dept_cardio, _ = Department.objects.get_or_create(
        tenant=tenant_caretrust,
        code="CARDIO",
        defaults={
            "name": "Cardiology & Vascular Institute",
            "description": "Comprehensive cardiac evaluations, interventional cardiology, echocardiography, and preventive heart care.",
            "icon_name": "HeartPulse",
            "is_active": True,
        }
    )

    dept_pulmo, _ = Department.objects.get_or_create(
        tenant=tenant_caretrust,
        code="PULMO",
        defaults={
            "name": "Pulmonology & Respiratory Medicine",
            "description": "Advanced diagnostic spirometry, asthma management, COPD therapy, and critical respiratory care.",
            "icon_name": "Wind",
            "is_active": True,
        }
    )

    dept_neuro, _ = Department.objects.get_or_create(
        tenant=tenant_caretrust,
        code="NEURO",
        defaults={
            "name": "Neurology & Cognitive Health",
            "description": "Evaluation of migraines, neurological disorders, neuropathy, and comprehensive stroke recovery.",
            "icon_name": "Brain",
            "is_active": True,
        }
    )

    dept_primary, _ = Department.objects.get_or_create(
        tenant=tenant_caretrust,
        code="PRIMARY",
        defaults={
            "name": "Family Medicine & Primary Care",
            "description": "Annual wellness exams, preventive screenings, adult immunizations, and chronic condition management.",
            "icon_name": "Stethoscope",
            "is_active": True,
        }
    )
    print("[+] Clinical Departments Initialized")

    # 4. Create User Accounts & Personas
    # Admin User
    admin_user, _ = User.objects.get_or_create(
        username="hospital_admin",
        defaults={
            "email": "admin@caretrust.health",
            "first_name": "Sarah",
            "last_name": "Jenkins",
            "role": "HOSPITAL_ADMIN",
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "phone": "+1 (617) 555-0120",
            "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
            "is_staff": True,
        }
    )
    admin_user.set_password("Admin@2026")
    admin_user.save()

    # Doctor 1: Dr. Sophia Chen (Cardiologist)
    doc_chen_user, _ = User.objects.get_or_create(
        username="doctor_chen",
        defaults={
            "email": "sophia.chen@caretrust.health",
            "first_name": "Sophia",
            "last_name": "Chen",
            "role": "DOCTOR",
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "phone": "+1 (617) 555-0341",
            "avatar_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&auto=format&fit=crop&q=80",
        }
    )
    doc_chen_user.set_password("Doctor@2026")
    doc_chen_user.save()

    doc_chen_profile, _ = DoctorProfile.objects.get_or_create(
        user=doc_chen_user,
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "department": dept_cardio,
            "license_number": "MED-MA-948102",
            "specialization": "Interventional Cardiology & Preventive Heart Health",
            "qualification": "MD, FACC (Harvard Medical School)",
            "experience_years": 14,
            "consultation_fee": Decimal("180.00"),
            "slot_duration_minutes": 30,
            "is_available_telemedicine": True,
            "rating": Decimal("4.95"),
            "review_count": 128,
            "office_room": "Heart Pavilion, Suite 402",
            "bio": "Dr. Sophia Chen is a board-certified cardiologist specializing in lipid management, preventive cardiology, coronary artery disease, and virtual telemedicine consultations."
        }
    )

    # Doctor 2: Dr. Marcus Vance (Pulmonologist)
    doc_vance_user, _ = User.objects.get_or_create(
        username="doctor_vance",
        defaults={
            "email": "marcus.vance@caretrust.health",
            "first_name": "Marcus",
            "last_name": "Vance",
            "role": "DOCTOR",
            "tenant": tenant_caretrust,
            "branch": branch_north,
            "phone": "+1 (617) 555-0452",
            "avatar_url": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150&auto=format&fit=crop&q=80",
        }
    )
    doc_vance_user.set_password("Doctor@2026")
    doc_vance_user.save()

    doc_vance_profile, _ = DoctorProfile.objects.get_or_create(
        user=doc_vance_user,
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_north,
            "department": dept_pulmo,
            "license_number": "MED-MA-884219",
            "specialization": "Pulmonary Disease & Critical Care Medicine",
            "qualification": "MD, FCCP (Johns Hopkins University)",
            "experience_years": 16,
            "consultation_fee": Decimal("165.00"),
            "slot_duration_minutes": 30,
            "is_available_telemedicine": True,
            "rating": Decimal("4.88"),
            "review_count": 94,
            "office_room": "North Pavilion, Clinic 2B",
            "bio": "Chief of Pulmonology at North Wing, specializing in adult bronchial asthma, chronic pulmonary symptoms, and long-COVID respiratory recovery."
        }
    )

    # Patient 1: Priya Sharma (Cardiac Patient)
    patient_priya_user, _ = User.objects.get_or_create(
        username="patient_priya",
        defaults={
            "email": "priya.sharma@gmail.com",
            "first_name": "Priya",
            "last_name": "Sharma",
            "role": "PATIENT",
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "phone": "+1 (617) 555-8834",
            "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80",
        }
    )
    patient_priya_user.set_password("Patient@2026")
    patient_priya_user.save()

    patient_priya_profile, _ = PatientProfile.objects.get_or_create(
        user=patient_priya_user,
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "mrn": "MRN-2026-90412",
            "date_of_birth": date(1988, 6, 14),
            "gender": "FEMALE",
            "blood_group": "O+",
            "emergency_contact_name": "Rajesh Sharma",
            "emergency_contact_phone": "+1 (617) 555-8835",
            "emergency_contact_relation": "Spouse",
            "address_line": "42 Commonwealth Ave, Apt 3B",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02116",
            "insurance_provider": "BlueCross BlueShield Massachusetts",
            "insurance_policy_number": "BCBS-9842104-E",
        }
    )

    # Patient 2: David Miller (Chronic Care / Pulmonology)
    patient_david_user, _ = User.objects.get_or_create(
        username="patient_david",
        defaults={
            "email": "david.miller@gmail.com",
            "first_name": "David",
            "last_name": "Miller",
            "role": "PATIENT",
            "tenant": tenant_caretrust,
            "branch": branch_north,
            "phone": "+1 (617) 555-7721",
            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        }
    )
    patient_david_user.set_password("Patient@2026")
    patient_david_user.save()

    patient_david_profile, _ = PatientProfile.objects.get_or_create(
        user=patient_david_user,
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_north,
            "mrn": "MRN-2026-88104",
            "date_of_birth": date(1974, 11, 23),
            "gender": "MALE",
            "blood_group": "A+",
            "emergency_contact_name": "Elena Miller",
            "emergency_contact_phone": "+1 (617) 555-7722",
            "emergency_contact_relation": "Sister",
            "address_line": "89 Harvard Street",
            "city": "Cambridge",
            "state": "MA",
            "postal_code": "02139",
            "insurance_provider": "Aetna Health Advantage",
            "insurance_policy_number": "AET-7719204-P",
        }
    )
    print(f"[+] Personas Created: Dr. Sophia Chen, Dr. Marcus Vance, Priya Sharma, David Miller")

    # 5. Seed Longitudinal Medical History & Allergies for Priya Sharma
    Allergy.objects.get_or_create(
        patient=patient_priya_profile,
        allergen="Penicillin & Beta-lactams",
        defaults={
            "tenant": tenant_caretrust,
            "reaction": "Acute cutaneous urticaria, pruritus, facial edema",
            "severity": "MODERATE",
            "identified_date": date(2018, 4, 12),
        }
    )
    Allergy.objects.get_or_create(
        patient=patient_priya_profile,
        allergen="Shellfish / Iodine Contrast",
        defaults={
            "tenant": tenant_caretrust,
            "reaction": "Mild nausea, diffuse erythematous rash",
            "severity": "MILD",
            "identified_date": date(2021, 9, 5),
        }
    )

    MedicalHistory.objects.get_or_create(
        patient=patient_priya_profile,
        condition_name="Essential Primary Hypertension",
        defaults={
            "tenant": tenant_caretrust,
            "onset_year": 2022,
            "status": "Managed with oral ACE-inhibitor (Lisinopril 10mg QD)",
            "notes": "Maintains average clinic BP 124/80 with lifestyle and drug therapy."
        }
    )
    MedicalHistory.objects.get_or_create(
        patient=patient_priya_profile,
        condition_name="Hyperlipidemia (Elevated LDL)",
        defaults={
            "tenant": tenant_caretrust,
            "onset_year": 2023,
            "status": "Active Management with Statin",
            "notes": "Target LDL < 100 mg/dL under Dr. Sophia Chen supervision."
        }
    )

    # 6. Seed Realistic Clinical Encounters & Prescriptions
    today = date.today()

    # Past completed encounter (2 weeks ago)
    past_appt, _ = Appointment.objects.get_or_create(
        appointment_number="APT-2026-PAST01",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "patient": patient_priya_profile,
            "doctor": doc_chen_profile,
            "appointment_date": today - timedelta(days=14),
            "start_time": time(10, 0),
            "end_time": time(10, 30),
            "appointment_type": "TELEMEDICINE",
            "status": "COMPLETED",
            "reason_for_visit": "Quarterly cardiovascular evaluation and lipid panel review.",
            "notes": "Patient reported good medication tolerance.",
        }
    )

    past_encounter, _ = Encounter.objects.get_or_create(
        encounter_number="ENC-2026-90412-01",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "appointment": past_appt,
            "patient": patient_priya_profile,
            "doctor": doc_chen_profile,
            "encounter_date": today - timedelta(days=14),
            "encounter_type": "TELEMEDICINE",
            "status": "SIGNED",
            "chief_complaint": "Follow-up blood pressure monitoring and lipid optimization.",
            "vitals": {
                "bp_systolic": 124,
                "bp_diastolic": 78,
                "heart_rate": 68,
                "temp_c": 36.7,
                "spo2": 99,
                "weight_kg": 64.0,
                "height_cm": 165,
                "bmi": 23.5
            },
            "subjective_notes": "Patient Priya Sharma reports zero chest tightness, palpitations, or exertional dyspnea. Adherent to low-sodium Mediterranean diet.",
            "physical_examination": "Telemedicine video inspection: Alert, well-appearing, in no acute respiratory distress. Speech fluent, normal affect.",
            "assessment": "Stable essential hypertension and controlled hyperlipidemia with favorable response to statin therapy.",
            "clinical_plan": "Continue Lisinopril 10mg daily and Atorvastatin 20mg at bedtime. Order repeat Fasting Lipid Panel and Comprehensive Metabolic Panel in 3 months.",
            "signed_by": doc_chen_profile,
            "signed_at": datetime.now() - timedelta(days=14),
        }
    )

    Diagnosis.objects.get_or_create(
        encounter=past_encounter,
        icd10_code="I10",
        defaults={
            "tenant": tenant_caretrust,
            "patient": patient_priya_profile,
            "description": "Essential (primary) hypertension",
            "severity": "MODERATE",
            "is_primary": True,
            "diagnosed_date": today - timedelta(days=14),
        }
    )

    Diagnosis.objects.get_or_create(
        encounter=past_encounter,
        icd10_code="E78.00",
        defaults={
            "tenant": tenant_caretrust,
            "patient": patient_priya_profile,
            "description": "Pure hypercholesterolemia, unspecified",
            "severity": "MILD",
            "is_primary": False,
            "diagnosed_date": today - timedelta(days=14),
        }
    )

    # Active Prescription
    rx_priya, _ = Prescription.objects.get_or_create(
        prescription_number="RX-2026-CARDIO-8812",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "encounter": past_encounter,
            "patient": patient_priya_profile,
            "doctor": doc_chen_profile,
            "status": "ACTIVE",
            "issued_date": today - timedelta(days=14),
            "valid_until": today + timedelta(days=180),
            "special_instructions": "Take Lisinopril every morning with a full glass of water. Take Atorvastatin at night.",
        }
    )

    PrescriptionItem.objects.get_or_create(
        prescription=rx_priya,
        medication_name="Lisinopril Tablets USP",
        defaults={
            "dosage": "10 mg",
            "route": "ORAL",
            "frequency": "Once daily each morning",
            "duration_days": 90,
            "quantity": 90,
            "instructions": "Monitor home blood pressure weekly.",
        }
    )

    PrescriptionItem.objects.get_or_create(
        prescription=rx_priya,
        medication_name="Atorvastatin Calcium (Lipitor)",
        defaults={
            "dosage": "20 mg",
            "route": "ORAL",
            "frequency": "Once daily at bedtime",
            "duration_days": 90,
            "quantity": 90,
            "instructions": "Report any unexpected muscle aches immediately.",
        }
    )

    # 7. Seed Diagnostic Reports (Approved and Pending)
    # Approved Comprehensive Metabolic Panel (CMP)
    LabReport.objects.get_or_create(
        report_number="LAB-2026-CMP-4019",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "test_name": "Comprehensive Metabolic Panel (CMP-14)",
            "test_code": "24323-8",
            "category": "BIOCHEMISTRY",
            "patient": patient_priya_profile,
            "ordering_doctor": doc_chen_profile,
            "status": "APPROVED",
            "order_date": today - timedelta(days=10),
            "collected_at": datetime.now() - timedelta(days=10, hours=2),
            "specimen_type": "Venous Serum (Gold Top SST)",
            "results": [
                {"name": "Fasting Serum Glucose", "value": "92", "unit": "mg/dL", "reference_range": "70 - 99", "flag": "NORMAL"},
                {"name": "Blood Urea Nitrogen (BUN)", "value": "14", "unit": "mg/dL", "reference_range": "7 - 20", "flag": "NORMAL"},
                {"name": "Serum Creatinine", "value": "0.85", "unit": "mg/dL", "reference_range": "0.50 - 1.10", "flag": "NORMAL"},
                {"name": "Estimated GFR (eGFR)", "value": ">90", "unit": "mL/min/1.73m2", "reference_range": ">= 60", "flag": "NORMAL"},
                {"name": "Serum Sodium (Na)", "value": "140", "unit": "mEq/L", "reference_range": "136 - 145", "flag": "NORMAL"},
                {"name": "Serum Potassium (K)", "value": "4.2", "unit": "mEq/L", "reference_range": "3.5 - 5.1", "flag": "NORMAL"},
                {"name": "Serum Chloride (Cl)", "value": "102", "unit": "mEq/L", "reference_range": "98 - 107", "flag": "NORMAL"},
                {"name": "Carbon Dioxide (CO2)", "value": "25", "unit": "mEq/L", "reference_range": "22 - 29", "flag": "NORMAL"},
                {"name": "Serum Calcium", "value": "9.4", "unit": "mg/dL", "reference_range": "8.6 - 10.3", "flag": "NORMAL"},
                {"name": "Total Bilirubin", "value": "0.6", "unit": "mg/dL", "reference_range": "0.2 - 1.2", "flag": "NORMAL"},
                {"name": "ALT (SGPT)", "value": "22", "unit": "U/L", "reference_range": "7 - 35", "flag": "NORMAL"},
                {"name": "AST (SGOT)", "value": "19", "unit": "U/L", "reference_range": "8 - 33", "flag": "NORMAL"},
            ],
            "conclusion": "Electrolytes, renal parameters, and hepatic transaminases are within normal reference limits. Stable renal function on ACE inhibitor.",
            "approved_by": "Dr. Eleanor Vance, MD (Chief Clinical Pathologist)",
            "approved_at": datetime.now() - timedelta(days=9),
            "document_url": "/api/v1/diagnostics/lab-reports/lab-cmp-4019.pdf",
        }
    )

    # Approved Lipid Panel
    LabReport.objects.get_or_create(
        report_number="LAB-2026-LIPID-8821",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "test_name": "Standard Lipid Profile (Fasting)",
            "test_code": "57698-3",
            "category": "BIOCHEMISTRY",
            "patient": patient_priya_profile,
            "ordering_doctor": doc_chen_profile,
            "status": "APPROVED",
            "order_date": today - timedelta(days=10),
            "collected_at": datetime.now() - timedelta(days=10, hours=2),
            "specimen_type": "Venous Serum (Gold Top SST)",
            "results": [
                {"name": "Total Cholesterol", "value": "178", "unit": "mg/dL", "reference_range": "< 200", "flag": "NORMAL"},
                {"name": "Triglycerides", "value": "130", "unit": "mg/dL", "reference_range": "< 150", "flag": "NORMAL"},
                {"name": "HDL Cholesterol ('Good')", "value": "58", "unit": "mg/dL", "reference_range": ">= 50", "flag": "NORMAL"},
                {"name": "LDL Calculated ('Bad')", "value": "94", "unit": "mg/dL", "reference_range": "< 100", "flag": "NORMAL"},
                {"name": "Non-HDL Cholesterol", "value": "120", "unit": "mg/dL", "reference_range": "< 130", "flag": "NORMAL"},
            ],
            "conclusion": "Favorable lipid reduction achieved. LDL has declined below target threshold of 100 mg/dL with current Atorvastatin 20mg regimen.",
            "approved_by": "Dr. Eleanor Vance, MD (Chief Clinical Pathologist)",
            "approved_at": datetime.now() - timedelta(days=9),
            "document_url": "/api/v1/diagnostics/lab-reports/lab-lipid-8821.pdf",
        }
    )

    # Approved Radiology: Transthoracic Echocardiogram
    RadiologyReport.objects.get_or_create(
        study_number="RAD-2026-ECHO-1104",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "study_name": "Transthoracic Echocardiogram (Complete 2D + Doppler)",
            "modality": "ECHOCARDIOGRAM",
            "body_part": "Cardiac Anatomy & Hemodynamics",
            "patient": patient_priya_profile,
            "ordering_doctor": doc_chen_profile,
            "radiologist_name": "Dr. Arthur Sterling, MD (Cardiovascular Imaging)",
            "study_date": today - timedelta(days=20),
            "status": "APPROVED",
            "clinical_history": "Hypertension screening. Assessment of left ventricular mass and valvular competence.",
            "findings": "Left ventricle size is normal. Normal systolic function with estimated Left Ventricular Ejection Fraction (LVEF) 62%. No regional wall motion abnormalities. Normal diastolic filling pattern. Mitral and aortic valves appear thin and pliable with trace regurgitation within physiologic limits. Normal right ventricular size and systolic function.",
            "impression": "1. Preserved global left ventricular systolic function (LVEF 62%).\n2. No evidence of pathologic concentric left ventricular hypertrophy.\n3. Structurally normal cardiac valves.",
            "key_images": [
                "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=300&auto=format&fit=crop&q=80"
            ],
            "approved_at": datetime.now() - timedelta(days=19),
        }
    )

    # Unapproved Lab Report (Status: ANALYZED) for David Miller
    # Demonstrates that patient portal strictly hides unapproved records!
    LabReport.objects.get_or_create(
        report_number="LAB-2026-CBC-PENDING",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_north,
            "test_name": "Complete Blood Count with Differential (CBC)",
            "test_code": "85025",
            "category": "HEMATOLOGY",
            "patient": patient_david_profile,
            "ordering_doctor": doc_vance_profile,
            "status": "ANALYZED", # UNAPPROVED!
            "order_date": today - timedelta(days=1),
            "collected_at": datetime.now() - timedelta(hours=14),
            "specimen_type": "Whole Blood (Lavender K2-EDTA)",
            "results": [
                {"name": "White Blood Cell Count", "value": "7.2", "unit": "x10^3/uL", "reference_range": "4.5 - 11.0", "flag": "NORMAL"},
                {"name": "Hemoglobin", "value": "14.8", "unit": "g/dL", "reference_range": "13.5 - 17.5", "flag": "NORMAL"},
            ],
            "conclusion": "Specimen analyzed by hematology bench. Awaiting attending pathologist digital sign-off.",
        }
    )

    # 8. Seed Upcoming Appointments & Telemedicine Virtual Rooms
    # Appointment TODAY with Dr. Sophia Chen for Priya Sharma (Telemedicine!)
    today_appt, _ = Appointment.objects.get_or_create(
        appointment_number="APT-2026-LIVE01",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "patient": patient_priya_profile,
            "doctor": doc_chen_profile,
            "appointment_date": today,
            "start_time": time(14, 0),
            "end_time": time(14, 30),
            "appointment_type": "TELEMEDICINE",
            "status": "CONFIRMED",
            "reason_for_visit": "Virtual Telemedicine consultation: Review latest normal lipid panel and verify exercise tolerance.",
            "notes": "Telemedicine video enabled. Patient notified to prepare home blood pressure log.",
            "checked_in_at": datetime.now() - timedelta(minutes=15),
        }
    )

    # Telemedicine Session for today's appointment
    tele_session_live, _ = TelemedicineSession.objects.get_or_create(
        appointment=today_appt,
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "room_code": "CARE-VIRTUAL-83921",
            "doctor_token": "doc_token_sophia_chen_live_83921",
            "patient_token": "pat_token_priya_sharma_live_83921",
            "status": "SCHEDULED",
            "recording_enabled": False, # HIPAA compliant
            "clinical_quick_notes": "Patient reports good tolerance to statin.",
        }
    )

    # Upcoming Appointment next week for Priya Sharma
    Appointment.objects.get_or_create(
        appointment_number="APT-2026-UPCOMING02",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "patient": patient_priya_profile,
            "doctor": doc_chen_profile,
            "appointment_date": today + timedelta(days=7),
            "start_time": time(11, 30),
            "end_time": time(12, 0),
            "appointment_type": "IN_PERSON",
            "status": "CONFIRMED",
            "reason_for_visit": "Routine in-clinic blood pressure check & resting 12-lead ECG.",
        }
    )

    # Appointment TODAY for David Miller with Dr. Marcus Vance
    today_david_appt, _ = Appointment.objects.get_or_create(
        appointment_number="APT-2026-DAVID01",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_north,
            "patient": patient_david_profile,
            "doctor": doc_vance_profile,
            "appointment_date": today,
            "start_time": time(15, 0),
            "end_time": time(15, 30),
            "appointment_type": "TELEMEDICINE",
            "status": "CONFIRMED",
            "reason_for_visit": "Seasonal asthma trigger assessment and peak flow review.",
        }
    )

    TelemedicineSession.objects.get_or_create(
        appointment=today_david_appt,
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_north,
            "room_code": "CARE-VIRTUAL-77104",
            "doctor_token": "doc_token_marcus_vance_77104",
            "patient_token": "pat_token_david_miller_77104",
            "status": "SCHEDULED",
        }
    )

    # 9. Seed Financial Invoices & Payments (Member 6)
    # Fully Paid Invoice (Past visit)
    inv_paid, _ = Invoice.objects.get_or_create(
        invoice_number="INV-2026-008912",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "patient": patient_priya_profile,
            "appointment": past_appt,
            "issue_date": today - timedelta(days=14),
            "due_date": today + timedelta(days=16),
            "status": "PAID",
            "subtotal": Decimal("245.00"),
            "tax_amount": Decimal("0.00"),
            "discount_amount": Decimal("25.00"),
            "total_amount": Decimal("220.00"),
            "paid_amount": Decimal("220.00"),
            "balance_due": Decimal("0.00"),
            "line_items": [
                {"description": "Telemedicine Virtual Consultation (Dr. Sophia Chen)", "quantity": 1, "unit_price": 180.00, "total": 180.00},
                {"description": "Cardiovascular Health Management Coordination", "quantity": 1, "unit_price": 65.00, "total": 65.00},
            ],
            "notes": "Settled in full via patient credit card portal.",
        }
    )

    Payment.objects.get_or_create(
        payment_reference="PAY-SIM-CC-994120",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "receipt_number": "REC-2026-994120",
            "invoice": inv_paid,
            "amount": Decimal("220.00"),
            "payment_method": "CREDIT_CARD",
            "status": "SUCCESS",
            "is_sandbox_simulation": True,
            "notes": "Sandbox payment processed. Verified mock authorization.",
        }
    )

    # Unpaid Outstanding Invoice (Diagnostic Lab Fees)
    Invoice.objects.get_or_create(
        invoice_number="INV-2026-009415",
        defaults={
            "tenant": tenant_caretrust,
            "branch": branch_main,
            "patient": patient_priya_profile,
            "issue_date": today - timedelta(days=5),
            "due_date": today + timedelta(days=25),
            "status": "UNPAID",
            "subtotal": Decimal("110.00"),
            "tax_amount": Decimal("0.00"),
            "discount_amount": Decimal("0.00"),
            "total_amount": Decimal("110.00"),
            "paid_amount": Decimal("0.00"),
            "balance_due": Decimal("110.00"),
            "line_items": [
                {"description": "Comprehensive Metabolic Panel (CMP-14) Lab Fee", "quantity": 1, "unit_price": 65.00, "total": 65.00},
                {"description": "Fasting Lipid Profile Laboratory Investigation", "quantity": 1, "unit_price": 45.00, "total": 45.00},
            ],
            "notes": "Co-insurance copay after BlueCross coverage deduction.",
        }
    )

    # 10. Seed Notifications for Priya Sharma and Doctors
    NotificationDispatcher.dispatch_appointment_created(today_appt)
    NotificationDispatcher.dispatch_telemedicine_invite(tele_session_live)

    lab_cmp = LabReport.objects.filter(report_number="LAB-2026-CMP-4019").first()
    if lab_cmp:
        NotificationDispatcher.dispatch_lab_report_approved(lab_cmp)

    echo_rad = RadiologyReport.objects.filter(study_number="RAD-2026-ECHO-1104").first()
    if echo_rad:
        NotificationDispatcher.dispatch_radiology_report_approved(echo_rad)

    print("=" * 70)
    print("HMS MULTI-TENANT ENTERPRISE SEEDING COMPLETE SUCCESSFULLY!")
    print("=" * 70)

if __name__ == '__main__':
    seed_hms_database()
