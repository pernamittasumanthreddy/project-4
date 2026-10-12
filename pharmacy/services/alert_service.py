"""HMS Pharmacy Alert Service — Member 5
Computes real-time dynamic inventory alerts directly from persisted database data.
"""

from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, Any, List
from django.db.models import Sum

from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch, BatchStatus
from pharmacy.models.purchasing import PurchaseOrder, POStatus
from pharmacy.models.returns import StockQuarantine
from clinical.models import Prescription, PrescriptionStatus


class AlertService:
    """Calculates operational and clinical inventory alerts for an authorized tenant and branch."""

    @classmethod
    def get_alerts_summary(cls, tenant, branch=None) -> Dict[str, Any]:
        """Calculates consolidated counts of active alerts."""
        today = date.today()
        near_expiry_cutoff = today + timedelta(days=60)

        # 1. Batches queries
        batches_base = MedicineBatch.objects.filter(tenant=tenant)
        if branch:
            batches_base = batches_base.filter(branch=branch)

        expired_batches_count = batches_base.filter(
            expiry_date__lte=today,
            status__in=[BatchStatus.ACTIVE, BatchStatus.EXPIRED],
            available_quantity__gt=Decimal('0.00')
        ).count()

        near_expiry_batches_count = batches_base.filter(
            expiry_date__gt=today,
            expiry_date__lte=near_expiry_cutoff,
            status=BatchStatus.ACTIVE,
            available_quantity__gt=Decimal('0.00')
        ).count()

        quarantined_count = StockQuarantine.objects.filter(tenant=tenant, is_resolved=False)
        if branch:
            quarantined_count = quarantined_count.filter(branch=branch)
        quarantined_items_count = quarantined_count.count()

        # 2. Medicine stock levels
        meds_base = Medicine.objects.filter(tenant=tenant, is_active=True, is_deleted=False)
        low_stock_count = 0
        out_of_stock_count = 0

        for med in meds_base:
            stock = med.get_total_stock(branch=branch)
            if stock <= Decimal('0.00'):
                out_of_stock_count += 1
            elif stock <= med.reorder_level:
                low_stock_count += 1

        # 3. Procurement & Prescriptions
        po_query = PurchaseOrder.objects.filter(tenant=tenant, status__in=[POStatus.DRAFT, POStatus.SUBMITTED])
        rx_query = Prescription.objects.filter(tenant=tenant, status__in=[PrescriptionStatus.PENDING, PrescriptionStatus.PARTIALLY_DISPENSED])
        if branch:
            po_query = po_query.filter(branch=branch)
            rx_query = rx_query.filter(branch=branch)

        return {
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'expired_batches_count': expired_batches_count,
            'near_expiry_batches_count': near_expiry_batches_count,
            'quarantined_items_count': quarantined_items_count,
            'pending_po_count': po_query.count(),
            'pending_prescriptions_count': rx_query.count(),
            'total_critical_alerts': expired_batches_count + out_of_stock_count + quarantined_items_count
        }

    @classmethod
    def get_low_stock_medicines(cls, tenant, branch=None) -> List[Dict[str, Any]]:
        """Returns detailed records of medicines requiring replenishment."""
        meds = Medicine.objects.filter(tenant=tenant, is_active=True, is_deleted=False)
        results = []
        for m in meds:
            current_stock = m.get_total_stock(branch=branch)
            if current_stock <= m.reorder_level:
                results.append({
                    'id': str(m.id),
                    'code': m.code,
                    'brand_name': m.brand_name,
                    'generic_name': m.generic_name,
                    'strength': m.strength,
                    'current_stock': current_stock,
                    'reorder_level': m.reorder_level,
                    'reorder_quantity': m.reorder_quantity,
                    'is_out_of_stock': current_stock <= Decimal('0.00')
                })
        return results

    @classmethod
    def get_expiring_batches(cls, tenant, branch=None, days_threshold: int = 60) -> List[MedicineBatch]:
        """Returns batches expiring within specified threshold."""
        today = date.today()
        cutoff = today + timedelta(days=days_threshold)
        query = MedicineBatch.objects.filter(
            tenant=tenant,
            expiry_date__lte=cutoff,
            status=BatchStatus.ACTIVE,
            available_quantity__gt=Decimal('0.00')
        ).order_by('expiry_date')
        if branch:
            query = query.filter(branch=branch)
        return list(query)
