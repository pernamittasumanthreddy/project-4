import pytest
from clinical.services.sequencer_service import ClinicalSequencerService

def test_sequencer_service():
    res = ClinicalSequencerService.generate_sequence("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
