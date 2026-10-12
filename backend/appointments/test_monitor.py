import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment, OPDQueueToken
from appointments.monitor_service import QueueMonitorService

@pytest.mark.django_db
def test_queue_monitor():
    tenant = Tenant.objects.create(name="Queue Clinic", slug="queue-clinic")
    branch = HospitalBranch.objects.create(tenant=tenant, name="OPD Unit", code="OPD")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="Medicine", code="MED")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-M-1", first_name="Clark", last_name="Kent", phone="+1005")
    apt = Appointment.objects.create(
        tenant=tenant, appointment_number="APT-Q-1", patient=patient,
        doctor_id="doc_q", doctor_name="Dr. Strange", branch=branch, department=dept,
        appointment_date="2026-10-12", start_time="10:00", end_time="10:15"
    )
    OPDQueueToken.objects.create(tenant=tenant, appointment=apt, branch=branch, department=dept, doctor_id="doc_q", token_number=7, status="CALLED", room_number="Cabin 4")
    board = QueueMonitorService.get_active_display_board(tenant, branch.id)
    assert len(board) == 1
    assert board[0]["token_number"] == 7
    assert board[0]["status"] == "CALLED"
