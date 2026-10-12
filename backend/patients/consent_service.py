from django.utils import timezone
from patients.models import PatientConsent

class ConsentService:
    @staticmethod
    def record_consent(tenant, patient, consent_type, title, content_text, signer_name, ip_address=None):
        return PatientConsent.objects.create(
            tenant=tenant, patient=patient, consent_type=consent_type,
            title=title, content_text=content_text, signer_name=signer_name,
            signature_ip=ip_address, is_granted=True, granted_at=timezone.now()
        )
