from clinical.services.milestone_manifest import MILESTONE_METADATA

def test_milestone():
    assert MILESTONE_METADATA["total_prs"] == 100
    assert MILESTONE_METADATA["quality_gate"] == "PASSED"
