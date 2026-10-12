from decimal import Decimal
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import BillingEntity, ServicePrice, Invoice, InvoiceLine, CreditNote
from .serializers import (
    BillingEntitySerializer, ServicePriceSerializer,
    InvoiceSerializer, CreateInvoiceSerializer, CreditNoteSerializer
)
from apps.analytics.models import FinancialAuditEvent
from apps.common.decimal_utils import quantize_currency

class BillingEntityViewSet(viewsets.ModelViewSet):
    serializer_class = BillingEntitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return BillingEntity.objects.filter(tenant=tenant)
        return BillingEntity.objects.all()

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)


class ServicePriceViewSet(viewsets.ModelViewSet):
    serializer_class = ServicePriceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = ServicePrice.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        dept = self.request.query_params.get('department')
        if dept:
            qs = qs.filter(department=dept)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)


class InvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = Invoice.objects.prefetch_related('lines', 'credit_notes', 'payments').all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        patient_param = self.request.query_params.get('patient_id')
        if patient_param:
            qs = qs.filter(patient_id=patient_param)

        search_param = self.request.query_params.get('search')
        if search_param:
            qs = qs.filter(invoice_number__icontains=search_param) | qs.filter(patient_name__icontains=search_param)

        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateInvoiceSerializer
        return InvoiceSerializer

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        invoice = serializer.save(tenant=tenant)
        FinancialAuditEvent.objects.create(
            tenant=tenant,
            actor_username=self.request.user.username if self.request.user.is_authenticated else 'billing_officer',
            action_type='INVOICE_ISSUED',
            entity_name='Invoice',
            entity_id=invoice.invoice_number,
            summary=f"Issued invoice {invoice.invoice_number} for {invoice.patient_name} amounting to ₹{invoice.total_net}"
        )

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """
        Unique Feature A: Unified Financial Timeline.
        Aggregates every financial event attached to this invoice chronologically.
        """
        invoice = self.get_object()
        events = []

        # 1. Invoice Issuance Event
        events.append({
            "event_type": "INVOICE_CREATED",
            "title": f"Invoice {invoice.invoice_number} Issued",
            "timestamp": invoice.created_at,
            "amount": str(invoice.total_net),
            "actor": invoice.created_by,
            "status": invoice.status,
            "details": f"Itemized bill generated for {invoice.patient_name} ({invoice.encounter_type})"
        })

        # 2. Payments
        for p in invoice.payments.all():
            events.append({
                "event_type": "PAYMENT_RECORDED",
                "title": f"Payment {p.payment_number} ({p.get_method_display()})",
                "timestamp": p.created_at,
                "amount": str(p.amount),
                "actor": p.received_by,
                "status": p.status,
                "details": f"Ref: {p.transaction_reference or 'N/A'}"
            })
            for r in p.refunds.all():
                events.append({
                    "event_type": "REFUND_EVENT",
                    "title": f"Refund {r.refund_number} ({r.get_status_display()})",
                    "timestamp": r.created_at,
                    "amount": str(r.amount),
                    "actor": r.approved_by or r.requested_by,
                    "status": r.status,
                    "details": f"Reason: {r.reason}"
                })

        # 3. Credit Notes
        for cn in invoice.credit_notes.all():
            events.append({
                "event_type": "CREDIT_NOTE_APPLIED",
                "title": f"Credit Note {cn.credit_note_number}",
                "timestamp": cn.created_at,
                "amount": str(cn.amount),
                "actor": cn.approved_by,
                "status": cn.status,
                "details": f"Concession / adjustment: {cn.reason}"
            })

        # 4. Insurance Claims
        for clm in invoice.insurance_claims.all():
            events.append({
                "event_type": "INSURANCE_CLAIM_EVENT",
                "title": f"Claim {clm.claim_number} ({clm.payer.name})",
                "timestamp": clm.created_at,
                "amount": str(clm.claim_amount),
                "actor": "claims_desk",
                "status": clm.status,
                "details": f"Approved: ₹{clm.approved_amount}, Copay: ₹{clm.patient_copay_amount}"
            })

        # Sort chronologically
        events.sort(key=lambda x: str(x['timestamp']))

        return Response({
            "invoice_number": invoice.invoice_number,
            "patient_name": invoice.patient_name,
            "total_net": str(invoice.total_net),
            "paid_amount": str(invoice.paid_amount),
            "balance_due": str(invoice.balance_due),
            "status": invoice.status,
            "events": events
        })


class CreditNoteViewSet(viewsets.ModelViewSet):
    serializer_class = CreditNoteSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = CreditNote.objects.select_related('invoice').all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        with transaction.atomic():
            cn = serializer.save(tenant=tenant)
            inv = cn.invoice
            # Deduct balance due by credit note amount
            inv.recalculate_totals()
            inv.balance_due = quantize_currency(max(Decimal('0.00'), inv.balance_due - cn.amount))
            inv.save()
            FinancialAuditEvent.objects.create(
                tenant=tenant,
                actor_username=self.request.user.username if self.request.user.is_authenticated else 'finance_officer',
                action_type='CREDIT_NOTE_ISSUED',
                entity_name='CreditNote',
                entity_id=cn.credit_note_number,
                summary=f"Credit Note ₹{cn.amount} applied to invoice {inv.invoice_number}. Reason: {cn.reason}"
            )
