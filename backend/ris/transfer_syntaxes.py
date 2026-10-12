"""
DICOM Part 5 Transfer Syntax UID Catalog.
"""
from typing import Dict

TRANSFER_SYNTAX_MAP: Dict[str, str] = {
    "1.2.840.10008.1.2": "Implicit VR Little Endian",
    "1.2.840.10008.1.2.1": "Explicit VR Little Endian",
    "1.2.840.10008.1.2.2": "Explicit VR Big Endian",
    "1.2.840.10008.1.2.4.50": "JPEG Baseline (Process 1)",
    "1.2.840.10008.1.2.4.70": "JPEG Lossless (Process 14)"
}

def lookup_transfer_syntax(uid: str) -> str:
    return TRANSFER_SYNTAX_MAP.get(uid, "Unknown Transfer Syntax")
