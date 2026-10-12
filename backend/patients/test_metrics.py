import pytest
from core.models import Tenant
from patients.models import Patient
from patients.metrics_service import PatientMetricsService

@pytest.mark.django_db
def test_metrics():
    t = Tenant.objects.create(name="Met Hosp", slug="met-hosp")
    Patient.objects.create(tenant=t, mrn="MRN-M-1", first_name="A", last_name="B", phone="+1011")
    stats = PatientMetricsService.get_registration_stats(t)
    assert stats["total_patients"] == 1
    assert stats["active_patients"] == 1
