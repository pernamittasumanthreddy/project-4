from decimal import Decimal
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import InsurancePayer, InsurancePolicy, InsuranceClaim, DenialLog
from .serializers import (
    InsurancePayerSerializer, InsurancePolicySerializer,
    InsuranceClaimSerializer, DenialLogSerializer
)
from apps.analytics.models import FinancialAuditEvent
from apps.common.decimal_utils import quantize_currency

class InsurancePayerViewSet(viewsets.ModelViewSet):
    serializer_class = InsurancePayerSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = InsurancePayer.objects.all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)


class InsurancePolicyViewSet(viewsets.ModelViewSet):
    serializer_class = InsurancePolicySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = InsurancePolicy.objects.select_related('payer').all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        patient_param = self.request.query_params.get('patient_id')
        if patient_param:
            qs = qs.filter(patient_id=patient_param)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        serializer.save(tenant=tenant)


class InsuranceClaimViewSet(viewsets.ModelViewSet):
    serializer_class = InsuranceClaimSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        qs = InsuranceClaim.objects.select_related('invoice', 'payer', 'policy').prefetch_related('denial_logs').all()
        if tenant:
            qs = qs.filter(tenant=tenant)
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        payer_param = self.request.query_params.get('payer_id')
        if payer_param:
            qs = qs.filter(payer_id=payer_param)
        return qs

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        claim_seq = InsuranceClaim.objects.filter(tenant=tenant).count() + 1
        claim_number = f"CLM-{timezone.now().year}-{claim_seq:05d}"
        
        claim = serializer.save(
            tenant=tenant,
            claim_number=claim_number,
            status='SUBMITTED'
        )

        FinancialAuditEvent.objects.create(
            tenant=tenant,
            actor_username=self.request.user.username if self.request.user.is_authenticated else 'tpa_coordinator',
            action_type='CLAIM_SUBMITTED',
            entity_name='InsuranceClaim',
            entity_id=claim.claim_number,
            summary=f"Claim {claim.claim_number} of ₹{claim.claim_amount} submitted to {claim.payer.name}"
        )

    @action(detail=True, methods=['post'])
    def adjudicate(self, request, pk=None):
        """
        Adjudicate an insurance claim:
        Payload: {
            "status": "APPROVED" | "PARTIALLY_APPROVED" | "REJECTED",
            "approved_amount": 45000.00,
            "patient_copay_amount": 5000.00,
            "deductible_amount": 0.00,
            "denial_code": "DOCS_MISSING" (if partial or rejected),
            "denial_reason": "Explanation..."
        }
        """
        claim = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['APPROVED', 'PARTIALLY_APPROVED', 'REJECTED']:
            return Response({"detail": "Invalid adjudication status."}, status=status.HTTP_400_BAD_REQUEST)

        claim.status = new_status
        claim.adjudication_date = timezone.now().date()
        claim.approved_amount = quantize_currency(request.data.get('approved_amount', claim.claim_amount if new_status == 'APPROVED' else 0))
        claim.patient_copay_amount = quantize_currency(request.data.get('patient_copay_amount', 0))
        claim.deductible_amount = quantize_currency(request.data.get('deductible_amount', 0))
        claim.denial_reason = request.data.get('denial_reason', '')

        # If rejected or partially approved, log into Denial Workbench
        if new_status in ['REJECTED', 'PARTIALLY_APPROVED']:
            DenialLog.objects.create(
                tenant=claim.tenant,
                claim=claim,
                denial_code=request.data.get('denial_code', 'DOCS_MISSING'),
                denial_reason=claim.denial_reason or 'Claim deduction/denial issued by TPA adjudicator.',
                resolved=False
            )

        claim.save()

        FinancialAuditEvent.objects.create(
            tenant=claim.tenant,
            actor_username=request.user.username if request.user.is_authenticated else 'tpa_adjudicator',
            action_type=f'CLAIM_{new_status}',
            entity_name='InsuranceClaim',
            entity_id=claim.claim_number,
            summary=f"Claim {claim.claim_number} adjudicated as {new_status}. Approved: ₹{claim.approved_amount}"
        )

        return Response(InsuranceClaimSerializer(claim).data)

    @action(detail=True, methods=['post'])
    def resubmit(self, request, pk=None):
        """
        Unique Feature C: Insurance Claim Denial Workbench Resubmission.
        Resolves deficiencies and resubmits to insurer with corrective action notes.
        """
        claim = self.get_object()
        corrective_action = request.data.get('corrective_action', 'Discharge summary and test reports attached.')
        
        claim.status = 'RESUBMITTED'
        claim.save()

        # Update last denial log
        latest_log = claim.denial_logs.filter(resolved=False).first()
        if latest_log:
            latest_log.resolved = True
            latest_log.corrective_action_taken = corrective_action
            latest_log.resubmitted_claim_reference = f"{claim.claim_number}-R1"
            latest_log.save()

        FinancialAuditEvent.objects.create(
            tenant=claim.tenant,
            actor_username=request.user.username if request.user.is_authenticated else 'claims_officer',
            action_type='CLAIM_RESUBMITTED',
            entity_name='InsuranceClaim',
            entity_id=claim.claim_number,
            summary=f"Claim {claim.claim_number} resubmitted to {claim.payer.name}. Action: {corrective_action}"
        )

        return Response(InsuranceClaimSerializer(claim).data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def denial_workbench(request):
    """
    Dedicated workbench for denied and partially approved insurance claims.
    """
    tenant = getattr(request, 'tenant', None)
    qs = InsuranceClaim.objects.filter(status__in=['REJECTED', 'PARTIALLY_APPROVED', 'RESUBMITTED'])
    if tenant:
        qs = qs.filter(tenant=tenant)
    serializer = InsuranceClaimSerializer(qs, many=True)
    return Response(serializer.data)
