"""HMS Command: Load WHO Essential Medicines & Formulary Dataset — Member 5
Loads standardized clinical drug catalogue, cold-chain monitors, and narcotic compliance records.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from datetime import date, timedelta
import random

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from pharmacy.models.catalogue import (
    MedicineCategory,
    Medicine,
    DosageForm,
    AdministrationRoute,
    DrugClassification,
)
from pharmacy.models.inventory import StorageLocation, MedicineBatch, BatchStatus
from pharmacy.models.cold_chain import TemperatureLog, StorageLocation, ThermalExcursionEvent
from pharmacy.data.who_essential_medicines import WHO_ESSENTIAL_MEDICINES_DATA


class Command(BaseCommand):
    help = "Loads standardized WHO Essential Medicines List and clinical formulary records."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Loading WHO Formulary and Clinical Knowledge Base..."))

        tenant = Tenant.objects.filter(is_active=True).first()
        if not tenant:
            self.stdout.write(self.style.ERROR("No active tenant found. Please run seed_pharmacy_demo first."))
            return

        hospital = Hospital.objects.filter(tenant=tenant).first()
        branch = Branch.objects.filter(hospital=hospital).first()

        with transaction.atomic():
            # Ensure Cold Storage and Narcotic Vault locations exist
            cold_room, _ = StorageLocation.objects.get_or_create(
                tenant=tenant,
                branch=branch,
                code="COLD-FRIDGE-01",
                defaults={
                    "name": "Cold Storage Vaccine Refrigerator",
                    "description": "2°C to 8°C Monitored Biological Refrigerator",
                    "is_cold_storage": True
                }
            )

            narcotic_vault, _ = StorageLocation.objects.get_or_create(
                tenant=tenant,
                branch=branch,
                code="VAULT-NARCOTIC-01",
                defaults={
                    "name": "Schedule II Double-Lock Narcotic Safe",
                    "description": "Double-lock perpetual controlled substance vault",
                    "is_cold_storage": False
                }
            )


            # 1. Load WHO Medicines
            created_count = 0
            for item in WHO_ESSENTIAL_MEDICINES_DATA:
                cat_name = item.get("category_name", "General Formulary")
                category, _ = MedicineCategory.objects.get_or_create(
                    tenant=tenant,
                    name=cat_name
                )

                med, created = Medicine.objects.get_or_create(
                    tenant=tenant,
                    code=item["code"],
                    defaults={
                        "brand_name": item["brand_name"],
                        "generic_name": item["generic_name"],
                        "active_ingredients": item.get("active_ingredients", ""),
                        "strength": item["strength"],
                        "dosage_form": getattr(DosageForm, item["dosage_form"], DosageForm.TABLET),
                        "route": getattr(AdministrationRoute, item["route"], AdministrationRoute.ORAL),
                        "classification": getattr(DrugClassification, item["classification"], DrugClassification.OTHER),
                        "category": category,
                        "unit_of_measure": item.get("unit_of_measure", "Box"),
                        "dispensing_unit": item.get("dispensing_unit", "Unit"),
                        "unit_price": Decimal(item["unit_price"]),
                        "reorder_level": Decimal(item["reorder_level"]),
                        "reorder_quantity": Decimal(item["reorder_quantity"]),
                        "storage_instructions": item.get("storage_instructions", "Store below 25°C"),
                        "barcode_sku": f"01003{random.randint(100000000, 999999999)}",
                        "requires_prescription": True
                    }
                )

                if created:
                    created_count += 1

                # Provision inventory batch for this medicine
                storage = cold_room if "INJECTION" in item["dosage_form"] or "INS" in item["code"] else None
                lot_number = f"LOT-{item['code'].replace('-', '')}-26"

                MedicineBatch.objects.get_or_create(
                    tenant=tenant,
                    branch=branch,
                    medicine=med,
                    batch_number=lot_number,
                    defaults={
                        "expiry_date": date.today() + timedelta(days=random.randint(120, 500)),
                        "purchase_cost": Decimal(item["unit_price"]) * Decimal("0.70"),
                        "selling_price": Decimal(item["unit_price"]),
                        "received_quantity": Decimal("200.00"),
                        "available_quantity": Decimal("180.00"),
                        "storage_location": storage,
                        "status": BatchStatus.ACTIVE
                    }
                )

            # 2. Add Cold Chain Temperature Sensor Readings
            for offset in range(5):
                temp = Decimal(str(round(4.0 + (random.random() * 1.5 - 0.75), 2)))
                TemperatureLog.objects.create(
                    tenant=tenant,
                    storage_location=cold_room,
                    recorded_temperature_celsius=temp,
                    humidity_percentage=Decimal("45.5"),
                    sensor_id="IOT-VACCINE-PROBE-01"
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {created_count} WHO Essential Medicines and clinical formulary items!"))
