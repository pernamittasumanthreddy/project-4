import pytest
from clinical.services.vital_outlier_detector import VitalSignsOutlierDetector

def test_vital_outlier_detector():
    res = VitalSignsOutlierDetector.detect_outliers("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
