"""
Master Patient Index (MPI) Identity Reconciliation Adapter for Member 2.
Implements deterministic MRN matching and fuzzy demographic matching.
"""

from typing import Dict, Any, Optional

class PatientIdentityMatcher:
    @staticmethod
    def match_patient(incoming_mrn: str, incoming_name: str, incoming_dob: str,
                      master_registry: Dict[str, Dict[str, Any]]) -> Optional[str]:
        # Exact MRN match
        for pid, record in master_registry.items():
            if record.get("mrn") == incoming_mrn:
                return pid
        # Demographic fallback
        clean_name = incoming_name.strip().upper()
        for pid, record in master_registry.items():
            if record.get("full_name", "").upper() == clean_name and record.get("dob") == incoming_dob:
                return pid
        return None
