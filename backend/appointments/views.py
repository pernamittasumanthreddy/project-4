import datetime
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import HospitalBranch, Department, AuditLog
from patients.models import Patient
from appointments.models import DoctorSchedule, DoctorLeave, Appointment, OPDQueueToken
from appointments.serializers import (
    DoctorScheduleSerializer,
    DoctorLeaveSerializer,
    AppointmentSerializer,
    BookAppointmentSerializer,
    OPDQueueTokenSerializer,
)


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorScheduleSerializer

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return DoctorSchedule.objects.none()
        return DoctorSchedule.objects.filter(tenant=tenant)

    @action(detail=False, methods=["get"], url_path="available-slots")
    def available_slots(self, request):
        """
        Generates available consultation slots for a specific doctor on a selected date.
        Filters out doctor leaves and existing confirmed appointments.
        """
        tenant = getattr(request, "tenant", None)
        doctor_id = request.query_params.get("doctor_id")
        date_str = request.query_params.get("date")

        if not doctor_id or not date_str:
            return Response({"error": "doctor_id and date are required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Check if doctor is on leave
        on_leave = DoctorLeave.objects.filter(
            tenant=tenant,
            doctor_id=doctor_id,
            start_date__lte=target_date,
            end_date__gte=target_date,
            is_approved=True
        ).exists()

        if on_leave:
            return Response({"doctor_id": doctor_id, "date": date_str, "on_leave": True, "slots": []})

        # 2. Get schedule for day of week
        day_of_week = target_date.weekday()
        schedules = DoctorSchedule.objects.filter(
            tenant=tenant,
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            is_active=True
        )

        # 3. Get existing booked appointments
        booked_times = set(
            Appointment.objects.filter(
                tenant=tenant,
                doctor_id=doctor_id,
                appointment_date=target_date,
                status__in=["SCHEDULED", "CONFIRMED", "CHECKED_IN", "IN_CONSULTATION"]
            ).values_list("start_time", flat=True)
        )

        available_slots = []
        for sched in schedules:
            current_time = datetime.datetime.combine(target_date, sched.start_time)
            end_time = datetime.datetime.combine(target_date, sched.end_time)
            slot_delta = datetime.timedelta(minutes=sched.slot_duration_minutes)
            buffer_delta = datetime.timedelta(minutes=sched.buffer_minutes)

            while current_time + slot_delta <= end_time:
                slot_start = current_time.time()
                slot_end = (current_time + slot_delta).time()

                is_booked = slot_start in booked_times

                available_slots.append({
                    "start_time": slot_start.strftime("%H:%M"),
                    "end_time": slot_end.strftime("%H:%M"),
                    "is_available": not is_booked,
                    "branch_id": str(sched.branch_id),
                    "department_id": str(sched.department_id)
                })

                current_time += slot_delta + buffer_delta

        return Response({
            "doctor_id": doctor_id,
            "date": date_str,
            "on_leave": False,
            "total_slots": len(available_slots),
            "slots": available_slots
        })


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    Handles appointment creation with concurrency protection (preventing double-booking),
    check-in workflow, and queue token assignment.
    """
    serializer_class = AppointmentSerializer
    filterset_fields = ["doctor_id", "status", "appointment_date", "appointment_type"]
    search_fields = ["appointment_number", "doctor_name", "patient__first_name", "patient__last_name", "patient__mrn"]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None)
        if not tenant:
            return Appointment.objects.none()
        return Appointment.objects.filter(tenant=tenant).select_related("patient", "branch", "department", "queue_token")

    def create(self, request, *args, **kwargs):
        tenant = getattr(request, "tenant", None)
        if not tenant:
            return Response({"error": "Tenant context required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookAppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data

        with transaction.atomic():
            # Concurrency row-level lock check: Ensure no concurrent booking occupies the exact slot
            conflict = Appointment.objects.select_for_update().filter(
                tenant=tenant,
                doctor_id=d["doctor_id"],
                appointment_date=d["appointment_date"],
                start_time=d["start_time"],
                status__in=["SCHEDULED", "CONFIRMED", "CHECKED_IN", "IN_CONSULTATION"]
            ).exists()

            if conflict:
                return Response(
                    {"error": "This slot was just booked by another patient. Please select an alternate time."},
                    status=status.HTTP_409_CONFLICT
                )

            # Generate appointment tracking number
            year = timezone.now().year
            apt_count = Appointment.objects.filter(tenant=tenant).count() + 1
            apt_number = f"APT-{year}-{apt_count:06d}"

            patient = Patient.objects.get(id=d["patient_id"], tenant=tenant)
            branch = HospitalBranch.objects.get(id=d["branch_id"], tenant=tenant)
            dept = Department.objects.get(id=d["department_id"], tenant=tenant)

            appointment = Appointment.objects.create(
                tenant=tenant,
                appointment_number=apt_number,
                patient=patient,
                doctor_id=d["doctor_id"],
                doctor_name=d["doctor_name"],
                branch=branch,
                department=dept,
                appointment_date=d["appointment_date"],
                start_time=d["start_time"],
                end_time=d["end_time"],
                appointment_type=d["appointment_type"],
                chief_complaint=d.get("chief_complaint", ""),
                status="CONFIRMED"
            )

        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="check-in")
    def check_in(self, request, pk=None):
        """
        Marks patient as checked-in at hospital reception and generates an OPD Queue Token.
        """
        appointment = self.get_object()
        tenant = appointment.tenant

        if appointment.status in ["CHECKED_IN", "IN_CONSULTATION", "COMPLETED"]:
            return Response({"error": f"Appointment is already {appointment.status}."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            today = timezone.now().date()
            # Calculate next token number for doctor on today's queue
            last_token = OPDQueueToken.objects.filter(
                tenant=tenant,
                doctor_id=appointment.doctor_id,
                queue_date=today
            ).order_by("-token_number").first()

            next_token = (last_token.token_number + 1) if last_token else 1

            appointment.status = "CHECKED_IN"
            appointment.checked_in_at = timezone.now()
            appointment.token_number = next_token
            appointment.save()

            queue_token = OPDQueueToken.objects.create(
                tenant=tenant,
                appointment=appointment,
                branch=appointment.branch,
                department=appointment.department,
                doctor_id=appointment.doctor_id,
                token_number=next_token,
                queue_date=today,
                status="WAITING"
            )

        return Response({
            "message": f"Patient checked in successfully. Token #{next_token} assigned.",
            "token_number": next_token,
            "appointment": AppointmentSerializer(appointment).data
        })

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_appointment(self, request, pk=None):
        appointment = self.get_object()
        reason = request.data.get("reason", "Cancelled by patient or reception")

        if appointment.status in ["COMPLETED", "CANCELLED"]:
            return Response({"error": f"Cannot cancel an appointment that is already {appointment.status}."}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = "CANCELLED"
        appointment.cancellation_reason = reason
        appointment.cancelled_at = timezone.now()
        appointment.save()

        # Update queue token if existed
        if hasattr(appointment, "queue_token"):
            appointment.queue_token.status = "SKIPPED"
            appointment.queue_token.save()

        return Response({"message": "Appointment cancelled.", "appointment": AppointmentSerializer(appointment).data})
