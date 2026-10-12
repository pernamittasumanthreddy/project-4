import pytest
from clinical.services.allergy_classifier import AllergySeverityClassifier

def test_allergy_classifier():
    res = AllergySeverityClassifier.classify_severity("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
