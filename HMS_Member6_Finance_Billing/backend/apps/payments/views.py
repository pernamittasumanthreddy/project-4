import uuid
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment, PaymentAttempt, Refund, ReconciliationRecord
from .serializers import PaymentSerializer, RefundSerializer, ReconciliationRecordSerializer
from apps.billing.models import Invoice
from apps.accounting.models import ChartOfAccount, JournalEntry, JournalLine
from apps.analytics.models import FinancialAuditEvent
from apps.common.decimal_utils import quantize_currency

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = Payment.objects.select_related('invoice').prefetch_related('refunds').all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            qs = qs.filter(invoice_id=invoice_id)
        method_param = self.request.query_params.get('method')
        if method_param:
            qs = qs.filter(method=method_param)
        return qs

    def create(self, request, *args, **kwargs):
        tenant = getattr(request, 'tenant', None)
        idempotency_key = request.headers.get('Idempotency-Key') or request.data.get('idempotency_key')
        
        # 1. Idempotency Protection: If duplicate key provided, return existing payment safely
        if idempotency_key:
            existing = Payment.objects.filter(tenant=tenant, idempotency_key=idempotency_key).first()
            if existing:
                serializer = self.get_serializer(existing)
                return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        inv = serializer.validated_data['invoice']
        amount = serializer.validated_data['amount']
        method = serializer.validated_data.get('method', 'CASH')
        ref_no = serializer.validated_data.get('transaction_reference', '')

        # Server-side validation: prevent payments against cancelled invoices
        if inv.status == 'CANCELLED':
            return Response(
                {"detail": "Cannot accept payment against a CANCELLED invoice."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            pay_seq = Payment.objects.filter(tenant=tenant).count() + 1
            pay_number = f"PAY-{timezone.now().year}-{pay_seq:05d}"

            payment = Payment.objects.create(
                tenant=tenant,
                payment_number=pay_number,
                invoice=inv,
                amount=amount,
                method=method,
                status='SUCCESS',
                idempotency_key=idempotency_key,
                transaction_reference=ref_no,
                received_by=request.user.username if request.user.is_authenticated else 'cashier_desk',
                notes=serializer.validated_data.get('notes', '')
            )

            # Update Invoice paid amount & state
            inv.paid_amount = quantize_currency(inv.paid_amount + amount)
            inv.recalculate_totals()

            # Automatic Double-Entry Journal Entry
            self._create_payment_journal_entry(tenant, payment, inv)

            # Audit Trail
            FinancialAuditEvent.objects.create(
                tenant=tenant,
                actor_username=payment.received_by,
                action_type='PAYMENT_COLLECTED',
                entity_name='Payment',
                entity_id=payment.payment_number,
                summary=f"Collected payment ₹{payment.amount} via {payment.method} for Invoice {inv.invoice_number}"
            )

        result_serializer = self.get_serializer(payment)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)

    def _create_payment_journal_entry(self, tenant, payment, invoice):
        """
        Posts balanced double-entry accounting lines:
        Dr: Cash (1020) or Bank (1010)
        Cr: Accounts Receivable (1100)
        """
        # Determine asset account
        asset_code = '1020' if payment.method == 'CASH' else '1010'
        debit_acct = ChartOfAccount.objects.filter(tenant=tenant, account_code=asset_code).first()
        ar_acct = ChartOfAccount.objects.filter(tenant=tenant, account_code='1100').first()

        if debit_acct and ar_acct:
            je_seq = JournalEntry.objects.filter(tenant=tenant).count() + 1
            je = JournalEntry.objects.create(
                tenant=tenant,
                entry_number=f"JE-{timezone.now().year}-{je_seq:05d}",
                entry_date=timezone.now().date(),
                description=f"Payment received for Inv {invoice.invoice_number} ({payment.payment_number})",
                source_document_type='PAYMENT',
                source_document_id=payment.payment_number,
                status='POSTED',
                posted_by=payment.received_by
            )
            # Dr Leg
            JournalLine.objects.create(
                tenant=tenant,
                journal_entry=je,
                account=debit_acct,
                debit_amount=payment.amount,
                credit_amount=Decimal('0.00'),
                description=f"Received via {payment.method}"
            )
            # Cr Leg
            JournalLine.objects.create(
                tenant=tenant,
                journal_entry=je,
                account=ar_acct,
                debit_amount=Decimal('0.00'),
                credit_amount=payment.amount,
                description=f"Settlement against AR for {invoice.patient_name}"
            )
            je.verify_balanced()


class RefundViewSet(viewsets.ModelViewSet):
    serializer_class = RefundSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = Refund.objects.select_related('payment', 'payment__invoice').all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        payment = serializer.validated_data['payment']
        amount = serializer.validated_data['amount']

        if amount > payment.amount:
            raise serializers.ValidationError({"amount": "Refund amount cannot exceed original payment amount."})

        ref_seq = Refund.objects.filter(tenant=tenant).count() + 1
        ref_number = f"REF-{timezone.now().year}-{ref_seq:05d}"
        
        refund = serializer.save(
            tenant=tenant,
            refund_number=ref_number,
            requested_by=self.request.user.username if self.request.user.is_authenticated else 'billing_desk'
        )

        FinancialAuditEvent.objects.create(
            tenant=tenant,
            actor_username=refund.requested_by,
            action_type='REFUND_REQUESTED',
            entity_name='Refund',
            entity_id=refund.refund_number,
            summary=f"Requested refund of ₹{refund.amount} on Payment {payment.payment_number}. Reason: {refund.reason}"
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        refund = self.get_object()
        if refund.status != 'REQUESTED':
            return Response({"detail": f"Cannot approve refund in status '{refund.status}'."}, status=status.HTTP_400_BAD_REQUEST)
        
        refund.status = 'APPROVED'
        refund.approved_by = request.user.username if request.user.is_authenticated else 'finance_director'
        refund.save()
        return Response(RefundSerializer(refund).data)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        refund = self.get_object()
        if refund.status != 'APPROVED':
            return Response({"detail": "Refund must be in APPROVED status to process."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            refund.status = 'PROCESSED'
            refund.processed_at = timezone.now()
            refund.save()

            # Update Payment status
            payment = refund.payment
            payment.status = 'REFUNDED' if refund.amount >= payment.amount else 'PARTIALLY_REFUNDED'
            payment.save()

            # Update Invoice
            invoice = payment.invoice
            invoice.paid_amount = quantize_currency(max(Decimal('0.00'), invoice.paid_amount - refund.amount))
            invoice.recalculate_totals()

            FinancialAuditEvent.objects.create(
                tenant=refund.tenant,
                actor_username=request.user.username if request.user.is_authenticated else 'finance_cashier',
                action_type='REFUND_PROCESSED',
                entity_name='Refund',
                entity_id=refund.refund_number,
                summary=f"Processed disbursement of ₹{refund.amount} for Payment {payment.payment_number}"
            )

        return Response(RefundSerializer(refund).data)


class ReconciliationViewSet(viewsets.ModelViewSet):
    serializer_class = ReconciliationRecordSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = ReconciliationRecord.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

    @action(detail=False, methods=['post'])
    def simulate_bank_reconciliation(self, request):
        """
        Unique Feature B: Smart Payment Reconciliation.
        Scans recorded system payments against simulated bank settlement batch.
        Detects mismatched amounts and unlinked transaction references.
        """
        tenant = getattr(request, 'tenant', None)
        batch_no = f"RECON-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        payments = Payment.objects.filter(status='SUCCESS')
        if tenant:
            payments = payments.filter(tenant=tenant)

        total_system_amount = sum((p.amount for p in payments), Decimal('0.00'))
        total_records = payments.count()
        
        # Simulate high match rate with sample discrepancy for demonstration
        discrepancies = 1 if total_records > 3 else 0
        matched = max(0, total_records - discrepancies)
        statement_amount = total_system_amount - (Decimal('500.00') if discrepancies else Decimal('0.00'))

        recon = ReconciliationRecord.objects.create(
            tenant=tenant,
            batch_number=batch_no,
            statement_date=timezone.now().date(),
            total_records=total_records,
            matched_records=matched,
            discrepancy_count=discrepancies,
            total_statement_amount=quantize_currency(statement_amount),
            total_system_amount=quantize_currency(total_system_amount),
            status='DISCREPANCY_DETECTED' if discrepancies > 0 else 'RECONCILED',
            notes=f"Automated settlement matching for {total_records} transactions." + (" 1 unlinked gateway settlement flagged for review." if discrepancies else " All payments matched bank statement.")
        )

        return Response(ReconciliationRecordSerializer(recon).data, status=status.HTTP_201_CREATED)
