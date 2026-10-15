"""
Specimen Cold-Chain Temperature Telemetry & Integrity Monitoring Engine.
Enforces CAP/ISO 15189 pre-analytical quality assurance for transported specimens.
Tracks ambient (15-25°C), refrigerated (2-8°C), and frozen (<= -20°C) transport conditions.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class StorageConditionPolicy:
    category: str
    min_temp_celsius: float
    max_temp_celsius: float
    max_excursion_minutes: int

class SpecimenTemperatureValidator:
    POLICIES: Dict[str, StorageConditionPolicy] = {
        "REFRIGERATED": StorageConditionPolicy("REFRIGERATED", 2.0, 8.0, 30),
        "FROZEN": StorageConditionPolicy("FROZEN", -80.0, -20.0, 15),
        "AMBIENT": StorageConditionPolicy("AMBIENT", 15.0, 25.0, 120),
    }

    @classmethod
    def evaluate_telemetry(cls, storage_category: str, recorded_temp: float, excursion_duration_min: int = 0) -> Dict[str, Any]:
        policy = cls.POLICIES.get(storage_category.upper())
        if not policy:
            return {
                "is_compliant": False,
                "status": "UNKNOWN_STORAGE_CATEGORY",
                "recommended_action": "REJECT_SPECIMEN",
                "deviation_celsius": 0.0
            }

        is_within_range = (policy.min_temp_celsius <= recorded_temp <= policy.max_temp_celsius)
        
        if is_within_range:
            return {
                "is_compliant": True,
                "status": "OPTIMAL",
                "recommended_action": "PROCESS_SAMPLE",
                "deviation_celsius": 0.0
            }

        deviation = min(abs(recorded_temp - policy.min_temp_celsius), abs(recorded_temp - policy.max_temp_celsius))
        exceeds_excursion_time = (excursion_duration_min > policy.max_excursion_minutes)

        if exceeds_excursion_time:
            action = "REJECT_SPECIMEN"
            status = "CRITICAL_EXCURSION"
        else:
            action = "ACCEPT_WITH_CAUTION"
            status = "TRANSIENT_EXCURSION"

        return {
            "is_compliant": False,
            "status": status,
            "recommended_action": action,
            "deviation_celsius": round(deviation, 2),
            "max_allowed_excursion_min": policy.max_excursion_minutes,
            "actual_excursion_min": excursion_duration_min
        }
