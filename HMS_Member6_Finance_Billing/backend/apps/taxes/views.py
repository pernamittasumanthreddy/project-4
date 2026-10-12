from decimal import Decimal
from django.db.models import Sum
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import TaxConfiguration, TaxTransaction
from .serializers import TaxConfigurationSerializer, TaxTransactionSerializer
from apps.billing.models import Invoice

class TaxConfigurationViewSet(viewsets.ModelViewSet):
    serializer_class = TaxConfigurationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return TaxConfiguration.objects.filter(tenant=tenant)
        return TaxConfiguration.objects.all()

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)


class TaxTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaxTransactionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return TaxTransaction.objects.filter(tenant=tenant)
        return TaxTransaction.objects.all()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def tax_summary_report(request):
    """
    Returns GST GSTR-1 summary totals for the active tenant.
    """
    tenant = getattr(request, 'tenant', None)
    invoices = Invoice.objects.filter(status__in=['ISSUED', 'PARTIALLY_PAID', 'PAID'])
    if tenant:
        invoices = invoices.filter(tenant=tenant)

    totals = invoices.aggregate(
        total_taxable=Sum('total_taxable'),
        total_cgst=Sum('total_cgst'),
        total_sgst=Sum('total_sgst'),
        total_igst=Sum('total_igst'),
        total_tax=Sum('total_tax')
    )

    data = {
        "tenant_id": tenant.id if tenant else "all",
        "taxable_turnover": str(totals['total_taxable'] or Decimal('0.00')),
        "cgst_collected": str(totals['total_cgst'] or Decimal('0.00')),
        "sgst_collected": str(totals['total_sgst'] or Decimal('0.00')),
        "igst_collected": str(totals['total_igst'] or Decimal('0.00')),
        "total_tax_collected": str(totals['total_tax'] or Decimal('0.00')),
        "active_slabs": TaxConfigurationSerializer(
            TaxConfiguration.objects.filter(tenant=tenant) if tenant else TaxConfiguration.objects.all(),
            many=True
        ).data
    }
    return Response(data)
