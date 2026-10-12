from decimal import Decimal
from django.db.models import Sum, Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import FinancialAuditEvent
from .serializers import FinancialAuditEventSerializer
from apps.billing.models import Invoice, InvoiceLine
from apps.payments.models import Payment, Refund
from apps.insurance.models import InsuranceClaim
from apps.accounting.models import JournalEntry
from apps.common.decimal_utils import quantize_currency

class FinancialAuditEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FinancialAuditEventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = FinancialAuditEvent.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        action_param = self.request.query_params.get('action_type')
        if action_param:
            qs = qs.filter(action_type=action_param)
        return qs


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def finance_dashboard_kpis(request):
    """
    Module 6.6: Financial Analytics & KPI Summary.
    Calculates live metrics strictly derived from persisted database records.
    """
    tenant = getattr(request, 'tenant', None)
    inv_qs = Invoice.objects.all()
    pay_qs = Payment.objects.filter(status='SUCCESS')
    clm_qs = InsuranceClaim.objects.all()
    lines_qs = InvoiceLine.objects.all()

    if tenant:
        inv_qs = inv_qs.filter(tenant=tenant)
        pay_qs = pay_qs.filter(tenant=tenant)
        clm_qs = clm_qs.filter(tenant=tenant)
        lines_qs = lines_qs.filter(tenant=tenant)

    # Invoicing aggregations
    billed_total = inv_qs.exclude(status='CANCELLED').aggregate(Sum('total_net'))['total_net__sum'] or Decimal('0.00')
    outstanding_total = inv_qs.exclude(status__in=['CANCELLED', 'PAID']).aggregate(Sum('balance_due'))['balance_due__sum'] or Decimal('0.00')
    collected_total = pay_qs.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Insurance claims
    total_claims_count = clm_qs.count()
    approved_claims_count = clm_qs.filter(status__in=['APPROVED', 'SETTLED']).count()
    rejected_claims_count = clm_qs.filter(status='REJECTED').count()
    pending_claims_count = clm_qs.filter(status__in=['SUBMITTED', 'PENDING_REVIEW', 'PRE_AUTH_PENDING']).count()
    pending_claims_amount = clm_qs.filter(status__in=['SUBMITTED', 'PENDING_REVIEW']).aggregate(Sum('claim_amount'))['claim_amount__sum'] or Decimal('0.00')

    # Department-wise revenue breakdown
    dept_revenue = {}
    for item in lines_qs.values('department').annotate(rev=Sum('net_amount')):
        dept_revenue[item['department']] = str(quantize_currency(item['rev'] or Decimal('0.00')))

    # Collection efficiency percentage
    efficiency_pct = Decimal('0.00')
    if billed_total > Decimal('0.00'):
        efficiency_pct = quantize_currency((collected_total / billed_total) * Decimal('100.00'))

    return Response({
        "total_billed": str(quantize_currency(billed_total)),
        "total_collected": str(quantize_currency(collected_total)),
        "outstanding_receivables": str(quantize_currency(outstanding_total)),
        "collection_efficiency_percentage": str(efficiency_pct),
        "insurance_kpis": {
            "total_claims": total_claims_count,
            "pending_claims": pending_claims_count,
            "pending_amount": str(quantize_currency(pending_claims_amount)),
            "approved_claims": approved_claims_count,
            "rejected_claims": rejected_claims_count
        },
        "department_revenue": dept_revenue,
        "recent_invoices_count": inv_qs.count(),
        "recent_payments_count": pay_qs.count()
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def financial_integrity_monitor(request):
    """
    Unique Feature D: Real-Time Financial Integrity Monitor.
    Runs automated forensic integrity scans across all ledger, invoice, payment, and refund records.
    """
    tenant = getattr(request, 'tenant', None)
    flags = []

    # 1. Unbalanced Journal Check (Double-entry invariant)
    journals = JournalEntry.objects.all()
    if tenant:
        journals = journals.filter(tenant=tenant)
    for je in journals:
        if je.total_debit != je.total_credit:
            flags.append({
                "severity": "CRITICAL",
                "category": "DOUBLE_ENTRY_UNBALANCED",
                "record_id": je.entry_number,
                "message": f"Journal Entry {je.entry_number} is unbalanced. Debit ₹{je.total_debit} != Credit ₹{je.total_credit}.",
                "remediation": "Review and post compensating adjusting journal line."
            })

    # 2. Duplicate Payment Reference Check
    payments = Payment.objects.filter(status='SUCCESS').exclude(transaction_reference='')
    if tenant:
        payments = payments.filter(tenant=tenant)
    ref_counts = {}
    for p in payments:
        ref = p.transaction_reference.strip()
        ref_counts[ref] = ref_counts.get(ref, [])
        ref_counts[ref].append(p.payment_number)

    for ref, p_list in ref_counts.items():
        if len(p_list) > 1:
            flags.append({
                "severity": "HIGH",
                "category": "DUPLICATE_PAYMENT_REFERENCE",
                "record_id": ref,
                "message": f"Bank reference '{ref}' is attached to multiple payments ({', '.join(p_list)}).",
                "remediation": "Audit bank settlement statement to rule out duplicate crediting."
            })

    # 3. Invoice Calculation Line Check
    invoices = Invoice.objects.exclude(status='CANCELLED')
    if tenant:
        invoices = invoices.filter(tenant=tenant)
    for inv in invoices:
        line_sum = sum((line.net_amount for line in inv.lines.all()), Decimal('0.00'))
        if quantize_currency(inv.total_net) != quantize_currency(line_sum):
            flags.append({
                "severity": "HIGH",
                "category": "INVOICE_TOTAL_MISMATCH",
                "record_id": inv.invoice_number,
                "message": f"Invoice {inv.invoice_number} header net ₹{inv.total_net} does not match sum of lines ₹{line_sum}.",
                "remediation": "Execute recalculate_totals() on invoice record."
            })

    # 4. Suspicious Refund Frequency Check
    refunds = Refund.objects.all()
    if tenant:
        refunds = refunds.filter(tenant=tenant)
    pay_refund_counts = {}
    for r in refunds:
        p_num = r.payment.payment_number
        pay_refund_counts[p_num] = pay_refund_counts.get(p_num, 0) + 1
    for p_num, count in pay_refund_counts.items():
        if count > 1:
            flags.append({
                "severity": "MEDIUM",
                "category": "MULTIPLE_REFUNDS_ON_PAYMENT",
                "record_id": p_num,
                "message": f"Payment {p_num} has {count} refund requests logged against it.",
                "remediation": "Verify authorization and cumulative refund limit before disbursing."
            })

    # Calculate overall integrity score
    score = 100
    for f in flags:
        if f['severity'] == 'CRITICAL':
            score -= 30
        elif f['severity'] == 'HIGH':
            score -= 15
        elif f['severity'] == 'MEDIUM':
            score -= 5
    score = max(0, score)

    return Response({
        "integrity_score": score,
        "status": "HEALTHY" if score >= 90 else ("NEEDS_ATTENTION" if score >= 70 else "ACTION_REQUIRED"),
        "total_checks_run": 5,
        "flagged_issues_count": len(flags),
        "issues": flags
    })
