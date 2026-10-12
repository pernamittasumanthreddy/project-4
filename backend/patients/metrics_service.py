from patients.models import Patient

class PatientMetricsService:
    @staticmethod
    def get_registration_stats(tenant):
        total = Patient.objects.filter(tenant=tenant).count()
        active = Patient.objects.filter(tenant=tenant, status="ACTIVE").count()
        merged = Patient.objects.filter(tenant=tenant, is_merged=True).count()
        return {"total_patients": total, "active_patients": active, "merged_profiles": merged}
