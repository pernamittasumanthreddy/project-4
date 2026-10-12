import pytest
from clinical.services.stroke_fasttrack_checklist import StrokeFastTrackChecklist

def test_stroke_fasttrack_checklist():
    res = StrokeFastTrackChecklist.evaluate_thrombolysis_eligibility("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
