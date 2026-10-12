"""HMS Pharmacy Dispensing Service — Member 5
Implements prescription review, FEFO batch allocation, atomic stock deduction,
and billing invoice generation.
"""

from decimal import Decimal
from datetime import date
from django.db import transaction
from django.core.exceptions import ValidationError

from clinical.models import Prescription, PrescriptionItem, PrescriptionStatus
from billing.models import BillingInvoice, BillingItem, InvoiceStatus
from pharmacy.models.catalogue import Medicine
from pharmacy.models.dispensing import DispenseRecord, DispensedItem, DispenseStatus
from pharmacy.models.ledger import MovementType
from pharmacy.services.fefo_service import FEFOService
from pharmacy.services.stock_service import StockService
from accounts.models import User
from core.permissions import record_audit_event


class DispensingService:
    """Coordinates prescription dispensing, stock deduction, and billing integration."""

    @classmethod
    @transaction.atomic
    def dispense_prescription(
        cls,
        prescription: Prescription,
        pharmacist: User,
        dispense_items_payload: list = None,
        notes: str = ""
    ) -> DispenseRecord:
        """Fulfills prescribed medication lines, deducts stock via FEFO, and notifies billing."""
        if prescription.status == PrescriptionStatus.DISPENSED:
            raise ValidationError("Prescription has already been completely dispensed.")
        if prescription.status == PrescriptionStatus.CANCELLED:
            raise ValidationError("Cannot dispense a cancelled prescription.")

        # Generate unique receipt number
        count = DispenseRecord.objects.filter(tenant=prescription.tenant).count() + 1
        dispense_number = f"DSP-{prescription.branch.code if prescription.branch else 'HQ'}-{date.today().year}-{count:05d}"

        record = DispenseRecord.objects.create(
            tenant=prescription.tenant,
            branch=prescription.branch,
            dispense_number=dispense_number,
            prescription=prescription,
            pharmacist=pharmacist,
            status=DispenseStatus.COMPLETED,
            notes=notes
        )

        total_dispense_price = Decimal('0.00')
        billing_items_to_create = []

        # Items to fulfill: if payload provided, use it; otherwise fulfill all remaining authorized items
        items_to_process = []
        if dispense_items_payload:
            for payload_entry in dispense_items_payload:
                p_item = PrescriptionItem.objects.select_for_update().get(
                    id=payload_entry['prescription_item_id'],
                    prescription=prescription
                )
                dispense_qty = Decimal(str(payload_entry.get('quantity_to_dispense', p_item.remaining_quantity)))
                items_to_process.append((p_item, dispense_qty, payload_entry.get('preferred_batch_id', None)))
        else:
            for p_item in prescription.items.select_for_update().all():
                if p_item.remaining_quantity > Decimal('0.00'):
                    items_to_process.append((p_item, p_item.remaining_quantity, None))

        if not items_to_process:
            raise ValidationError("No remaining quantities to dispense on this prescription.")

        for p_item, qty_to_dispense, preferred_batch_id in items_to_process:
            if qty_to_dispense <= Decimal('0.00'):
                continue
            if qty_to_dispense > p_item.remaining_quantity:
                raise ValidationError(
                    f"Cannot dispense {qty_to_dispense} units of '{p_item.medicine_name}'. "
                    f"Remaining authorized quantity: {p_item.remaining_quantity}"
                )

            # Match prescription item to medicine catalogue
            medicine = None
            if p_item.medicine_code:
                medicine = Medicine.objects.filter(tenant=prescription.tenant, code=p_item.medicine_code).first()
            if not medicine:
                medicine = Medicine.objects.filter(
                    tenant=prescription.tenant,
                    generic_name__iexact=p_item.medicine_name
                ).first() or Medicine.objects.filter(
                    tenant=prescription.tenant,
                    brand_name__iexact=p_item.medicine_name
                ).first()

            if not medicine:
                raise ValidationError(
                    f"Prescribed medication '{p_item.medicine_name}' not found in active hospital catalogue."
                )

            # FEFO Allocation across batches
            allocations = FEFOService.allocate_batches(
                medicine=medicine,
                required_quantity=qty_to_dispense,
                branch=prescription.branch,
                preferred_batch_id=preferred_batch_id
            )

            for alloc in allocations:
                batch = alloc['batch']
                alloc_qty = alloc['allocated_quantity']
                unit_price = alloc['unit_price']
                line_total = alloc_qty * unit_price

                # Deduct stock atomically with row lock
                StockService.deduct_stock(
                    batch_id=batch.id,
                    quantity=alloc_qty,
                    movement_type=MovementType.PRESCRIPTION_DISPENSE,
                    reference_type="DispenseRecord",
                    reference_id=str(record.id),
                    actor=pharmacist,
                    reason=f"Dispensation #{dispense_number} for Rx #{prescription.prescription_number}"
                )

                # Record DispensedItem
                DispensedItem.objects.create(
                    dispense_record=record,
                    prescription_item=p_item,
                    medicine=medicine,
                    batch=batch,
                    quantity_dispensed=alloc_qty,
                    unit_price=unit_price,
                    instructions_provided=p_item.instructions
                )

                total_dispense_price += line_total
                billing_items_to_create.append({
                    'code': medicine.code,
                    'name': f"{medicine.brand_name} ({medicine.strength}) - Batch {batch.batch_number}",
                    'quantity': alloc_qty,
                    'unit_price': unit_price,
                    'total_price': line_total
                })

            # Update prescription item fulfilled counter
            p_item.quantity_dispensed += qty_to_dispense
            p_item.save(update_fields=['quantity_dispensed'])

        # Update prescription overall status
        all_done = all(item.remaining_quantity <= Decimal('0.00') for item in prescription.items.all())
        prescription.status = PrescriptionStatus.DISPENSED if all_done else PrescriptionStatus.PARTIALLY_DISPENSED
        prescription.save(update_fields=['status', 'updated_at'])

        record.total_amount = total_dispense_price

        # Billing Module Integration: Generate Patient Invoice
        try:
            inv_count = BillingInvoice.objects.filter(tenant=prescription.tenant).count() + 1
            invoice_num = f"INV-RX-{date.today().year}-{inv_count:05d}"
            invoice = BillingInvoice.objects.create(
                tenant=prescription.tenant,
                branch=prescription.branch,
                patient=prescription.patient,
                invoice_number=invoice_num,
                total_amount=total_dispense_price,
                paid_amount=Decimal('0.00'),
                status=InvoiceStatus.PENDING,
                source_module='PHARMACY',
                reference_id=str(record.id)
            )
            for b_item in billing_items_to_create:
                BillingItem.objects.create(
                    invoice=invoice,
                    item_type='MEDICATION',
                    item_code=b_item['code'],
                    description=b_item['name'],
                    quantity=b_item['quantity'],
                    unit_price=b_item['unit_price'],
                    total_price=b_item['total_price']
                )
            record.billing_invoice_id = str(invoice.id)
        except Exception:
            # If billing fails, preserve dispensation without rolling back patient clinical delivery
            pass

        record.save(update_fields=['total_amount', 'billing_invoice_id'])

        record_audit_event(
            tenant=prescription.tenant,
            branch=prescription.branch,
            actor=pharmacist,
            event_type='PRESCRIPTION_DISPENSED',
            resource_type='dispense_record',
            resource_id=record.id,
            details={'rx_number': prescription.prescription_number, 'amount': str(total_dispense_price)}
        )

        return record
