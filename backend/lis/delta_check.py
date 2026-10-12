"""
Delta Check Engine for Member 4 Laboratory Management.
Calculates percentage change, rate of change, and absolute delta between consecutive patient results.
Flags acute clinical deterioration or potential specimen misidentification / mix-ups.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

@dataclass
class DeltaCheckRule:
    test_code: str
    test_name: str
    max_percent_change: float
    max_absolute_delta: float
    max_delta_hours: float
    alert_severity: str  # WARNING, CRITICAL

@dataclass
class DeltaCheckResult:
    test_code: str
    current_value: float
    previous_value: float
    percent_change: float
    absolute_delta: float
    hours_elapsed: float
    is_violation: bool
    severity: Optional[str] = None
    message: Optional[str] = None

class DeltaCheckEngine:
    DEFAULT_RULES: Dict[str, DeltaCheckRule] = {
        "POTASSIUM": DeltaCheckRule("POTASSIUM", "Serum Potassium", 30.0, 1.5, 48.0, "CRITICAL"),
        "CREATININE": DeltaCheckRule("CREATININE", "Serum Creatinine", 50.0, 0.8, 72.0, "WARNING"),
        "HEMOGLOBIN": DeltaCheckRule("HEMOGLOBIN", "Blood Hemoglobin", 25.0, 2.5, 48.0, "CRITICAL"),
        "PLATELETS": DeltaCheckRule("PLATELETS", "Platelet Count", 50.0, 80.0, 48.0, "WARNING"),
        "SODIUM": DeltaCheckRule("SODIUM", "Serum Sodium", 10.0, 10.0, 48.0, "WARNING"),
        "GLUCOSE": DeltaCheckRule("GLUCOSE", "Plasma Glucose", 100.0, 150.0, 24.0, "WARNING"),
        "CALCIUM": DeltaCheckRule("CALCIUM", "Total Serum Calcium", 20.0, 1.8, 48.0, "WARNING"),
    }

    def __init__(self, custom_rules: Optional[Dict[str, DeltaCheckRule]] = None):
        self.rules = self.DEFAULT_RULES.copy()
        if custom_rules:
            self.rules.update(custom_rules)

    def evaluate(self, test_code: str, current_value: float, previous_value: float, hours_elapsed: float) -> DeltaCheckResult:
        rule = self.rules.get(test_code.upper())
        if not rule:
            return DeltaCheckResult(
                test_code=test_code,
                current_value=current_value,
                previous_value=previous_value,
                percent_change=0.0,
                absolute_delta=abs(current_value - previous_value),
                hours_elapsed=hours_elapsed,
                is_violation=False,
                message="No delta check rule configured for test."
            )

        absolute_delta = abs(current_value - previous_value)
        percent_change = 0.0
        if previous_value != 0:
            percent_change = abs((current_value - previous_value) / previous_value) * 100.0

        if hours_elapsed > rule.max_delta_hours:
            return DeltaCheckResult(
                test_code=test_code,
                current_value=current_value,
                previous_value=previous_value,
                percent_change=percent_change,
                absolute_delta=absolute_delta,
                hours_elapsed=hours_elapsed,
                is_violation=False,
                message=f"Elapsed time ({hours_elapsed:.1f}h) exceeds rule window ({rule.max_delta_hours}h)."
            )

        is_violation = (percent_change > rule.max_percent_change) or (absolute_delta > rule.max_absolute_delta)
        severity = rule.alert_severity if is_violation else None
        msg = None
        if is_violation:
            msg = (f"Delta Check Alert: {rule.test_name} shifted by {percent_change:.1f}% "
                   f"(abs: {absolute_delta:.2f}) within {hours_elapsed:.1f}h. Threshold: {rule.max_percent_change}%.")

        return DeltaCheckResult(
            test_code=test_code,
            current_value=current_value,
            previous_value=previous_value,
            percent_change=percent_change,
            absolute_delta=absolute_delta,
            hours_elapsed=hours_elapsed,
            is_violation=is_violation,
            severity=severity,
            message=msg
        )
