import pytest
from clinical.services.emr_timeline_feed import EMRTimelineFeedStreamer

def test_emr_timeline_feed():
    res = EMRTimelineFeedStreamer.stream_timeline("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
