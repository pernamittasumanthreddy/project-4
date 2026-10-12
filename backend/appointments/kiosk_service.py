import datetime
from django.db import transaction
from django.utils import timezone
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment, OPDQueueToken


class WalkInKioskService:
    """
    Self-service kiosk and reception desk workflow for urgent walk-in OPD token issuance.
    """

    @classmethod
    def generate_walk_in_token(
        cls,
        tenant: Tenant,
        patient_id: str,
        doctor_id: str,
        doctor_name: str,
        branch_id: str,
        department_id: str,
        chief_complaint: str = "Walk-in acute care"
    ) -> dict:
        """
        Creates an immediate WALK_IN appointment and allocates the next real-time queue token.
        """
        today = timezone.now().date()
        now_time = timezone.now().time()

        patient = Patient.objects.filter(id=patient_id, tenant=tenant).first()
        if not patient:
            raise ValueError("Patient not found.")

        branch = HospitalBranch.objects.filter(id=branch_id, tenant=tenant).first()
        department = Department.objects.filter(id=department_id, tenant=tenant).first()

        if not branch or not department:
            raise ValueError("Branch or department not found.")

        with transaction.atomic():
            # Calculate next token number for this doctor's today queue
            last_token = OPDQueueToken.objects.filter(
                tenant=tenant,
                doctor_id=doctor_id,
                queue_date=today
            ).order_by("-token_number").first()

            next_token = (last_token.token_number + 1) if last_token else 1

            year = today.year
            count = Appointment.objects.filter(tenant=tenant).count() + 1
            apt_num = f"WLK-{year}-{count:06d}"

            apt = Appointment.objects.create(
                tenant=tenant,
                appointment_number=apt_num,
                patient=patient,
                doctor_id=doctor_id,
                doctor_name=doctor_name,
                branch=branch,
                department=department,
                appointment_date=today,
                start_time=now_time,
                end_time=(datetime.datetime.combine(today, now_time) + datetime.timedelta(minutes=15)).time(),
                appointment_type="WALK_IN",
                status="CHECKED_IN",
                token_number=next_token,
                chief_complaint=chief_complaint,
                checked_in_at=timezone.now()
            )

            queue_token = OPDQueueToken.objects.create(
                tenant=tenant,
                appointment=apt,
                branch=branch,
                department=department,
                doctor_id=doctor_id,
                token_number=next_token,
                queue_date=today,
                status="WAITING"
            )

        return {
            "appointment_id": str(apt.id),
            "appointment_number": apt.appointment_number,
            "token_number": next_token,
            "queue_date": str(today),
            "doctor_name": doctor_name,
            "patient_mrn": patient.mrn,
            "patient_name": patient.full_name,
            "status": "WAITING"
        }
