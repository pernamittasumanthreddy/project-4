"""
HL7 v2.5.1 Message Header (MSH) Parser and Acknowledgment (ACK) Router.
Extracts Sending/Receiving applications and generates RFC-compliant MSA-AA acknowledgments.
"""

from typing import Dict, Any
from datetime import datetime, timezone

class HL7MessageRouter:
    @staticmethod
    def generate_ack(original_msh_control_id: str, sending_app: str = "HMS_LIS_RIS",
                     ack_code: str = "AA", text_message: str = "Message accepted successfully") -> str:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        msh = f"MSH|^~\\&|{sending_app}|MEMBER4|EHR_CORE|TEAM_HMS|{ts}||ACK|ACK_{original_msh_control_id}|P|2.5.1"
        msa = f"MSA|{ack_code}|{original_msh_control_id}|{text_message}"
        return f"{msh}\r{msa}\r"
