import pytest
from clinical.services.cds_alert_engine import CDSAlertPriorityEngine

def test_cds_alert_engine():
    res = CDSAlertPriorityEngine.evaluate_alert_priority("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
