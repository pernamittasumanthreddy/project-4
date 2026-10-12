class GuardianProxyService:
    @staticmethod
    def verify_minor_representation(patient_age, relationship):
        if patient_age is not None and patient_age < 18:
            return relationship in ["PARENT", "LEGAL_GUARDIAN"]
        return True
