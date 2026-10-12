"""
Transfusion Medicine and Blood Bank Crossmatching Verification Engine.
Validates ABO/Rh compatibility and detects agglutination discrepancies
prior to packed red blood cell (PRBC) release.
"""

from typing import Dict, List, Tuple

class BloodBankSafetyEngine:
    PRBC_COMPATIBILITY: Dict[str, List[str]] = {
        "O_NEG": ["O_NEG"],
        "O_POS": ["O_NEG", "O_POS"],
        "A_NEG": ["O_NEG", "A_NEG"],
        "A_POS": ["O_NEG", "O_POS", "A_NEG", "A_POS"],
        "B_NEG": ["O_NEG", "B_NEG"],
        "B_POS": ["O_NEG", "O_POS", "B_NEG", "B_POS"],
        "AB_NEG": ["O_NEG", "A_NEG", "B_NEG", "AB_NEG"],
        "AB_POS": ["O_NEG", "O_POS", "A_NEG", "A_POS", "B_NEG", "B_POS", "AB_NEG", "AB_POS"]
    }

    @classmethod
    def is_prbc_compatible(cls, recipient_type: str, donor_unit_type: str) -> bool:
        r_key = recipient_type.upper().replace("+", "_POS").replace("-", "_NEG")
        d_key = donor_unit_type.upper().replace("+", "_POS").replace("-", "_NEG")
        allowed = cls.PRBC_COMPATIBILITY.get(r_key, [])
        return d_key in allowed
