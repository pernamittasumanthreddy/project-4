"""
Red-Flag Urgent Radiology Findings Dispatch and Acknowledgment Tracker.
Dispatches critical finding alerts (Tension Pneumothorax, Aortic Dissection, Hemorrhage).
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

@dataclass
class CriticalImagingAlert:
    alert_id: str
    study_instance_uid: str
    patient_id: str
    radiologist_id: str
    finding_description: str
    timestamp: datetime
    acknowledged_by_clinician: bool = False

class CriticalImagingAlertEngine:
    RED_FLAGS = [
        "AORTIC_DISSECTION",
        "EPIDURAL_HEMATOMA",
        "TENSION_PNEUMOTHORAX",
        "ACUTE_PULMONARY_EMBOLISM",
        "FREE_PERITONEAL_AIR"
    ]

    @classmethod
    def is_red_flag_condition(cls, finding_code: str) -> bool:
        return finding_code.upper() in cls.RED_FLAGS
