import pytest
from core.models import Tenant
from patients.models import Patient
from patients.barcode_service import PatientBarcodeService

@pytest.mark.django_db
def test_barcode_payload():
    t = Tenant.objects.create(name="Bar Hosp", slug="bar-hosp")
    p = Patient.objects.create(tenant=t, mrn="MRN-BAR-1", first_name="Jack", last_name="Ryan", phone="+1008")
    d = PatientBarcodeService.generate_wristband_payload(p)
    assert d["barcode_value"] == "*MRN-BAR-1*"
