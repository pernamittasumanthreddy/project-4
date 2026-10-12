"""HMS Pharmacy Reconciliation Service — Member 5
Implements physical stock count sessions, variance calculations, and adjustment authorizations.
"""

from decimal import Decimal
from datetime import date
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone as dj_timezone

from pharmacy.models.reconciliation import (
    StockCountSession,
    StockCountItem,
    CountSessionStatus,
)
from pharmacy.models.inventory import MedicineBatch, StorageLocation
from pharmacy.models.ledger import MovementType
from pharmacy.services.stock_service import StockService
from accounts.models import User
from core.permissions import record_audit_event


class ReconciliationService:
    """Manages physical stock counting sessions and compensating stock adjustments."""

    @classmethod
    def start_session(
        cls,
        branch,
        location: StorageLocation = None,
        initiated_by: User = None
    ) -> StockCountSession:
        """Starts a physical counting session and snapshots current balances."""
        count = StockCountSession.objects.filter(tenant=branch.tenant).count() + 1
        session_number = f"AUD-{branch.code}-{date.today().year}-{count:04d}"

        session = StockCountSession.objects.create(
            tenant=branch.tenant,
            branch=branch,
            session_number=session_number,
            storage_location=location,
            status=CountSessionStatus.IN_PROGRESS,
            initiated_by=initiated_by
        )

        # Snapshot current active batches in this branch/location
        batches_query = MedicineBatch.objects.filter(
            branch=branch,
            status='ACTIVE'
        )
        if location:
            batches_query = batches_query.filter(storage_location=location)

        for batch in batches_query:
            StockCountItem.objects.create(
                session=session,
                batch=batch,
                expected_quantity=batch.available_quantity,
                counted_quantity=batch.available_quantity,  # default to expected until counted
                unit_cost=batch.purchase_cost
            )

        session.recalculate_variance()
        return session

    @classmethod
    def update_item_count(
        cls,
        item: StockCountItem,
        physical_count: Decimal,
        reason: str = ""
    ) -> StockCountItem:
        """Records the physically verified count for a line item."""
        if item.session.status != CountSessionStatus.IN_PROGRESS:
            raise ValidationError("Can only update counts while session is IN_PROGRESS.")

        item.counted_quantity = Decimal(str(physical_count))
        item.discrepancy_reason = reason
        item.save()

        item.session.recalculate_variance()
        return item

    @classmethod
    def submit_session_for_review(cls, session: StockCountSession, actor: User) -> StockCountSession:
        """Transitions session IN_PROGRESS -> SUBMITTED."""
        if session.status != CountSessionStatus.IN_PROGRESS:
            raise ValidationError(f"Cannot submit session with status '{session.status}'. Must be IN_PROGRESS.")

        session.status = CountSessionStatus.SUBMITTED
        session.save(update_fields=['status', 'updated_at'])
        return session

    @classmethod
    @transaction.atomic
    def approve_session_and_post_adjustments(
        cls,
        session: StockCountSession,
        approver: User
    ) -> StockCountSession:
        """Approves the stock count audit and posts compensating ledger movements."""
        if session.status != CountSessionStatus.SUBMITTED:
            raise ValidationError(
                f"Cannot approve session with status '{session.status}'. Must be SUBMITTED."
            )

        for item in session.items.all():
            diff = item.discrepancy_quantity
            if diff == Decimal('0.00'):
                continue

            batch = item.batch
            if diff > Decimal('0.00'):
                # Physical surplus: add stock
                StockService.add_stock(
                    batch_id=batch.id,
                    quantity=diff,
                    movement_type=MovementType.STOCK_ADJUSTMENT,
                    reference_type="StockCountSession",
                    reference_id=str(session.id),
                    actor=approver,
                    reason=f"Audit #{session.session_number} surplus adjustment: {item.discrepancy_reason or 'Stock count count'}"
                )
            else:
                # Physical shortage / deficit: deduct stock
                deficit = abs(diff)
                StockService.deduct_stock(
                    batch_id=batch.id,
                    quantity=deficit,
                    movement_type=MovementType.STOCK_ADJUSTMENT,
                    reference_type="StockCountSession",
                    reference_id=str(session.id),
                    actor=approver,
                    reason=f"Audit #{session.session_number} shortage deduction: {item.discrepancy_reason or 'Stock count count'}"
                )

        session.status = CountSessionStatus.APPROVED
        session.approved_by = approver
        session.approved_at = dj_timezone.now()
        session.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])

        record_audit_event(
            tenant=session.tenant,
            branch=session.branch,
            actor=approver,
            event_type='STOCK_RECONCILIATION_APPROVED',
            resource_type='stock_count_session',
            resource_id=session.id,
            details={'session_number': session.session_number, 'variance': str(session.total_discrepancy_value)}
        )

        return session
