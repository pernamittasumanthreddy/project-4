import os
import json
import random

BASE_DIR = r"c:\Users\Lenovo\Desktop\Project 4"
DATA_DIR = os.path.join(BASE_DIR, "backend", "fixtures", "clinical_datasets")
os.makedirs(DATA_DIR, exist_ok=True)

first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
               "Diya", "Saanvi", "Ananya", "Aadhya", "Pari", "Chiara", "Myra", "Riya", "Anushka", "Fatima",
               "John", "David", "Michael", "Sarah", "Emily", "James", "Robert", "Emma", "Olivia", "Sophia"]
last_names = ["Sharma", "Verma", "Patel", "Reddy", "Rao", "Nair", "Iyer", "Kumar", "Singh", "Gupta",
              "Chowdhury", "Mukherjee", "Das", "Joshi", "Bhat", "Smith", "Johnson", "Williams", "Brown", "Jones"]

blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
allergies_pool = [
    {"allergen": "Amoxicillin", "severity": "Severe", "reaction": "Anaphylaxis"},
    {"allergen": "Penicillin", "severity": "Moderate", "reaction": "Hives"},
    {"allergen": "Sulfa Drugs", "severity": "Mild", "reaction": "Skin rash"},
    {"allergen": "Ibuprofen", "severity": "Moderate", "reaction": "Gastric irritation"},
    {"allergen": "Latex", "severity": "Severe", "reaction": "Contact dermatitis"},
    {"allergen": "Peanuts", "severity": "Severe", "reaction": "Respiratory distress"},
    {"allergen": "Contrast Media", "severity": "Moderate", "reaction": "Nausea & erythema"},
    {"allergen": "Morphine", "severity": "Mild", "reaction": "Pruritus"}
]

chronic_pool = [
    "Type 2 Diabetes Mellitus", "Essential Hypertension", "Coronary Artery Disease",
    "Bronchial Asthma", "Chronic Kidney Disease Stage 2", "Hypothyroidism",
    "Rheumatoid Arthritis", "Dyslipidemia", "Osteoarthritis", "Chronic Obstructive Pulmonary Disease"
]

print("Generating Master Patient Index (MPI) Synthetic Cohort...")
patients = []
for i in range(1, 2001):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    year = random.randint(1950, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob = f"{year:04d}-{month:02d}-{day:02d}"
    phone = f"+91{random.randint(7000000000, 9999999999)}"
    mrn = f"MRN-SYNTH-{i:06d}"
    bg = random.choice(blood_groups)
    selected_allergies = random.sample(allergies_pool, k=random.randint(0, 3))
    selected_chronic = random.sample(chronic_pool, k=random.randint(0, 3))

    patients.append({
        "mrn": mrn,
        "first_name": fn,
        "last_name": ln,
        "dob": dob,
        "gender": random.choice(["MALE", "FEMALE", "OTHER"]),
        "phone": phone,
        "blood_group": bg,
        "national_id": f"IND-ID-{random.randint(10000000, 99999999)}",
        "allergies": selected_allergies,
        "chronic_conditions": selected_chronic,
        "status": "ACTIVE"
    })

with open(os.path.join(DATA_DIR, "master_patient_cohort.json"), "w", encoding="utf-8") as f:
    json.dump(patients, f, indent=2)

print("Patients cohort written.")

print("Generating OPD Schedules & Appointment Manifests...")
appointments = []
for i in range(1, 1501):
    p = random.choice(patients)
    appointments.append({
        "appointment_number": f"APT-SYNTH-{i:06d}",
        "patient_mrn": p["mrn"],
        "doctor_name": f"Dr. {random.choice(first_names)} {random.choice(last_names)}",
        "department": random.choice(["Cardiology", "Neurology", "General Medicine", "Pediatrics", "Orthopedics"]),
        "appointment_date": f"2026-10-{random.randint(1, 30):02d}",
        "start_time": f"{random.randint(9, 16):02d}:{random.choice([0, 15, 30, 45]):02d}",
        "status": random.choice(["CONFIRMED", "COMPLETED", "CHECKED_IN", "CANCELLED"]),
        "chief_complaint": random.choice(["Routine checkup", "Fever and headache", "Chest discomfort", "Joint swelling", "Post-op consultation"])
    })

with open(os.path.join(DATA_DIR, "opd_appointment_manifests.json"), "w", encoding="utf-8") as f:
    json.dump(appointments, f, indent=2)

print("OPD manifests written.")

print("Generating Inpatient (IPD) Bed Admission & Transfer Logs...")
admissions = []
for i in range(1, 1201):
    p = random.choice(patients)
    ward = random.choice(["ICU Bay 1", "General Male Ward", "General Female Ward", "Pediatric Wing", "Private Deluxe Floor"])
    admissions.append({
        "admission_number": f"IPD-SYNTH-{i:06d}",
        "patient_mrn": p["mrn"],
        "admitting_clinician": f"Dr. {random.choice(first_names)} {random.choice(last_names)}",
        "ward": ward,
        "room_number": f"R-{random.randint(101, 405)}",
        "bed_number": f"B-{random.randint(1, 12)}",
        "status": random.choice(["ADMITTED", "DISCHARGED", "DISCHARGE_REQUESTED"]),
        "diagnosis": random.choice(["Acute Bronchitis", "Severe Gastroenteritis", "Hypertensive Crisis", "Fracture Femur", "Diabetic Ketoacidosis"]),
        "billing_cleared": random.choice([True, False])
    })

with open(os.path.join(DATA_DIR, "ipd_admission_records.json"), "w", encoding="utf-8") as f:
    json.dump(admissions, f, indent=2)

print("IPD admission records written.")
