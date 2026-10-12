import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from admissions.models import Ward, Room, Bed, Admission
from admissions.handover_service import NursingHandoverService

@pytest.mark.django_db
def test_handover():
    t = Tenant.objects.create(name="Handover Hosp", slug="hand-hosp")
    b = HospitalBranch.objects.create(tenant=t, name="B", code="B")
    d = Department.objects.create(tenant=t, branch=b, name="D", code="D")
    p = Patient.objects.create(tenant=t, mrn="MRN-H-1", first_name="A", last_name="B", phone="+1009")
    w = Ward.objects.create(tenant=t, branch=b, name="W")
    r = Room.objects.create(tenant=t, ward=w, room_number="R")
    bd = Bed.objects.create(tenant=t, room=r, bed_number="BD1")
    adm = Admission.objects.create(tenant=t, admission_number="IPD-H-1", patient=p, branch=b, department=d, admitting_doctor_id="doc", admitting_doctor_name="Doc", bed=bd)
    res = NursingHandoverService.create_handover_report(adm, "Nurse 1", "Nurse 2", ["Check BP at 2 PM"])
    assert res["status"] == "HANDED_OVER"
