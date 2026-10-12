"""
Test Suite: Patient Portal APIs & Workspaces (Member 7).
Covers dashboard statistics, profile editing constraints, report access, and appointment booking.
"""

from django.test import TestCase, Client
from datetime import date, time, timedelta
from decimal import Decimal

from apps.core.models import Tenant, HospitalBranch, User
from apps.appointments.models import Department, DoctorProfile, PatientProfile, Appointment
from apps.diagnostics.models import LabReport, RadiologyReport
from apps.clinical.models import Encounter, Prescription, PrescriptionItem, Allergy
from apps.billing.models import Invoice

class PatientPortalTestCase(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="CareTrust", slug="caretrust", domain="caretrust.local")
        self.branch = HospitalBranch.objects.create(tenant=self.tenant, name="Main Campus", code="MAIN", address="100 Ave", city="Boston", state="MA", postal_code="02115", phone="617-555-0100")
        
        # Doctor
        self.doc_user = User.objects.create(username="doc_chen", tenant=self.tenant, role="DOCTOR", first_name="Sophia", last_name="Chen")
        self.dept = Department.objects.create(tenant=self.tenant, name="Cardiology", code="CARDIO")
        self.doctor = DoctorProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.doc_user, department=self.dept, license_number="LIC-1234", specialization="Cardiology", consultation_fee=Decimal("150.00"))

        # Patient
        self.pat_user = User.objects.create(username="pat_priya", tenant=self.tenant, role="PATIENT", first_name="Priya", last_name="Sharma", email="priya@test.local")
        self.patient = PatientProfile.objects.create(tenant=self.tenant, branch=self.branch, user=self.pat_user, mrn="MRN-TEST-100", date_of_birth=date(1990, 1, 1), gender="FEMALE", blood_group="O+")

        # Approved Lab Report
        self.lab_approved = LabReport.objects.create(
            tenant=self.tenant,
            report_number="LAB-APP-1",
            test_name="Lipid Panel",
            patient=self.patient,
            status="APPROVED",
            order_date=date.today(),
            results=[{"name": "Cholesterol", "value": "180", "unit": "mg/dL", "flag": "NORMAL"}]
        )

        # Unapproved Draft Lab Report
        self.lab_draft = LabReport.objects.create(
            tenant=self.tenant,
            report_number="LAB-DRAFT-2",
            test_name="Sensitive Biomarker",
            patient=self.patient,
            status="ANALYZED", # Unapproved!
            order_date=date.today(),
            results=[{"name": "Marker X", "value": "Elevated", "flag": "HIGH"}]
        )

        # Invoices
        self.invoice = Invoice.objects.create(
            tenant=self.tenant,
            invoice_number="INV-TEST-001",
            patient=self.patient,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            status="UNPAID",
            subtotal=Decimal("150.00"),
            total_amount=Decimal("150.00"),
            paid_amount=Decimal("0.00"),
            balance_due=Decimal("150.00"),
            line_items=[{"description": "Cardiology Visit", "quantity": 1, "unit_price": 150.00, "total": 150.00}]
        )

        self.client = Client()

    def test_patient_dashboard_returns_real_data(self):
        """Dashboard returns verified patient info, metrics, and approved reports."""
        response = self.client.get('/api/v1/patient-portal/dashboard/', HTTP_X_IMPERSONATE_USER='pat_priya')
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['patient']['mrn'], 'MRN-TEST-100')
        self.assertEqual(data['patient']['full_name'], 'Priya Sharma')
        self.assertEqual(data['summary_stats']['approved_lab_reports_count'], 1)
        self.assertEqual(data['summary_stats']['outstanding_balance_usd'], 150.0)

    def test_patient_medical_records_strictly_suppresses_unapproved_reports(self):
        """
        Security requirement: Patient portal MUST ONLY show approved reports.
        Draft or unapproved reports must never be leaked to the patient.
        """
        response = self.client.get('/api/v1/patient-portal/medical-records/', HTTP_X_IMPERSONATE_USER='pat_priya')
        self.assertEqual(response.status_code, 200)
        labs = response.data['lab_reports']
        report_numbers = [r['report_number'] for r in labs]
        
        self.assertIn('LAB-APP-1', report_numbers)
        self.assertNotIn('LAB-DRAFT-2', report_numbers)

    def test_patient_profile_updates_contact_info_safely(self):
        """Patient can update contact/address, but cannot alter MRN or clinician diagnoses."""
        update_payload = {
            "emergency_contact_name": "Updated Contact",
            "emergency_contact_phone": "+1-555-999-0000",
            "address_line": "77 Beacon St",
            "city": "Boston",
            "mrn": "FORGED-MRN-999" # Should be ignored!
        }
        response = self.client.put(
            '/api/v1/patient-portal/profile/',
            data=update_payload,
            content_type='application/json',
            HTTP_X_IMPERSONATE_USER='pat_priya'
        )
        self.assertEqual(response.status_code, 200)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.emergency_contact_name, "Updated Contact")
        self.assertEqual(self.patient.mrn, "MRN-TEST-100") # Unchanged!

    def test_patient_appointment_booking_and_conflict_handling(self):
        """Patient books appointment with doctor and verifies duplicate slot prevention."""
        target_date = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        booking_payload = {
            "doctor_id": str(self.doctor.id),
            "appointment_date": target_date,
            "start_time": "10:00:00",
            "appointment_type": "TELEMEDICINE",
            "reason_for_visit": "Hypertension routine follow-up"
        }

        # 1. First booking succeeds
        resp1 = self.client.post(
            '/api/v1/appointments/',
            data=booking_payload,
            content_type='application/json',
            HTTP_X_IMPERSONATE_USER='pat_priya'
        )
        self.assertEqual(resp1.status_code, 201)
        self.assertEqual(resp1.data['doctor_name'], 'Dr. Sophia Chen')

        # 2. Duplicate booking for the same slot is rejected with validation error
        resp2 = self.client.post(
            '/api/v1/appointments/',
            data=booking_payload,
            content_type='application/json',
            HTTP_X_IMPERSONATE_USER='pat_priya'
        )
        self.assertEqual(resp2.status_code, 400)
        self.assertIn('start_time', resp2.data)
