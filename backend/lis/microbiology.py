"""
Microbiology Culture Identification and Antimicrobial Susceptibility Testing (AST).
Encodes CLSI M100 Minimum Inhibitory Concentration (MIC) interpretations (S, I, R).
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AntibioticSusceptibility:
    antibiotic_name: str
    mic_value: str
    interpretation: str  # S = Susceptible, I = Intermediate, R = Resistant

@dataclass
class CultureIsolate:
    isolate_number: int
    organism_name: str
    colony_count: str
    susceptibilities: List[AntibioticSusceptibility]

class MicrobiologyEngine:
    @staticmethod
    def interpret_ampicillin_ecoli(mic_ug_ml: float) -> str:
        if mic_ug_ml <= 8.0:
            return "S"
        elif mic_ug_ml == 16.0:
            return "I"
        return "R"
