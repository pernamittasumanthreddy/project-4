import pytest
from clinical.services.cross_allergy_matrix import CrossAllergyMatrix

def test_cross_allergy_matrix():
    res = CrossAllergyMatrix.check_cross_reactivity("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
