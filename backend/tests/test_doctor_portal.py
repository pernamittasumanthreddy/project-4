"""
Test Suite: Doctor Portal Workspace & Clinical APIs (Member 7).
Covers clinician schedule, consultation notes, vitals recording, and digital sign-off lock.
"""

from django.test import TestCase, Client
from datetime import date, time, timedelta
from decimal import Decimal

from apps.core.models import Tenant, HospitalBranch, User
from apps.appointments.models import Department, DoctorProfile, PatientProfile, Appointment
from apps.clinical.models import Encounter, Diagnosis, Prescription

class DoctorPortalTestCase(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="CareTrust", slug="caretrust", domain="caretrust.local")
        self.branch = HospitalBranch.objects.create(tenant=self.tenant, name="Main Campus", code="MAIN", address="100 Ave", city="Boston", state="MA", postal_code="02115", phone="617-555-0100")
        
        self.doc_user = User.objects.create(username="doc_chen", tenant=self.tenant, role="DOCTOR", first_name="Sophia", last_name="Chen")
        self.dept = Department.objects.create(tenant=self.tenant, name="Cardiology", code="CARDIO")
        self.doctor = DoctorProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.doc_user, department=self.dept, license_number="LIC-1234", specialization="Cardiology")

        self.pat_user = User.objects.create(username="pat_priya", tenant=self.tenant, role="PATIENT", first_name="Priya", last_name="Sharma")
        self.patient = PatientProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.pat_user, mrn="MRN-TEST-100")

        self.today = date.today()
        self.appointment = Appointment.objects.create(
            tenant=self.tenant,
            branch=self.branch,
            appointment_number="APT-DOC-001",
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=self.today,
            start_time=time(14, 0),
            end_time=time(14, 30),
            appointment_type="TELEMEDICINE",
            status="CONFIRMED",
            reason_for_visit="Cardiac evaluation"
        )

        self.client = Client()

    def test_doctor_dashboard_returns_today_metrics(self):
        """Dashboard returns today's appointments and metrics for the doctor."""
        response = self.client.get('/api/v1/doctor-portal/dashboard/', HTTP_X_IMPERSONATE_USER='doc_chen')
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['doctor']['name'], 'Dr. Sophia Chen')
        self.assertEqual(data['today_metrics']['total_scheduled_today'], 1)

    def test_consultation_workspace_loads_and_updates_soap_notes(self):
        """Consultation workspace initializes draft and accepts updated clinical assessment."""
        # 1. Fetch workspace
        resp = self.client.get(
            f'/api/v1/doctor-portal/consultation/{self.appointment.id}/',
            HTTP_X_IMPERSONATE_USER='doc_chen'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['patient_summary']['mrn'], 'MRN-TEST-100')
        encounter_id = resp.data['encounter']['id']

        # 2. Update SOAP notes & vitals
        update_payload = {
            "chief_complaint": "Controlled hypertension follow-up",
            "subjective_notes": "Patient exercises 4 days a week with zero chest pain.",
            "assessment": "Stage 1 essential hypertension, well managed.",
            "clinical_plan": "Continue current regimen. Recheck in 6 months.",
            "vitals": {"bp_systolic": 120, "bp_diastolic": 78, "heart_rate": 70, "spo2": 99}
        }
        resp2 = self.client.post(
            f'/api/v1/doctor-portal/consultation/{self.appointment.id}/',
            data=update_payload,
            content_type='application/json',
            HTTP_X_IMPERSONATE_USER='doc_chen'
        )
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.data['encounter']['status'], 'DRAFT')

        # 3. Sign encounter
        sign_resp = self.client.post(
            f'/api/v1/clinical/encounters/{encounter_id}/sign/',
            HTTP_X_IMPERSONATE_USER='doc_chen'
        )
        self.assertEqual(sign_resp.status_code, 200)
        self.assertEqual(sign_resp.data['encounter']['status'], 'SIGNED')

        # 4. Attempting to edit a signed encounter is rejected!
        fail_edit = self.client.post(
            f'/api/v1/doctor-portal/consultation/{self.appointment.id}/',
            data={"subjective_notes": "Attempted tamper"},
            content_type='application/json',
            HTTP_X_IMPERSONATE_USER='doc_chen'
        )
        self.assertEqual(fail_edit.status_code, 400)
        self.assertIn('already signed and locked', fail_edit.data['error'])
