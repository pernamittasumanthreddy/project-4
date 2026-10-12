"""
Demographic-Stratified Biological Reference Range Partitioner.
Partitions reference limits by age category (neonate, pediatric, adult, geriatric)
and biological sex per CLSI C28-A3 guidelines.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Tuple

@dataclass
class StratifiedRange:
    age_min_years: float
    age_max_years: float
    sex: str  # M, F, ALL
    low_limit: float
    high_limit: float
    unit: str

class ReferenceRangePartitioner:
    HEMOGLOBIN_PARTITIONS = [
        StratifiedRange(0.0, 0.1, "ALL", 14.0, 24.0, "g/dL"),    # Neonate
        StratifiedRange(0.1, 12.0, "ALL", 11.5, 15.5, "g/dL"),  # Child
        StratifiedRange(12.0, 120.0, "M", 13.8, 17.2, "g/dL"),  # Adult Male
        StratifiedRange(12.0, 120.0, "F", 12.1, 15.1, "g/dL")   # Adult Female
    ]

    @classmethod
    def get_hemoglobin_range(cls, age_years: float, sex: str) -> Tuple[float, float, str]:
        for r in cls.HEMOGLOBIN_PARTITIONS:
            if r.age_min_years <= age_years < r.age_max_years:
                if r.sex == "ALL" or r.sex.upper() == sex.upper():
                    return r.low_limit, r.high_limit, r.unit
        return 12.0, 16.0, "g/dL"
