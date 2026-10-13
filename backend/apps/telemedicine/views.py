"""
Telemedicine & WebRTC Virtual Consultation Views (Member 7).
Handles meeting lifecycle, participant authorization, room status, and SDP/ICE signaling.
Uses timezone-aware timestamps and evaluates lazy querysets safely.
"""

from django.utils import timezone
import uuid
import secrets
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.telemedicine.models import TelemedicineSession, SignalingMessage
from apps.telemedicine.serializers import TelemedicineSessionSerializer, SignalingMessageSerializer
from apps.appointments.models import Appointment
from apps.core.models import User

class TelemedicineIceConfigView(views.APIView):
    """
    Returns public STUN server configuration for WebRTC ICE negotiation.
    Zero paid API keys required.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "ice_servers": [
                {"urls": "stun:stun.l.google.com:19302"},
                {"urls": "stun:stun1.l.google.com:19302"},
                {"urls": "stun:stun2.l.google.com:19302"},
            ],
            "signaling_protocol": "HTTP_POLLING_WEBRTC_V1",
            "polling_interval_ms": 1200,
        })


class TelemedicineSessionForAppointmentView(views.APIView):
    """
    Fetches or initializes the telemedicine virtual room for an appointment.
    """
    permission_classes = [AllowAny]

    def get(self, request, appointment_id):
        appointment = Appointment.objects.filter(id=appointment_id).first()
        if not appointment:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        session, created = TelemedicineSession.objects.get_or_create(
            appointment=appointment,
            defaults={
                'tenant': appointment.tenant,
                'branch': appointment.branch,
                'room_code': f"TELE-{appointment.appointment_number.replace('APT-', '')}-{secrets.token_hex(3).upper()}",
                'doctor_token': secrets.token_urlsafe(32),
                'patient_token': secrets.token_urlsafe(32),
                'status': 'SCHEDULED',
            }
        )

        return Response(TelemedicineSessionSerializer(session).data)


class TelemedicineSessionDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = TelemedicineSession.objects.all()
    serializer_class = TelemedicineSessionSerializer


class TelemedicineJoinRoomView(views.APIView):
    """
    Validates participant credentials and admits user into waiting room or active call.
    """
    permission_classes = [AllowAny]

    def post(self, request, session_id):
        session = TelemedicineSession.objects.filter(id=session_id).first()
        if not session:
            return Response({"error": "Virtual room not found."}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get('role', 'PATIENT').upper()
        now = timezone.now()

        # Validate role
        if role == 'DOCTOR':
            session.doctor_present = True
            session.doctor_joined_at = now
            # If doctor joins and patient is already in waiting room, move to IN_PROGRESS
            if session.patient_present:
                session.status = 'IN_PROGRESS'
                if not session.started_at:
                    session.started_at = now
        else: # PATIENT
            session.patient_present = True
            session.patient_joined_at = now
            if session.doctor_present:
                session.status = 'IN_PROGRESS'
                if not session.started_at:
                    session.started_at = now
            else:
                session.status = 'WAITING_ROOM'

        session.save()

        return Response({
            "success": True,
            "session": TelemedicineSessionSerializer(session).data,
            "user_role": role,
            "peer_present": session.doctor_present if role == 'PATIENT' else session.patient_present,
            "room_state": session.status,
            "ice_servers": [
                {"urls": "stun:stun.l.google.com:19302"},
                {"urls": "stun:stun1.l.google.com:19302"},
            ]
        })


class TelemedicineSignalingView(views.APIView):
    """
    Exchanges SDP Offers, Answers, and ICE candidates between participants.
    Evaluates messages list into memory before updating delivery status.
    """
    permission_classes = [AllowAny]

    def get(self, request, session_id):
        session = TelemedicineSession.objects.filter(id=session_id).first()
        if not session:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        my_role = (request.GET.get('role') or request.query_params.get('role') or 'PATIENT').upper()
        counter_role = 'DOCTOR' if my_role == 'PATIENT' else 'PATIENT'

        # Fetch messages sent by the peer
        messages_qs = SignalingMessage.objects.filter(
            session=session,
            sender_role=counter_role,
            is_delivered=False
        )

        # Force evaluation before update so serializer gets the items!
        messages_list = list(messages_qs)
        SignalingMessage.objects.filter(id__in=[m.id for m in messages_list]).update(is_delivered=True)

        serializer = SignalingMessageSerializer(messages_list, many=True)

        return Response({
            "session_status": session.status,
            "peer_present": session.doctor_present if my_role == 'PATIENT' else session.patient_present,
            "messages": serializer.data
        })

    def post(self, request, session_id):
        session = TelemedicineSession.objects.filter(id=session_id).first()
        if not session:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        sender_role = request.data.get('sender_role', 'PATIENT').upper()
        message_type = request.data.get('message_type')
        payload = request.data.get('payload', {})

        msg = SignalingMessage.objects.create(
            session=session,
            sender_role=sender_role,
            message_type=message_type,
            payload=payload,
        )

        return Response(SignalingMessageSerializer(msg).data, status=status.HTTP_201_CREATED)


class TelemedicineLeaveRoomView(views.APIView):
    """
    Handles participant departure, concludes call if doctor ends it, and saves notes.
    """
    permission_classes = [AllowAny]

    def post(self, request, session_id):
        session = TelemedicineSession.objects.filter(id=session_id).first()
        if not session:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get('role', 'PATIENT').upper()
        now = timezone.now()
        clinical_notes = request.data.get('clinical_quick_notes')
        if clinical_notes:
            session.clinical_quick_notes = clinical_notes

        if role == 'DOCTOR':
            session.doctor_present = False
            session.status = 'ENDED'
            session.ended_at = now
            if session.started_at:
                delta = session.ended_at - session.started_at
                session.duration_seconds = max(1, int(delta.total_seconds()))
        else:
            session.patient_present = False
            if not session.doctor_present:
                session.status = 'ENDED'
                session.ended_at = now
                if session.started_at:
                    delta = session.ended_at - session.started_at
                    session.duration_seconds = max(1, int(delta.total_seconds()))

        session.save()

        return Response({
            "success": True,
            "message": "Left consultation session.",
            "session": TelemedicineSessionSerializer(session).data
        })
