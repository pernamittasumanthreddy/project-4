"""HMS Pharmacy Stock Service — Member 5
Provides atomic, concurrency-safe inventory mutations with row-level locks and ledger updates.
"""

import uuid
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.ledger import StockMovement, MovementType
from accounts.models import User


class StockService:
    """Manages transactional stock mutations and ledger entries."""

    @classmethod
    @transaction.atomic
    def deduct_stock(
        cls,
        batch_id: uuid.UUID,
        quantity: Decimal,
        movement_type: MovementType,
        reference_type: str,
        reference_id: str,
        actor: User,
        reason: str = "",
        idempotency_key: str = None
    ) -> StockMovement:
        """Atomically deducts quantity from a stock batch using row-level locking."""
        qty = Decimal(str(quantity))
        if qty <= Decimal('0.00'):
            raise ValidationError("Deduction quantity must be positive.")

        # Idempotency check: prevent duplicate stock deduction on retried requests
        if idempotency_key:
            existing = StockMovement.objects.filter(
                tenant=actor.tenant,
                idempotency_key=idempotency_key
            ).first()
            if existing:
                return existing

        # Acquire pessimistic row-level lock on the batch
        batch = MedicineBatch.objects.select_for_update().get(id=batch_id)

        if batch.available_quantity < qty:
            raise ValidationError(
                f"Insufficient stock in Batch {batch.batch_number}. Available: {batch.available_quantity}, Requested: {qty}"
            )

        qty_before = batch.available_quantity
        qty_after = qty_before - qty

        batch.available_quantity = qty_after
        batch.check_and_update_status()
        batch.save(update_fields=['available_quantity', 'status', 'updated_at'])

        # Record immutable ledger entry
        movement = StockMovement.objects.create(
            tenant=batch.tenant,
            branch=batch.branch,
            medicine=batch.medicine,
            batch=batch,
            movement_type=movement_type,
            quantity_change=-qty,
            quantity_before=qty_before,
            quantity_after=qty_after,
            unit_cost=batch.purchase_cost,
            total_cost=qty * batch.purchase_cost,
            reference_type=reference_type,
            reference_id=str(reference_id),
            actor=actor,
            reason=reason,
            idempotency_key=idempotency_key
        )

        return movement

    @classmethod
    @transaction.atomic
    def add_stock(
        cls,
        batch_id: uuid.UUID,
        quantity: Decimal,
        movement_type: MovementType,
        reference_type: str,
        reference_id: str,
        actor: User,
        reason: str = "",
        idempotency_key: str = None
    ) -> StockMovement:
        """Atomically increases stock quantity in a batch (e.g. goods receipt, approved adjustment)."""
        qty = Decimal(str(quantity))
        if qty <= Decimal('0.00'):
            raise ValidationError("Addition quantity must be positive.")

        if idempotency_key:
            existing = StockMovement.objects.filter(
                tenant=actor.tenant,
                idempotency_key=idempotency_key
            ).first()
            if existing:
                return existing

        batch = MedicineBatch.objects.select_for_update().get(id=batch_id)

        qty_before = batch.available_quantity
        qty_after = qty_before + qty

        batch.available_quantity = qty_after
        batch.check_and_update_status()
        batch.save(update_fields=['available_quantity', 'status', 'updated_at'])

        movement = StockMovement.objects.create(
            tenant=batch.tenant,
            branch=batch.branch,
            medicine=batch.medicine,
            batch=batch,
            movement_type=movement_type,
            quantity_change=qty,
            quantity_before=qty_before,
            quantity_after=qty_after,
            unit_cost=batch.purchase_cost,
            total_cost=qty * batch.purchase_cost,
            reference_type=reference_type,
            reference_id=str(reference_id),
            actor=actor,
            reason=reason,
            idempotency_key=idempotency_key
        )

        return movement
