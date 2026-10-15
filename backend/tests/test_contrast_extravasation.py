"""
Automated Unit Tests for RIS Contrast Extravasation Protocol.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from ris.contrast_extravasation import ContrastExtravasationManager

def test_mild_extravasation_assessment():
    res = ContrastExtravasationManager.assess_incident(estimated_volume_ml=12.0)
    assert res["grade"] == "MILD"
    assert res["requires_surgical_consult"] is False
    assert res["safety_incident_logged"] is True

def test_moderate_extravasation_assessment():
    res = ContrastExtravasationManager.assess_incident(estimated_volume_ml=45.0)
    assert res["grade"] == "MODERATE"
    assert res["requires_surgical_consult"] is False
    assert 6 in res["monitoring_intervals_hours"]

def test_severe_extravasation_by_large_volume():
    res = ContrastExtravasationManager.assess_incident(estimated_volume_ml=120.0)
    assert res["grade"] == "SEVERE"
    assert res["requires_surgical_consult"] is True
    assert any("Plastic / Vascular Surgery Consult" in action for action in res["immediate_interventions"])

def test_severe_extravasation_by_neurovascular_symptom():
    res = ContrastExtravasationManager.assess_incident(estimated_volume_ml=18.0, has_paresthesia=True)
    assert res["grade"] == "SEVERE"
    assert res["requires_surgical_consult"] is True

if __name__ == "__main__":
    test_mild_extravasation_assessment()
    test_moderate_extravasation_assessment()
    test_severe_extravasation_by_large_volume()
    test_severe_extravasation_by_neurovascular_symptom()
    print("All contrast extravasation protocol tests passed successfully!")
