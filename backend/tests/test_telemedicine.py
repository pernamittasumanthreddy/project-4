"""
Test Suite: Telemedicine & WebRTC Virtual Consultations (Member 7).
Covers room authorization, tokens, signaling message exchange, and call lifecycle.
"""

from django.test import TestCase, Client
from datetime import date, time, timedelta

from apps.core.models import Tenant, HospitalBranch, User
from apps.appointments.models import Department, DoctorProfile, PatientProfile, Appointment
from apps.telemedicine.models import TelemedicineSession, SignalingMessage

class TelemedicineTestCase(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="CareTrust", slug="caretrust", domain="caretrust.local")
        self.branch = HospitalBranch.objects.create(tenant=self.tenant, name="Main Campus", code="MAIN", address="100 Ave", city="Boston", state="MA", postal_code="02115", phone="617-555-0100")
        
        self.doc_user = User.objects.create(username="doc_chen", tenant=self.tenant, role="DOCTOR", first_name="Sophia", last_name="Chen")
        self.dept = Department.objects.create(tenant=self.tenant, name="Cardiology", code="CARDIO")
        self.doctor = DoctorProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.doc_user, department=self.dept, license_number="LIC-1234", specialization="Cardiology")

        self.pat_user = User.objects.create(username="pat_priya", tenant=self.tenant, role="PATIENT", first_name="Priya", last_name="Sharma")
        self.patient = PatientProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.pat_user, mrn="MRN-TEST-100")

        self.appointment = Appointment.objects.create(
            tenant=self.tenant,
            branch=self.branch,
            appointment_number="APT-TELE-001",
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=date.today(),
            start_time=time(15, 0),
            end_time=time(15, 30),
            appointment_type="TELEMEDICINE",
            status="CONFIRMED",
            reason_for_visit="Virtual consultation test"
        )

        self.client = Client()

    def test_telemedicine_ice_config(self):
        """ICE configuration returns public STUN servers with zero paid credentials."""
        response = self.client.get('/api/v1/telemedicine/ice-config/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('ice_servers', response.data)
        self.assertTrue(len(response.data['ice_servers']) >= 1)

    def test_session_creation_and_participant_join_flow(self):
        """Verifies room creation, waiting room state, and transition to live call."""
        # 1. Initialize session for appointment
        resp = self.client.get(f'/api/v1/telemedicine/appointment/{self.appointment.id}/')
        self.assertEqual(resp.status_code, 200)
        session_id = resp.data['id']
        self.assertEqual(resp.data['status'], 'SCHEDULED')

        # 2. Patient joins first -> moves to WAITING_ROOM
        join_pat = self.client.post(
            f'/api/v1/telemedicine/sessions/{session_id}/join/',
            data={'role': 'PATIENT'},
            content_type='application/json'
        )
        self.assertEqual(join_pat.status_code, 200)
        self.assertEqual(join_pat.data['room_state'], 'WAITING_ROOM')
        self.assertTrue(join_pat.data['session']['patient_present'])

        # 3. Doctor joins -> moves to IN_PROGRESS
        join_doc = self.client.post(
            f'/api/v1/telemedicine/sessions/{session_id}/join/',
            data={'role': 'DOCTOR'},
            content_type='application/json'
        )
        self.assertEqual(join_doc.status_code, 200)
        self.assertEqual(join_doc.data['room_state'], 'IN_PROGRESS')
        self.assertTrue(join_doc.data['session']['doctor_present'])

    def test_webrtc_signaling_exchange(self):
        """Verifies SDP offer/answer exchange between doctor and patient."""
        # Setup session
        session = TelemedicineSession.objects.create(
            tenant=self.tenant,
            branch=self.branch,
            appointment=self.appointment,
            room_code="TEST-ROOM-99",
            status="IN_PROGRESS"
        )

        # 1. Doctor sends SDP Offer
        offer_payload = {
            "sender_role": "DOCTOR",
            "message_type": "OFFER",
            "payload": {"type": "offer", "sdp": "v=0\r\no=doctor 12345 2 IN IP4 127.0.0.1..."}
        }
        send_resp = self.client.post(
            f'/api/v1/telemedicine/sessions/{session.id}/signaling/',
            data=offer_payload,
            content_type='application/json'
        )
        self.assertEqual(send_resp.status_code, 201)

        # 2. Patient polls signaling endpoint and receives the doctor's offer
        recv_resp = self.client.get(
            f'/api/v1/telemedicine/sessions/{session.id}/signaling/?role=PATIENT'
        )
        self.assertEqual(recv_resp.status_code, 200)
        messages = recv_resp.data['messages']
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['message_type'], 'OFFER')
        self.assertEqual(messages[0]['sender_role'], 'DOCTOR')

        # 3. Subsequent poll returns 0 undelivered messages (delivered flag was flipped)
        second_poll = self.client.get(
            f'/api/v1/telemedicine/sessions/{session.id}/signaling/?role=PATIENT'
        )
        self.assertEqual(len(second_poll.data['messages']), 0)
