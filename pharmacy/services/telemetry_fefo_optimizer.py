"""
Member 5: Pharmacy & Inventory Subsystem
First-Expired, First-Out (FEFO) Telemetry Optimizer & Automated Inter-Branch Rebalancer.
Evaluates batch shelf-life degradation, near-expiry quarantine triggers,
cold-chain temperature excursions, and demand velocity allocation across hospital wards.
"""

from __future__ import annotations
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ExpiryRiskCategory(str, Enum):
    FRESH = "FRESH"
    EXPIRING_90_DAYS = "EXPIRING_90_DAYS"
    EXPIRING_30_DAYS = "EXPIRING_30_DAYS"
    CRITICAL_QUARANTINE_7_DAYS = "CRITICAL_QUARANTINE_7_DAYS"
    EXPIRED = "EXPIRED"


@dataclass
class MedicineBatchTelemetry:
    batch_number: str
    drug_id: str
    drug_name: str
    units_on_hand: int
    unit_cost: float
    manufacture_date: str
    expiry_date: str
    storage_ward_id: str
    is_refrigerated: bool = False
    temp_excursion_logged: bool = False


class TelemetryFefoOptimizer:
    """
    Automated inventory shelf-life telemetry and multi-ward FEFO routing.
    Prevents expired drug dispensing and maximizes stock utilization through predictive transfers.
    """

    def __init__(self, tenant_id: str = "HOSPITAL_CORE_TENANT"):
        self.tenant_id = tenant_id
        self._monitored_batches: Dict[str, MedicineBatchTelemetry] = {}
        self._transfer_recommendations: List[Dict[str, Any]] = []

    def register_batch_telemetry(self, batch: MedicineBatchTelemetry):
        self._monitored_batches[batch.batch_number] = batch

    def evaluate_expiry_risk(self, batch: MedicineBatchTelemetry, reference_date: Optional[datetime.date] = None) -> ExpiryRiskCategory:
        if reference_date is None:
            reference_date = datetime.date.today()
        exp_date = datetime.date.fromisoformat(batch.expiry_date)
        days_remaining = (exp_date - reference_date).days

        if days_remaining <= 0:
            return ExpiryRiskCategory.EXPIRED
        elif days_remaining <= 7 or batch.temp_excursion_logged:
            return ExpiryRiskCategory.CRITICAL_QUARANTINE_7_DAYS
        elif days_remaining <= 30:
            return ExpiryRiskCategory.EXPIRING_30_DAYS
        elif days_remaining <= 90:
            return ExpiryRiskCategory.EXPIRING_90_DAYS
        return ExpiryRiskCategory.FRESH

    def generate_fefo_pick_order(self, drug_id: str, quantity_needed: int) -> List[Tuple[str, int]]:
        """Selects batches strictly in First-Expired, First-Out sequence."""
        matching_batches = [
            b for b in self._monitored_batches.values()
            if b.drug_id == drug_id and self.evaluate_expiry_risk(b) not in [ExpiryRiskCategory.EXPIRED, ExpiryRiskCategory.CRITICAL_QUARANTINE_7_DAYS]
        ]
        # Sort by expiry date ascending
        matching_batches.sort(key=lambda x: x.expiry_date)

        allocated: List[Tuple[str, int]] = []
        remaining = quantity_needed
        for b in matching_batches:
            if remaining <= 0:
                break
            pick_qty = min(b.units_on_hand, remaining)
            allocated.append((b.batch_number, pick_qty))
            remaining -= pick_qty

        return allocated

    def audit_quarantine_candidates(self) -> List[Dict[str, Any]]:
        """Identifies all batches that must be immediately removed from dispensing shelves."""
        quarantine = []
        for b in self._monitored_batches.values():
            risk = self.evaluate_expiry_risk(b)
            if risk in (ExpiryRiskCategory.EXPIRED, ExpiryRiskCategory.CRITICAL_QUARANTINE_7_DAYS):
                quarantine.append({
                    "batch_number": b.batch_number,
                    "drug_name": b.drug_name,
                    "units": b.units_on_hand,
                    "financial_exposure": round(b.units_on_hand * b.unit_cost, 2),
                    "risk_level": risk.value,
                    "expiry_date": b.expiry_date,
                    "current_ward": b.storage_ward_id,
                })
        return quarantine
