import pytest
from clinical.services.sliding_scale_insulin import GlycemicSlidingScaleMatrix

def test_sliding_scale_insulin():
    res = GlycemicSlidingScaleMatrix.titrate_insulin_units("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
