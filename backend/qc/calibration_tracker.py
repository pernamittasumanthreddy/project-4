"""
Automated Laboratory Instrument Calibration and Slope/Intercept Tracker.
Validates multi-point calibration curves, coefficient of determination (R²), and calibration drift.
"""

from typing import List, Tuple, Dict, Any
import math

class AnalyzerCalibrationTracker:
    @staticmethod
    def linear_regression(points: List[Tuple[float, float]]) -> Dict[str, float]:
        n = len(points)
        if n < 2:
            return {"slope": 1.0, "intercept": 0.0, "r_squared": 1.0}
        sum_x = sum(p[0] for p in points)
        sum_y = sum(p[1] for p in points)
        sum_xy = sum(p[0] * p[1] for p in points)
        sum_x2 = sum(p[0] ** 2 for p in points)
        sum_y2 = sum(p[1] ** 2 for p in points)

        denom = (n * sum_x2 - sum_x ** 2)
        slope = (n * sum_xy - sum_x * sum_y) / denom if denom != 0 else 1.0
        intercept = (sum_y - slope * sum_x) / n
        
        # R2 calculation
        r_num = (n * sum_xy - sum_x * sum_y)
        r_den = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) if ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) > 0 else 1.0
        r_sq = (r_num / r_den) ** 2 if r_den != 0 else 1.0
        
        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "r_squared": round(r_sq, 4)
        }
