import pytest
import datetime
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from appointments.leave_service import DoctorLeaveService

@pytest.mark.django_db
def test_doctor_leave_impact():
    tenant = Tenant.objects.create(name="Leave Hosp", slug="leave-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="ENT", code="ENT")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-L-1", first_name="Paul", last_name="Walker", phone="+1002")
    apt = Appointment.objects.create(
        tenant=tenant, appointment_number="APT-LV-1", patient=patient,
        doctor_id="doc_leave", doctor_name="Dr. Watson", branch=branch, department=dept,
        appointment_date=datetime.date(2026, 11, 1), start_time=datetime.time(10,0), end_time=datetime.time(10,15)
    )
    res = DoctorLeaveService.apply_doctor_leave(tenant, "doc_leave", "Dr. Watson", datetime.date(2026, 10, 30), datetime.date(2026, 11, 2), "Medical conference")
    assert res["impacted_appointments"] == 1
    apt.refresh_from_db()
    assert apt.status == "RESCHEDULED"
