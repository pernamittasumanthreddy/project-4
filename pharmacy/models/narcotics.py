"""HMS Controlled Substances & Perpetual Narcotic Ledger — Member 5
Provides strict regulatory compliance for Schedule II-V controlled substances:
- Double-witness sign-off on dispensing and partial dose wastage.
- Shift-based perpetual inventory balance logging.
- Discrepancy flagging and DEA/Regulatory audit reports.
"""

from django.db import models
from decimal import Decimal
from core.models import BaseTenantModel
from accounts.models import User
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch
from pharmacy.models.dispensing import DispenseRecord


class ControlledSubstanceSchedule(models.TextChoices):
    SCHEDULE_I = "SCH_I", "Schedule I (No accepted medical use)"
    SCHEDULE_II = "SCH_II", "Schedule II (High abuse potential, severe dependence)"
    SCHEDULE_III = "SCH_III", "Schedule III (Moderate to low physical dependence)"
    SCHEDULE_IV = "SCH_IV", "Schedule IV (Low potential for abuse)"
    SCHEDULE_V = "SCH_V", "Schedule V (Lowest abuse potential)"


class NarcoticDispenseLog(BaseTenantModel):
    """Detailed record of each controlled substance dispensation requiring double-witness verification."""
    dispense_record = models.ForeignKey(DispenseRecord, on_delete=models.CASCADE, related_name='narcotic_logs')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='narcotic_logs')
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT, related_name='narcotic_logs')

    schedule = models.CharField(max_length=20, choices=ControlledSubstanceSchedule.choices, default=ControlledSubstanceSchedule.SCHEDULE_II)
    quantity_dispensed = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_administered = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    quantity_wasted = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), help_text="Unused partial vial or ampoule disposed")

    primary_pharmacist = models.ForeignKey(User, on_delete=models.PROTECT, related_name='narcotics_dispensed_primary')
    witness_clinician = models.ForeignKey(User, on_delete=models.PROTECT, related_name='narcotics_dispensed_witnessed', help_text="Mandatory second licensed witness")

    waste_reason = models.CharField(max_length=255, blank=True, help_text="Reason for discarded quantity (e.g., partial dose, dropped ampoule)")
    patient_mrn = models.CharField(max_length=100)
    administration_time = models.DateTimeField(null=True, blank=True)
    is_reconciled = models.BooleanField(default=False)

    class Meta:
        db_table = 'pharmacy_narcotic_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"NARCOTIC-{self.medicine.brand_name}-QTY:{self.quantity_dispensed}-WITNESS:{self.witness_clinician.username}"


class NarcoticShiftAudit(BaseTenantModel):
    """Shift-change physical count comparison verifying perpetual controlled vault totals."""
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='shift_audits')
    batch = models.ForeignKey(MedicineBatch, on_delete=models.PROTECT, related_name='shift_audits')

    expected_vault_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    physical_count_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    discrepancy = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    outgoing_pharmacist = models.ForeignKey(User, on_delete=models.PROTECT, related_name='narcotics_handover_outgoing')
    incoming_pharmacist = models.ForeignKey(User, on_delete=models.PROTECT, related_name='narcotics_handover_incoming')

    shift_name = models.CharField(max_length=50, default="Day Shift")
    notes = models.TextField(blank=True)
    is_discrepancy_resolved = models.BooleanField(default=True)

    class Meta:
        db_table = 'pharmacy_narcotic_shift_audits'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.discrepancy = self.physical_count_quantity - self.expected_vault_quantity
        if self.discrepancy != Decimal("0.00"):
            self.is_discrepancy_resolved = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SHIFT-AUDIT-{self.shift_name}-{self.medicine.brand_name}-DISC:{self.discrepancy}"
