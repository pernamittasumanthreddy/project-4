from typing import List, Dict, Any
from appointments.models import Appointment

class PatientPortalService:
    @staticmethod
    def get_upcoming_and_past_appointments(tenant, patient_id) -> Dict[str, List[Dict[str, Any]]]:
        all_apts = Appointment.objects.filter(tenant=tenant, patient_id=patient_id).order_by("appointment_date")
        upcoming = []
        past = []
        for a in all_apts:
            item = {
                "appointment_number": a.appointment_number,
                "doctor_name": a.doctor_name,
                "date": str(a.appointment_date),
                "time": str(a.start_time),
                "status": a.status,
                "type": a.appointment_type
            }
            if a.status in ["SCHEDULED", "CONFIRMED", "CHECKED_IN"]:
                upcoming.append(item)
            else:
                past.append(item)
        return {"upcoming": upcoming, "past": past}
