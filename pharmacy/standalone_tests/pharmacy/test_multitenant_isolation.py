"""HMS Pharmacy Multi-Tenant Isolation Tests — Member 5
Validates Section 15: Guarantees strict multi-tenant boundary separation between healthcare organizations.
"""

import pytest
from decimal import Decimal
from rest_framework.test import APIClient

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from datetime import date, timedelta


@pytest.fixture
def setup_two_tenants():
    # Tenant A
    t_a = Tenant.objects.create(name="Hospital Alpha", subdomain="alpha")
    h_a = Hospital.objects.create(tenant=t_a, name="Alpha Facility")
    b_a = Branch.objects.create(hospital=h_a, name="Alpha Central", code="AL1")
    user_a = User.objects.create_user(
        username="user_alpha", password="Password123!", role=UserRole.PHARMACIST, tenant=t_a, branch=b_a
    )
    med_a = Medicine.objects.create(
        tenant=t_a, code="MED-ALPHA-1", brand_name="AlphaMed", generic_name="GenA", strength="100mg"
    )

    # Tenant B
    t_b = Tenant.objects.create(name="Hospital Beta", subdomain="beta")
    h_b = Hospital.objects.create(tenant=t_b, name="Beta Facility")
    b_b = Branch.objects.create(hospital=h_b, name="Beta Central", code="BT1")
    user_b = User.objects.create_user(
        username="user_beta", password="Password123!", role=UserRole.PHARMACIST, tenant=t_b, branch=b_b
    )
    med_b = Medicine.objects.create(
        tenant=t_b, code="MED-BETA-1", brand_name="BetaMed", generic_name="GenB", strength="200mg"
    )

    return t_a, b_a, user_a, med_a, t_b, b_b, user_b, med_b


@pytest.mark.django_db
class TestMultiTenantIsolation:

    def test_catalogue_query_isolation(self, setup_two_tenants):
        """Verifies ORM query filtering isolates medicine catalogue between tenants."""
        t_a, _, _, med_a, t_b, _, _, med_b = setup_two_tenants

        qs_a = Medicine.objects.filter(tenant=t_a)
        qs_b = Medicine.objects.filter(tenant=t_b)

        assert qs_a.count() == 1
        assert qs_a.first().brand_name == "AlphaMed"

        assert qs_b.count() == 1
        assert qs_b.first().brand_name == "BetaMed"

    def test_api_cross_tenant_read_blocked(self, setup_two_tenants):
        """Verifies authenticated User A cannot read or retrieve User B's medicine via API."""
        t_a, b_a, user_a, med_a, t_b, b_b, user_b, med_b = setup_two_tenants

        client = APIClient()
        client.force_authenticate(user=user_a)

        # User A requests medicine belonging to Tenant B
        url = f"/api/pharmacy/medicines/{med_b.id}/"
        response = client.get(url, HTTP_X_TENANT_ID=str(t_a.id))

        # Must return 404 Not Found (or 403 Forbidden)
        assert response.status_code in [404, 403]

    def test_api_cross_tenant_listing_isolated(self, setup_two_tenants):
        """Verifies API listing endpoint only returns records for the authenticated tenant."""
        t_a, b_a, user_a, med_a, t_b, b_b, user_b, med_b = setup_two_tenants

        client = APIClient()
        client.force_authenticate(user=user_a)

        response = client.get("/api/pharmacy/medicines/", HTTP_X_TENANT_ID=str(t_a.id))
        assert response.status_code == 200
        results = response.data.get('results', response.data)

        # Must contain AlphaMed and NEVER BetaMed
        codes = [item['code'] for item in results]
        assert "MED-ALPHA-1" in codes
        assert "MED-BETA-1" not in codes
