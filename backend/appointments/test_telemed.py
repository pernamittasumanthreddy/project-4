import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from appointments.telemed_service import TelemedicineSlotAllocator

@pytest.mark.django_db
def test_telemed_allocation():
    t = Tenant.objects.create(name="Tele Hosp", slug="tele-hosp")
    b = HospitalBranch.objects.create(tenant=t, name="B", code="B")
    d = Department.objects.create(tenant=t, branch=b, name="D", code="D")
    p = Patient.objects.create(tenant=t, mrn="MRN-TEL-1", first_name="A", last_name="B", phone="+1010")
    apt = Appointment.objects.create(tenant=t, appointment_number="APT-TEL-1", patient=p, doctor_id="d", doctor_name="Doc", branch=b, department=d, appointment_date="2026-10-12", start_time="12:00", end_time="12:15")
    res = TelemedicineSlotAllocator.allocate_secure_room(apt)
    assert len(res["room_token"]) > 10
