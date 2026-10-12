import pytest
from clinical.services.stemi_door_to_balloon_tracker import STEMIDoorToBalloonTracker

def test_stemi_door_to_balloon_tracker():
    res = STEMIDoorToBalloonTracker.track_door_to_balloon("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
