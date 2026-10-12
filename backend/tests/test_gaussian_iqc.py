"""Unit tests for Gaussian IQC."""
import pytest
from qc.gaussian_iqc import GaussianIQCStatistics

def test_gaussian_cv():
    cv = GaussianIQCStatistics.calculate_cv(mean=100.0, sd=5.0)
    assert cv == 5.0
