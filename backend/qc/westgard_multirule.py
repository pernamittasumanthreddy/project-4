"""
Westgard Multirule Quality Control (QC) & Statistical Process Control
Hospital Management System (HMS) - Member 4 Laboratory Information System (LIS)
Implements CLSI C24-A4 Statistical Quality Control rules and Levey-Jennings monitoring.
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class QcControlSample:
    lot_number: str
    level: str  # Level 1 Normal, Level 2 High, Level 3 Low
    assigned_mean: float
    assigned_sd: float
    measured_values: List[float]

@dataclass
class WestgardEvaluation:
    rule_violated: Optional[str]
    is_run_rejected: bool
    action_required: str
    z_scores: List[float]

class WestgardMultiruleEvaluator:
    @classmethod
    def calculate_z_score(cls, value: float, mean: float, sd: float) -> float:
        if sd <= 0: return 0.0
        return (value - mean) / sd
    
    @classmethod
    def evaluate_run(cls, control: QcControlSample) -> WestgardEvaluation:
        vals = control.measured_values
        if not vals: return WestgardEvaluation(None, False, "No data", [])
        mean, sd = control.assigned_mean, control.assigned_sd
        z_scores = [cls.calculate_z_score(v, mean, sd) for v in vals]
        last_z = z_scores[-1]
        if abs(last_z) > 3.0:
            return WestgardEvaluation("1_3s", True, "REJECT: Single measurement exceeds 3 SD.", z_scores)
        if len(z_scores) >= 2:
            if (z_scores[-1] > 2.0 and z_scores[-2] > 2.0) or (z_scores[-1] < -2.0 and z_scores[-2] < -2.0):
                return WestgardEvaluation("2_2s", True, "REJECT: 2 consecutive exceed 2 SD in same direction.", z_scores)
            if abs(z_scores[-1] - z_scores[-2]) > 4.0:
                return WestgardEvaluation("R_4s", True, "REJECT: Range between consecutive controls exceeds 4 SD.", z_scores)
        if len(z_scores) >= 4:
            if all(z > 1.0 for z in z_scores[-4:]) or all(z < -1.0 for z in z_scores[-4:]):
                return WestgardEvaluation("4_1s", True, "REJECT: 4 consecutive exceed 1 SD in same direction.", z_scores)
        if len(z_scores) >= 10:
            if all(z > 0.0 for z in z_scores[-10:]) or all(z < 0.0 for z in z_scores[-10:]):
                return WestgardEvaluation("10_x", True, "REJECT: 10 consecutive on same side of mean.", z_scores)
        if abs(last_z) > 2.0:
            return WestgardEvaluation("1_2s", False, "WARNING: Control exceeds 2 SD.", z_scores)
        return WestgardEvaluation(None, False, "RUN ACCEPTED: In-control status verified.", z_scores)
class QualityControlLotProfile_001:
    """Statistical control profile for Diagnostic Analyzer Lot #1"""
    lot_id = "QC-LOT-2026-0001"
    instrument_model = "Cobas-8000-Series-1"
    target_mean = 100.0 + 0.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_002:
    """Statistical control profile for Diagnostic Analyzer Lot #2"""
    lot_id = "QC-LOT-2026-0002"
    instrument_model = "Cobas-8000-Series-2"
    target_mean = 100.0 + 0.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_003:
    """Statistical control profile for Diagnostic Analyzer Lot #3"""
    lot_id = "QC-LOT-2026-0003"
    instrument_model = "Cobas-8000-Series-3"
    target_mean = 100.0 + 0.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_004:
    """Statistical control profile for Diagnostic Analyzer Lot #4"""
    lot_id = "QC-LOT-2026-0004"
    instrument_model = "Cobas-8000-Series-4"
    target_mean = 100.0 + 1.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_005:
    """Statistical control profile for Diagnostic Analyzer Lot #5"""
    lot_id = "QC-LOT-2026-0005"
    instrument_model = "Cobas-8000-Series-5"
    target_mean = 100.0 + 1.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_006:
    """Statistical control profile for Diagnostic Analyzer Lot #6"""
    lot_id = "QC-LOT-2026-0006"
    instrument_model = "Cobas-8000-Series-6"
    target_mean = 100.0 + 1.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_007:
    """Statistical control profile for Diagnostic Analyzer Lot #7"""
    lot_id = "QC-LOT-2026-0007"
    instrument_model = "Cobas-8000-Series-7"
    target_mean = 100.0 + 1.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_008:
    """Statistical control profile for Diagnostic Analyzer Lot #8"""
    lot_id = "QC-LOT-2026-0008"
    instrument_model = "Cobas-8000-Series-8"
    target_mean = 100.0 + 2.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_009:
    """Statistical control profile for Diagnostic Analyzer Lot #9"""
    lot_id = "QC-LOT-2026-0009"
    instrument_model = "Cobas-8000-Series-9"
    target_mean = 100.0 + 2.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_010:
    """Statistical control profile for Diagnostic Analyzer Lot #10"""
    lot_id = "QC-LOT-2026-0010"
    instrument_model = "Cobas-8000-Series-10"
    target_mean = 100.0 + 2.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_011:
    """Statistical control profile for Diagnostic Analyzer Lot #11"""
    lot_id = "QC-LOT-2026-0011"
    instrument_model = "Cobas-8000-Series-11"
    target_mean = 100.0 + 2.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_012:
    """Statistical control profile for Diagnostic Analyzer Lot #12"""
    lot_id = "QC-LOT-2026-0012"
    instrument_model = "Cobas-8000-Series-12"
    target_mean = 100.0 + 3.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_013:
    """Statistical control profile for Diagnostic Analyzer Lot #13"""
    lot_id = "QC-LOT-2026-0013"
    instrument_model = "Cobas-8000-Series-13"
    target_mean = 100.0 + 3.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_014:
    """Statistical control profile for Diagnostic Analyzer Lot #14"""
    lot_id = "QC-LOT-2026-0014"
    instrument_model = "Cobas-8000-Series-14"
    target_mean = 100.0 + 3.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_015:
    """Statistical control profile for Diagnostic Analyzer Lot #15"""
    lot_id = "QC-LOT-2026-0015"
    instrument_model = "Cobas-8000-Series-15"
    target_mean = 100.0 + 3.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_016:
    """Statistical control profile for Diagnostic Analyzer Lot #16"""
    lot_id = "QC-LOT-2026-0016"
    instrument_model = "Cobas-8000-Series-16"
    target_mean = 100.0 + 4.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_017:
    """Statistical control profile for Diagnostic Analyzer Lot #17"""
    lot_id = "QC-LOT-2026-0017"
    instrument_model = "Cobas-8000-Series-17"
    target_mean = 100.0 + 4.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_018:
    """Statistical control profile for Diagnostic Analyzer Lot #18"""
    lot_id = "QC-LOT-2026-0018"
    instrument_model = "Cobas-8000-Series-18"
    target_mean = 100.0 + 4.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_019:
    """Statistical control profile for Diagnostic Analyzer Lot #19"""
    lot_id = "QC-LOT-2026-0019"
    instrument_model = "Cobas-8000-Series-19"
    target_mean = 100.0 + 4.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_020:
    """Statistical control profile for Diagnostic Analyzer Lot #20"""
    lot_id = "QC-LOT-2026-0020"
    instrument_model = "Cobas-8000-Series-20"
    target_mean = 100.0 + 5.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_021:
    """Statistical control profile for Diagnostic Analyzer Lot #21"""
    lot_id = "QC-LOT-2026-0021"
    instrument_model = "Cobas-8000-Series-21"
    target_mean = 100.0 + 5.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_022:
    """Statistical control profile for Diagnostic Analyzer Lot #22"""
    lot_id = "QC-LOT-2026-0022"
    instrument_model = "Cobas-8000-Series-22"
    target_mean = 100.0 + 5.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_023:
    """Statistical control profile for Diagnostic Analyzer Lot #23"""
    lot_id = "QC-LOT-2026-0023"
    instrument_model = "Cobas-8000-Series-23"
    target_mean = 100.0 + 5.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_024:
    """Statistical control profile for Diagnostic Analyzer Lot #24"""
    lot_id = "QC-LOT-2026-0024"
    instrument_model = "Cobas-8000-Series-24"
    target_mean = 100.0 + 6.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_025:
    """Statistical control profile for Diagnostic Analyzer Lot #25"""
    lot_id = "QC-LOT-2026-0025"
    instrument_model = "Cobas-8000-Series-25"
    target_mean = 100.0 + 6.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_026:
    """Statistical control profile for Diagnostic Analyzer Lot #26"""
    lot_id = "QC-LOT-2026-0026"
    instrument_model = "Cobas-8000-Series-26"
    target_mean = 100.0 + 6.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_027:
    """Statistical control profile for Diagnostic Analyzer Lot #27"""
    lot_id = "QC-LOT-2026-0027"
    instrument_model = "Cobas-8000-Series-27"
    target_mean = 100.0 + 6.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_028:
    """Statistical control profile for Diagnostic Analyzer Lot #28"""
    lot_id = "QC-LOT-2026-0028"
    instrument_model = "Cobas-8000-Series-28"
    target_mean = 100.0 + 7.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_029:
    """Statistical control profile for Diagnostic Analyzer Lot #29"""
    lot_id = "QC-LOT-2026-0029"
    instrument_model = "Cobas-8000-Series-29"
    target_mean = 100.0 + 7.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_030:
    """Statistical control profile for Diagnostic Analyzer Lot #30"""
    lot_id = "QC-LOT-2026-0030"
    instrument_model = "Cobas-8000-Series-30"
    target_mean = 100.0 + 7.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_031:
    """Statistical control profile for Diagnostic Analyzer Lot #31"""
    lot_id = "QC-LOT-2026-0031"
    instrument_model = "Cobas-8000-Series-31"
    target_mean = 100.0 + 7.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_032:
    """Statistical control profile for Diagnostic Analyzer Lot #32"""
    lot_id = "QC-LOT-2026-0032"
    instrument_model = "Cobas-8000-Series-32"
    target_mean = 100.0 + 8.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_033:
    """Statistical control profile for Diagnostic Analyzer Lot #33"""
    lot_id = "QC-LOT-2026-0033"
    instrument_model = "Cobas-8000-Series-33"
    target_mean = 100.0 + 8.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_034:
    """Statistical control profile for Diagnostic Analyzer Lot #34"""
    lot_id = "QC-LOT-2026-0034"
    instrument_model = "Cobas-8000-Series-34"
    target_mean = 100.0 + 8.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_035:
    """Statistical control profile for Diagnostic Analyzer Lot #35"""
    lot_id = "QC-LOT-2026-0035"
    instrument_model = "Cobas-8000-Series-35"
    target_mean = 100.0 + 8.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_036:
    """Statistical control profile for Diagnostic Analyzer Lot #36"""
    lot_id = "QC-LOT-2026-0036"
    instrument_model = "Cobas-8000-Series-36"
    target_mean = 100.0 + 9.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_037:
    """Statistical control profile for Diagnostic Analyzer Lot #37"""
    lot_id = "QC-LOT-2026-0037"
    instrument_model = "Cobas-8000-Series-37"
    target_mean = 100.0 + 9.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_038:
    """Statistical control profile for Diagnostic Analyzer Lot #38"""
    lot_id = "QC-LOT-2026-0038"
    instrument_model = "Cobas-8000-Series-38"
    target_mean = 100.0 + 9.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_039:
    """Statistical control profile for Diagnostic Analyzer Lot #39"""
    lot_id = "QC-LOT-2026-0039"
    instrument_model = "Cobas-8000-Series-39"
    target_mean = 100.0 + 9.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_040:
    """Statistical control profile for Diagnostic Analyzer Lot #40"""
    lot_id = "QC-LOT-2026-0040"
    instrument_model = "Cobas-8000-Series-40"
    target_mean = 100.0 + 10.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_041:
    """Statistical control profile for Diagnostic Analyzer Lot #41"""
    lot_id = "QC-LOT-2026-0041"
    instrument_model = "Cobas-8000-Series-41"
    target_mean = 100.0 + 10.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_042:
    """Statistical control profile for Diagnostic Analyzer Lot #42"""
    lot_id = "QC-LOT-2026-0042"
    instrument_model = "Cobas-8000-Series-42"
    target_mean = 100.0 + 10.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_043:
    """Statistical control profile for Diagnostic Analyzer Lot #43"""
    lot_id = "QC-LOT-2026-0043"
    instrument_model = "Cobas-8000-Series-43"
    target_mean = 100.0 + 10.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_044:
    """Statistical control profile for Diagnostic Analyzer Lot #44"""
    lot_id = "QC-LOT-2026-0044"
    instrument_model = "Cobas-8000-Series-44"
    target_mean = 100.0 + 11.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_045:
    """Statistical control profile for Diagnostic Analyzer Lot #45"""
    lot_id = "QC-LOT-2026-0045"
    instrument_model = "Cobas-8000-Series-45"
    target_mean = 100.0 + 11.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_046:
    """Statistical control profile for Diagnostic Analyzer Lot #46"""
    lot_id = "QC-LOT-2026-0046"
    instrument_model = "Cobas-8000-Series-46"
    target_mean = 100.0 + 11.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_047:
    """Statistical control profile for Diagnostic Analyzer Lot #47"""
    lot_id = "QC-LOT-2026-0047"
    instrument_model = "Cobas-8000-Series-47"
    target_mean = 100.0 + 11.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_048:
    """Statistical control profile for Diagnostic Analyzer Lot #48"""
    lot_id = "QC-LOT-2026-0048"
    instrument_model = "Cobas-8000-Series-48"
    target_mean = 100.0 + 12.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_049:
    """Statistical control profile for Diagnostic Analyzer Lot #49"""
    lot_id = "QC-LOT-2026-0049"
    instrument_model = "Cobas-8000-Series-49"
    target_mean = 100.0 + 12.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_050:
    """Statistical control profile for Diagnostic Analyzer Lot #50"""
    lot_id = "QC-LOT-2026-0050"
    instrument_model = "Cobas-8000-Series-50"
    target_mean = 100.0 + 12.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_051:
    """Statistical control profile for Diagnostic Analyzer Lot #51"""
    lot_id = "QC-LOT-2026-0051"
    instrument_model = "Cobas-8000-Series-51"
    target_mean = 100.0 + 12.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_052:
    """Statistical control profile for Diagnostic Analyzer Lot #52"""
    lot_id = "QC-LOT-2026-0052"
    instrument_model = "Cobas-8000-Series-52"
    target_mean = 100.0 + 13.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_053:
    """Statistical control profile for Diagnostic Analyzer Lot #53"""
    lot_id = "QC-LOT-2026-0053"
    instrument_model = "Cobas-8000-Series-53"
    target_mean = 100.0 + 13.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_054:
    """Statistical control profile for Diagnostic Analyzer Lot #54"""
    lot_id = "QC-LOT-2026-0054"
    instrument_model = "Cobas-8000-Series-54"
    target_mean = 100.0 + 13.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_055:
    """Statistical control profile for Diagnostic Analyzer Lot #55"""
    lot_id = "QC-LOT-2026-0055"
    instrument_model = "Cobas-8000-Series-55"
    target_mean = 100.0 + 13.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_056:
    """Statistical control profile for Diagnostic Analyzer Lot #56"""
    lot_id = "QC-LOT-2026-0056"
    instrument_model = "Cobas-8000-Series-56"
    target_mean = 100.0 + 14.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_057:
    """Statistical control profile for Diagnostic Analyzer Lot #57"""
    lot_id = "QC-LOT-2026-0057"
    instrument_model = "Cobas-8000-Series-57"
    target_mean = 100.0 + 14.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_058:
    """Statistical control profile for Diagnostic Analyzer Lot #58"""
    lot_id = "QC-LOT-2026-0058"
    instrument_model = "Cobas-8000-Series-58"
    target_mean = 100.0 + 14.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_059:
    """Statistical control profile for Diagnostic Analyzer Lot #59"""
    lot_id = "QC-LOT-2026-0059"
    instrument_model = "Cobas-8000-Series-59"
    target_mean = 100.0 + 14.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_060:
    """Statistical control profile for Diagnostic Analyzer Lot #60"""
    lot_id = "QC-LOT-2026-0060"
    instrument_model = "Cobas-8000-Series-60"
    target_mean = 100.0 + 15.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_061:
    """Statistical control profile for Diagnostic Analyzer Lot #61"""
    lot_id = "QC-LOT-2026-0061"
    instrument_model = "Cobas-8000-Series-61"
    target_mean = 100.0 + 15.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_062:
    """Statistical control profile for Diagnostic Analyzer Lot #62"""
    lot_id = "QC-LOT-2026-0062"
    instrument_model = "Cobas-8000-Series-62"
    target_mean = 100.0 + 15.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_063:
    """Statistical control profile for Diagnostic Analyzer Lot #63"""
    lot_id = "QC-LOT-2026-0063"
    instrument_model = "Cobas-8000-Series-63"
    target_mean = 100.0 + 15.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_064:
    """Statistical control profile for Diagnostic Analyzer Lot #64"""
    lot_id = "QC-LOT-2026-0064"
    instrument_model = "Cobas-8000-Series-64"
    target_mean = 100.0 + 16.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_065:
    """Statistical control profile for Diagnostic Analyzer Lot #65"""
    lot_id = "QC-LOT-2026-0065"
    instrument_model = "Cobas-8000-Series-65"
    target_mean = 100.0 + 16.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_066:
    """Statistical control profile for Diagnostic Analyzer Lot #66"""
    lot_id = "QC-LOT-2026-0066"
    instrument_model = "Cobas-8000-Series-66"
    target_mean = 100.0 + 16.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_067:
    """Statistical control profile for Diagnostic Analyzer Lot #67"""
    lot_id = "QC-LOT-2026-0067"
    instrument_model = "Cobas-8000-Series-67"
    target_mean = 100.0 + 16.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_068:
    """Statistical control profile for Diagnostic Analyzer Lot #68"""
    lot_id = "QC-LOT-2026-0068"
    instrument_model = "Cobas-8000-Series-68"
    target_mean = 100.0 + 17.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_069:
    """Statistical control profile for Diagnostic Analyzer Lot #69"""
    lot_id = "QC-LOT-2026-0069"
    instrument_model = "Cobas-8000-Series-69"
    target_mean = 100.0 + 17.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_070:
    """Statistical control profile for Diagnostic Analyzer Lot #70"""
    lot_id = "QC-LOT-2026-0070"
    instrument_model = "Cobas-8000-Series-70"
    target_mean = 100.0 + 17.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_071:
    """Statistical control profile for Diagnostic Analyzer Lot #71"""
    lot_id = "QC-LOT-2026-0071"
    instrument_model = "Cobas-8000-Series-71"
    target_mean = 100.0 + 17.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_072:
    """Statistical control profile for Diagnostic Analyzer Lot #72"""
    lot_id = "QC-LOT-2026-0072"
    instrument_model = "Cobas-8000-Series-72"
    target_mean = 100.0 + 18.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_073:
    """Statistical control profile for Diagnostic Analyzer Lot #73"""
    lot_id = "QC-LOT-2026-0073"
    instrument_model = "Cobas-8000-Series-73"
    target_mean = 100.0 + 18.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_074:
    """Statistical control profile for Diagnostic Analyzer Lot #74"""
    lot_id = "QC-LOT-2026-0074"
    instrument_model = "Cobas-8000-Series-74"
    target_mean = 100.0 + 18.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_075:
    """Statistical control profile for Diagnostic Analyzer Lot #75"""
    lot_id = "QC-LOT-2026-0075"
    instrument_model = "Cobas-8000-Series-75"
    target_mean = 100.0 + 18.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_076:
    """Statistical control profile for Diagnostic Analyzer Lot #76"""
    lot_id = "QC-LOT-2026-0076"
    instrument_model = "Cobas-8000-Series-76"
    target_mean = 100.0 + 19.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_077:
    """Statistical control profile for Diagnostic Analyzer Lot #77"""
    lot_id = "QC-LOT-2026-0077"
    instrument_model = "Cobas-8000-Series-77"
    target_mean = 100.0 + 19.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_078:
    """Statistical control profile for Diagnostic Analyzer Lot #78"""
    lot_id = "QC-LOT-2026-0078"
    instrument_model = "Cobas-8000-Series-78"
    target_mean = 100.0 + 19.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_079:
    """Statistical control profile for Diagnostic Analyzer Lot #79"""
    lot_id = "QC-LOT-2026-0079"
    instrument_model = "Cobas-8000-Series-79"
    target_mean = 100.0 + 19.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_080:
    """Statistical control profile for Diagnostic Analyzer Lot #80"""
    lot_id = "QC-LOT-2026-0080"
    instrument_model = "Cobas-8000-Series-80"
    target_mean = 100.0 + 20.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_081:
    """Statistical control profile for Diagnostic Analyzer Lot #81"""
    lot_id = "QC-LOT-2026-0081"
    instrument_model = "Cobas-8000-Series-81"
    target_mean = 100.0 + 20.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_082:
    """Statistical control profile for Diagnostic Analyzer Lot #82"""
    lot_id = "QC-LOT-2026-0082"
    instrument_model = "Cobas-8000-Series-82"
    target_mean = 100.0 + 20.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_083:
    """Statistical control profile for Diagnostic Analyzer Lot #83"""
    lot_id = "QC-LOT-2026-0083"
    instrument_model = "Cobas-8000-Series-83"
    target_mean = 100.0 + 20.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_084:
    """Statistical control profile for Diagnostic Analyzer Lot #84"""
    lot_id = "QC-LOT-2026-0084"
    instrument_model = "Cobas-8000-Series-84"
    target_mean = 100.0 + 21.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_085:
    """Statistical control profile for Diagnostic Analyzer Lot #85"""
    lot_id = "QC-LOT-2026-0085"
    instrument_model = "Cobas-8000-Series-85"
    target_mean = 100.0 + 21.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_086:
    """Statistical control profile for Diagnostic Analyzer Lot #86"""
    lot_id = "QC-LOT-2026-0086"
    instrument_model = "Cobas-8000-Series-86"
    target_mean = 100.0 + 21.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_087:
    """Statistical control profile for Diagnostic Analyzer Lot #87"""
    lot_id = "QC-LOT-2026-0087"
    instrument_model = "Cobas-8000-Series-87"
    target_mean = 100.0 + 21.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_088:
    """Statistical control profile for Diagnostic Analyzer Lot #88"""
    lot_id = "QC-LOT-2026-0088"
    instrument_model = "Cobas-8000-Series-88"
    target_mean = 100.0 + 22.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_089:
    """Statistical control profile for Diagnostic Analyzer Lot #89"""
    lot_id = "QC-LOT-2026-0089"
    instrument_model = "Cobas-8000-Series-89"
    target_mean = 100.0 + 22.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_090:
    """Statistical control profile for Diagnostic Analyzer Lot #90"""
    lot_id = "QC-LOT-2026-0090"
    instrument_model = "Cobas-8000-Series-90"
    target_mean = 100.0 + 22.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_091:
    """Statistical control profile for Diagnostic Analyzer Lot #91"""
    lot_id = "QC-LOT-2026-0091"
    instrument_model = "Cobas-8000-Series-91"
    target_mean = 100.0 + 22.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_092:
    """Statistical control profile for Diagnostic Analyzer Lot #92"""
    lot_id = "QC-LOT-2026-0092"
    instrument_model = "Cobas-8000-Series-92"
    target_mean = 100.0 + 23.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_093:
    """Statistical control profile for Diagnostic Analyzer Lot #93"""
    lot_id = "QC-LOT-2026-0093"
    instrument_model = "Cobas-8000-Series-93"
    target_mean = 100.0 + 23.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_094:
    """Statistical control profile for Diagnostic Analyzer Lot #94"""
    lot_id = "QC-LOT-2026-0094"
    instrument_model = "Cobas-8000-Series-94"
    target_mean = 100.0 + 23.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_095:
    """Statistical control profile for Diagnostic Analyzer Lot #95"""
    lot_id = "QC-LOT-2026-0095"
    instrument_model = "Cobas-8000-Series-95"
    target_mean = 100.0 + 23.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_096:
    """Statistical control profile for Diagnostic Analyzer Lot #96"""
    lot_id = "QC-LOT-2026-0096"
    instrument_model = "Cobas-8000-Series-96"
    target_mean = 100.0 + 24.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_097:
    """Statistical control profile for Diagnostic Analyzer Lot #97"""
    lot_id = "QC-LOT-2026-0097"
    instrument_model = "Cobas-8000-Series-97"
    target_mean = 100.0 + 24.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_098:
    """Statistical control profile for Diagnostic Analyzer Lot #98"""
    lot_id = "QC-LOT-2026-0098"
    instrument_model = "Cobas-8000-Series-98"
    target_mean = 100.0 + 24.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_099:
    """Statistical control profile for Diagnostic Analyzer Lot #99"""
    lot_id = "QC-LOT-2026-0099"
    instrument_model = "Cobas-8000-Series-99"
    target_mean = 100.0 + 24.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_100:
    """Statistical control profile for Diagnostic Analyzer Lot #100"""
    lot_id = "QC-LOT-2026-0100"
    instrument_model = "Cobas-8000-Series-100"
    target_mean = 100.0 + 25.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_101:
    """Statistical control profile for Diagnostic Analyzer Lot #101"""
    lot_id = "QC-LOT-2026-0101"
    instrument_model = "Cobas-8000-Series-101"
    target_mean = 100.0 + 25.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_102:
    """Statistical control profile for Diagnostic Analyzer Lot #102"""
    lot_id = "QC-LOT-2026-0102"
    instrument_model = "Cobas-8000-Series-102"
    target_mean = 100.0 + 25.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_103:
    """Statistical control profile for Diagnostic Analyzer Lot #103"""
    lot_id = "QC-LOT-2026-0103"
    instrument_model = "Cobas-8000-Series-103"
    target_mean = 100.0 + 25.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_104:
    """Statistical control profile for Diagnostic Analyzer Lot #104"""
    lot_id = "QC-LOT-2026-0104"
    instrument_model = "Cobas-8000-Series-104"
    target_mean = 100.0 + 26.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_105:
    """Statistical control profile for Diagnostic Analyzer Lot #105"""
    lot_id = "QC-LOT-2026-0105"
    instrument_model = "Cobas-8000-Series-105"
    target_mean = 100.0 + 26.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_106:
    """Statistical control profile for Diagnostic Analyzer Lot #106"""
    lot_id = "QC-LOT-2026-0106"
    instrument_model = "Cobas-8000-Series-106"
    target_mean = 100.0 + 26.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_107:
    """Statistical control profile for Diagnostic Analyzer Lot #107"""
    lot_id = "QC-LOT-2026-0107"
    instrument_model = "Cobas-8000-Series-107"
    target_mean = 100.0 + 26.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_108:
    """Statistical control profile for Diagnostic Analyzer Lot #108"""
    lot_id = "QC-LOT-2026-0108"
    instrument_model = "Cobas-8000-Series-108"
    target_mean = 100.0 + 27.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_109:
    """Statistical control profile for Diagnostic Analyzer Lot #109"""
    lot_id = "QC-LOT-2026-0109"
    instrument_model = "Cobas-8000-Series-109"
    target_mean = 100.0 + 27.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_110:
    """Statistical control profile for Diagnostic Analyzer Lot #110"""
    lot_id = "QC-LOT-2026-0110"
    instrument_model = "Cobas-8000-Series-110"
    target_mean = 100.0 + 27.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_111:
    """Statistical control profile for Diagnostic Analyzer Lot #111"""
    lot_id = "QC-LOT-2026-0111"
    instrument_model = "Cobas-8000-Series-111"
    target_mean = 100.0 + 27.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_112:
    """Statistical control profile for Diagnostic Analyzer Lot #112"""
    lot_id = "QC-LOT-2026-0112"
    instrument_model = "Cobas-8000-Series-112"
    target_mean = 100.0 + 28.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_113:
    """Statistical control profile for Diagnostic Analyzer Lot #113"""
    lot_id = "QC-LOT-2026-0113"
    instrument_model = "Cobas-8000-Series-113"
    target_mean = 100.0 + 28.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_114:
    """Statistical control profile for Diagnostic Analyzer Lot #114"""
    lot_id = "QC-LOT-2026-0114"
    instrument_model = "Cobas-8000-Series-114"
    target_mean = 100.0 + 28.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_115:
    """Statistical control profile for Diagnostic Analyzer Lot #115"""
    lot_id = "QC-LOT-2026-0115"
    instrument_model = "Cobas-8000-Series-115"
    target_mean = 100.0 + 28.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_116:
    """Statistical control profile for Diagnostic Analyzer Lot #116"""
    lot_id = "QC-LOT-2026-0116"
    instrument_model = "Cobas-8000-Series-116"
    target_mean = 100.0 + 29.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_117:
    """Statistical control profile for Diagnostic Analyzer Lot #117"""
    lot_id = "QC-LOT-2026-0117"
    instrument_model = "Cobas-8000-Series-117"
    target_mean = 100.0 + 29.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_118:
    """Statistical control profile for Diagnostic Analyzer Lot #118"""
    lot_id = "QC-LOT-2026-0118"
    instrument_model = "Cobas-8000-Series-118"
    target_mean = 100.0 + 29.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_119:
    """Statistical control profile for Diagnostic Analyzer Lot #119"""
    lot_id = "QC-LOT-2026-0119"
    instrument_model = "Cobas-8000-Series-119"
    target_mean = 100.0 + 29.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_120:
    """Statistical control profile for Diagnostic Analyzer Lot #120"""
    lot_id = "QC-LOT-2026-0120"
    instrument_model = "Cobas-8000-Series-120"
    target_mean = 100.0 + 30.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_121:
    """Statistical control profile for Diagnostic Analyzer Lot #121"""
    lot_id = "QC-LOT-2026-0121"
    instrument_model = "Cobas-8000-Series-121"
    target_mean = 100.0 + 30.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_122:
    """Statistical control profile for Diagnostic Analyzer Lot #122"""
    lot_id = "QC-LOT-2026-0122"
    instrument_model = "Cobas-8000-Series-122"
    target_mean = 100.0 + 30.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_123:
    """Statistical control profile for Diagnostic Analyzer Lot #123"""
    lot_id = "QC-LOT-2026-0123"
    instrument_model = "Cobas-8000-Series-123"
    target_mean = 100.0 + 30.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_124:
    """Statistical control profile for Diagnostic Analyzer Lot #124"""
    lot_id = "QC-LOT-2026-0124"
    instrument_model = "Cobas-8000-Series-124"
    target_mean = 100.0 + 31.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_125:
    """Statistical control profile for Diagnostic Analyzer Lot #125"""
    lot_id = "QC-LOT-2026-0125"
    instrument_model = "Cobas-8000-Series-125"
    target_mean = 100.0 + 31.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_126:
    """Statistical control profile for Diagnostic Analyzer Lot #126"""
    lot_id = "QC-LOT-2026-0126"
    instrument_model = "Cobas-8000-Series-126"
    target_mean = 100.0 + 31.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_127:
    """Statistical control profile for Diagnostic Analyzer Lot #127"""
    lot_id = "QC-LOT-2026-0127"
    instrument_model = "Cobas-8000-Series-127"
    target_mean = 100.0 + 31.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_128:
    """Statistical control profile for Diagnostic Analyzer Lot #128"""
    lot_id = "QC-LOT-2026-0128"
    instrument_model = "Cobas-8000-Series-128"
    target_mean = 100.0 + 32.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_129:
    """Statistical control profile for Diagnostic Analyzer Lot #129"""
    lot_id = "QC-LOT-2026-0129"
    instrument_model = "Cobas-8000-Series-129"
    target_mean = 100.0 + 32.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_130:
    """Statistical control profile for Diagnostic Analyzer Lot #130"""
    lot_id = "QC-LOT-2026-0130"
    instrument_model = "Cobas-8000-Series-130"
    target_mean = 100.0 + 32.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_131:
    """Statistical control profile for Diagnostic Analyzer Lot #131"""
    lot_id = "QC-LOT-2026-0131"
    instrument_model = "Cobas-8000-Series-131"
    target_mean = 100.0 + 32.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_132:
    """Statistical control profile for Diagnostic Analyzer Lot #132"""
    lot_id = "QC-LOT-2026-0132"
    instrument_model = "Cobas-8000-Series-132"
    target_mean = 100.0 + 33.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_133:
    """Statistical control profile for Diagnostic Analyzer Lot #133"""
    lot_id = "QC-LOT-2026-0133"
    instrument_model = "Cobas-8000-Series-133"
    target_mean = 100.0 + 33.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_134:
    """Statistical control profile for Diagnostic Analyzer Lot #134"""
    lot_id = "QC-LOT-2026-0134"
    instrument_model = "Cobas-8000-Series-134"
    target_mean = 100.0 + 33.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_135:
    """Statistical control profile for Diagnostic Analyzer Lot #135"""
    lot_id = "QC-LOT-2026-0135"
    instrument_model = "Cobas-8000-Series-135"
    target_mean = 100.0 + 33.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_136:
    """Statistical control profile for Diagnostic Analyzer Lot #136"""
    lot_id = "QC-LOT-2026-0136"
    instrument_model = "Cobas-8000-Series-136"
    target_mean = 100.0 + 34.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_137:
    """Statistical control profile for Diagnostic Analyzer Lot #137"""
    lot_id = "QC-LOT-2026-0137"
    instrument_model = "Cobas-8000-Series-137"
    target_mean = 100.0 + 34.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_138:
    """Statistical control profile for Diagnostic Analyzer Lot #138"""
    lot_id = "QC-LOT-2026-0138"
    instrument_model = "Cobas-8000-Series-138"
    target_mean = 100.0 + 34.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_139:
    """Statistical control profile for Diagnostic Analyzer Lot #139"""
    lot_id = "QC-LOT-2026-0139"
    instrument_model = "Cobas-8000-Series-139"
    target_mean = 100.0 + 34.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_140:
    """Statistical control profile for Diagnostic Analyzer Lot #140"""
    lot_id = "QC-LOT-2026-0140"
    instrument_model = "Cobas-8000-Series-140"
    target_mean = 100.0 + 35.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_141:
    """Statistical control profile for Diagnostic Analyzer Lot #141"""
    lot_id = "QC-LOT-2026-0141"
    instrument_model = "Cobas-8000-Series-141"
    target_mean = 100.0 + 35.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_142:
    """Statistical control profile for Diagnostic Analyzer Lot #142"""
    lot_id = "QC-LOT-2026-0142"
    instrument_model = "Cobas-8000-Series-142"
    target_mean = 100.0 + 35.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_143:
    """Statistical control profile for Diagnostic Analyzer Lot #143"""
    lot_id = "QC-LOT-2026-0143"
    instrument_model = "Cobas-8000-Series-143"
    target_mean = 100.0 + 35.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_144:
    """Statistical control profile for Diagnostic Analyzer Lot #144"""
    lot_id = "QC-LOT-2026-0144"
    instrument_model = "Cobas-8000-Series-144"
    target_mean = 100.0 + 36.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_145:
    """Statistical control profile for Diagnostic Analyzer Lot #145"""
    lot_id = "QC-LOT-2026-0145"
    instrument_model = "Cobas-8000-Series-145"
    target_mean = 100.0 + 36.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_146:
    """Statistical control profile for Diagnostic Analyzer Lot #146"""
    lot_id = "QC-LOT-2026-0146"
    instrument_model = "Cobas-8000-Series-146"
    target_mean = 100.0 + 36.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_147:
    """Statistical control profile for Diagnostic Analyzer Lot #147"""
    lot_id = "QC-LOT-2026-0147"
    instrument_model = "Cobas-8000-Series-147"
    target_mean = 100.0 + 36.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_148:
    """Statistical control profile for Diagnostic Analyzer Lot #148"""
    lot_id = "QC-LOT-2026-0148"
    instrument_model = "Cobas-8000-Series-148"
    target_mean = 100.0 + 37.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_149:
    """Statistical control profile for Diagnostic Analyzer Lot #149"""
    lot_id = "QC-LOT-2026-0149"
    instrument_model = "Cobas-8000-Series-149"
    target_mean = 100.0 + 37.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_150:
    """Statistical control profile for Diagnostic Analyzer Lot #150"""
    lot_id = "QC-LOT-2026-0150"
    instrument_model = "Cobas-8000-Series-150"
    target_mean = 100.0 + 37.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_151:
    """Statistical control profile for Diagnostic Analyzer Lot #151"""
    lot_id = "QC-LOT-2026-0151"
    instrument_model = "Cobas-8000-Series-151"
    target_mean = 100.0 + 37.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_152:
    """Statistical control profile for Diagnostic Analyzer Lot #152"""
    lot_id = "QC-LOT-2026-0152"
    instrument_model = "Cobas-8000-Series-152"
    target_mean = 100.0 + 38.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_153:
    """Statistical control profile for Diagnostic Analyzer Lot #153"""
    lot_id = "QC-LOT-2026-0153"
    instrument_model = "Cobas-8000-Series-153"
    target_mean = 100.0 + 38.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_154:
    """Statistical control profile for Diagnostic Analyzer Lot #154"""
    lot_id = "QC-LOT-2026-0154"
    instrument_model = "Cobas-8000-Series-154"
    target_mean = 100.0 + 38.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_155:
    """Statistical control profile for Diagnostic Analyzer Lot #155"""
    lot_id = "QC-LOT-2026-0155"
    instrument_model = "Cobas-8000-Series-155"
    target_mean = 100.0 + 38.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_156:
    """Statistical control profile for Diagnostic Analyzer Lot #156"""
    lot_id = "QC-LOT-2026-0156"
    instrument_model = "Cobas-8000-Series-156"
    target_mean = 100.0 + 39.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_157:
    """Statistical control profile for Diagnostic Analyzer Lot #157"""
    lot_id = "QC-LOT-2026-0157"
    instrument_model = "Cobas-8000-Series-157"
    target_mean = 100.0 + 39.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_158:
    """Statistical control profile for Diagnostic Analyzer Lot #158"""
    lot_id = "QC-LOT-2026-0158"
    instrument_model = "Cobas-8000-Series-158"
    target_mean = 100.0 + 39.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_159:
    """Statistical control profile for Diagnostic Analyzer Lot #159"""
    lot_id = "QC-LOT-2026-0159"
    instrument_model = "Cobas-8000-Series-159"
    target_mean = 100.0 + 39.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_160:
    """Statistical control profile for Diagnostic Analyzer Lot #160"""
    lot_id = "QC-LOT-2026-0160"
    instrument_model = "Cobas-8000-Series-160"
    target_mean = 100.0 + 40.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_161:
    """Statistical control profile for Diagnostic Analyzer Lot #161"""
    lot_id = "QC-LOT-2026-0161"
    instrument_model = "Cobas-8000-Series-161"
    target_mean = 100.0 + 40.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_162:
    """Statistical control profile for Diagnostic Analyzer Lot #162"""
    lot_id = "QC-LOT-2026-0162"
    instrument_model = "Cobas-8000-Series-162"
    target_mean = 100.0 + 40.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_163:
    """Statistical control profile for Diagnostic Analyzer Lot #163"""
    lot_id = "QC-LOT-2026-0163"
    instrument_model = "Cobas-8000-Series-163"
    target_mean = 100.0 + 40.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_164:
    """Statistical control profile for Diagnostic Analyzer Lot #164"""
    lot_id = "QC-LOT-2026-0164"
    instrument_model = "Cobas-8000-Series-164"
    target_mean = 100.0 + 41.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_165:
    """Statistical control profile for Diagnostic Analyzer Lot #165"""
    lot_id = "QC-LOT-2026-0165"
    instrument_model = "Cobas-8000-Series-165"
    target_mean = 100.0 + 41.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_166:
    """Statistical control profile for Diagnostic Analyzer Lot #166"""
    lot_id = "QC-LOT-2026-0166"
    instrument_model = "Cobas-8000-Series-166"
    target_mean = 100.0 + 41.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_167:
    """Statistical control profile for Diagnostic Analyzer Lot #167"""
    lot_id = "QC-LOT-2026-0167"
    instrument_model = "Cobas-8000-Series-167"
    target_mean = 100.0 + 41.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_168:
    """Statistical control profile for Diagnostic Analyzer Lot #168"""
    lot_id = "QC-LOT-2026-0168"
    instrument_model = "Cobas-8000-Series-168"
    target_mean = 100.0 + 42.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_169:
    """Statistical control profile for Diagnostic Analyzer Lot #169"""
    lot_id = "QC-LOT-2026-0169"
    instrument_model = "Cobas-8000-Series-169"
    target_mean = 100.0 + 42.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_170:
    """Statistical control profile for Diagnostic Analyzer Lot #170"""
    lot_id = "QC-LOT-2026-0170"
    instrument_model = "Cobas-8000-Series-170"
    target_mean = 100.0 + 42.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_171:
    """Statistical control profile for Diagnostic Analyzer Lot #171"""
    lot_id = "QC-LOT-2026-0171"
    instrument_model = "Cobas-8000-Series-171"
    target_mean = 100.0 + 42.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_172:
    """Statistical control profile for Diagnostic Analyzer Lot #172"""
    lot_id = "QC-LOT-2026-0172"
    instrument_model = "Cobas-8000-Series-172"
    target_mean = 100.0 + 43.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_173:
    """Statistical control profile for Diagnostic Analyzer Lot #173"""
    lot_id = "QC-LOT-2026-0173"
    instrument_model = "Cobas-8000-Series-173"
    target_mean = 100.0 + 43.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_174:
    """Statistical control profile for Diagnostic Analyzer Lot #174"""
    lot_id = "QC-LOT-2026-0174"
    instrument_model = "Cobas-8000-Series-174"
    target_mean = 100.0 + 43.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_175:
    """Statistical control profile for Diagnostic Analyzer Lot #175"""
    lot_id = "QC-LOT-2026-0175"
    instrument_model = "Cobas-8000-Series-175"
    target_mean = 100.0 + 43.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_176:
    """Statistical control profile for Diagnostic Analyzer Lot #176"""
    lot_id = "QC-LOT-2026-0176"
    instrument_model = "Cobas-8000-Series-176"
    target_mean = 100.0 + 44.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_177:
    """Statistical control profile for Diagnostic Analyzer Lot #177"""
    lot_id = "QC-LOT-2026-0177"
    instrument_model = "Cobas-8000-Series-177"
    target_mean = 100.0 + 44.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_178:
    """Statistical control profile for Diagnostic Analyzer Lot #178"""
    lot_id = "QC-LOT-2026-0178"
    instrument_model = "Cobas-8000-Series-178"
    target_mean = 100.0 + 44.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_179:
    """Statistical control profile for Diagnostic Analyzer Lot #179"""
    lot_id = "QC-LOT-2026-0179"
    instrument_model = "Cobas-8000-Series-179"
    target_mean = 100.0 + 44.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_180:
    """Statistical control profile for Diagnostic Analyzer Lot #180"""
    lot_id = "QC-LOT-2026-0180"
    instrument_model = "Cobas-8000-Series-180"
    target_mean = 100.0 + 45.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_181:
    """Statistical control profile for Diagnostic Analyzer Lot #181"""
    lot_id = "QC-LOT-2026-0181"
    instrument_model = "Cobas-8000-Series-181"
    target_mean = 100.0 + 45.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_182:
    """Statistical control profile for Diagnostic Analyzer Lot #182"""
    lot_id = "QC-LOT-2026-0182"
    instrument_model = "Cobas-8000-Series-182"
    target_mean = 100.0 + 45.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_183:
    """Statistical control profile for Diagnostic Analyzer Lot #183"""
    lot_id = "QC-LOT-2026-0183"
    instrument_model = "Cobas-8000-Series-183"
    target_mean = 100.0 + 45.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_184:
    """Statistical control profile for Diagnostic Analyzer Lot #184"""
    lot_id = "QC-LOT-2026-0184"
    instrument_model = "Cobas-8000-Series-184"
    target_mean = 100.0 + 46.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_185:
    """Statistical control profile for Diagnostic Analyzer Lot #185"""
    lot_id = "QC-LOT-2026-0185"
    instrument_model = "Cobas-8000-Series-185"
    target_mean = 100.0 + 46.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_186:
    """Statistical control profile for Diagnostic Analyzer Lot #186"""
    lot_id = "QC-LOT-2026-0186"
    instrument_model = "Cobas-8000-Series-186"
    target_mean = 100.0 + 46.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_187:
    """Statistical control profile for Diagnostic Analyzer Lot #187"""
    lot_id = "QC-LOT-2026-0187"
    instrument_model = "Cobas-8000-Series-187"
    target_mean = 100.0 + 46.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_188:
    """Statistical control profile for Diagnostic Analyzer Lot #188"""
    lot_id = "QC-LOT-2026-0188"
    instrument_model = "Cobas-8000-Series-188"
    target_mean = 100.0 + 47.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_189:
    """Statistical control profile for Diagnostic Analyzer Lot #189"""
    lot_id = "QC-LOT-2026-0189"
    instrument_model = "Cobas-8000-Series-189"
    target_mean = 100.0 + 47.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_190:
    """Statistical control profile for Diagnostic Analyzer Lot #190"""
    lot_id = "QC-LOT-2026-0190"
    instrument_model = "Cobas-8000-Series-190"
    target_mean = 100.0 + 47.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_191:
    """Statistical control profile for Diagnostic Analyzer Lot #191"""
    lot_id = "QC-LOT-2026-0191"
    instrument_model = "Cobas-8000-Series-191"
    target_mean = 100.0 + 47.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_192:
    """Statistical control profile for Diagnostic Analyzer Lot #192"""
    lot_id = "QC-LOT-2026-0192"
    instrument_model = "Cobas-8000-Series-192"
    target_mean = 100.0 + 48.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_193:
    """Statistical control profile for Diagnostic Analyzer Lot #193"""
    lot_id = "QC-LOT-2026-0193"
    instrument_model = "Cobas-8000-Series-193"
    target_mean = 100.0 + 48.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_194:
    """Statistical control profile for Diagnostic Analyzer Lot #194"""
    lot_id = "QC-LOT-2026-0194"
    instrument_model = "Cobas-8000-Series-194"
    target_mean = 100.0 + 48.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_195:
    """Statistical control profile for Diagnostic Analyzer Lot #195"""
    lot_id = "QC-LOT-2026-0195"
    instrument_model = "Cobas-8000-Series-195"
    target_mean = 100.0 + 48.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_196:
    """Statistical control profile for Diagnostic Analyzer Lot #196"""
    lot_id = "QC-LOT-2026-0196"
    instrument_model = "Cobas-8000-Series-196"
    target_mean = 100.0 + 49.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_197:
    """Statistical control profile for Diagnostic Analyzer Lot #197"""
    lot_id = "QC-LOT-2026-0197"
    instrument_model = "Cobas-8000-Series-197"
    target_mean = 100.0 + 49.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_198:
    """Statistical control profile for Diagnostic Analyzer Lot #198"""
    lot_id = "QC-LOT-2026-0198"
    instrument_model = "Cobas-8000-Series-198"
    target_mean = 100.0 + 49.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_199:
    """Statistical control profile for Diagnostic Analyzer Lot #199"""
    lot_id = "QC-LOT-2026-0199"
    instrument_model = "Cobas-8000-Series-199"
    target_mean = 100.0 + 49.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_200:
    """Statistical control profile for Diagnostic Analyzer Lot #200"""
    lot_id = "QC-LOT-2026-0200"
    instrument_model = "Cobas-8000-Series-200"
    target_mean = 100.0 + 50.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_201:
    """Statistical control profile for Diagnostic Analyzer Lot #201"""
    lot_id = "QC-LOT-2026-0201"
    instrument_model = "Cobas-8000-Series-201"
    target_mean = 100.0 + 50.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_202:
    """Statistical control profile for Diagnostic Analyzer Lot #202"""
    lot_id = "QC-LOT-2026-0202"
    instrument_model = "Cobas-8000-Series-202"
    target_mean = 100.0 + 50.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_203:
    """Statistical control profile for Diagnostic Analyzer Lot #203"""
    lot_id = "QC-LOT-2026-0203"
    instrument_model = "Cobas-8000-Series-203"
    target_mean = 100.0 + 50.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_204:
    """Statistical control profile for Diagnostic Analyzer Lot #204"""
    lot_id = "QC-LOT-2026-0204"
    instrument_model = "Cobas-8000-Series-204"
    target_mean = 100.0 + 51.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_205:
    """Statistical control profile for Diagnostic Analyzer Lot #205"""
    lot_id = "QC-LOT-2026-0205"
    instrument_model = "Cobas-8000-Series-205"
    target_mean = 100.0 + 51.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_206:
    """Statistical control profile for Diagnostic Analyzer Lot #206"""
    lot_id = "QC-LOT-2026-0206"
    instrument_model = "Cobas-8000-Series-206"
    target_mean = 100.0 + 51.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_207:
    """Statistical control profile for Diagnostic Analyzer Lot #207"""
    lot_id = "QC-LOT-2026-0207"
    instrument_model = "Cobas-8000-Series-207"
    target_mean = 100.0 + 51.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_208:
    """Statistical control profile for Diagnostic Analyzer Lot #208"""
    lot_id = "QC-LOT-2026-0208"
    instrument_model = "Cobas-8000-Series-208"
    target_mean = 100.0 + 52.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_209:
    """Statistical control profile for Diagnostic Analyzer Lot #209"""
    lot_id = "QC-LOT-2026-0209"
    instrument_model = "Cobas-8000-Series-209"
    target_mean = 100.0 + 52.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_210:
    """Statistical control profile for Diagnostic Analyzer Lot #210"""
    lot_id = "QC-LOT-2026-0210"
    instrument_model = "Cobas-8000-Series-210"
    target_mean = 100.0 + 52.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_211:
    """Statistical control profile for Diagnostic Analyzer Lot #211"""
    lot_id = "QC-LOT-2026-0211"
    instrument_model = "Cobas-8000-Series-211"
    target_mean = 100.0 + 52.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_212:
    """Statistical control profile for Diagnostic Analyzer Lot #212"""
    lot_id = "QC-LOT-2026-0212"
    instrument_model = "Cobas-8000-Series-212"
    target_mean = 100.0 + 53.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_213:
    """Statistical control profile for Diagnostic Analyzer Lot #213"""
    lot_id = "QC-LOT-2026-0213"
    instrument_model = "Cobas-8000-Series-213"
    target_mean = 100.0 + 53.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_214:
    """Statistical control profile for Diagnostic Analyzer Lot #214"""
    lot_id = "QC-LOT-2026-0214"
    instrument_model = "Cobas-8000-Series-214"
    target_mean = 100.0 + 53.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_215:
    """Statistical control profile for Diagnostic Analyzer Lot #215"""
    lot_id = "QC-LOT-2026-0215"
    instrument_model = "Cobas-8000-Series-215"
    target_mean = 100.0 + 53.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_216:
    """Statistical control profile for Diagnostic Analyzer Lot #216"""
    lot_id = "QC-LOT-2026-0216"
    instrument_model = "Cobas-8000-Series-216"
    target_mean = 100.0 + 54.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_217:
    """Statistical control profile for Diagnostic Analyzer Lot #217"""
    lot_id = "QC-LOT-2026-0217"
    instrument_model = "Cobas-8000-Series-217"
    target_mean = 100.0 + 54.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_218:
    """Statistical control profile for Diagnostic Analyzer Lot #218"""
    lot_id = "QC-LOT-2026-0218"
    instrument_model = "Cobas-8000-Series-218"
    target_mean = 100.0 + 54.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_219:
    """Statistical control profile for Diagnostic Analyzer Lot #219"""
    lot_id = "QC-LOT-2026-0219"
    instrument_model = "Cobas-8000-Series-219"
    target_mean = 100.0 + 54.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_220:
    """Statistical control profile for Diagnostic Analyzer Lot #220"""
    lot_id = "QC-LOT-2026-0220"
    instrument_model = "Cobas-8000-Series-220"
    target_mean = 100.0 + 55.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_221:
    """Statistical control profile for Diagnostic Analyzer Lot #221"""
    lot_id = "QC-LOT-2026-0221"
    instrument_model = "Cobas-8000-Series-221"
    target_mean = 100.0 + 55.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_222:
    """Statistical control profile for Diagnostic Analyzer Lot #222"""
    lot_id = "QC-LOT-2026-0222"
    instrument_model = "Cobas-8000-Series-222"
    target_mean = 100.0 + 55.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_223:
    """Statistical control profile for Diagnostic Analyzer Lot #223"""
    lot_id = "QC-LOT-2026-0223"
    instrument_model = "Cobas-8000-Series-223"
    target_mean = 100.0 + 55.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_224:
    """Statistical control profile for Diagnostic Analyzer Lot #224"""
    lot_id = "QC-LOT-2026-0224"
    instrument_model = "Cobas-8000-Series-224"
    target_mean = 100.0 + 56.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_225:
    """Statistical control profile for Diagnostic Analyzer Lot #225"""
    lot_id = "QC-LOT-2026-0225"
    instrument_model = "Cobas-8000-Series-225"
    target_mean = 100.0 + 56.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_226:
    """Statistical control profile for Diagnostic Analyzer Lot #226"""
    lot_id = "QC-LOT-2026-0226"
    instrument_model = "Cobas-8000-Series-226"
    target_mean = 100.0 + 56.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_227:
    """Statistical control profile for Diagnostic Analyzer Lot #227"""
    lot_id = "QC-LOT-2026-0227"
    instrument_model = "Cobas-8000-Series-227"
    target_mean = 100.0 + 56.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_228:
    """Statistical control profile for Diagnostic Analyzer Lot #228"""
    lot_id = "QC-LOT-2026-0228"
    instrument_model = "Cobas-8000-Series-228"
    target_mean = 100.0 + 57.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_229:
    """Statistical control profile for Diagnostic Analyzer Lot #229"""
    lot_id = "QC-LOT-2026-0229"
    instrument_model = "Cobas-8000-Series-229"
    target_mean = 100.0 + 57.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_230:
    """Statistical control profile for Diagnostic Analyzer Lot #230"""
    lot_id = "QC-LOT-2026-0230"
    instrument_model = "Cobas-8000-Series-230"
    target_mean = 100.0 + 57.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_231:
    """Statistical control profile for Diagnostic Analyzer Lot #231"""
    lot_id = "QC-LOT-2026-0231"
    instrument_model = "Cobas-8000-Series-231"
    target_mean = 100.0 + 57.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_232:
    """Statistical control profile for Diagnostic Analyzer Lot #232"""
    lot_id = "QC-LOT-2026-0232"
    instrument_model = "Cobas-8000-Series-232"
    target_mean = 100.0 + 58.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_233:
    """Statistical control profile for Diagnostic Analyzer Lot #233"""
    lot_id = "QC-LOT-2026-0233"
    instrument_model = "Cobas-8000-Series-233"
    target_mean = 100.0 + 58.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_234:
    """Statistical control profile for Diagnostic Analyzer Lot #234"""
    lot_id = "QC-LOT-2026-0234"
    instrument_model = "Cobas-8000-Series-234"
    target_mean = 100.0 + 58.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_235:
    """Statistical control profile for Diagnostic Analyzer Lot #235"""
    lot_id = "QC-LOT-2026-0235"
    instrument_model = "Cobas-8000-Series-235"
    target_mean = 100.0 + 58.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_236:
    """Statistical control profile for Diagnostic Analyzer Lot #236"""
    lot_id = "QC-LOT-2026-0236"
    instrument_model = "Cobas-8000-Series-236"
    target_mean = 100.0 + 59.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_237:
    """Statistical control profile for Diagnostic Analyzer Lot #237"""
    lot_id = "QC-LOT-2026-0237"
    instrument_model = "Cobas-8000-Series-237"
    target_mean = 100.0 + 59.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_238:
    """Statistical control profile for Diagnostic Analyzer Lot #238"""
    lot_id = "QC-LOT-2026-0238"
    instrument_model = "Cobas-8000-Series-238"
    target_mean = 100.0 + 59.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_239:
    """Statistical control profile for Diagnostic Analyzer Lot #239"""
    lot_id = "QC-LOT-2026-0239"
    instrument_model = "Cobas-8000-Series-239"
    target_mean = 100.0 + 59.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_240:
    """Statistical control profile for Diagnostic Analyzer Lot #240"""
    lot_id = "QC-LOT-2026-0240"
    instrument_model = "Cobas-8000-Series-240"
    target_mean = 100.0 + 60.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_241:
    """Statistical control profile for Diagnostic Analyzer Lot #241"""
    lot_id = "QC-LOT-2026-0241"
    instrument_model = "Cobas-8000-Series-241"
    target_mean = 100.0 + 60.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_242:
    """Statistical control profile for Diagnostic Analyzer Lot #242"""
    lot_id = "QC-LOT-2026-0242"
    instrument_model = "Cobas-8000-Series-242"
    target_mean = 100.0 + 60.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_243:
    """Statistical control profile for Diagnostic Analyzer Lot #243"""
    lot_id = "QC-LOT-2026-0243"
    instrument_model = "Cobas-8000-Series-243"
    target_mean = 100.0 + 60.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_244:
    """Statistical control profile for Diagnostic Analyzer Lot #244"""
    lot_id = "QC-LOT-2026-0244"
    instrument_model = "Cobas-8000-Series-244"
    target_mean = 100.0 + 61.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_245:
    """Statistical control profile for Diagnostic Analyzer Lot #245"""
    lot_id = "QC-LOT-2026-0245"
    instrument_model = "Cobas-8000-Series-245"
    target_mean = 100.0 + 61.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_246:
    """Statistical control profile for Diagnostic Analyzer Lot #246"""
    lot_id = "QC-LOT-2026-0246"
    instrument_model = "Cobas-8000-Series-246"
    target_mean = 100.0 + 61.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_247:
    """Statistical control profile for Diagnostic Analyzer Lot #247"""
    lot_id = "QC-LOT-2026-0247"
    instrument_model = "Cobas-8000-Series-247"
    target_mean = 100.0 + 61.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_248:
    """Statistical control profile for Diagnostic Analyzer Lot #248"""
    lot_id = "QC-LOT-2026-0248"
    instrument_model = "Cobas-8000-Series-248"
    target_mean = 100.0 + 62.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_249:
    """Statistical control profile for Diagnostic Analyzer Lot #249"""
    lot_id = "QC-LOT-2026-0249"
    instrument_model = "Cobas-8000-Series-249"
    target_mean = 100.0 + 62.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_250:
    """Statistical control profile for Diagnostic Analyzer Lot #250"""
    lot_id = "QC-LOT-2026-0250"
    instrument_model = "Cobas-8000-Series-250"
    target_mean = 100.0 + 62.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_251:
    """Statistical control profile for Diagnostic Analyzer Lot #251"""
    lot_id = "QC-LOT-2026-0251"
    instrument_model = "Cobas-8000-Series-251"
    target_mean = 100.0 + 62.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_252:
    """Statistical control profile for Diagnostic Analyzer Lot #252"""
    lot_id = "QC-LOT-2026-0252"
    instrument_model = "Cobas-8000-Series-252"
    target_mean = 100.0 + 63.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_253:
    """Statistical control profile for Diagnostic Analyzer Lot #253"""
    lot_id = "QC-LOT-2026-0253"
    instrument_model = "Cobas-8000-Series-253"
    target_mean = 100.0 + 63.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_254:
    """Statistical control profile for Diagnostic Analyzer Lot #254"""
    lot_id = "QC-LOT-2026-0254"
    instrument_model = "Cobas-8000-Series-254"
    target_mean = 100.0 + 63.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_255:
    """Statistical control profile for Diagnostic Analyzer Lot #255"""
    lot_id = "QC-LOT-2026-0255"
    instrument_model = "Cobas-8000-Series-255"
    target_mean = 100.0 + 63.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_256:
    """Statistical control profile for Diagnostic Analyzer Lot #256"""
    lot_id = "QC-LOT-2026-0256"
    instrument_model = "Cobas-8000-Series-256"
    target_mean = 100.0 + 64.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_257:
    """Statistical control profile for Diagnostic Analyzer Lot #257"""
    lot_id = "QC-LOT-2026-0257"
    instrument_model = "Cobas-8000-Series-257"
    target_mean = 100.0 + 64.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_258:
    """Statistical control profile for Diagnostic Analyzer Lot #258"""
    lot_id = "QC-LOT-2026-0258"
    instrument_model = "Cobas-8000-Series-258"
    target_mean = 100.0 + 64.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_259:
    """Statistical control profile for Diagnostic Analyzer Lot #259"""
    lot_id = "QC-LOT-2026-0259"
    instrument_model = "Cobas-8000-Series-259"
    target_mean = 100.0 + 64.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_260:
    """Statistical control profile for Diagnostic Analyzer Lot #260"""
    lot_id = "QC-LOT-2026-0260"
    instrument_model = "Cobas-8000-Series-260"
    target_mean = 100.0 + 65.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_261:
    """Statistical control profile for Diagnostic Analyzer Lot #261"""
    lot_id = "QC-LOT-2026-0261"
    instrument_model = "Cobas-8000-Series-261"
    target_mean = 100.0 + 65.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_262:
    """Statistical control profile for Diagnostic Analyzer Lot #262"""
    lot_id = "QC-LOT-2026-0262"
    instrument_model = "Cobas-8000-Series-262"
    target_mean = 100.0 + 65.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_263:
    """Statistical control profile for Diagnostic Analyzer Lot #263"""
    lot_id = "QC-LOT-2026-0263"
    instrument_model = "Cobas-8000-Series-263"
    target_mean = 100.0 + 65.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_264:
    """Statistical control profile for Diagnostic Analyzer Lot #264"""
    lot_id = "QC-LOT-2026-0264"
    instrument_model = "Cobas-8000-Series-264"
    target_mean = 100.0 + 66.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_265:
    """Statistical control profile for Diagnostic Analyzer Lot #265"""
    lot_id = "QC-LOT-2026-0265"
    instrument_model = "Cobas-8000-Series-265"
    target_mean = 100.0 + 66.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_266:
    """Statistical control profile for Diagnostic Analyzer Lot #266"""
    lot_id = "QC-LOT-2026-0266"
    instrument_model = "Cobas-8000-Series-266"
    target_mean = 100.0 + 66.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_267:
    """Statistical control profile for Diagnostic Analyzer Lot #267"""
    lot_id = "QC-LOT-2026-0267"
    instrument_model = "Cobas-8000-Series-267"
    target_mean = 100.0 + 66.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_268:
    """Statistical control profile for Diagnostic Analyzer Lot #268"""
    lot_id = "QC-LOT-2026-0268"
    instrument_model = "Cobas-8000-Series-268"
    target_mean = 100.0 + 67.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_269:
    """Statistical control profile for Diagnostic Analyzer Lot #269"""
    lot_id = "QC-LOT-2026-0269"
    instrument_model = "Cobas-8000-Series-269"
    target_mean = 100.0 + 67.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_270:
    """Statistical control profile for Diagnostic Analyzer Lot #270"""
    lot_id = "QC-LOT-2026-0270"
    instrument_model = "Cobas-8000-Series-270"
    target_mean = 100.0 + 67.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_271:
    """Statistical control profile for Diagnostic Analyzer Lot #271"""
    lot_id = "QC-LOT-2026-0271"
    instrument_model = "Cobas-8000-Series-271"
    target_mean = 100.0 + 67.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_272:
    """Statistical control profile for Diagnostic Analyzer Lot #272"""
    lot_id = "QC-LOT-2026-0272"
    instrument_model = "Cobas-8000-Series-272"
    target_mean = 100.0 + 68.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_273:
    """Statistical control profile for Diagnostic Analyzer Lot #273"""
    lot_id = "QC-LOT-2026-0273"
    instrument_model = "Cobas-8000-Series-273"
    target_mean = 100.0 + 68.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_274:
    """Statistical control profile for Diagnostic Analyzer Lot #274"""
    lot_id = "QC-LOT-2026-0274"
    instrument_model = "Cobas-8000-Series-274"
    target_mean = 100.0 + 68.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_275:
    """Statistical control profile for Diagnostic Analyzer Lot #275"""
    lot_id = "QC-LOT-2026-0275"
    instrument_model = "Cobas-8000-Series-275"
    target_mean = 100.0 + 68.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_276:
    """Statistical control profile for Diagnostic Analyzer Lot #276"""
    lot_id = "QC-LOT-2026-0276"
    instrument_model = "Cobas-8000-Series-276"
    target_mean = 100.0 + 69.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_277:
    """Statistical control profile for Diagnostic Analyzer Lot #277"""
    lot_id = "QC-LOT-2026-0277"
    instrument_model = "Cobas-8000-Series-277"
    target_mean = 100.0 + 69.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_278:
    """Statistical control profile for Diagnostic Analyzer Lot #278"""
    lot_id = "QC-LOT-2026-0278"
    instrument_model = "Cobas-8000-Series-278"
    target_mean = 100.0 + 69.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_279:
    """Statistical control profile for Diagnostic Analyzer Lot #279"""
    lot_id = "QC-LOT-2026-0279"
    instrument_model = "Cobas-8000-Series-279"
    target_mean = 100.0 + 69.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_280:
    """Statistical control profile for Diagnostic Analyzer Lot #280"""
    lot_id = "QC-LOT-2026-0280"
    instrument_model = "Cobas-8000-Series-280"
    target_mean = 100.0 + 70.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_281:
    """Statistical control profile for Diagnostic Analyzer Lot #281"""
    lot_id = "QC-LOT-2026-0281"
    instrument_model = "Cobas-8000-Series-281"
    target_mean = 100.0 + 70.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_282:
    """Statistical control profile for Diagnostic Analyzer Lot #282"""
    lot_id = "QC-LOT-2026-0282"
    instrument_model = "Cobas-8000-Series-282"
    target_mean = 100.0 + 70.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_283:
    """Statistical control profile for Diagnostic Analyzer Lot #283"""
    lot_id = "QC-LOT-2026-0283"
    instrument_model = "Cobas-8000-Series-283"
    target_mean = 100.0 + 70.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_284:
    """Statistical control profile for Diagnostic Analyzer Lot #284"""
    lot_id = "QC-LOT-2026-0284"
    instrument_model = "Cobas-8000-Series-284"
    target_mean = 100.0 + 71.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_285:
    """Statistical control profile for Diagnostic Analyzer Lot #285"""
    lot_id = "QC-LOT-2026-0285"
    instrument_model = "Cobas-8000-Series-285"
    target_mean = 100.0 + 71.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_286:
    """Statistical control profile for Diagnostic Analyzer Lot #286"""
    lot_id = "QC-LOT-2026-0286"
    instrument_model = "Cobas-8000-Series-286"
    target_mean = 100.0 + 71.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_287:
    """Statistical control profile for Diagnostic Analyzer Lot #287"""
    lot_id = "QC-LOT-2026-0287"
    instrument_model = "Cobas-8000-Series-287"
    target_mean = 100.0 + 71.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_288:
    """Statistical control profile for Diagnostic Analyzer Lot #288"""
    lot_id = "QC-LOT-2026-0288"
    instrument_model = "Cobas-8000-Series-288"
    target_mean = 100.0 + 72.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_289:
    """Statistical control profile for Diagnostic Analyzer Lot #289"""
    lot_id = "QC-LOT-2026-0289"
    instrument_model = "Cobas-8000-Series-289"
    target_mean = 100.0 + 72.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_290:
    """Statistical control profile for Diagnostic Analyzer Lot #290"""
    lot_id = "QC-LOT-2026-0290"
    instrument_model = "Cobas-8000-Series-290"
    target_mean = 100.0 + 72.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_291:
    """Statistical control profile for Diagnostic Analyzer Lot #291"""
    lot_id = "QC-LOT-2026-0291"
    instrument_model = "Cobas-8000-Series-291"
    target_mean = 100.0 + 72.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_292:
    """Statistical control profile for Diagnostic Analyzer Lot #292"""
    lot_id = "QC-LOT-2026-0292"
    instrument_model = "Cobas-8000-Series-292"
    target_mean = 100.0 + 73.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_293:
    """Statistical control profile for Diagnostic Analyzer Lot #293"""
    lot_id = "QC-LOT-2026-0293"
    instrument_model = "Cobas-8000-Series-293"
    target_mean = 100.0 + 73.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_294:
    """Statistical control profile for Diagnostic Analyzer Lot #294"""
    lot_id = "QC-LOT-2026-0294"
    instrument_model = "Cobas-8000-Series-294"
    target_mean = 100.0 + 73.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_295:
    """Statistical control profile for Diagnostic Analyzer Lot #295"""
    lot_id = "QC-LOT-2026-0295"
    instrument_model = "Cobas-8000-Series-295"
    target_mean = 100.0 + 73.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_296:
    """Statistical control profile for Diagnostic Analyzer Lot #296"""
    lot_id = "QC-LOT-2026-0296"
    instrument_model = "Cobas-8000-Series-296"
    target_mean = 100.0 + 74.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_297:
    """Statistical control profile for Diagnostic Analyzer Lot #297"""
    lot_id = "QC-LOT-2026-0297"
    instrument_model = "Cobas-8000-Series-297"
    target_mean = 100.0 + 74.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_298:
    """Statistical control profile for Diagnostic Analyzer Lot #298"""
    lot_id = "QC-LOT-2026-0298"
    instrument_model = "Cobas-8000-Series-298"
    target_mean = 100.0 + 74.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_299:
    """Statistical control profile for Diagnostic Analyzer Lot #299"""
    lot_id = "QC-LOT-2026-0299"
    instrument_model = "Cobas-8000-Series-299"
    target_mean = 100.0 + 74.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_300:
    """Statistical control profile for Diagnostic Analyzer Lot #300"""
    lot_id = "QC-LOT-2026-0300"
    instrument_model = "Cobas-8000-Series-300"
    target_mean = 100.0 + 75.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_301:
    """Statistical control profile for Diagnostic Analyzer Lot #301"""
    lot_id = "QC-LOT-2026-0301"
    instrument_model = "Cobas-8000-Series-301"
    target_mean = 100.0 + 75.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_302:
    """Statistical control profile for Diagnostic Analyzer Lot #302"""
    lot_id = "QC-LOT-2026-0302"
    instrument_model = "Cobas-8000-Series-302"
    target_mean = 100.0 + 75.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_303:
    """Statistical control profile for Diagnostic Analyzer Lot #303"""
    lot_id = "QC-LOT-2026-0303"
    instrument_model = "Cobas-8000-Series-303"
    target_mean = 100.0 + 75.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_304:
    """Statistical control profile for Diagnostic Analyzer Lot #304"""
    lot_id = "QC-LOT-2026-0304"
    instrument_model = "Cobas-8000-Series-304"
    target_mean = 100.0 + 76.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_305:
    """Statistical control profile for Diagnostic Analyzer Lot #305"""
    lot_id = "QC-LOT-2026-0305"
    instrument_model = "Cobas-8000-Series-305"
    target_mean = 100.0 + 76.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_306:
    """Statistical control profile for Diagnostic Analyzer Lot #306"""
    lot_id = "QC-LOT-2026-0306"
    instrument_model = "Cobas-8000-Series-306"
    target_mean = 100.0 + 76.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_307:
    """Statistical control profile for Diagnostic Analyzer Lot #307"""
    lot_id = "QC-LOT-2026-0307"
    instrument_model = "Cobas-8000-Series-307"
    target_mean = 100.0 + 76.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_308:
    """Statistical control profile for Diagnostic Analyzer Lot #308"""
    lot_id = "QC-LOT-2026-0308"
    instrument_model = "Cobas-8000-Series-308"
    target_mean = 100.0 + 77.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_309:
    """Statistical control profile for Diagnostic Analyzer Lot #309"""
    lot_id = "QC-LOT-2026-0309"
    instrument_model = "Cobas-8000-Series-309"
    target_mean = 100.0 + 77.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_310:
    """Statistical control profile for Diagnostic Analyzer Lot #310"""
    lot_id = "QC-LOT-2026-0310"
    instrument_model = "Cobas-8000-Series-310"
    target_mean = 100.0 + 77.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_311:
    """Statistical control profile for Diagnostic Analyzer Lot #311"""
    lot_id = "QC-LOT-2026-0311"
    instrument_model = "Cobas-8000-Series-311"
    target_mean = 100.0 + 77.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_312:
    """Statistical control profile for Diagnostic Analyzer Lot #312"""
    lot_id = "QC-LOT-2026-0312"
    instrument_model = "Cobas-8000-Series-312"
    target_mean = 100.0 + 78.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_313:
    """Statistical control profile for Diagnostic Analyzer Lot #313"""
    lot_id = "QC-LOT-2026-0313"
    instrument_model = "Cobas-8000-Series-313"
    target_mean = 100.0 + 78.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_314:
    """Statistical control profile for Diagnostic Analyzer Lot #314"""
    lot_id = "QC-LOT-2026-0314"
    instrument_model = "Cobas-8000-Series-314"
    target_mean = 100.0 + 78.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_315:
    """Statistical control profile for Diagnostic Analyzer Lot #315"""
    lot_id = "QC-LOT-2026-0315"
    instrument_model = "Cobas-8000-Series-315"
    target_mean = 100.0 + 78.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_316:
    """Statistical control profile for Diagnostic Analyzer Lot #316"""
    lot_id = "QC-LOT-2026-0316"
    instrument_model = "Cobas-8000-Series-316"
    target_mean = 100.0 + 79.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_317:
    """Statistical control profile for Diagnostic Analyzer Lot #317"""
    lot_id = "QC-LOT-2026-0317"
    instrument_model = "Cobas-8000-Series-317"
    target_mean = 100.0 + 79.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_318:
    """Statistical control profile for Diagnostic Analyzer Lot #318"""
    lot_id = "QC-LOT-2026-0318"
    instrument_model = "Cobas-8000-Series-318"
    target_mean = 100.0 + 79.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_319:
    """Statistical control profile for Diagnostic Analyzer Lot #319"""
    lot_id = "QC-LOT-2026-0319"
    instrument_model = "Cobas-8000-Series-319"
    target_mean = 100.0 + 79.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_320:
    """Statistical control profile for Diagnostic Analyzer Lot #320"""
    lot_id = "QC-LOT-2026-0320"
    instrument_model = "Cobas-8000-Series-320"
    target_mean = 100.0 + 80.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_321:
    """Statistical control profile for Diagnostic Analyzer Lot #321"""
    lot_id = "QC-LOT-2026-0321"
    instrument_model = "Cobas-8000-Series-321"
    target_mean = 100.0 + 80.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_322:
    """Statistical control profile for Diagnostic Analyzer Lot #322"""
    lot_id = "QC-LOT-2026-0322"
    instrument_model = "Cobas-8000-Series-322"
    target_mean = 100.0 + 80.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_323:
    """Statistical control profile for Diagnostic Analyzer Lot #323"""
    lot_id = "QC-LOT-2026-0323"
    instrument_model = "Cobas-8000-Series-323"
    target_mean = 100.0 + 80.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_324:
    """Statistical control profile for Diagnostic Analyzer Lot #324"""
    lot_id = "QC-LOT-2026-0324"
    instrument_model = "Cobas-8000-Series-324"
    target_mean = 100.0 + 81.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_325:
    """Statistical control profile for Diagnostic Analyzer Lot #325"""
    lot_id = "QC-LOT-2026-0325"
    instrument_model = "Cobas-8000-Series-325"
    target_mean = 100.0 + 81.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_326:
    """Statistical control profile for Diagnostic Analyzer Lot #326"""
    lot_id = "QC-LOT-2026-0326"
    instrument_model = "Cobas-8000-Series-326"
    target_mean = 100.0 + 81.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_327:
    """Statistical control profile for Diagnostic Analyzer Lot #327"""
    lot_id = "QC-LOT-2026-0327"
    instrument_model = "Cobas-8000-Series-327"
    target_mean = 100.0 + 81.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_328:
    """Statistical control profile for Diagnostic Analyzer Lot #328"""
    lot_id = "QC-LOT-2026-0328"
    instrument_model = "Cobas-8000-Series-328"
    target_mean = 100.0 + 82.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_329:
    """Statistical control profile for Diagnostic Analyzer Lot #329"""
    lot_id = "QC-LOT-2026-0329"
    instrument_model = "Cobas-8000-Series-329"
    target_mean = 100.0 + 82.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_330:
    """Statistical control profile for Diagnostic Analyzer Lot #330"""
    lot_id = "QC-LOT-2026-0330"
    instrument_model = "Cobas-8000-Series-330"
    target_mean = 100.0 + 82.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_331:
    """Statistical control profile for Diagnostic Analyzer Lot #331"""
    lot_id = "QC-LOT-2026-0331"
    instrument_model = "Cobas-8000-Series-331"
    target_mean = 100.0 + 82.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_332:
    """Statistical control profile for Diagnostic Analyzer Lot #332"""
    lot_id = "QC-LOT-2026-0332"
    instrument_model = "Cobas-8000-Series-332"
    target_mean = 100.0 + 83.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_333:
    """Statistical control profile for Diagnostic Analyzer Lot #333"""
    lot_id = "QC-LOT-2026-0333"
    instrument_model = "Cobas-8000-Series-333"
    target_mean = 100.0 + 83.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_334:
    """Statistical control profile for Diagnostic Analyzer Lot #334"""
    lot_id = "QC-LOT-2026-0334"
    instrument_model = "Cobas-8000-Series-334"
    target_mean = 100.0 + 83.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_335:
    """Statistical control profile for Diagnostic Analyzer Lot #335"""
    lot_id = "QC-LOT-2026-0335"
    instrument_model = "Cobas-8000-Series-335"
    target_mean = 100.0 + 83.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_336:
    """Statistical control profile for Diagnostic Analyzer Lot #336"""
    lot_id = "QC-LOT-2026-0336"
    instrument_model = "Cobas-8000-Series-336"
    target_mean = 100.0 + 84.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_337:
    """Statistical control profile for Diagnostic Analyzer Lot #337"""
    lot_id = "QC-LOT-2026-0337"
    instrument_model = "Cobas-8000-Series-337"
    target_mean = 100.0 + 84.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_338:
    """Statistical control profile for Diagnostic Analyzer Lot #338"""
    lot_id = "QC-LOT-2026-0338"
    instrument_model = "Cobas-8000-Series-338"
    target_mean = 100.0 + 84.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_339:
    """Statistical control profile for Diagnostic Analyzer Lot #339"""
    lot_id = "QC-LOT-2026-0339"
    instrument_model = "Cobas-8000-Series-339"
    target_mean = 100.0 + 84.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_340:
    """Statistical control profile for Diagnostic Analyzer Lot #340"""
    lot_id = "QC-LOT-2026-0340"
    instrument_model = "Cobas-8000-Series-340"
    target_mean = 100.0 + 85.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_341:
    """Statistical control profile for Diagnostic Analyzer Lot #341"""
    lot_id = "QC-LOT-2026-0341"
    instrument_model = "Cobas-8000-Series-341"
    target_mean = 100.0 + 85.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_342:
    """Statistical control profile for Diagnostic Analyzer Lot #342"""
    lot_id = "QC-LOT-2026-0342"
    instrument_model = "Cobas-8000-Series-342"
    target_mean = 100.0 + 85.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_343:
    """Statistical control profile for Diagnostic Analyzer Lot #343"""
    lot_id = "QC-LOT-2026-0343"
    instrument_model = "Cobas-8000-Series-343"
    target_mean = 100.0 + 85.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_344:
    """Statistical control profile for Diagnostic Analyzer Lot #344"""
    lot_id = "QC-LOT-2026-0344"
    instrument_model = "Cobas-8000-Series-344"
    target_mean = 100.0 + 86.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_345:
    """Statistical control profile for Diagnostic Analyzer Lot #345"""
    lot_id = "QC-LOT-2026-0345"
    instrument_model = "Cobas-8000-Series-345"
    target_mean = 100.0 + 86.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_346:
    """Statistical control profile for Diagnostic Analyzer Lot #346"""
    lot_id = "QC-LOT-2026-0346"
    instrument_model = "Cobas-8000-Series-346"
    target_mean = 100.0 + 86.5
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_347:
    """Statistical control profile for Diagnostic Analyzer Lot #347"""
    lot_id = "QC-LOT-2026-0347"
    instrument_model = "Cobas-8000-Series-347"
    target_mean = 100.0 + 86.75
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_348:
    """Statistical control profile for Diagnostic Analyzer Lot #348"""
    lot_id = "QC-LOT-2026-0348"
    instrument_model = "Cobas-8000-Series-348"
    target_mean = 100.0 + 87.0
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected

class QualityControlLotProfile_349:
    """Statistical control profile for Diagnostic Analyzer Lot #349"""
    lot_id = "QC-LOT-2026-0349"
    instrument_model = "Cobas-8000-Series-349"
    target_mean = 100.0 + 87.25
    target_sd = 2.15
    target_cv_percent = 2.15
    @classmethod
    def calculate_levey_jennings_points(cls, n_points: int = 30) -> List[float]:
        return [cls.target_mean + math.sin(i * 0.35) * cls.target_sd for i in range(n_points)]
    @classmethod
    def is_in_control(cls, values: List[float]) -> bool:
        sample = QcControlSample(cls.lot_id, "Level 1", cls.target_mean, cls.target_sd, values)
        return not WestgardMultiruleEvaluator.evaluate_run(sample).is_run_rejected
