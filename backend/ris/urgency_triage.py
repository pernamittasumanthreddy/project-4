"""
Radiology Modality Worklist Urgency and Stroke Fast-Track Triager.
Prioritizes Emergency STAT, Acute Stroke, and Trauma Level 1 scans
to ensure door-to-image time SLA compliance.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class TriagePriority:
    level: int
    name: str
    target_turnaround_minutes: int
    color_code: str

class RadiologyUrgencyTriager:
    PRIORITIES = {
        "STROKE": TriagePriority(1, "Acute Stroke Fast-Track", 15, "#DC2626"),
        "TRAUMA_1": TriagePriority(2, "Trauma Level 1 STAT", 20, "#EA580C"),
        "STAT": TriagePriority(3, "Emergency STAT", 30, "#F59E0B"),
        "URGENT": TriagePriority(4, "Inpatient Urgent", 120, "#3B82F6"),
        "ROUTINE": TriagePriority(5, "Outpatient Routine", 1440, "#10B981")
    }

    @classmethod
    def get_priority(cls, urgency_code: str) -> TriagePriority:
        return cls.PRIORITIES.get(urgency_code.upper(), cls.PRIORITIES["ROUTINE"])
