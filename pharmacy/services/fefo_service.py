"""HMS Pharmacy FEFO Service — Member 5
Implements First Expiry, First Out (FEFO) batch allocation algorithm.
Enforces non-negotiable rules:
- Excludes expired, quarantined, and recalled stock.
- Prevents negative stock.
- Greedily allocates earliest-expiring eligible batches.
"""

from datetime import date
from decimal import Decimal
from typing import List, Dict, Any
from django.core.exceptions import ValidationError
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.catalogue import Medicine


class InsufficientStockError(ValidationError):
    """Raised when available eligible stock is insufficient for dispensing."""
    pass


class ExpiredStockError(ValidationError):
    """Raised when an attempt is made to allocate an expired batch."""
    pass


class FEFOService:
    """Manages batch allocation using FEFO (First Expiry, First Out) rules."""

    @classmethod
    def get_eligible_batches(cls, medicine: Medicine, branch=None) -> List[MedicineBatch]:
        """Queries active, non-expired batches sorted by earliest expiry date."""
        today = date.today()
        queryset = MedicineBatch.objects.filter(
            medicine=medicine,
            status=BatchStatus.ACTIVE,
            available_quantity__gt=Decimal('0.00'),
            expiry_date__gt=today
        ).order_by('expiry_date', 'created_at')

        if branch:
            queryset = queryset.filter(branch=branch)

        return list(queryset)

    @classmethod
    def allocate_batches(
        cls,
        medicine: Medicine,
        required_quantity: Decimal,
        branch=None,
        preferred_batch_id=None
    ) -> List[Dict[str, Any]]:
        """Allocates batches to fulfill required quantity using FEFO.
        Returns:
            List of dicts: [{'batch': MedicineBatch, 'allocated_quantity': Decimal, 'unit_price': Decimal}]
        """
        required_qty = Decimal(str(required_quantity))
        if required_qty <= Decimal('0.00'):
            raise ValidationError("Required quantity must be greater than zero.")

        today = date.today()

        # If an authorized staff member explicitly requested a specific eligible batch
        if preferred_batch_id:
            batch = MedicineBatch.objects.filter(id=preferred_batch_id).first()
            if not batch:
                raise ValidationError("Requested batch does not exist.")
            if batch.is_expired or batch.status != BatchStatus.ACTIVE:
                raise ExpiredStockError(f"Batch {batch.batch_number} is expired or inactive and cannot be dispensed.")
            if batch.available_quantity < required_qty:
                raise InsufficientStockError(
                    f"Requested batch {batch.batch_number} has only {batch.available_quantity} available, but {required_qty} requested."
                )
            return [{
                'batch': batch,
                'allocated_quantity': required_qty,
                'unit_price': batch.selling_price
            }]

        # Standard FEFO Allocation Strategy
        eligible_batches = cls.get_eligible_batches(medicine, branch=branch)
        total_available = sum(b.available_quantity for b in eligible_batches)

        if total_available < required_qty:
            raise InsufficientStockError(
                f"Insufficient eligible stock for '{medicine.brand_name}'. "
                f"Required: {required_qty}, Total Available (Non-expired): {total_available}"
            )

        allocations: List[Dict[str, Any]] = []
        remaining = required_qty

        for batch in eligible_batches:
            if remaining <= Decimal('0.00'):
                break

            take_qty = min(batch.available_quantity, remaining)
            allocations.append({
                'batch': batch,
                'allocated_quantity': take_qty,
                'unit_price': batch.selling_price
            })
            remaining -= take_qty

        if remaining > Decimal('0.00'):
            raise InsufficientStockError(f"Could not completely fulfill {required_qty} units.")

        return allocations
