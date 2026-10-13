"""
Automated Unit Tests for QC, Levey-Jennings, Delta Checks, and Critical Escalation.
"""
import pytest
from lis.delta_check import DeltaCheckEngine
from lis.critical_escalation import CriticalAlertEscalationEngine, CriticalAlertNotification
from datetime import datetime, timezone, timedelta
from qc.levey_jennings_renderer import LeveyJenningsSVGRenderer
from qc.calibration_tracker import AnalyzerCalibrationTracker
from qc.proficiency_testing import ProficiencyTestingTracker

def test_delta_check_detection():
    engine = DeltaCheckEngine()
    # Potassium jump from 4.0 to 6.0 in 2 hours -> absolute change 2.0 exceeds 1.5, percent change 50% > 30%
    res = engine.evaluate("POTASSIUM", current_value=6.0, previous_value=4.0, hours_elapsed=2.0)
    assert res.is_violation is True
    assert res.severity == "CRITICAL"

def test_delta_check_normal():
    engine = DeltaCheckEngine()
    res = engine.evaluate("POTASSIUM", current_value=4.2, previous_value=4.1, hours_elapsed=12.0)
    assert res.is_violation is False

def test_critical_alert_escalation_lifecycle():
    engine = CriticalAlertEscalationEngine()
    alert = CriticalAlertNotification(
        alert_id="ALT-1", tenant_id="T1", patient_id="PT-1", patient_name="John Doe",
        test_name="Potassium", critical_value="6.8", reference_range="3.5 - 5.1",
        detected_at=datetime.now(timezone.utc) - timedelta(minutes=25),
        ordering_physician_id="DOC-1"
    )
    # 25 mins elapsed > 15 mins for Level 1 -> should escalate to level 2
    escalated = engine.check_escalation_status(alert)
    assert escalated is True
    assert alert.escalation_level == 2

    # Technologist records call log with read-back confirmed -> marked acknowledged
    engine.record_call_log(
        alert, caller_id="TECH-1", recipient_name="Dr. Smith",
        recipient_role="Attending", contact_number="555-0199",
        read_back_confirmed=True, notes="Verified critical potassium."
    )
    assert alert.status == "ACKNOWLEDGED"

def test_levey_jennings_svg_generation():
    svg = LeveyJenningsSVGRenderer.render_svg(mean=100.0, sd=5.0, values=[98.0, 101.0, 104.0, 99.0])
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "stroke="#10b981"" in svg

def test_analyzer_calibration_tracker():
    res = AnalyzerCalibrationTracker.linear_regression([(1, 2), (2, 4), (3, 6), (4, 8)])
    assert res["slope"] == 2.0
    assert res["r_squared"] == 1.0

def test_proficiency_testing_sdi():
    eval_res = ProficiencyTestingTracker.calculate_sdi(lab_result=105.0, peer_group_mean=100.0, peer_group_sd=2.5)
    assert eval_res["sdi"] == 2.0
    assert eval_res["performance"] in ["ACCEPTABLE", "QUESTIONABLE"]
