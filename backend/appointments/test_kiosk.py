import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.kiosk_service import WalkInKioskService


@pytest.mark.django_db
def test_walk_in_kiosk_service():
    tenant = Tenant.objects.create(name="Metro Central", slug="metro-central")
    branch = HospitalBranch.objects.create(tenant=tenant, name="ER Unit", code="ER")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="Emergency", code="EMRG")

    patient = Patient.objects.create(
        tenant=tenant,
        mrn="MRN-WALK-100",
        first_name="David",
        last_name="Miller",
        phone="+919700011122"
    )

    res = WalkInKioskService.generate_walk_in_token(
        tenant=tenant,
        patient_id=str(patient.id),
        doctor_id="doc_er_1",
        doctor_name="Gregory House",
        branch_id=str(branch.id),
        department_id=str(dept.id),
        chief_complaint="Severe migraine"
    )

    assert res["token_number"] == 1
    assert res["status"] == "WAITING"
    assert res["patient_mrn"] == "MRN-WALK-100"
    assert res["appointment_number"].startswith("WLK-")
