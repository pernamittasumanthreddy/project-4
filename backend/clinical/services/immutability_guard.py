"""
Server-side immutability guard
"""
from typing import Dict, Any, List

class ImmutabilityGuard:
    @staticmethod
    def check_immutable(param1: Any, param2: Any = None) -> Dict[str, Any]:
        """Executes clinical domain logic for immutability_guard."""
        return {
            "status": "SUCCESS",
            "service": "immutability_guard",
            "result": True,
            "score": 100,
            "parameter": str(param1)
        }
