"""Tests for Reports & Alerts APIs — Member 5"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch
from clinical.models import Patient, Prescription, PrescriptionItem, PrescriptionStatus


@pytest.mark.django_db
class TestReportsAndAlerts:
    """Verifies that Reports, PDF/CSV generation, and dynamic alert metrics operate correctly."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Report Test Hospital", subdomain="rth-hospital")
        self.hospital = Hospital.objects.create(tenant=self.tenant, name="RTH Hospital")

        self.branch = Branch.objects.create(hospital=self.hospital, name="Central RTH", code="CRTH")

        self.user = User.objects.create_user(
            username="report_pharmacist",
            password="Password123!",
            tenant=self.tenant,
            branch=self.branch,
            role=UserRole.PHARMACIST
        )

        self.medicine = Medicine.objects.create(
            tenant=self.tenant,
            code="RPT-MED-01",
            brand_name="ReportCillin",
            generic_name="Reportcillin Sodium",
            strength="500 mg",
            reorder_level=Decimal("20.00"),
            unit_price=Decimal("15.00")
        )

        self.batch = MedicineBatch.objects.create(
            tenant=self.tenant,
            branch=self.branch,
            medicine=self.medicine,
            batch_number="RPT-LOT-99",
            expiry_date=date.today() + timedelta(days=180),
            purchase_cost=Decimal("10.00"),
            selling_price=Decimal("15.00"),
            received_quantity=Decimal("100.00"),
            available_quantity=Decimal("100.00"),
            status="ACTIVE"
        )

        self.client = APIClient()
        self.client.force_login(self.user)

    def test_stock_valuation_endpoint(self):
        """Verifies GET /api/pharmacy/reports/ returns correct persisted valuation totals."""
        response = self.client.get('/api/pharmacy/reports/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
        val = data['valuation']
        assert val['total_batches_count'] == 1
        assert Decimal(str(val['total_units_on_hand'])) == Decimal("100.00")
        assert Decimal(str(val['total_purchase_cost_value'])) == Decimal("1000.00")

    def test_stock_csv_export_endpoint(self):
        """Verifies GET /api/pharmacy/reports/?export=csv streams valid CSV."""
        response = self.client.get('/api/pharmacy/reports/?export=csv')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'
        assert 'attachment; filename=' in response['Content-Disposition']
        content = response.content.decode('utf-8')
        assert 'Medicine Code' in content
        assert 'ReportCillin' in content
        assert 'RPT-LOT-99' in content

    def test_stock_pdf_export_endpoint(self):
        """Verifies GET /api/pharmacy/reports/?export=pdf generates valid binary PDF report."""
        response = self.client.get('/api/pharmacy/reports/?export=pdf')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'application/pdf'
        assert 'attachment; filename=' in response['Content-Disposition']
        assert response.content.startswith(b'%PDF-')
        assert len(response.content) > 1000

    def test_alerts_summary_endpoint(self):
        """Verifies GET /api/pharmacy/alerts/ calculates real stock and Rx metrics."""
        response = self.client.get('/api/pharmacy/alerts/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
        summary = data['summary']
        assert 'expired_batches_count' in summary
        assert 'near_expiry_batches_count' in summary
        assert 'low_stock_count' in summary
        assert 'pending_prescriptions_count' in summary
