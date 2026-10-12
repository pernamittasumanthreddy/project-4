"""
Test Suite: End-to-End Cross-Module Integration Workflow (Members 1 - 7).
Simulates full patient & clinician lifecycle across the enterprise HMS SaaS platform.
"""

from django.test import TestCase, Client
from datetime import date, time, timedelta
from decimal import Decimal

from apps.core.models import Tenant, HospitalBranch, User
from apps.appointments.models import Department, DoctorProfile, PatientProfile, Appointment
from apps.clinical.models import Encounter, Diagnosis, Prescription, PrescriptionItem
from apps.diagnostics.models import LabReport
from apps.billing.models import Invoice, Payment
from apps.telemedicine.models import TelemedicineSession
from apps.notifications.models import Notification

class CrossModuleIntegrationE2ETestCase(TestCase):
    def setUp(self):
        # Member 1: Core Foundation & Tenant
        self.tenant = Tenant.objects.create(name="CareTrust Health System", slug="caretrust", domain="caretrust.health")
        self.branch = HospitalBranch.objects.create(tenant=self.tenant, name="Main Campus", code="MAIN", address="100 Hospital Way", city="Boston", state="MA", postal_code="02115", phone="617-555-0100")

        # Member 2: Doctor & Patient
        self.doc_user = User.objects.create(username="doctor_chen", tenant=self.tenant, role="DOCTOR", first_name="Sophia", last_name="Chen")
        self.dept = Department.objects.create(tenant=self.tenant, name="Cardiology", code="CARDIO")
        self.doctor = DoctorProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.doc_user, department=self.dept, license_number="MED-101", specialization="Cardiology", consultation_fee=Decimal("180.00"))

        self.pat_user = User.objects.create(username="patient_priya", tenant=self.tenant, role="PATIENT", first_name="Priya", last_name="Sharma")
        self.patient = PatientProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.pat_user, mrn="MRN-E2E-001")

        self.client = Client()

    def test_complete_patient_journey_e2e(self):
        """
        Full lifecycle test:
        1. Patient books appointment
        2. Doctor sees appointment and documents consultation
        3. Encounter signed and finalized
        4. Lab report approved
        5. Invoice generated & settled via sandbox
        6. Telemedicine call conducted
        7. Patient checks records and notifications
        """
        # Step 1: Patient books telemedicine appointment
        target_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        book_resp = self.client.post(
            '/api/v1/appointments/',
            data={
                "doctor_id": str(self.doctor.id),
                "appointment_date": target_date,
                "start_time": "14:00:00",
                "appointment_type": "TELEMEDICINE",
                "reason_for_visit": "Hypertension follow-up and chest tightness check"
            },
            content_type='application/json',
            HTTP_X_IMPERSONATE_USER='patient_priya'
        )
        self.assertEqual(book_resp.status_code, 201)
        appt_id = book_resp.data['id']
        appt_number = book_resp.data['appointment_number']

        # Step 2: Doctor views schedule and opens consultation workspace
        schedule_resp = self.client.get('/api/v1/doctor-portal/schedule/', HTTP_X_IMPERSONATE_USER='doctor_chen')
        self.assertEqual(schedule_resp.status_code, 200)

        ws_resp = self.client.get(f'/api/v1/doctor-portal/consultation/{appt_id}/', HTTP_X_IMPERSONATE_USER='doctor_chen')
        self.assertEqual(ws_resp.status_code, 200)
        encounter_id = ws_resp.data['encounter']['id']

        # Step 3: Doctor documents SOAP notes, vitals, diagnosis, and signs encounter
        doc_update = {
            "chief_complaint": "Hypertension check",
            "vitals": {"bp_systolic": 126, "bp_diastolic": 80, "heart_rate": 72, "spo2": 99},
            "assessment": "Stage 1 essential hypertension, stable.",
            "clinical_plan": "Continue Lisinopril 10mg daily.",
            "new_diagnosis": {
                "icd10_code": "I10",
                "description": "Essential (primary) hypertension",
                "severity": "MODERATE",
                "is_primary": True
            }
        }
        update_resp = self.client.post(
            f'/api/v1/doctor-portal/consultation/{appt_id}/',
            data=doc_update,
            content_type='application/json',
            HTTP_X_IMPERSONATE_USER='doctor_chen'
        )
        self.assertEqual(update_resp.status_code, 200)

        sign_resp = self.client.post(f'/api/v1/clinical/encounters/{encounter_id}/sign/', HTTP_X_IMPERSONATE_USER='doctor_chen')
        self.assertEqual(sign_resp.status_code, 200)
        self.assertEqual(sign_resp.data['encounter']['status'], 'SIGNED')

        # Step 4: Laboratory test ordered and approved
        lab_report = LabReport.objects.create(
            tenant=self.tenant,
            report_number="LAB-E2E-1",
            test_name="Lipid Profile",
            patient=self.patient,
            ordering_doctor=self.doctor,
            status="ORDERED",
            order_date=date.today(),
            results=[{"name": "Total Cholesterol", "value": "175", "unit": "mg/dL", "flag": "NORMAL"}]
        )
        approve_resp = self.client.post(f'/api/v1/diagnostics/lab-reports/{lab_report.id}/approve/')
        self.assertEqual(approve_resp.status_code, 200)
        self.assertEqual(approve_resp.data['report']['status'], 'APPROVED')

        # Step 5: Billing invoice generated and settled via sandbox
        invoice = Invoice.objects.create(
            tenant=self.tenant,
            invoice_number="INV-E2E-001",
            patient=self.patient,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            status="UNPAID",
            subtotal=Decimal("180.00"),
            total_amount=Decimal("180.00"),
            paid_amount=Decimal("0.00"),
            balance_due=Decimal("180.00"),
            line_items=[{"description": "Telemedicine Consultation", "quantity": 1, "unit_price": 180.00, "total": 180.00}]
        )
        pay_resp = self.client.post(
            f'/api/v1/billing/invoices/{invoice.id}/pay-sandbox/',
            data={"payment_method": "CREDIT_CARD"}
        )
        self.assertEqual(pay_resp.status_code, 200)
        self.assertEqual(pay_resp.data['invoice']['status'], 'PAID')
        self.assertEqual(Decimal(str(pay_resp.data['invoice']['balance_due'])), Decimal('0.00'))

        # Step 6: Virtual Telemedicine Session lifecycle
        tele_resp = self.client.get(f'/api/v1/telemedicine/appointment/{appt_id}/')
        self.assertEqual(tele_resp.status_code, 200)
        tele_id = tele_resp.data['id']

        # Patient joins
        self.client.post(f'/api/v1/telemedicine/sessions/{tele_id}/join/', data={'role': 'PATIENT'})
        # Doctor joins
        join_d = self.client.post(f'/api/v1/telemedicine/sessions/{tele_id}/join/', data={'role': 'DOCTOR'})
        self.assertEqual(join_d.data['room_state'], 'IN_PROGRESS')

        # Conclude call
        leave_resp = self.client.post(
            f'/api/v1/telemedicine/sessions/{tele_id}/leave/',
            data={'role': 'DOCTOR', 'clinical_quick_notes': 'Call concluded successfully.'}
        )
        self.assertEqual(leave_resp.data['session']['status'], 'ENDED')

        # Step 7: Patient reviews dashboard and records
        dash_resp = self.client.get('/api/v1/patient-portal/dashboard/', HTTP_X_IMPERSONATE_USER='patient_priya')
        self.assertEqual(dash_resp.status_code, 200)
        # Outstanding balance should now be zero (invoice was paid)
        self.assertEqual(dash_resp.data['summary_stats']['outstanding_balance_usd'], 0.0)
        self.assertTrue(dash_resp.data['summary_stats']['approved_lab_reports_count'] >= 1)

        # Check notifications were generated across events
        notifs_resp = self.client.get('/api/v1/notifications/', HTTP_X_IMPERSONATE_USER='patient_priya')
        self.assertEqual(notifs_resp.status_code, 200)
        self.assertTrue(notifs_resp.data['total_count'] >= 2)
