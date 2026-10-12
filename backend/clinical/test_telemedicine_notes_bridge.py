import pytest
from clinical.services.telemedicine_notes_bridge import TelemedicineNotesBridge

def test_telemedicine_notes_bridge():
    res = TelemedicineNotesBridge.bridge_telemed_session("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
