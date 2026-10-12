from appointments.models import DoctorLeave, Appointment

class DoctorLeaveService:
    @staticmethod
    def apply_doctor_leave(tenant, doctor_id, doctor_name, start_date, end_date, reason=""):
        leave = DoctorLeave.objects.create(
            tenant=tenant, doctor_id=doctor_id, doctor_name=doctor_name,
            start_date=start_date, end_date=end_date, reason=reason, is_approved=True
        )
        conflicts = Appointment.objects.filter(
            tenant=tenant, doctor_id=doctor_id,
            appointment_date__gte=start_date, appointment_date__lte=end_date,
            status__in=["SCHEDULED", "CONFIRMED"]
        )
        count = conflicts.count()
        conflicts.update(status="RESCHEDULED", cancellation_reason=f"Doctor leave: {reason}")
        return {"leave_id": str(leave.id), "impacted_appointments": count}
