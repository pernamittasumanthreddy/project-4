import pytest
from clinical.services.anticoagulation_monitor import AnticoagulationMonitor

def test_anticoagulation_monitor():
    res = AnticoagulationMonitor.evaluate_inr_target("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
