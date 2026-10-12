from typing import Dict, Any
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
