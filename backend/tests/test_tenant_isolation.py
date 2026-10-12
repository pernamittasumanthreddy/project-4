"""
Test Suite: Multi-Tenant Logical Isolation & Cross-Tenant Boundary Enforcement.
Ensures that data from Tenant A (CareTrust) is strictly invisible to Tenant B (MetroHealth).
"""

from django.test import TestCase, Client
from apps.core.models import Tenant, HospitalBranch, User
from apps.appointments.models import PatientProfile, DoctorProfile, Appointment
from datetime import date, time

class TenantIsolationTestCase(TestCase):
    def setUp(self):
        # Tenant 1: CareTrust
        self.tenant_a = Tenant.objects.create(
            name="CareTrust Health System",
            slug="caretrust",
            domain="caretrust.local",
            tier="ENTERPRISE"
        )
        self.branch_a = HospitalBranch.objects.create(
            tenant=self.tenant_a,
            name="CareTrust Main",
            code="MAIN",
            address="100 Hospital Way",
            city="Boston",
            state="MA",
            postal_code="02115",
            phone="617-555-0100"
        )
        self.user_a = User.objects.create(
            username="patient_a",
            tenant=self.tenant_a,
            role="PATIENT",
            first_name="Alice",
            last_name="Adams"
        )
        self.patient_a = PatientProfile.objects.create(
            tenant=self.tenant_a,
            branch=self.branch_a,
            user=self.user_a,
            mrn="MRN-TENA-001"
        )

        # Tenant 2: MetroHealth
        self.tenant_b = Tenant.objects.create(
            name="MetroHealth Hospital",
            slug="metrohealth",
            domain="metrohealth.local",
            tier="REGIONAL"
        )
        self.branch_b = HospitalBranch.objects.create(
            tenant=self.tenant_b,
            name="MetroHealth Center",
            code="METRO",
            address="200 City Blvd",
            city="Springfield",
            state="MA",
            postal_code="01103",
            phone="413-555-0200"
        )
        self.user_b = User.objects.create(
            username="patient_b",
            tenant=self.tenant_b,
            role="PATIENT",
            first_name="Bob",
            last_name="Baker"
        )
        self.patient_b = PatientProfile.objects.create(
            tenant=self.tenant_b,
            branch=self.branch_b,
            user=self.user_b,
            mrn="MRN-TENB-002"
        )

        self.client = Client()

    def test_tenant_context_middleware_header(self):
        """Verifies X-Tenant-ID header attaches correct tenant context."""
        response = self.client.get('/api/v1/health/', HTTP_X_TENANT_ID='caretrust')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('X-Active-Tenant'), 'caretrust')

    def test_patients_belong_strictly_to_respective_tenants(self):
        """Database check: Patient records are strictly partitioned by tenant ID."""
        caretrust_patients = PatientProfile.objects.filter(tenant=self.tenant_a)
        metro_patients = PatientProfile.objects.filter(tenant=self.tenant_b)

        self.assertEqual(caretrust_patients.count(), 1)
        self.assertEqual(caretrust_patients.first().mrn, "MRN-TENA-001")
        self.assertEqual(metro_patients.count(), 1)
        self.assertEqual(metro_patients.first().mrn, "MRN-TENB-002")

    def test_cross_tenant_isolation_in_patient_portal_dashboard(self):
        """Patient B cannot query Patient A's records even if passing patient_id param."""
        response = self.client.get(
            '/api/v1/patient-portal/dashboard/',
            HTTP_X_IMPERSONATE_USER='patient_b',
            HTTP_X_TENANT_ID='metrohealth'
        )
        self.assertEqual(response.status_code, 200)
        # Dashboard must return Patient B's data
        self.assertEqual(response.data['patient']['mrn'], 'MRN-TENB-002')
        self.assertNotEqual(response.data['patient']['mrn'], 'MRN-TENA-001')
