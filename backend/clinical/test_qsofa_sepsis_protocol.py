import pytest
from clinical.services.qsofa_sepsis_protocol import QSOFASepsisProtocol

def test_qsofa_sepsis_protocol():
    res = QSOFASepsisProtocol.screen_qsofa("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
