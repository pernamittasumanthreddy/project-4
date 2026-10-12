import pytest
import datetime
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from appointments.notifications import AppointmentNotificationService


@pytest.mark.django_db
def test_dispatch_booking_confirmation():
    tenant = Tenant.objects.create(name="City Hospital", slug="city-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main Clinic", code="MAIN")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="OPD", code="OPD")
    patient = Patient.objects.create(
        tenant=tenant,
        mrn="MRN-TEST-001",
        first_name="Alice",
        last_name="Smith",
        phone="+919876543210",
        email="alice@example.com"
    )

    apt = Appointment.objects.create(
        tenant=tenant,
        appointment_number="APT-2026-9999",
        patient=patient,
        doctor_id="doc_1",
        doctor_name="Gregory House",
        branch=branch,
        department=dept,
        appointment_date=datetime.date(2026, 10, 20),
        start_time=datetime.time(10, 30),
        end_time=datetime.time(10, 45),
        status="CONFIRMED"
    )

    payload = AppointmentNotificationService.dispatch_booking_confirmation(apt)

    assert payload["status"] == "DELIVERED"
    assert payload["recipient_phone"] == "+919876543210"
    assert "APT-2026-9999" in payload["message"]