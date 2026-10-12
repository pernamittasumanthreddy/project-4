import pytest
import datetime
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from patients.portal_service import PatientPortalService

@pytest.mark.django_db
def test_portal_appointments():
    tenant = Tenant.objects.create(name="Portal Hosp", slug="portal-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="General", code="GEN")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-P-1", first_name="Peter", last_name="Parker", phone="+1007")
    Appointment.objects.create(
        tenant=tenant, appointment_number="APT-PORT-1", patient=patient,
        doctor_id="doc_p", doctor_name="Dr. Connors", branch=branch, department=dept,
        appointment_date=datetime.date(2026, 12, 1), start_time=datetime.time(11,0), end_time=datetime.time(11,15),
        status="CONFIRMED"
    )
    res = PatientPortalService.get_upcoming_and_past_appointments(tenant, str(patient.id))
    assert len(res["upcoming"]) == 1
    assert len(res["past"]) == 0
