import pytest
import datetime
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from patients.timeline_service import PatientTimelineService

@pytest.mark.django_db
def test_timeline():
    tenant = Tenant.objects.create(name="Timeline Hosp", slug="timeline-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="General", code="GEN")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-T-1", first_name="Tom", last_name="Cruise", phone="+1001")
    Appointment.objects.create(
        tenant=tenant, appointment_number="APT-TL-1", patient=patient,
        doctor_id="d1", doctor_name="Dr. McCoy", branch=branch, department=dept,
        appointment_date=datetime.date(2026, 10, 15), start_time=datetime.time(9,0), end_time=datetime.time(9,15)
    )
    events = PatientTimelineService.get_patient_timeline(tenant, str(patient.id))
    assert len(events) == 1
    assert events[0]["event_type"] == "APPOINTMENT"
