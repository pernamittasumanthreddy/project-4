class PatientBarcodeService:
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
