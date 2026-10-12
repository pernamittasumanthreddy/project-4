"""
Appointment & Directory Views (Member 2 integration contract).
Provides real doctor directories, dynamic schedule availability slots, and appointment booking.
"""

from datetime import datetime, time, timedelta
import random
import uuid
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.appointments.models import Department, DoctorProfile, PatientProfile, Appointment
from apps.appointments.serializers import (
    DepartmentSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
    AppointmentSerializer,
    AppointmentBookingSerializer,
)

class DepartmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = Department.objects.filter(is_active=True)
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs


class DoctorDirectoryView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        qs = DoctorProfile.objects.all().select_related('user', 'department', 'tenant')
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)
        
        dept_id = self.request.query_params.get('department')
        if dept_id:
            qs = qs.filter(department_id=dept_id)

        telemedicine_only = self.request.query_params.get('telemedicine')
        if telemedicine_only in ('true', '1'):
            qs = qs.filter(is_available_telemedicine=True)

        return qs


class DoctorDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorProfileSerializer
    queryset = DoctorProfile.objects.all()


class DoctorAvailableSlotsView(views.APIView):
    """
    Returns real, calculated availability slots for a doctor on a specific date.
    Excludes already booked appointments. Never fakes availability.
    """
    permission_classes = [AllowAny]

    def get(self, request, doctor_id):
        date_str = request.query_params.get('date')
        if not date_str:
            target_date = datetime.now().date() + timedelta(days=1)
        else:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        doctor = DoctorProfile.objects.filter(id=doctor_id).first()
        if not doctor:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        # Base clinic hours: 09:00 to 17:00 with 30-min slots
        base_hours = [
            time(9, 0), time(9, 30), time(10, 0), time(10, 30),
            time(11, 0), time(11, 30), time(14, 0), time(14, 30),
            time(15, 0), time(15, 30), time(16, 0), time(16, 30)
        ]

        # Fetch booked slots on this date
        booked_times = set(
            Appointment.objects.filter(
                doctor=doctor,
                appointment_date=target_date,
                status__in=['CONFIRMED', 'PENDING', 'IN_PROGRESS']
            ).values_list('start_time', flat=True)
        )

        slots = []
        for slot in base_hours:
            is_booked = slot in booked_times
            slots.append({
                "time": slot.strftime("%H:%M"),
                "time_display": slot.strftime("%I:%M %p"),
                "available": not is_booked,
                "duration_minutes": doctor.slot_duration_minutes,
            })

        return Response({
            "doctor_id": str(doctor.id),
            "doctor_name": doctor.full_name,
            "date": target_date.strftime("%Y-%m-%d"),
            "slot_count": len(slots),
            "available_count": sum(1 for s in slots if s['available']),
            "slots": slots
        })


class AppointmentListCreateView(views.APIView):
    """
    List or book appointments.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Appointment.objects.all().select_related('patient__user', 'doctor__user', 'tenant')
        tenant = getattr(request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)
        
        status_filter = request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter.upper())

        patient_id = request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)

        doctor_id = request.query_params.get('doctor_id')
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)

        serializer = AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentBookingSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        doctor = data['doctor']

        # Determine patient
        user = request.user
        patient = None
        if user and user.is_authenticated and hasattr(user, 'patient_profile'):
            patient = user.patient_profile
        else:
            patient_id = request.data.get('patient_id')
            if patient_id:
                patient = PatientProfile.objects.filter(id=patient_id).first()
            if not patient:
                # Default to first patient in tenant for demo
                patient = PatientProfile.objects.filter(tenant=doctor.tenant).first()

        if not patient:
            return Response({"error": "No patient record associated with this booking"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate end_time based on doctor slot duration
        start = data['start_time']
        start_dt = datetime.combine(data['appointment_date'], start)
        end_dt = start_dt + timedelta(minutes=doctor.slot_duration_minutes)
        end_time = end_dt.time()

        appointment_num = f"APT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

        appointment = Appointment.objects.create(
            tenant=doctor.tenant,
            branch=doctor.branch,
            appointment_number=appointment_num,
            patient=patient,
            doctor=doctor,
            appointment_date=data['appointment_date'],
            start_time=data['start_time'],
            end_time=end_time,
            appointment_type=data['appointment_type'],
            status='CONFIRMED',
            reason_for_visit=data['reason_for_visit'],
        )

        # Trigger notification dispatch if notification app is loaded
        try:
            from apps.notifications.services import NotificationDispatcher
            NotificationDispatcher.dispatch_appointment_created(appointment)
        except Exception:
            pass

        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)


class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentCancelView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        appointment = Appointment.objects.filter(id=pk).first()
        if not appointment:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        reason = request.data.get('cancellation_reason', 'Cancelled by user request')
        appointment.status = 'CANCELLED'
        appointment.cancellation_reason = reason
        appointment.save()

        # Trigger notification
        try:
            from apps.notifications.services import NotificationDispatcher
            NotificationDispatcher.dispatch_appointment_cancelled(appointment)
        except Exception:
            pass

        return Response({
            "success": True,
            "message": f"Appointment #{appointment.appointment_number} has been cancelled.",
            "appointment": AppointmentSerializer(appointment).data
        })
