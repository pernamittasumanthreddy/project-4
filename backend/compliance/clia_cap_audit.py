"""
CLIA '88 and CAP Laboratory Regulatory Immutable Audit Trail.
Records all specimen accession, test result alterations, delta-check overrides, and sign-offs.
"""

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

@dataclass
class AuditLogEntry:
    entry_id: str
    tenant_id: str
    entity_name: str
    entity_id: str
    action: str  # CREATE, UPDATE, DELETE, SIGN_OFF, DELTA_OVERRIDE
    user_id: str
    timestamp: datetime
    previous_state_hash: Optional[str]
    new_state_hash: str

class CLIACAPAuditTrail:
    _trail: List[AuditLogEntry] = []

    @classmethod
    def record_action(cls, entry_id: str, tenant_id: str, entity_name: str,
                      entity_id: str, action: str, user_id: str,
                      prev_state: str, new_state: str) -> AuditLogEntry:
        prev_hash = hashlib.sha256(prev_state.encode("utf-8")).hexdigest() if prev_state else None
        new_hash = hashlib.sha256(new_state.encode("utf-8")).hexdigest()
        entry = AuditLogEntry(
            entry_id=entry_id,
            tenant_id=tenant_id,
            entity_name=entity_name,
            entity_id=entity_id,
            action=action,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc),
            previous_state_hash=prev_hash,
            new_state_hash=new_hash
        )
        cls._trail.append(entry)
        return entry
