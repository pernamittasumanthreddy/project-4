import pytest
from clinical.services.clinical_quality_metrics import ClinicalQualityMetrics

def test_clinical_quality_metrics():
    res = ClinicalQualityMetrics.calculate_indicators("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
