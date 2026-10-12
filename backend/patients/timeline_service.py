from typing import List, Dict, Any
from appointments.models import Appointment
from admissions.models import Admission

class PatientTimelineService:
    @staticmethod
    def get_patient_timeline(tenant, patient_id) -> List[Dict[str, Any]]:
        timeline = []
        for apt in Appointment.objects.filter(tenant=tenant, patient_id=patient_id).order_by("-appointment_date"):
            timeline.append({
                "event_type": "APPOINTMENT",
                "date": str(apt.appointment_date),
                "summary": f"Consultation with Dr. {apt.doctor_name}",
                "status": apt.status,
                "ref_number": apt.appointment_number
            })
        for adm in Admission.objects.filter(tenant=tenant, patient_id=patient_id).order_by("-admission_date"):
            timeline.append({
                "event_type": "ADMISSION",
                "date": str(adm.admission_date.date()),
                "summary": f"Inpatient admission in {adm.bed.room.ward.name}",
                "status": adm.status,
                "ref_number": adm.admission_number
            })
        timeline.sort(key=lambda x: x["date"], reverse=True)
        return timeline
