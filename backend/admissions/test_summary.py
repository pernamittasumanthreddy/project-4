import pytest
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from admissions.models import Ward, Room, Bed, Admission
from admissions.summary_service import DischargeSummaryService

@pytest.mark.django_db
def test_discharge_doc_generation():
    tenant = Tenant.objects.create(name="Summary Hosp", slug="summary-hosp")
    branch = HospitalBranch.objects.create(tenant=tenant, name="Main", code="M")
    dept = Department.objects.create(tenant=tenant, branch=branch, name="Surgery", code="SUR")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-S-1", first_name="Tony", last_name="Stark", phone="+1006")
    ward = Ward.objects.create(tenant=tenant, branch=branch, name="Post-Op")
    room = Room.objects.create(tenant=tenant, ward=ward, room_number="P1")
    bed = Bed.objects.create(tenant=tenant, room=room, bed_number="B1")
    adm = Admission.objects.create(
        tenant=tenant, admission_number="IPD-DOC-1", patient=patient, branch=branch, department=dept,
        admitting_doctor_id="doc_s", admitting_doctor_name="Dr. Cho", bed=bed, admission_diagnosis="Appendicitis", status="DISCHARGED", billing_cleared=True
    )
    doc = DischargeSummaryService.generate_discharge_document(adm)
    assert doc["patient_name"] == "Tony Stark"
    assert doc["billing_status"] == "CLEARED"
