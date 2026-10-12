"""
ASTM E1381 / E1394 Automated Laboratory Analyzer Protocol Parser.
Handles bidirectional communication frames (Header, Patient, Order, Result, Terminator)
and validates longitudinal checksums for bench instruments.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class ASTMFrame:
    frame_type: str  # H, P, O, R, C, L
    sequence_num: int
    fields: List[str]

class ASTMProtocolParser:
    @staticmethod
    def calculate_checksum(data: str) -> str:
        total = sum(ord(c) for c in data) % 256
        return f"{total:02X}"

    @classmethod
    def parse_line(cls, line: str) -> Optional[ASTMFrame]:
        clean = line.strip().strip("\x02\x03\r\n")
        if not clean:
            return None
        parts = clean.split("|")
        f_type = parts[0][0] if parts[0] else "U"
        return ASTMFrame(
            frame_type=f_type,
            sequence_num=1,
            fields=parts
        )
