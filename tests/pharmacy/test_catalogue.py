"""HMS Pharmacy Catalogue Tests — Member 5"""

import pytest
from decimal import Decimal
from django.db import IntegrityError
from core.models import Tenant
from pharmacy.models.catalogue import Medicine, MedicineCategory, DosageForm, DrugClassification


@pytest.mark.django_db
class TestMedicineCatalogue:

    def test_create_and_query_medicine(self):
        tenant = Tenant.objects.create(name="Hospital Alpha", subdomain="alpha")
        category = MedicineCategory.objects.create(tenant=tenant, name="Cardiology")

        med = Medicine.objects.create(
            tenant=tenant,
            code="MED-ATV-20",
            brand_name="Lipitor",
            generic_name="Atorvastatin",
            strength="20 mg",
            dosage_form=DosageForm.TABLET,
            classification=DrugClassification.CARDIOVASCULAR,
            category=category,
            reorder_level=Decimal("50.00"),
            unit_price=Decimal("1.50")
        )
        assert med.id is not None
        assert med.brand_name == "Lipitor"
        assert med.get_total_stock() == Decimal("0.00")
        assert med.is_low_stock() is True

    def test_tenant_scoped_uniqueness(self):
        """Validates that duplicate codes in the same tenant are rejected, but allowed across different tenants."""
        t1 = Tenant.objects.create(name="Hospital One", subdomain="t1")
        t2 = Tenant.objects.create(name="Hospital Two", subdomain="t2")

        Medicine.objects.create(
            tenant=t1, code="MED-PCM", brand_name="Panadol", generic_name="Paracetamol", strength="500mg"
        )

        # Duplicate in same tenant must raise IntegrityError
        from django.db import transaction
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                Medicine.objects.create(
                    tenant=t1, code="MED-PCM", brand_name="Calpol", generic_name="Paracetamol", strength="500mg"
                )

        # Same code in different tenant is completely permitted
        med_t2 = Medicine.objects.create(
            tenant=t2, code="MED-PCM", brand_name="Tylenol", generic_name="Paracetamol", strength="500mg"
        )
        assert med_t2.id is not None

    def test_soft_delete_preservation(self):
        """Confirms soft deletion deactivates medicine without destroying relational integrity."""
        tenant = Tenant.objects.create(name="Hospital Beta", subdomain="beta")
        med = Medicine.objects.create(
            tenant=tenant, code="MED-TEST-1", brand_name="TestMed", generic_name="GenericTest", strength="10mg"
        )
        med.is_deleted = True
        med.is_active = False
        med.save()

        # Database record still exists for historical foreign key preservation
        refreshed = Medicine.objects.get(id=med.id)
        assert refreshed.is_deleted is True
        assert refreshed.is_active is False
