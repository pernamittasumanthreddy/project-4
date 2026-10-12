import os
import json
import random

BASE_DIR = r"c:\Users\Lenovo\Desktop\Project 4"
DATA_DIR = os.path.join(BASE_DIR, "backend", "fixtures", "clinical_datasets")

drugs = ["Paracetamol 500mg", "Metformin 500mg", "Atorvastatin 20mg", "Amlodipine 5mg", "Azithromycin 500mg", "Pantoprazole 40mg", "Ceftriaxone 1g", "Salbutamol Inhaler"]

encounters = []
for i in range(1, 2001):
    encounters.append({
        "encounter_id": f"ENC-{i:06d}",
        "mrn": f"MRN-SYNTH-{random.randint(1, 2000):06d}",
        "vitals": {
            "bp_systolic": random.randint(110, 150),
            "bp_diastolic": random.randint(70, 95),
            "pulse": random.randint(60, 100),
            "temp_f": round(random.uniform(97.5, 101.5), 1),
            "spo2": random.randint(94, 100)
        },
        "prescriptions": [
            {"drug": random.choice(drugs), "dosage": "1-0-1", "duration_days": random.randint(3, 14)}
            for _ in range(random.randint(1, 3))
        ],
        "clinical_notes": "Patient presented with reported symptoms. Clinical examination performed and stable vitals noted.",
        "follow_up_recommended": random.choice([True, False])
    })

with open(os.path.join(DATA_DIR, "encounter_clinical_notes.json"), "w", encoding="utf-8") as f:
    json.dump(encounters, f, indent=2)

print("Clinical encounter records generated.")
