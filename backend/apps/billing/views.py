"""
Billing Views (Member 6 integration contract).
Provides invoice summaries, itemized charges, and simulated sandbox payments.
"""

from decimal import Decimal
from datetime import datetime
import uuid
import random
from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.billing.models import Invoice, Payment
from apps.billing.serializers import InvoiceSerializer, PaymentSerializer

class InvoiceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        qs = Invoice.objects.all().select_related('patient__user', 'tenant').prefetch_related('payments')
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)

        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)

        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param.upper())

        return qs


class InvoiceDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class PaymentSandboxProcessView(views.APIView):
    """
    Simulated Sandbox Payment Gateway Processor.
    Allows testing invoice settlement in local development with zero external API credentials.
    Generates verifiable receipt number and updates balance.
    """
    permission_classes = [AllowAny]

    def post(self, request, invoice_id):
        invoice = Invoice.objects.filter(id=invoice_id).first()
        if not invoice:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

        if invoice.balance_due <= Decimal('0.00'):
            return Response(
                {"error": "This invoice is already fully paid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount_str = request.data.get('amount')
        amount = Decimal(str(amount_str)) if amount_str else invoice.balance_due

        if amount <= Decimal('0.00'):
            return Response({"error": "Payment amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get('payment_method', 'CREDIT_CARD')
        receipt_no = f"REC-{datetime.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
        ref_no = f"PAY-SIM-{uuid.uuid4().hex[:12].upper()}"

        payment = Payment.objects.create(
            tenant=invoice.tenant,
            branch=invoice.branch,
            invoice=invoice,
            payment_reference=ref_no,
            receipt_number=receipt_no,
            amount=amount,
            payment_method=payment_method,
            status='SUCCESS',
            is_sandbox_simulation=True,
            notes=f"Simulated local payment via {payment_method}. No real bank credentials billed."
        )

        invoice.paid_amount += amount
        invoice.update_totals()
        invoice.save()

        # Trigger notification
        try:
            from apps.notifications.services import NotificationDispatcher
            NotificationDispatcher.dispatch_payment_receipt_generated(payment)
        except Exception:
            pass

        return Response({
            "success": True,
            "message": f"Payment of ${amount:.2f} processed successfully in sandbox mode.",
            "payment": PaymentSerializer(payment).data,
            "invoice": InvoiceSerializer(invoice).data,
        })
