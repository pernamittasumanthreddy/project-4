"""
Automated Reflex Testing Rule Engine for Member 4 Laboratory.
Evaluates primary diagnostic parameters and cascades automated secondary test orders
(e.g., Abnormal TSH -> Free T4, Reactive HCV Ab -> HCV RNA PCR).
"""

from dataclasses import dataclass
from typing import List, Optional, Callable, Dict

@dataclass
class ReflexTrigger:
    trigger_code: str
    trigger_test_name: str
    target_reflex_test_code: str
    target_reflex_test_name: str
    condition_description: str

class ReflexRuleEngine:
    RULES: List[ReflexTrigger] = [
        ReflexTrigger("TSH", "Thyroid Stimulating Hormone", "FT4", "Free Thyroxine (FT4)", "TSH < 0.45 or > 4.50 uIU/mL"),
        ReflexTrigger("HCV_AB", "Hepatitis C Antibody", "HCV_RNA", "HCV RNA Quantitative PCR", "HCV Ab Index >= 1.0 (Reactive)"),
        ReflexTrigger("UA_LEUK", "Urinalysis Leukocyte Esterase", "URINE_CULT", "Urine Bacterial Culture & Sensitivity", "Leukocyte Esterase Positive"),
        ReflexTrigger("ANA_SCREEN", "ANA Screen IFA", "ANA_TITER", "ANA Comprehensive Titer and Pattern", "ANA IFA Positive"),
        ReflexTrigger("TOTAL_BILI", "Total Bilirubin", "DIRECT_BILI", "Direct / Conjugated Bilirubin", "Total Bili > 1.2 mg/dL")
    ]

    @staticmethod
    def check_reflex_needed(test_code: str, value: float) -> Optional[ReflexTrigger]:
        code = test_code.upper()
        if code == "TSH" and (value < 0.45 or value > 4.50):
            return ReflexRuleEngine.RULES[0]
        elif code == "TOTAL_BILI" and value > 1.2:
            return ReflexRuleEngine.RULES[4]
        return None
