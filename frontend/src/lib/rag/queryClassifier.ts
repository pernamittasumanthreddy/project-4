export interface QueryClassification {
  intent: 'CLINICAL_GUIDELINE' | 'POLICY_SOP' | 'PATIENT_RECORD' | 'MEDICATION_FORMULARY' | 'BILLING_INSURANCE' | 'EMERGENCY_TRAUMA' | 'GENERAL_HOSPITAL';
  isAutonomousDiagnosisRequest: boolean;
  isPrescriptionRequest: boolean;
  isAcuteEmergency: boolean;
  extractedKeywords: string[];
  safetyNotice?: string;
}

export class QueryClassifier {
  public classify(query: string): QueryClassification {
    const qLower = query.toLowerCase();

    // Check for autonomous medical diagnosis attempts
    const isAutonomousDiagnosisRequest = (
      qLower.includes('diagnose') ||
      qLower.includes('what disease do i have') ||
      qLower.includes('what is wrong with me') ||
      qLower.includes('do i have cancer') ||
      qLower.includes('tell me what is causing my chest pain') ||
      qLower.includes('what illness is this')
    );

    // Check for independent prescription attempt
    const isPrescriptionRequest = (
      qLower.includes('prescribe me') ||
      qLower.includes('what should i take for') ||
      qLower.includes('order this drug for me') ||
      qLower.includes('prescribe medication')
    );

    // Check for acute emergency keywords
    const isAcuteEmergency = (
      qLower.includes('code blue') ||
      qLower.includes('cardiac arrest') ||
      qLower.includes('massive trauma') ||
      qLower.includes('unresponsive patient') ||
      qLower.includes('severe anaphylaxis')
    );

    let intent: QueryClassification['intent'] = 'GENERAL_HOSPITAL';

    if (qLower.includes('emergency') || qLower.includes('triage') || qLower.includes('code blue') || qLower.includes('stemi') || qLower.includes('stroke') || qLower.includes('trauma')) {
      intent = 'EMERGENCY_TRAUMA';
    } else if (qLower.includes('sepsis') || qLower.includes('guideline') || qLower.includes('protocol') || qLower.includes('egfr') || qLower.includes('radiation') || qLower.includes('mri')) {
      intent = 'CLINICAL_GUIDELINE';
    } else if (qLower.includes('medication') || qLower.includes('drug') || qLower.includes('formulary') || qLower.includes('dispens') || qLower.includes('cold chain') || qLower.includes('storage') || qLower.includes('pharmacy')) {
      intent = 'MEDICATION_FORMULARY';
    } else if (qLower.includes('patient') || qLower.includes('lab') || qLower.includes('troponin') || qLower.includes('vital') || qLower.includes('mrn') || qLower.includes('pt-10023') || qLower.includes('history')) {
      intent = 'PATIENT_RECORD';
    } else if (qLower.includes('bill') || qLower.includes('insurance') || qLower.includes('tariff') || qLower.includes('refund') || qLower.includes('claim') || qLower.includes('pre-auth') || qLower.includes('copay')) {
      intent = 'BILLING_INSURANCE';
    } else if (qLower.includes('policy') || qLower.includes('sop') || qLower.includes('visitor') || qLower.includes('admission') || qLower.includes('discharge') || qLower.includes('leave') || qLower.includes('handbook')) {
      intent = 'POLICY_SOP';
    }

    let safetyNotice: string | undefined;
    if (isAutonomousDiagnosisRequest) {
      safetyNotice = 'I can provide information from approved hospital documents, but I cannot independently diagnose a medical condition. Please consult an authorized healthcare professional.';
    } else if (isPrescriptionRequest) {
      safetyNotice = 'I can reference approved hospital formulary medications and dosing guidelines, but I cannot independently prescribe medications. Prescriptions must be authored by a licensed physician.';
    }

    return {
      intent,
      isAutonomousDiagnosisRequest,
      isPrescriptionRequest,
      isAcuteEmergency,
      extractedKeywords: qLower.split(/\s+/).filter(w => w.length > 3),
      safetyNotice
    };
  }
}
