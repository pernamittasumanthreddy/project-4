import pytest
from clinical.services.sbar_handover_formatter import SBARHandoverFormatter

def test_sbar_handover_formatter():
    res = SBARHandoverFormatter.format_sbar("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
