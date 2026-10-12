"""
Clinical Laboratory Turnaround Time (TAT) Analytics Engine.
Computes accession-to-result and order-to-verification metrics, 90th percentile TAT,
and STAT SLA compliance rate.
"""

from typing import List, Dict, Any
import statistics

class TurnaroundTimeAnalytics:
    @staticmethod
    def calculate_tat_metrics(turnaround_minutes: List[float], stat_cutoff_min: float = 45.0) -> Dict[str, Any]:
        if not turnaround_minutes:
            return {"count": 0, "mean_min": 0.0, "median_min": 0.0, "p90_min": 0.0, "sla_compliance_rate": 100.0}
        
        sorted_tat = sorted(turnaround_minutes)
        n = len(sorted_tat)
        mean_tat = statistics.mean(sorted_tat)
        median_tat = statistics.median(sorted_tat)
        p90_idx = int(0.9 * n)
        p90_tat = sorted_tat[min(p90_idx, n - 1)]
        within_sla = sum(1 for t in sorted_tat if t <= stat_cutoff_min)
        compliance_rate = (within_sla / n) * 100.0

        return {
            "count": n,
            "mean_min": round(mean_tat, 1),
            "median_min": round(median_tat, 1),
            "p90_min": round(p90_tat, 1),
            "sla_compliance_rate": round(compliance_rate, 1)
        }
