"""
Radiology Modality Equipment Utilization and Operational Analytics.
Calculates scanner throughput, slot occupancy percentage, and downtime metrics.
"""

from typing import List, Dict, Any

class ModalityUtilizationAnalytics:
    @staticmethod
    def calculate_utilization(operating_hours: float, exam_durations_minutes: List[float]) -> Dict[str, Any]:
        total_avail_min = operating_hours * 60.0
        used_min = sum(exam_durations_minutes)
        occupancy = (used_min / total_avail_min * 100.0) if total_avail_min > 0 else 0.0
        return {
            "total_available_minutes": total_avail_min,
            "total_scan_minutes": round(used_min, 1),
            "occupancy_rate_percent": round(min(occupancy, 100.0), 1),
            "total_exams_performed": len(exam_durations_minutes)
        }
