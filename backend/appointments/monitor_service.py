from typing import List, Dict, Any
from appointments.models import OPDQueueToken

class QueueMonitorService:
    @staticmethod
    def get_active_display_board(tenant, branch_id, doctor_id=None) -> List[Dict[str, Any]]:
        qs = OPDQueueToken.objects.filter(tenant=tenant, branch_id=branch_id, status__in=["WAITING", "CALLED", "ENGAGED"])
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        return [
            {
                "token_number": t.token_number,
                "doctor_name": t.appointment.doctor_name,
                "room_number": t.room_number or "Cabin 1",
                "status": t.status,
                "patient_name": t.appointment.patient.full_name
            } for t in qs.order_by("token_number")
        ]
