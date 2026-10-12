"""
Integration Boundary Contracts (Read-Only Adapters)
Conforms to: Master Prompt Section 5 - Integration Boundaries:
"If another module is required for integration, use only its existing interfaces,
documented contracts, or minimal mock data strictly necessary for testing Member 6's workflows.
Do not build the other module itself."
"""

# Synthetic reference directory for cross-module integration testing
MOCK_PATIENTS = {
    "PAT-1001": {
        "id": "PAT-1001",
        "mrn": "MRN-2026-00891",
        "full_name": "Aarav Sharma",
        "age": 42,
        "gender": "Male",
        "phone": "+91 98765 43210",
        "state_code": "07", # Delhi
        "city": "New Delhi",
        "emergency_contact": "Pooja Sharma (+91 98765 43211)"
    },
    "PAT-1002": {
        "id": "PAT-1002",
        "mrn": "MRN-2026-00912",
        "full_name": "Priyanka Patel",
        "age": 29,
        "gender": "Female",
        "phone": "+91 98222 11223",
        "state_code": "27", # Maharashtra (Inter-state relative to Delhi hospital)
        "city": "Mumbai",
        "emergency_contact": "Raj Patel (+91 98222 11224)"
    },
    "PAT-1003": {
        "id": "PAT-1003",
        "mrn": "MRN-2026-01044",
        "full_name": "Rohan Deshmukh",
        "age": 61,
        "gender": "Male",
        "phone": "+91 98333 44556",
        "state_code": "07",
        "city": "New Delhi",
        "emergency_contact": "Anita Deshmukh"
    }
}

MOCK_ENCOUNTERS = {
    "ENC-5001": {
        "id": "ENC-5001",
        "patient_id": "PAT-1001",
        "type": "OPD",
        "doctor_name": "Dr. Sunita Rao (Cardiology)",
        "department": "Cardiology",
        "date": "2026-10-10"
    },
    "ENC-5002": {
        "id": "ENC-5002",
        "patient_id": "PAT-1002",
        "type": "IPD",
        "doctor_name": "Dr. Vikram Seth (Orthopedics)",
        "department": "Orthopedics",
        "ward_room": "Deluxe Ward - Bed 304",
        "admission_date": "2026-10-08",
        "discharge_date": "2026-10-12"
    }
}

def resolve_patient_contract(patient_id: str) -> dict:
    """Returns patient demographic data reference or a safe synthetic default."""
    if patient_id in MOCK_PATIENTS:
        return MOCK_PATIENTS[patient_id]
    return {
        "id": patient_id,
        "mrn": f"MRN-{patient_id}",
        "full_name": f"Patient {patient_id}",
        "age": 35,
        "gender": "Other",
        "phone": "+91 90000 00000",
        "state_code": "07",
        "city": "New Delhi"
    }

def resolve_encounter_contract(encounter_id: str) -> dict:
    """Returns clinical encounter reference or a safe synthetic default."""
    if encounter_id in MOCK_ENCOUNTERS:
        return MOCK_ENCOUNTERS[encounter_id]
    return {
        "id": encounter_id,
        "patient_id": "PAT-1001",
        "type": "OPD",
        "doctor_name": "Attending Physician",
        "department": "General Medicine",
        "date": "2026-10-12"
    }
