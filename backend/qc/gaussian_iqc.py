"""
Gaussian Normal Distribution and Analytical Z-Score Engine for Quality Control.
"""
import math

class GaussianIQCStatistics:
    @staticmethod
    def calculate_cv(mean: float, sd: float) -> float:
        if mean == 0:
            return 0.0
        return round((sd / mean) * 100.0, 2)
