"""
Pharmacy Views (Member 5 integration contract).
Provides formulary search, medication stock, and dispensing history.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.pharmacy.models import Medication, DispensingOrder
from apps.pharmacy.serializers import MedicationSerializer, DispensingOrderSerializer

class MedicationListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MedicationSerializer

    def get_queryset(self):
        qs = Medication.objects.all()
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(generic_name__icontains=search) | qs.filter(brand_name__icontains=search)
        return qs


class DispensingOrderListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DispensingOrderSerializer

    def get_queryset(self):
        qs = DispensingOrder.objects.all().select_related('patient', 'prescription')
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            qs = qs.filter(tenant=tenant)
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        return qs
