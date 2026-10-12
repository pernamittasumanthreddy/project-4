"""
Clinical EMR Views (Member 3 integration contract).
Provides patient encounter records, SOAP consultation notes, diagnoses, and prescription workflows.
"""

from datetime import datetime, date
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.clinical.models import Encounter, Diagnosis, Prescription, PrescriptionItem, Allergy, MedicalHistory
from apps.clinical.serializers import (
    EncounterSerializer,
    DiagnosisSerializer,
    PrescriptionSerializer,
    AllergySerializer,
    MedicalHistorySerializer,
)
from apps.appointments.models import PatientProfile, DoctorProfile

class EncounterListCreateView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Encounter.objects.all().select_related('patient__user', 'doctor__user', 'tenant')
        tenant = getattr(request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)

        patient_id = request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)

        doctor_id = request.query_params.get('doctor_id')
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)

        status_param = request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param.upper())

        serializer = EncounterSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')

        patient = PatientProfile.objects.filter(id=patient_id).first()
        doctor = DoctorProfile.objects.filter(id=doctor_id).first()

        if not patient or not doctor:
            return Response(
                {"error": "Valid patient_id and doctor_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        encounter_num = f"ENC-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"

        encounter = Encounter.objects.create(
            tenant=doctor.tenant,
            branch=doctor.branch,
            encounter_number=encounter_num,
            patient=patient,
            doctor=doctor,
            encounter_date=data.get('encounter_date', date.today()),
            encounter_type=data.get('encounter_type', 'TELEMEDICINE'),
            status='DRAFT',
            chief_complaint=data.get('chief_complaint', 'Consultation evaluation'),
            vitals=data.get('vitals', {}),
            subjective_notes=data.get('subjective_notes', ''),
            physical_examination=data.get('physical_examination', ''),
            assessment=data.get('assessment', ''),
            clinical_plan=data.get('clinical_plan', ''),
        )

        return Response(EncounterSerializer(encounter).data, status=status.HTTP_201_CREATED)


class EncounterDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer


class EncounterSignView(views.APIView):
    """
    Finalizes and digitally signs a clinical encounter.
    Locked after signing to preserve HIPAA audit trail integrity.
    """
    permission_classes = [AllowAny]

    def post(self, request, pk):
        encounter = Encounter.objects.filter(id=pk).first()
        if not encounter:
            return Response({"error": "Encounter not found"}, status=status.HTTP_404_NOT_FOUND)

        if encounter.status == 'SIGNED':
            return Response(
                {"error": "This encounter has already been locked and signed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.utils import timezone
        doctor = encounter.doctor
        encounter.status = 'SIGNED'
        encounter.signed_by = doctor
        encounter.signed_at = timezone.now()
        encounter.save()

        # Update associated appointment status to COMPLETED if linked
        if encounter.appointment:
            encounter.appointment.status = 'COMPLETED'
            encounter.appointment.save()

        # Dispatch clinical update notification
        try:
            from apps.notifications.services import NotificationDispatcher
            NotificationDispatcher.dispatch_clinical_summary_signed(encounter)
        except Exception:
            pass

        return Response({
            "success": True,
            "message": f"Encounter #{encounter.encounter_number} signed by {doctor.full_name}.",
            "encounter": EncounterSerializer(encounter).data
        })


class PrescriptionListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        qs = Prescription.objects.all().prefetch_related('items').select_related('patient', 'doctor')
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)

        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)

        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param.upper())

        return qs


class PatientEMRSummaryView(views.APIView):
    """
    Aggregates comprehensive longitudinal health record for a patient.
    Integrates Encounters, Diagnoses, Allergies, Chronic History, and Prescriptions.
    """
    permission_classes = [AllowAny]

    def get(self, request, patient_id):
        patient = PatientProfile.objects.filter(id=patient_id).first()
        if not patient:
            return Response({"error": "Patient profile not found."}, status=status.HTTP_404_NOT_FOUND)

        allergies = Allergy.objects.filter(patient=patient)
        history = MedicalHistory.objects.filter(patient=patient)
        diagnoses = Diagnosis.objects.filter(patient=patient)
        prescriptions = Prescription.objects.filter(patient=patient)
        encounters = Encounter.objects.filter(patient=patient)

        return Response({
            "patient": {
                "id": str(patient.id),
                "mrn": patient.mrn,
                "name": patient.full_name,
                "blood_group": patient.blood_group,
                "gender": patient.gender,
                "dob": patient.date_of_birth,
            },
            "allergies": AllergySerializer(allergies, many=True).data,
            "medical_history": MedicalHistorySerializer(history, many=True).data,
            "diagnoses": DiagnosisSerializer(diagnoses, many=True).data,
            "prescriptions": PrescriptionSerializer(prescriptions, many=True).data,
            "encounters_count": encounters.count(),
        })
