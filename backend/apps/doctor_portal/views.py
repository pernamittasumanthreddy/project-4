"""
Doctor Portal APIs (Member 7).
Clinical decision workspace, daily agenda, patient queue, and encounter documentation.
"""

from datetime import datetime, date, timedelta
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.appointments.models import DoctorProfile, Appointment, PatientProfile
from apps.appointments.serializers import AppointmentSerializer, DoctorProfileSerializer
from apps.clinical.models import Encounter, Diagnosis, Prescription, PrescriptionItem, Allergy, MedicalHistory
from apps.clinical.serializers import EncounterSerializer, DiagnosisSerializer, PrescriptionSerializer, AllergySerializer
from apps.diagnostics.models import LabReport, RadiologyReport
from apps.diagnostics.serializers import LabReportSerializer, RadiologyReportSerializer
from apps.telemedicine.models import TelemedicineSession
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from apps.core.models import User, AuditLog

def resolve_doctor_for_request(request):
    """Helper to resolve physician from active session or demo fallback."""
    django_request = getattr(request, '_request', request)
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and hasattr(user, 'doctor_profile'):
        return user.doctor_profile

    # Check X-Impersonate-User header from META
    impersonate = django_request.META.get('HTTP_X_IMPERSONATE_USER')
    if impersonate:
        u = User.objects.filter(username=impersonate).first()
        if u and hasattr(u, 'doctor_profile'):
            return u.doctor_profile

    # Fallback to primary seeded doctor (Dr. Sophia Chen)
    return DoctorProfile.objects.first()



class DoctorDashboardView(views.APIView):
    """
    Central Doctor Dashboard API.
    Provides today's appointments, patient queue, pending lab reviews, and follow-ups.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        doctor = resolve_doctor_for_request(request)
        if not doctor:
            return Response({"error": "Physician profile not found"}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()

        # 1. Appointments for today
        all_appts = Appointment.objects.filter(doctor=doctor).select_related('patient__user')
        todays_appts = all_appts.filter(appointment_date=today).order_by('start_time')
        upcoming_appts = all_appts.filter(appointment_date__gt=today).order_by('appointment_date', 'start_time')[:10]

        # 2. Patient Queue & In-Progress stats
        waiting_count = todays_appts.filter(status='CONFIRMED', checked_in_at__isnull=False).count()
        in_progress_count = todays_appts.filter(status='IN_PROGRESS').count()
        completed_today_count = todays_appts.filter(status='COMPLETED').count()

        # 3. Pending diagnostic investigations requiring clinical review
        pending_labs = LabReport.objects.filter(ordering_doctor=doctor, status__in=['ORDERED', 'COLLECTED', 'ANALYZED']).count()
        pending_imaging = RadiologyReport.objects.filter(ordering_doctor=doctor, status__in=['ORDERED', 'CAPTURED']).count()

        # 4. Telemedicine sessions today
        tele_sessions = TelemedicineSession.objects.filter(appointment__doctor=doctor, appointment__appointment_date=today)

        # 5. Doctor notifications
        notifications = Notification.objects.filter(recipient=doctor.user, is_read=False).order_by('-created_at')[:5]

        # Audit
        if doctor.tenant:
            AuditLog.objects.create(
                tenant=doctor.tenant,
                user=doctor.user,
                action="VIEW_DOCTOR_DASHBOARD",
                resource_type="DOCTOR_DASHBOARD",
                resource_id=str(doctor.id),
                details={"doctor_license": doctor.license_number}
            )

        return Response({
            "doctor": {
                "id": str(doctor.id),
                "name": doctor.full_name,
                "first_name": doctor.user.first_name,
                "specialization": doctor.specialization,
                "department": doctor.department.name if doctor.department else "General Medicine",
                "office_room": doctor.office_room,
                "avatar_url": doctor.user.avatar_url,
                "tenant_name": doctor.tenant.name if doctor.tenant else "CareTrust Health",
            },
            "today_metrics": {
                "total_scheduled_today": todays_appts.count(),
                "waiting_patients_count": waiting_count,
                "active_consultations_count": in_progress_count,
                "completed_consultations_today": completed_today_count,
                "pending_lab_reviews": pending_labs,
                "pending_radiology_reviews": pending_imaging,
                "virtual_consultations_today": tele_sessions.count(),
            },
            "today_appointments": AppointmentSerializer(todays_appts, many=True).data,
            "upcoming_appointments": AppointmentSerializer(upcoming_appts, many=True).data,
            "recent_notifications": NotificationSerializer(notifications, many=True).data,
        })


class DoctorScheduleAgendaView(views.APIView):
    """
    Physician Schedule Agenda supporting Daily and Weekly calendar views.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        doctor = resolve_doctor_for_request(request)
        if not doctor:
            return Response({"error": "Physician not found"}, status=status.HTTP_404_NOT_FOUND)

        view_mode = request.query_params.get('view', 'day') # 'day' or 'week'
        date_str = request.query_params.get('date')

        if date_str:
            try:
                base_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                base_date = date.today()
        else:
            base_date = date.today()

        if view_mode == 'week':
            start_date = base_date - timedelta(days=base_date.weekday())
            end_date = start_date + timedelta(days=6)
            appts = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__range=[start_date, end_date]
            ).select_related('patient__user').order_by('appointment_date', 'start_time')
        else:
            start_date = base_date
            end_date = base_date
            appts = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=base_date
            ).select_related('patient__user').order_by('start_time')

        return Response({
            "doctor_id": str(doctor.id),
            "doctor_name": doctor.full_name,
            "view_mode": view_mode,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "total_appointments": appts.count(),
            "appointments": AppointmentSerializer(appts, many=True).data
        })


class DoctorConsultationWorkspaceView(views.APIView):
    """
    Comprehensive Clinical Consultation Workspace.
    Integrates SOAP notes, vital signs, allergy checks, lab/radiology review, and prescription writing.
    """
    permission_classes = [AllowAny]

    def get(self, request, appointment_id):
        appointment = Appointment.objects.filter(id=appointment_id).select_related('patient__user', 'doctor__user').first()
        if not appointment:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        patient = appointment.patient
        doctor = appointment.doctor

        # Fetch or initialize clinical encounter
        encounter, created = Encounter.objects.get_or_create(
            appointment=appointment,
            defaults={
                'tenant': appointment.tenant,
                'branch': appointment.branch,
                'encounter_number': f"ENC-{appointment.appointment_number.replace('APT-', '')}",
                'patient': patient,
                'doctor': doctor,
                'encounter_date': appointment.appointment_date,
                'encounter_type': appointment.appointment_type,
                'status': 'DRAFT',
                'chief_complaint': appointment.reason_for_visit,
                'vitals': {
                    "bp_systolic": 122,
                    "bp_diastolic": 78,
                    "heart_rate": 72,
                    "temp_c": 36.8,
                    "spo2": 98,
                    "weight_kg": 68.5,
                    "height_cm": 172,
                }
            }
        )

        # Longitudinal EMR data
        allergies = Allergy.objects.filter(patient=patient)
        history = MedicalHistory.objects.filter(patient=patient)
        past_encounters = Encounter.objects.filter(patient=patient, status='SIGNED').exclude(id=encounter.id)[:5]
        lab_reports = LabReport.objects.filter(patient=patient).order_by('-order_date')[:6]
        radiology_reports = RadiologyReport.objects.filter(patient=patient).order_by('-study_date')[:4]
        active_prescriptions = Prescription.objects.filter(patient=patient, status='ACTIVE').prefetch_related('items')

        # Virtual session
        tele_session = TelemedicineSession.objects.filter(appointment=appointment).first()

        return Response({
            "appointment": AppointmentSerializer(appointment).data,
            "encounter": EncounterSerializer(encounter).data,
            "patient_summary": {
                "id": str(patient.id),
                "mrn": patient.mrn,
                "name": patient.full_name,
                "gender": patient.gender,
                "dob": patient.date_of_birth,
                "blood_group": patient.blood_group,
                "insurance": f"{patient.insurance_provider} ({patient.insurance_policy_number})"
            },
            "allergies": AllergySerializer(allergies, many=True).data,
            "medical_history": [
                {"id": str(h.id), "condition": h.condition_name, "onset_year": h.onset_year, "status": h.status}
                for h in history
            ],
            "active_prescriptions": PrescriptionSerializer(active_prescriptions, many=True).data,
            "lab_reports": LabReportSerializer(lab_reports, many=True).data,
            "radiology_reports": RadiologyReportSerializer(radiology_reports, many=True).data,
            "past_encounters_count": past_encounters.count(),
            "telemedicine_session_id": str(tele_session.id) if tele_session else None,
        })

    def post(self, request, appointment_id):
        """Save SOAP notes, vitals, or add diagnosis/prescription to encounter."""
        appointment = Appointment.objects.filter(id=appointment_id).first()
        if not appointment:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        encounter = Encounter.objects.filter(appointment=appointment).first()
        if not encounter:
            return Response({"error": "Encounter record not found"}, status=status.HTTP_404_NOT_FOUND)

        if encounter.status == 'SIGNED':
            return Response(
                {"error": "This clinical encounter is already signed and locked. Cannot modify signed records."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data

        # Update clinical documentation
        if 'vitals' in data:
            encounter.vitals = data['vitals']
        if 'chief_complaint' in data:
            encounter.chief_complaint = data['chief_complaint']
        if 'subjective_notes' in data:
            encounter.subjective_notes = data['subjective_notes']
        if 'physical_examination' in data:
            encounter.physical_examination = data['physical_examination']
        if 'assessment' in data:
            encounter.assessment = data['assessment']
        if 'clinical_plan' in data:
            encounter.clinical_plan = data['clinical_plan']

        encounter.save()

        # Add new diagnosis if supplied
        new_diag = data.get('new_diagnosis')
        if new_diag and new_diag.get('description'):
            Diagnosis.objects.create(
                tenant=encounter.tenant,
                branch=encounter.branch,
                encounter=encounter,
                patient=encounter.patient,
                icd10_code=new_diag.get('icd10_code', 'R69'),
                description=new_diag.get('description'),
                severity=new_diag.get('severity', 'MODERATE'),
                is_primary=new_diag.get('is_primary', False),
                diagnosed_date=date.today(),
            )

        # Add new prescription if supplied
        new_rx = data.get('new_prescription')
        if new_rx and new_rx.get('medications'):
            rx = Prescription.objects.create(
                tenant=encounter.tenant,
                branch=encounter.branch,
                prescription_number=f"RX-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                encounter=encounter,
                patient=encounter.patient,
                doctor=encounter.doctor,
                status='ACTIVE',
                issued_date=date.today(),
                valid_until=date.today() + timedelta(days=90),
                special_instructions=new_rx.get('instructions', ''),
            )
            for m in new_rx.get('medications', []):
                PrescriptionItem.objects.create(
                    prescription=rx,
                    medication_name=m.get('medication_name', 'Amoxicillin'),
                    dosage=m.get('dosage', '500 mg'),
                    route=m.get('route', 'ORAL'),
                    frequency=m.get('frequency', 'Twice daily after meals'),
                    duration_days=m.get('duration_days', 7),
                    quantity=m.get('quantity', 14),
                    instructions=m.get('instructions', ''),
                )

        return Response({
            "success": True,
            "message": "Clinical consultation notes updated.",
            "encounter": EncounterSerializer(encounter).data
        })
