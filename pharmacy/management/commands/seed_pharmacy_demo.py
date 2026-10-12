"""HMS Pharmacy Seed Data Command — Member 5
Provisions multi-tenant sample data, formulary medicines, FEFO batches, and test prescriptions.
"""

from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core.models import Tenant, Hospital, Branch
from accounts.models import UserRole
from pharmacy.models import (
    DosageForm,
    AdministrationRoute,
    DrugClassification,
    MedicineCategory,
    Medicine,
    Supplier,
    StorageLocation,
    MedicineBatch,
    BatchStatus,
    PurchaseOrder,
    PurchaseOrderItem,
    POStatus,
)
from clinical.models import Patient, Prescription, PrescriptionItem, PrescriptionStatus

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds realistic multi-tenant demonstration data for HMS Pharmacy & Inventory'

    def handle(self, *args, **options):
        self.stdout.write("Initializing multi-tenant pharmacy seed data...")

        # 1. Tenant & Facility
        tenant, _ = Tenant.objects.get_or_create(
            subdomain="apex",
            defaults={"name": "Apex Healthcare Network", "is_active": True}
        )
        hospital, _ = Hospital.objects.get_or_create(
            tenant=tenant,
            name="Apex General Hospital",
            defaults={
                "license_number": "HOSP-MED-2026-99",
                "tax_identifier": "27AABCA1234F1Z5",
                "address": "450 Health Avenue, Metro Central",
                "phone": "+1-800-555-0199",
                "email": "info@apexgeneral.org"
            }
        )
        branch, _ = Branch.objects.get_or_create(
            hospital=hospital,
            code="MCB",
            defaults={
                "name": "Main City Hospital Facility",
                "is_main_branch": True,
                "address": "450 Health Avenue, Floor 1"
            }
        )

        # 2. Staff Users
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@apexgeneral.org",
                password="AdminPass123!",
                role=UserRole.SUPER_ADMIN,
                tenant=tenant,
                branch=branch
            )
            self.stdout.write("Created Superuser: admin (pass: AdminPass123!)")

        pharmacist, _ = User.objects.get_or_create(
            username="pharmacist",
            defaults={
                "email": "rx@apexgeneral.org",
                "role": UserRole.PHARMACIST,
                "tenant": tenant,
                "branch": branch,
                "first_name": "Sarah",
                "last_name": "Jenkins",
                "license_number": "RPH-88491"
            }
        )
        pharmacist.set_password("PharmacistPass123!")
        pharmacist.save()

        inventory_mgr, _ = User.objects.get_or_create(
            username="inventory_mgr",
            defaults={
                "email": "inventory@apexgeneral.org",
                "role": UserRole.INVENTORY_MANAGER,
                "tenant": tenant,
                "branch": branch,
                "first_name": "David",
                "last_name": "Miller"
            }
        )
        inventory_mgr.set_password("InventoryPass123!")
        inventory_mgr.save()

        doctor, _ = User.objects.get_or_create(
            username="doctor",
            defaults={
                "email": "dr.roberts@apexgeneral.org",
                "role": UserRole.DOCTOR,
                "tenant": tenant,
                "branch": branch,
                "first_name": "Arthur",
                "last_name": "Roberts",
                "license_number": "MD-39201"
            }
        )
        doctor.set_password("DoctorPass123!")
        doctor.save()

        # 3. Suppliers
        sup_apex, _ = Supplier.objects.get_or_create(
            tenant=tenant,
            code="SUP-APEX",
            defaults={
                "name": "Apex Pharma Distributors Ltd",
                "contact_person": "Vikram Patel",
                "phone": "+91-9876543210",
                "email": "sales@apexdistributors.com",
                "address": "Plot 12, Industrial Area Phase II",
                "gstin": "27AAACA1234Q1Z8",
                "payment_terms": "Net 30 Days"
            }
        )
        sup_sun, _ = Supplier.objects.get_or_create(
            tenant=tenant,
            code="SUP-SUN",
            defaults={
                "name": "Sunlight Healthcare Logistics",
                "contact_person": "Pooja Sharma",
                "phone": "+91-9123456789",
                "email": "orders@sunlightlogistics.com",
                "payment_terms": "Net 15 Days"
            }
        )

        # 4. Storage Locations
        loc_main, _ = StorageLocation.objects.get_or_create(
            tenant=tenant,
            branch=branch,
            code="LOC-MAIN-A",
            defaults={"name": "Main Dispensary Rack A", "is_cold_storage": False}
        )
        loc_cold, _ = StorageLocation.objects.get_or_create(
            tenant=tenant,
            branch=branch,
            code="LOC-COLD-1",
            defaults={"name": "Cold Storage Fridge (2-8°C)", "is_cold_storage": True}
        )

        # 5. Medicine Categories & Formulary
        cat_anti, _ = MedicineCategory.objects.get_or_create(
            tenant=tenant,
            name="Antibiotics",
            defaults={"description": "Systemic antimicrobial therapeutic agents"}
        )
        cat_pain, _ = MedicineCategory.objects.get_or_create(
            tenant=tenant,
            name="Analgesics & Antipyretics",
            defaults={"description": "Pain and fever management medications"}
        )
        cat_cardio, _ = MedicineCategory.objects.get_or_create(
            tenant=tenant,
            name="Cardiovascular & Endocrine",
            defaults={"description": "Hypertension, diabetes, and endocrine care"}
        )

        med_amox, _ = Medicine.objects.get_or_create(
            tenant=tenant,
            code="MED-AMX-500",
            defaults={
                "brand_name": "Amoxil",
                "generic_name": "Amoxicillin",
                "active_ingredients": "Amoxicillin Trihydrate 500mg",
                "strength": "500 mg",
                "dosage_form": DosageForm.CAPSULE,
                "route": AdministrationRoute.ORAL,
                "manufacturer": "GlaxoSmithKline",
                "classification": DrugClassification.ANTIBIOTIC,
                "category": cat_anti,
                "requires_prescription": True,
                "unit_of_measure": "Strip of 10",
                "dispensing_unit": "Capsule",
                "reorder_level": Decimal("100.00"),
                "reorder_quantity": Decimal("500.00"),
                "unit_price": Decimal("0.85"),
                "is_active": True
            }
        )

        med_dolo, _ = Medicine.objects.get_or_create(
            tenant=tenant,
            code="MED-PCM-650",
            defaults={
                "brand_name": "Dolo 650",
                "generic_name": "Paracetamol",
                "active_ingredients": "Acetaminophen 650mg",
                "strength": "650 mg",
                "dosage_form": DosageForm.TABLET,
                "route": AdministrationRoute.ORAL,
                "manufacturer": "Micro Labs",
                "classification": DrugClassification.ANTIPYRETIC,
                "category": cat_pain,
                "requires_prescription": False,
                "unit_of_measure": "Strip of 15",
                "dispensing_unit": "Tablet",
                "reorder_level": Decimal("150.00"),
                "reorder_quantity": Decimal("1000.00"),
                "unit_price": Decimal("0.25"),
                "is_active": True
            }
        )

        med_azee, _ = Medicine.objects.get_or_create(
            tenant=tenant,
            code="MED-AZI-500",
            defaults={
                "brand_name": "Azee 500",
                "generic_name": "Azithromycin",
                "active_ingredients": "Azithromycin Dihydrate 500mg",
                "strength": "500 mg",
                "dosage_form": DosageForm.TABLET,
                "route": AdministrationRoute.ORAL,
                "manufacturer": "Cipla Ltd",
                "classification": DrugClassification.ANTIBIOTIC,
                "category": cat_anti,
                "requires_prescription": True,
                "unit_of_measure": "Strip of 3",
                "dispensing_unit": "Tablet",
                "reorder_level": Decimal("50.00"),
                "reorder_quantity": Decimal("200.00"),
                "unit_price": Decimal("2.10"),
                "is_active": True
            }
        )

        # 6. Physical Batches with discrete FEFO expiration dates
        today = date.today()

        # Batch 1: Expiring in 6 months (Primary FEFO for Amoxicillin)
        MedicineBatch.objects.get_or_create(
            branch=branch,
            medicine=med_amox,
            batch_number="AMX-2026-B1",
            defaults={
                "tenant": tenant,
                "expiry_date": today + timedelta(days=180),
                "manufacturing_date": today - timedelta(days=90),
                "supplier": sup_apex,
                "storage_location": loc_main,
                "purchase_cost": Decimal("0.50"),
                "selling_price": Decimal("0.85"),
                "received_quantity": Decimal("400.00"),
                "available_quantity": Decimal("350.00"),
                "status": BatchStatus.ACTIVE
            }
        )

        # Batch 2: Expiring in 18 months (Secondary FEFO for Amoxicillin)
        MedicineBatch.objects.get_or_create(
            branch=branch,
            medicine=med_amox,
            batch_number="AMX-2026-B2",
            defaults={
                "tenant": tenant,
                "expiry_date": today + timedelta(days=540),
                "manufacturing_date": today - timedelta(days=30),
                "supplier": sup_apex,
                "storage_location": loc_main,
                "purchase_cost": Decimal("0.52"),
                "selling_price": Decimal("0.85"),
                "received_quantity": Decimal("600.00"),
                "available_quantity": Decimal("600.00"),
                "status": BatchStatus.ACTIVE
            }
        )

        # Batch 3: Near-expiry batch for Paracetamol (Expiring in 45 days)
        MedicineBatch.objects.get_or_create(
            branch=branch,
            medicine=med_dolo,
            batch_number="DOLO-NEAR-EXP",
            defaults={
                "tenant": tenant,
                "expiry_date": today + timedelta(days=45),
                "manufacturing_date": today - timedelta(days=300),
                "supplier": sup_sun,
                "storage_location": loc_main,
                "purchase_cost": Decimal("0.12"),
                "selling_price": Decimal("0.25"),
                "received_quantity": Decimal("200.00"),
                "available_quantity": Decimal("180.00"),
                "status": BatchStatus.ACTIVE
            }
        )

        # Batch 4: Expired batch (To test system strictly blocks dispensing expired medicine)
        MedicineBatch.objects.get_or_create(
            branch=branch,
            medicine=med_azee,
            batch_number="AZEE-EXP-OLD",
            defaults={
                "tenant": tenant,
                "expiry_date": today - timedelta(days=15),
                "manufacturing_date": today - timedelta(days=500),
                "supplier": sup_sun,
                "storage_location": loc_main,
                "purchase_cost": Decimal("1.20"),
                "selling_price": Decimal("2.10"),
                "received_quantity": Decimal("100.00"),
                "available_quantity": Decimal("50.00"),
                "status": BatchStatus.EXPIRED
            }
        )

        # 7. Clinical Patients & Pending Prescriptions
        pat1, _ = Patient.objects.get_or_create(
            tenant=tenant,
            mrn="MRN-2026-001",
            defaults={
                "branch": branch,
                "full_name": "Eleanor Vance",
                "gender": "FEMALE",
                "date_of_birth": date(1988, 4, 12),
                "contact_number": "+1-555-0144"
            }
        )

        rx1, _ = Prescription.objects.get_or_create(
            tenant=tenant,
            prescription_number="RX-2026-1001",
            defaults={
                "branch": branch,
                "patient": pat1,
                "prescriber": doctor,
                "diagnosis": "Acute Upper Respiratory Tract Infection",
                "clinical_notes": "Prescribed 5-day course of Amoxicillin and fever relief.",
                "status": PrescriptionStatus.PENDING
            }
        )

        PrescriptionItem.objects.get_or_create(
            prescription=rx1,
            medicine_code="MED-AMX-500",
            defaults={
                "medicine_name": "Amoxicillin",
                "dosage": "500 mg",
                "frequency": "Three times daily (TID)",
                "duration_days": 5,
                "quantity_prescribed": Decimal("15.00"),
                "quantity_dispensed": Decimal("0.00"),
                "instructions": "Take after meals with a full glass of water"
            }
        )

        PrescriptionItem.objects.get_or_create(
            prescription=rx1,
            medicine_code="MED-PCM-650",
            defaults={
                "medicine_name": "Paracetamol",
                "dosage": "650 mg",
                "frequency": "Every 6 hours PRN for fever",
                "duration_days": 3,
                "quantity_prescribed": Decimal("10.00"),
                "quantity_dispensed": Decimal("0.00"),
                "instructions": "For fever over 100.5°F"
            }
        )

        # 8. Purchase Order Sample
        po1, _ = PurchaseOrder.objects.get_or_create(
            tenant=tenant,
            order_number="PO-MCB-2026-0001",
            defaults={
                "branch": branch,
                "supplier": sup_apex,
                "status": POStatus.APPROVED,
                "expected_delivery_date": today + timedelta(days=7),
                "created_by": inventory_mgr,
                "notes": "Emergency procurement buffer replenishment"
            }
        )
        PurchaseOrderItem.objects.get_or_create(
            purchase_order=po1,
            medicine=med_azee,
            defaults={
                "quantity_ordered": Decimal("100.00"),
                "quantity_received": Decimal("0.00"),
                "unit_cost": Decimal("1.25")
            }
        )
        po1.recalculate_total()

        self.stdout.write(self.style.SUCCESS("Successfully seeded comprehensive pharmacy & inventory demo data!"))
