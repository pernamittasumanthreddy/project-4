import pytest
from clinical.services.news2_escalation_protocol import NEWS2EscalationProtocol

def test_news2_escalation_protocol():
    res = NEWS2EscalationProtocol.evaluate_news2("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
