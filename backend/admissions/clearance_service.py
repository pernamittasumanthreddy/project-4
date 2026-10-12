class DischargeClearanceService:
    @staticmethod
    def verify_all_clearances(pharmacy_cleared, lab_cleared, billing_cleared):
        return {
            "is_discharge_ready": pharmacy_cleared and lab_cleared and billing_cleared,
            "pharmacy": pharmacy_cleared,
            "lab": lab_cleared,
            "billing": billing_cleared
        }
