import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from admissions.models import Ward, Room, Bed
from admissions.emergency_service import EmergencyAdmissionService

@pytest.mark.django_db
def test_emergency_intake():
    tenant = Tenant.objects.create(name="ER Clinic", slug="er-clinic")
    branch = HospitalBranch.objects.create(tenant=tenant, name="ER", code="ER")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="Trauma", code="TRM")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-E-1", first_name="Bruce", last_name="Wayne", phone="+1004")
    ward = Ward.objects.create(tenant=tenant, branch=branch, name="Trauma Bay")
    room = Room.objects.create(tenant=tenant, ward=ward, room_number="T1")
    bed = Bed.objects.create(tenant=tenant, room=room, bed_number="TB-1", status="AVAILABLE")
    adm = EmergencyAdmissionService.admit_emergency(tenant, patient, branch, dept, "doc_er", "Dr. Alfred", bed, "Blunt force trauma")
    assert adm.status == "ADMITTED"
    assert "URGENT-ER" in adm.admission_diagnosis
