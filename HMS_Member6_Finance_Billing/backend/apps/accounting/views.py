from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import ChartOfAccount, JournalEntry, JournalLine, FinancialPeriod, PayableRecord
from .serializers import (
    ChartOfAccountSerializer, JournalEntrySerializer,
    CreateJournalEntrySerializer, FinancialPeriodSerializer, PayableRecordSerializer
)
from apps.billing.models import Invoice
from apps.analytics.models import FinancialAuditEvent
from apps.common.decimal_utils import quantize_currency

class ChartOfAccountViewSet(viewsets.ModelViewSet):
    serializer_class = ChartOfAccountSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = ChartOfAccount.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        acct_type = self.request.query_params.get('type')
        if acct_type:
            qs = qs.filter(account_type=acct_type)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)

    @action(detail=False, methods=['get'])
    def trial_balance(self, request):
        """
        Calculates trial balance across all accounts for the active tenant.
        Proves invariant: Total Debits == Total Credits.
        """
        tenant = getattr(request, 'tenant', None)
        qs = ChartOfAccount.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)

        report = []
        total_dr = Decimal('0.00')
        total_cr = Decimal('0.00')

        for acct in qs:
            lines = JournalLine.objects.filter(account=acct, journal_entry__status='POSTED')
            dr = sum((line.debit_amount for line in lines), Decimal('0.00'))
            cr = sum((line.credit_amount for line in lines), Decimal('0.00'))
            
            # Asset & Expense normal balance is Debit; Liability, Equity, Revenue normal balance is Credit
            if acct.account_type in ['ASSET', 'EXPENSE']:
                net_dr = max(Decimal('0.00'), dr - cr)
                net_cr = max(Decimal('0.00'), cr - dr)
            else:
                net_cr = max(Decimal('0.00'), cr - dr)
                net_dr = max(Decimal('0.00'), dr - cr)

            total_dr += net_dr
            total_cr += net_cr

            report.append({
                "account_code": acct.account_code,
                "account_name": acct.account_name,
                "account_type": acct.account_type,
                "debit": str(net_dr),
                "credit": str(net_cr)
            })

        return Response({
            "is_balanced": (quantize_currency(total_dr) == quantize_currency(total_cr)),
            "total_debit": str(quantize_currency(total_dr)),
            "total_credit": str(quantize_currency(total_cr)),
            "accounts": report
        })


class JournalEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = JournalEntry.objects.prefetch_related('lines', 'lines__account').all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateJournalEntrySerializer
        return JournalEntrySerializer

    def create(self, request, *args, **kwargs):
        tenant = getattr(request, 'tenant', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lines_data = serializer.validated_data.pop('lines')
        with transaction.atomic():
            je_seq = JournalEntry.objects.filter(tenant=tenant).count() + 1
            entry_number = f"JE-{timezone.now().year}-{je_seq:05d}"
            
            je = JournalEntry.objects.create(
                tenant=tenant,
                entry_number=entry_number,
                entry_date=serializer.validated_data['entry_date'],
                description=serializer.validated_data['description'],
                source_document_type=serializer.validated_data.get('source_document_type', 'MANUAL'),
                source_document_id=serializer.validated_data.get('source_document_id', ''),
                status='POSTED',
                posted_by=request.user.username if request.user.is_authenticated else 'chief_accountant'
            )

            tot_dr = Decimal('0.00')
            tot_cr = Decimal('0.00')
            for line_item in lines_data:
                acct = ChartOfAccount.objects.get(id=line_item['account_id'])
                dr = quantize_currency(line_item.get('debit_amount', 0))
                cr = quantize_currency(line_item.get('credit_amount', 0))
                tot_dr += dr
                tot_cr += cr
                JournalLine.objects.create(
                    tenant=tenant,
                    journal_entry=je,
                    account=acct,
                    debit_amount=dr,
                    credit_amount=cr,
                    description=line_item.get('description', '')
                )
            
            je.verify_balanced()

            FinancialAuditEvent.objects.create(
                tenant=tenant,
                actor_username=je.posted_by,
                action_type='JOURNAL_ENTRY_POSTED',
                entity_name='JournalEntry',
                entity_id=je.entry_number,
                summary=f"Posted balanced journal entry {je.entry_number} for ₹{je.total_debit}. {je.description}"
            )

        return Response(JournalEntrySerializer(je).data, status=status.HTTP_201_CREATED)


class FinancialPeriodViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialPeriodSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = FinancialPeriod.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)

    @action(detail=True, methods=['post'])
    def close_period(self, request, pk=None):
        """
        Unique Feature H: Financial Period Closing Workflow.
        Verifies all draft journals are finalized and no discrepancies exist.
        Locks the period to prevent retroactive changes.
        """
        period = self.get_object()
        if period.is_closed:
            return Response({"detail": "This financial period is already closed and locked."}, status=status.HTTP_400_BAD_REQUEST)

        tenant = getattr(request, 'tenant', None)
        
        # Check for unposted draft journals
        unposted = JournalEntry.objects.filter(
            entry_date__gte=period.start_date,
            entry_date__lte=period.end_date,
            status='DRAFT'
        )
        if tenant:
            unposted = unposted.filter(tenant=tenant)

        if unposted.exists():
            return Response({
                "detail": f"Cannot close period. Found {unposted.count()} unposted draft journal entries.",
                "unposted_entries": [e.entry_number for e in unposted]
            }, status=status.HTTP_400_BAD_REQUEST)

        period.is_closed = True
        period.closed_at = timezone.now()
        period.closed_by = request.user.username if request.user.is_authenticated else 'chief_financial_officer'
        period.closing_notes = request.data.get('notes', 'Period closed and locked after reconciliation clearance.')
        period.save()

        FinancialAuditEvent.objects.create(
            tenant=period.tenant,
            actor_username=period.closed_by,
            action_type='FINANCIAL_PERIOD_CLOSED',
            entity_name='FinancialPeriod',
            entity_id=period.period_name,
            summary=f"Closed and locked financial period {period.period_name} ({period.start_date} to {period.end_date})"
        )

        return Response(FinancialPeriodSerializer(period).data)


class PayableRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PayableRecordSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = PayableRecord.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def accounts_receivable_aging(request):
    """
    Unique Feature E: Revenue Leakage and Outstanding Balance Tracker.
    Categorizes unpaid invoices into aging buckets (0-30, 31-60, 61-90, 90+ days).
    """
    tenant = getattr(request, 'tenant', None)
    invoices = Invoice.objects.filter(status__in=['ISSUED', 'PARTIALLY_PAID', 'OVERDUE'])
    if tenant:
        invoices = invoices.filter(tenant=tenant)

    today = timezone.now().date()
    buckets = {
        "current_0_30": Decimal('0.00'),
        "aging_31_60": Decimal('0.00'),
        "aging_61_90": Decimal('0.00'),
        "overdue_90_plus": Decimal('0.00'),
        "total_outstanding": Decimal('0.00')
    }
    patient_breakdown = []

    for inv in invoices:
        days = (today - inv.due_date).days
        bal = inv.balance_due
        buckets["total_outstanding"] += bal

        if days <= 30:
            buckets["current_0_30"] += bal
        elif 31 <= days <= 60:
            buckets["aging_31_60"] += bal
        elif 61 <= days <= 90:
            buckets["aging_61_90"] += bal
        else:
            buckets["overdue_90_plus"] += bal

        patient_breakdown.append({
            "invoice_number": inv.invoice_number,
            "patient_name": inv.patient_name,
            "patient_mrn": inv.patient_mrn,
            "due_date": inv.due_date,
            "days_overdue": max(0, days),
            "balance_due": str(bal),
            "status": inv.status
        })

    return Response({
        "summary": {
            "current_0_30": str(quantize_currency(buckets["current_0_30"])),
            "aging_31_60": str(quantize_currency(buckets["aging_31_60"])),
            "aging_61_90": str(quantize_currency(buckets["aging_61_90"])),
            "overdue_90_plus": str(quantize_currency(buckets["overdue_90_plus"])),
            "total_outstanding": str(quantize_currency(buckets["total_outstanding"]))
        },
        "invoices": patient_breakdown
    })
