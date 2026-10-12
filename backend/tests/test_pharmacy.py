"""
Test Suite: Member 5 — Pharmacy & Inventory Module Integration.
Verifies medication formulary, stock search, dispensing orders, and multi-tenant isolation.
"""

from django.test import TestCase, Client
from datetime import date, timedelta
from decimal import Decimal
from apps.core.models import Tenant, HospitalBranch, User
from apps.appointments.models import Department, DoctorProfile, PatientProfile
from apps.clinical.models import Prescription
from apps.pharmacy.models import Medication, DispensingOrder


class PharmacyModuleIntegrationTestCase(TestCase):
    def setUp(self):
        # Tenant 1: Apex Health
        self.tenant1 = Tenant.objects.create(
            name="Apex Health Systems",
            slug="apex-health",
            domain="apex.health"
        )
        self.branch1 = HospitalBranch.objects.create(
            tenant=self.tenant1,
            name="Apex Main Hospital",
            code="APEX-MAIN"
        )
        self.user1 = User.objects.create(
            username="apex_pharmacist",
            tenant=self.tenant1,
            role="PHARMACIST"
        )
        self.doc_user = User.objects.create(
            username="apex_doctor",
            tenant=self.tenant1,
            role="DOCTOR"
        )
        self.dept = Department.objects.create(
            tenant=self.tenant1,
            name="General Medicine",
            code="GENMED"
        )
        self.doctor = DoctorProfile.objects.create(
            tenant=self.tenant1,
            branch=self.branch1,
            user=self.doc_user,
            department=self.dept,
            license_number="LIC-MD-501",
            specialization="Internal Medicine"
        )
        self.patient1 = PatientProfile.objects.create(
            tenant=self.tenant1,
            branch=self.branch1,
            user=self.user1,
            mrn="MRN-APEX-001"
        )

        # Medications for Tenant 1
        self.med1 = Medication.objects.create(
            tenant=self.tenant1,
            generic_name="Amoxicillin",
            brand_name="Amoxil",
            dosage_form="Capsule",
            strength="500 mg",
            unit_price=Decimal("12.50"),
            stock_quantity=200,
            reorder_level=30
        )
        self.med2 = Medication.objects.create(
            tenant=self.tenant1,
            generic_name="Metformin",
            brand_name="Glucophage",
            dosage_form="Tablet",
            strength="500 mg",
            unit_price=Decimal("8.00"),
            stock_quantity=20,
            reorder_level=50
        )

        # Tenant 2: Metro Health (For tenant isolation checks)
        self.tenant2 = Tenant.objects.create(
            name="Metro Health Network",
            slug="metro-health",
            domain="metro.health"
        )
        self.med_t2 = Medication.objects.create(
            tenant=self.tenant2,
            generic_name="Atorvastatin",
            brand_name="Lipitor",
            dosage_form="Tablet",
            strength="20 mg",
            unit_price=Decimal("22.00"),
            stock_quantity=100
        )

        self.client = Client()

    def test_medication_creation_and_attributes(self):
        """Verifies medication formulary model attributes and formatting."""
        self.assertEqual(str(self.med1), "Amoxicillin (Amoxil) 500 mg")
        self.assertEqual(self.med1.stock_quantity, 200)
        self.assertEqual(self.med1.unit_price, Decimal("12.50"))

    def test_medication_search_and_listing_api(self):
        """Tests medication API search by generic name and brand name."""
        resp = self.client.get('/api/v1/pharmacy/medications/?search=Amox')
        self.assertEqual(resp.status_code, 200)
        results = resp.data.get('results', resp.data)
        generic_names = [m['generic_name'] for m in results]
        self.assertIn("Amoxicillin", generic_names)

    def test_medication_tenant_isolation(self):
        """Ensures medications from different tenants are isolated."""
        resp = self.client.get('/api/v1/pharmacy/medications/', HTTP_X_TENANT_ID=str(self.tenant1.id))
        self.assertEqual(resp.status_code, 200)
        results = resp.data.get('results', resp.data)
        for m in results:
            self.assertNotEqual(m['generic_name'], "Atorvastatin")

    def test_dispensing_order_flow(self):
        """Tests medication dispensing transaction linked to prescription."""
        today = date.today()
        rx = Prescription.objects.create(
            tenant=self.tenant1,
            prescription_number="RX-APEX-001",
            patient=self.patient1,
            doctor=self.doctor,
            status="ACTIVE",
            issued_date=today,
            valid_until=today + timedelta(days=30),
            special_instructions="Take with food"
        )
        order = DispensingOrder.objects.create(
            tenant=self.tenant1,
            dispense_number="DSP-2026-001",
            prescription=rx,
            patient=self.patient1,
            pharmacist_name="David Ross, PharmD",
            status="DISPENSED",
            total_amount=Decimal("25.00")
        )
        self.assertEqual(order.status, "DISPENSED")
        self.assertIn("DSP-2026-001", str(order))

        # Retrieve via API
        resp = self.client.get(f'/api/v1/pharmacy/dispensing-orders/?patient_id={self.patient1.id}')
        self.assertEqual(resp.status_code, 200)
        results = resp.data.get('results', resp.data)
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]['dispense_number'], "DSP-2026-001")
