"""HMS Cold Chain & Vaccine/Biological Temperature Monitoring System — Member 5
Tracks storage temperatures for temperature-sensitive medications (2-8°C, -20°C, -80°C),
detects thermal excursions, and automatically flags affected batches into quarantine holding.
"""

from django.db import models
from decimal import Decimal
from core.models import BaseTenantModel
from pharmacy.models.inventory import StorageLocation, MedicineBatch


class TemperatureZone(models.TextChoices):
    ROOM_TEMPERATURE = "ROOM_TEMP", "Controlled Room Temperature (15°C - 25°C)"
    REFRIGERATED = "REFRIGERATED", "Cold Storage (2°C - 8°C)"
    FREEZER = "FREEZER", "Standard Freezer (-25°C - -10°C)"
    ULTRA_LOW = "ULTRA_LOW", "Ultra-Low Cryo (-86°C - -60°C)"


class TemperatureLog(BaseTenantModel):
    """IoT sensor or manual calibrated thermometer reading for pharmacy storage location."""
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE, related_name='temperature_logs')
    recorded_temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    min_safe_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("2.00"))
    max_safe_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("8.00"))

    is_excursion = models.BooleanField(default=False, help_text="True if temperature breached safe limits")
    sensor_id = models.CharField(max_length=100, default="SENSOR-MAIN-FRIDGE-01")

    class Meta:
        db_table = 'pharmacy_temperature_logs'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-detect thermal excursion
        temp = self.recorded_temperature_celsius
        if temp < self.min_safe_threshold or temp > self.max_safe_threshold:
            self.is_excursion = True
        else:
            self.is_excursion = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TEMP-{self.storage_location.name}-{self.recorded_temperature_celsius}°C-EXCURSION:{self.is_excursion}"


class ThermalExcursionEvent(BaseTenantModel):
    """Incident report when a cold-chain storage unit experiences an out-of-spec event."""
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE, related_name='excursion_events')
    peak_temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes out of specification")

    root_cause = models.CharField(max_length=255, default="Compressor defrost cycle / Power interruption")
    action_taken = models.TextField(default="Immediate transfer of inventory to backup cold storage unit")
    affected_batches_quarantined = models.BooleanField(default=False)
    stability_data_reviewed = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pharmacy_thermal_excursions'
        ordering = ['-created_at']

    def __str__(self):
        return f"EXCURSION-{self.storage_location.name}-PEAK:{self.peak_temperature_celsius}°C"
