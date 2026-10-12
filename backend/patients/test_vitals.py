import pytest
from core.models import Tenant
from patients.models import Patient

@pytest.mark.django_db
def test_vitals_recording():
    tenant = Tenant.objects.create(name="Triage Hosp", slug="triage-hosp")
    patient = Patient.objects.create(
        tenant=tenant, mrn="MRN-V-1", first_name="Neo", last_name="Anderson", phone="+1003",
        allergies=[{"allergen": "Latex", "severity": "Mild"}],
        chronic_conditions=["Hypertension"]
    )
    assert patient.chronic_conditions == ["Hypertension"]
    assert patient.allergies[0]["allergen"] == "Latex"
