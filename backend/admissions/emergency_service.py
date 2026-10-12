from django.utils import timezone
from admissions.models import Admission, Bed

class EmergencyAdmissionService:
    @staticmethod
    def admit_emergency(tenant, patient, branch, department, doctor_id, doctor_name, bed, diagnosis):
        bed.status = "OCCUPIED"
        bed.save()
        year = timezone.now().year
        count = Admission.objects.filter(tenant=tenant).count() + 1
        return Admission.objects.create(
            tenant=tenant, admission_number=f"EMR-{year}-{count:06d}",
            patient=patient, branch=branch, department=department,
            admitting_doctor_id=doctor_id, admitting_doctor_name=doctor_name,
            bed=bed, admission_diagnosis=f"[URGENT-ER] {diagnosis}", status="ADMITTED"
        )
