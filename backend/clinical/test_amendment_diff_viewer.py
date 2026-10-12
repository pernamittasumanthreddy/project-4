import pytest
from clinical.services.amendment_diff_viewer import AmendmentDiffViewer

def test_amendment_diff_viewer():
    res = AmendmentDiffViewer.compute_visual_diff("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
