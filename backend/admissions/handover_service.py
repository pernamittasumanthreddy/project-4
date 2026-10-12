class NursingHandoverService:
    @staticmethod
    def create_handover_report(admission, outgoing_nurse, incoming_nurse, pending_tasks):
        return {
            "admission_number": admission.admission_number,
            "bed": admission.bed.bed_number,
            "outgoing_nurse": outgoing_nurse,
            "incoming_nurse": incoming_nurse,
            "pending_tasks": pending_tasks,
            "status": "HANDED_OVER"
        }
