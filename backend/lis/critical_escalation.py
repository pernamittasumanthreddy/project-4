"""
Critical Panic Value Escalation Protocol for Member 4 Laboratory.
Enforces CLIA/CAP guidelines requiring immediate notification of ordering physicians
with telephone contact logs, read-back verification timestamps, and hierarchical escalation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

@dataclass
class CallLogEntry:
    timestamp: datetime
    caller_technologist_id: str
    recipient_name: str
    recipient_role: str
    contact_number: str
    read_back_confirmed: bool
    notes: str

@dataclass
class CriticalAlertNotification:
    alert_id: str
    tenant_id: str
    patient_id: str
    patient_name: str
    test_name: str
    critical_value: str
    reference_range: str
    detected_at: datetime
    ordering_physician_id: str
    status: str = "PENDING"  # PENDING, NOTIFIED, ESCALATED, ACKNOWLEDGED
    escalation_level: int = 1
    call_logs: List[CallLogEntry] = field(default_factory=list)

class CriticalAlertEscalationEngine:
    ESCALATION_TIMEOUTS_MINUTES = {
        1: 15,  # Level 1: Primary Ordering Clinician within 15 min
        2: 30,  # Level 2: Ward Charge Nurse / Senior Registrar within 30 min
        3: 60   # Level 3: Medical Director / CMO escalation
    }

    def record_call_log(self, alert: CriticalAlertNotification, caller_id: str,
                        recipient_name: str, recipient_role: str,
                        contact_number: str, read_back_confirmed: bool, notes: str) -> None:
        entry = CallLogEntry(
            timestamp=datetime.now(timezone.utc),
            caller_technologist_id=caller_id,
            recipient_name=recipient_name,
            recipient_role=recipient_role,
            contact_number=contact_number,
            read_back_confirmed=read_back_confirmed,
            notes=notes
        )
        alert.call_logs.append(entry)
        if read_back_confirmed:
            alert.status = "ACKNOWLEDGED"

    def check_escalation_status(self, alert: CriticalAlertNotification, current_time: Optional[datetime] = None) -> bool:
        if alert.status == "ACKNOWLEDGED":
            return False
        now = current_time or datetime.now(timezone.utc)
        elapsed_min = (now - alert.detected_at).total_seconds() / 60.0
        
        timeout = self.ESCALATION_TIMEOUTS_MINUTES.get(alert.escalation_level, 60)
        if elapsed_min > timeout and alert.escalation_level < 3:
            alert.escalation_level += 1
            alert.status = "ESCALATED"
            return True
        return False
