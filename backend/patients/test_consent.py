import pytest
from core.models import Tenant
from patients.models import Patient
from patients.consent_service import ConsentService

@pytest.mark.django_db
def test_consent_record():
    tenant = Tenant.objects.create(name="Consent Care", slug="consent-care")
    patient = Patient.objects.create(tenant=tenant, mrn="MRN-C-1", first_name="Sam", last_name="Altman", phone="+1000")
    consent = ConsentService.record_consent(tenant, patient, "GENERAL_TREATMENT", "OPD Terms", "Terms acknowledged", "Sam Altman")
    assert consent.is_granted is True
    assert consent.signer_name == "Sam Altman"
