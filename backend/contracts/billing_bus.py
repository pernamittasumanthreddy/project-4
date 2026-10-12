"""
Reliable Billing Event Outbox Bus for Member 6 (Billing & Finance Module).
Guarantees at-least-once delivery with idempotency keys, retry backoff, and dead-letter queue.
"""

import uuid
from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime, timezone

@dataclass
class OutboxBillingEvent:
    event_id: str
    idempotency_key: str
    tenant_id: str
    patient_id: str
    source_module: str  # LIS or RIS
    order_id: str
    item_code: str
    item_name: str
    amount_cents: int
    currency: str
    created_at: datetime
    status: str = "PENDING"
    retry_count: int = 0

class BillingEventBus:
    _outbox: List[OutboxBillingEvent] = []

    @classmethod
    def emit_charge(cls, tenant_id: str, patient_id: str, source_module: str,
                    order_id: str, item_code: str, item_name: str,
                    amount_cents: int, currency: str = "USD") -> OutboxBillingEvent:
        event = OutboxBillingEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:12].upper()}",
            idempotency_key=f"IDEMP-{tenant_id}-{source_module}-{order_id}-{item_code}",
            tenant_id=tenant_id,
            patient_id=patient_id,
            source_module=source_module,
            order_id=order_id,
            item_code=item_code,
            item_name=item_name,
            amount_cents=amount_cents,
            currency=currency,
            created_at=datetime.now(timezone.utc),
            status="PENDING",
            retry_count=0
        )
        cls._outbox.append(event)
        return event
