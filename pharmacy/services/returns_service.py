"""HMS Pharmacy Returns & Quarantine Service — Member 5
Implements patient returns, quarantine routing, and supplier returns.
"""

from decimal import Decimal
from datetime import date
from django.db import transaction, models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils import timezone as dj_timezone

from pharmacy.models.dispensing import DispenseRecord, DispensedItem
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.supplier import Supplier
from pharmacy.models.returns import (
    PatientReturn,
    SupplierReturn,
    StockQuarantine,
    ReturnCondition,
    QuarantineResolution,
)
from pharmacy.models.ledger import MovementType
from pharmacy.services.stock_service import StockService
from accounts.models import User
from core.permissions import record_audit_event


class ReturnsService:
    """Manages patient returns into quarantine, supplier return deductions, and quarantine resolution."""

    @classmethod
    @transaction.atomic
    def process_patient_return(
        cls,
        dispense_record: DispenseRecord,
        dispensed_item_id: str,
        quantity_returned: Decimal,
        condition: ReturnCondition,
        reason: str,
        received_by: User
    ) -> PatientReturn:
        """Processes patient medication return into inspection quarantine."""
        qty = Decimal(str(quantity_returned))
        if qty <= Decimal('0.00'):
            raise ValidationError("Return quantity must be greater than zero.")

        item = DispensedItem.objects.select_for_update().get(id=dispensed_item_id, dispense_record=dispense_record)

        # Check previously returned quantity for this dispensed line item
        prior_returns = PatientReturn.objects.filter(
            dispense_record=dispense_record,
            medicine=item.medicine,
            batch=item.batch
        ).aggregate(total=models.Sum('quantity_returned'))['total'] or Decimal('0.00')

        if (prior_returns + qty) > item.quantity_dispensed:
            raise ValidationError(
                f"Cannot return {qty} units. Originally dispensed: {item.quantity_dispensed}, "
                f"already returned: {prior_returns}."
            )

        count = PatientReturn.objects.filter(tenant=dispense_record.tenant).count() + 1
        return_number = f"RET-{dispense_record.branch.code if dispense_record.branch else 'HQ'}-{date.today().year}-{count:04d}"

        # Route returned medication into quarantine (never directly into active stock!)
        quarantine = StockQuarantine.objects.create(
            tenant=dispense_record.tenant,
            branch=dispense_record.branch,
            batch=item.batch,
            medicine=item.medicine,
            quantity=qty,
            source="PATIENT_RETURN",
            reason=f"Patient Return #{return_number}: {reason}"
        )

        item.batch.quarantined_quantity += qty
        item.batch.save(update_fields=['quarantined_quantity', 'updated_at'])

        refund_amt = qty * item.unit_price

        patient_return = PatientReturn.objects.create(
            tenant=dispense_record.tenant,
            branch=dispense_record.branch,
            return_number=return_number,
            dispense_record=dispense_record,
            patient=dispense_record.prescription.patient,
            medicine=item.medicine,
            batch=item.batch,
            quantity_returned=qty,
            condition=condition,
            reason=reason,
            routed_to_quarantine=True,
            refund_amount=refund_amt,
            received_by=received_by
        )

        record_audit_event(
            tenant=dispense_record.tenant,
            branch=dispense_record.branch,
            actor=received_by,
            event_type='PATIENT_MEDICATION_RETURN',
            resource_type='patient_return',
            resource_id=patient_return.id,
            details={'return_number': return_number, 'refund': str(refund_amt)}
        )

        return patient_return

    @classmethod
    @transaction.atomic
    def process_supplier_return(
        cls,
        batch: MedicineBatch,
        supplier: Supplier,
        quantity: Decimal,
        reason: str,
        authorized_by: User
    ) -> SupplierReturn:
        """Processes return of unusable/recalled stock back to the supplier, deducting inventory."""
        qty = Decimal(str(quantity))
        if qty <= Decimal('0.00'):
            raise ValidationError("Quantity must be greater than zero.")
        if batch.available_quantity < qty:
            raise ValidationError(
                f"Cannot return {qty} units. Batch {batch.batch_number} has only {batch.available_quantity} available."
            )

        count = SupplierReturn.objects.filter(tenant=batch.tenant).count() + 1
        return_number = f"SRET-{batch.branch.code if batch.branch else 'HQ'}-{date.today().year}-{count:04d}"

        # Deduct stock via StockService
        StockService.deduct_stock(
            batch_id=batch.id,
            quantity=qty,
            movement_type=MovementType.SUPPLIER_RETURN,
            reference_type="SupplierReturn",
            reference_id=return_number,
            actor=authorized_by,
            reason=f"Supplier Return #{return_number}: {reason}"
        )

        total_credit = qty * batch.purchase_cost

        supp_return = SupplierReturn.objects.create(
            tenant=batch.tenant,
            branch=batch.branch,
            return_number=return_number,
            supplier=supplier,
            medicine=batch.medicine,
            batch=batch,
            quantity=qty,
            unit_cost=batch.purchase_cost,
            total_credit=total_credit,
            reason=reason,
            authorized_by=authorized_by
        )

        return supp_return

    @classmethod
    @transaction.atomic
    def resolve_quarantine(
        cls,
        quarantine: StockQuarantine,
        resolution: QuarantineResolution,
        resolution_notes: str,
        resolver: User
    ) -> StockQuarantine:
        """Resolves quarantined stock (Destruction, return to supplier, or approved release)."""
        if quarantine.is_resolved:
            raise ValidationError("This quarantine case has already been resolved.")

        batch = MedicineBatch.objects.select_for_update().get(id=quarantine.batch.id)

        if resolution == QuarantineResolution.RESTORED_TO_STOCK:
            # Authorized release: move from quarantined to available
            batch.quarantined_quantity = max(Decimal('0.00'), batch.quarantined_quantity - quarantine.quantity)
            batch.save(update_fields=['quarantined_quantity'])
            StockService.add_stock(
                batch_id=batch.id,
                quantity=quarantine.quantity,
                movement_type=MovementType.QUARANTINE_MOVE,
                reference_type="StockQuarantine",
                reference_id=str(quarantine.id),
                actor=resolver,
                reason=f"Approved release from quarantine: {resolution_notes}"
            )
        else:
            # Biohazard destruction or return to supplier: reduce quarantined count
            batch.quarantined_quantity = max(Decimal('0.00'), batch.quarantined_quantity - quarantine.quantity)
            batch.save(update_fields=['quarantined_quantity'])

        quarantine.is_resolved = True
        quarantine.resolution = resolution
        quarantine.resolution_notes = resolution_notes
        quarantine.resolved_by = resolver
        quarantine.resolved_at = dj_timezone.now()
        quarantine.save(update_fields=['is_resolved', 'resolution', 'resolution_notes', 'resolved_by', 'resolved_at'])

        return quarantine
