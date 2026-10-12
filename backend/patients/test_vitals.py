import pytest
from core.models import Tenant
from patients.models import Patient
from patients.vitals_model import PatientVitals

@pytest.mark.django_db
def test_vitals_recording():
    tenant = Tenant.objects.create(name="Triage Hosp", slug="triage-hosp")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-V-1", first_name="Neo", last_name="Anderson", phone="+1003")
    v = PatientVitals.objects.create(tenant=tenant, patient=patient, systolic_bp=120, diastolic_bp=80, heart_rate=72)
    assert v.systolic_bp == 120
    assert v.diastolic_bp == 80
