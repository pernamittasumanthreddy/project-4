"""HMS Pharmacy UI Views — Member 5
Renders server-side hospital interface templates integrated with multi-tenant context.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from pharmacy.models import (
    Medicine,
    MedicineBatch,
    Supplier,
    PurchaseOrder,
    DispenseRecord,
    StockMovement,
    StockQuarantine,
    StockCountSession,
)
from clinical.models import Prescription, PrescriptionStatus
from pharmacy.services.alert_service import AlertService
from pharmacy.services.report_service import ReportService
from pharmacy.services.dispensing_service import DispensingService


def pharmacy_dashboard(request):
    """Pharmacy overview dashboard with real-time alerts and KPI metrics."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    alerts = AlertService.get_alerts_summary(tenant, branch)
    valuation = ReportService.get_stock_valuation(tenant, branch)
    recent_movements = StockMovement.objects.filter(tenant=tenant).order_by('-created_at')[:8]
    pending_prescriptions = Prescription.objects.filter(
        tenant=tenant,
        status__in=[PrescriptionStatus.PENDING, PrescriptionStatus.PARTIALLY_DISPENSED]
    ).order_by('-created_at')[:5]

    context = {
        'alerts': alerts,
        'valuation': valuation,
        'recent_movements': recent_movements,
        'pending_prescriptions': pending_prescriptions,
        'page_title': 'Pharmacy & Inventory Dashboard'
    }
    return render(request, 'pharmacy/dashboard.html', context)


def medicine_catalogue(request):
    """Medicine catalogue search, listing, and inventory status."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    search = request.GET.get('search', '')
    queryset = Medicine.objects.filter(tenant=tenant, is_deleted=False)
    if search:
        queryset = queryset.filter(
            brand_name__icontains=search
        ) | queryset.filter(
            generic_name__icontains=search
        ) | queryset.filter(
            code__icontains=search
        )

    medicines = list(queryset.order_by('brand_name'))
    # Precompute stock levels
    for med in medicines:
        med.stock_level = med.get_total_stock(branch=branch)
        med.low_stock = med.is_low_stock(branch=branch)

    context = {
        'medicines': medicines,
        'search_query': search,
        'page_title': 'Medicine Catalogue'
    }
    return render(request, 'pharmacy/catalogue.html', context)


def batch_management(request):
    """Batch-wise stock tracking, FEFO ordering, and expiration countdown."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    batches = MedicineBatch.objects.filter(tenant=tenant)
    if branch:
        batches = batches.filter(branch=branch)

    status_filter = request.GET.get('status', '')
    if status_filter:
        batches = batches.filter(status=status_filter)

    batches = batches.order_by('expiry_date')

    context = {
        'batches': batches,
        'status_filter': status_filter,
        'page_title': 'Batch & Expiry Management'
    }
    return render(request, 'pharmacy/batches.html', context)


def dispensing_queue(request):
    """Prescription dispensing queue fulfilling clinical orders."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    prescriptions = Prescription.objects.filter(
        tenant=tenant,
        status__in=[PrescriptionStatus.PENDING, PrescriptionStatus.PARTIALLY_DISPENSED]
    ).order_by('-created_at')

    recent_dispensations = DispenseRecord.objects.filter(tenant=tenant).order_by('-created_at')[:10]

    context = {
        'prescriptions': prescriptions,
        'recent_dispensations': recent_dispensations,
        'page_title': 'Prescription Dispensing'
    }
    return render(request, 'pharmacy/dispensing.html', context)


def purchasing_management(request):
    """Purchase orders and goods receipt dashboard."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    orders = PurchaseOrder.objects.filter(tenant=tenant).order_by('-created_at')
    suppliers = Supplier.objects.filter(tenant=tenant, is_active=True)

    context = {
        'orders': orders,
        'suppliers': suppliers,
        'page_title': 'Purchase Orders & Inward'
    }
    return render(request, 'pharmacy/purchasing.html', context)


def returns_and_quarantine(request):
    """Medication returns and quarantine inspection area."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    quarantines = StockQuarantine.objects.filter(tenant=tenant, is_resolved=False).order_by('-created_at')

    context = {
        'quarantines': quarantines,
        'page_title': 'Returns & Quarantine'
    }
    return render(request, 'pharmacy/returns.html', context)


def reconciliation_dashboard(request):
    """Physical inventory counting and audit reconciliation sessions."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    sessions = StockCountSession.objects.filter(tenant=tenant).order_by('-created_at')

    context = {
        'sessions': sessions,
        'page_title': 'Inventory Reconciliation'
    }
    return render(request, 'pharmacy/reconciliation.html', context)


def reports_dashboard(request):
    """Stock valuation, wastage analysis, and CSV/PDF export generation."""
    tenant = getattr(request, 'tenant', None)
    branch = getattr(request, 'branch', None)

    valuation = ReportService.get_stock_valuation(tenant, branch)

    context = {
        'valuation': valuation,
        'page_title': 'Pharmacy Reports & Exports'
    }
    return render(request, 'pharmacy/reports.html', context)
