"""
Automated Unit Tests for Radiation Dose and Contrast Safety Monitoring.
"""
import pytest
from ris.radiation_dose import RadiationDoseMonitor
from ris.contrast_safety import ContrastMediaSafetyEngine
from ris.urgency_triage import RadiologyUrgencyTriager
from ris.birads_audit import BIRADSAuditEngine

def test_radiation_dose_drl_exceedance():
    # Head CT with CTDI 85.0 mGy > DRL of 75.0 mGy
    res = RadiationDoseMonitor.check_dose_exceedance("HEAD", ctdi=85.0, dlp=900.0)
    assert res["exceeds_drl"] is True
    assert res["ctdi_ratio"] > 1.0

def test_contrast_safety_egfr_screening():
    res_high = ContrastMediaSafetyEngine.evaluate_contrast_risk(egfr_ml_min=24.0, contrast_agent_type="Omnipaque")
    assert res_high["risk_tier"] == "HIGH"
    assert res_high["safe_to_administer"] is False

    res_safe = ContrastMediaSafetyEngine.evaluate_contrast_risk(egfr_ml_min=65.0, contrast_agent_type="Omnipaque")
    assert res_safe["risk_tier"] == "LOW"
    assert res_safe["safe_to_administer"] is True

def test_radiology_urgency_triage():
    prio_stroke = RadiologyUrgencyTriager.get_priority("STROKE")
    assert prio_stroke.target_turnaround_minutes == 15

    prio_routine = RadiologyUrgencyTriager.get_priority("ROUTINE")
    assert prio_routine.target_turnaround_minutes == 1440

def test_birads_audit_classification():
    cat4 = BIRADSAuditEngine.get_assessment(4)
    assert cat4.assessment == "Suspicious"
    assert "biopsy" in cat4.recommendation.lower()
