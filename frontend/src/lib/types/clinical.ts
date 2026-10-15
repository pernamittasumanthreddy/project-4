import { DepartmentType, HospitalRole } from './roles';
export type { DepartmentType, HospitalRole };

/**
 * CLINICAL ENCOUNTER TYPES
 */
export type EncounterType = 
  | 'Outpatient Consultation'
  | 'Inpatient Daily Round'
  | 'Emergency Intake'
  | 'Telemedicine Review'
  | 'Specialist Referral'
  | 'Pre-Operative Assessment'
  | 'Post-Operative Follow-Up'
  | 'Discharge Evaluation';

export type EncounterStatus = 
  | 'Scheduled'
  | 'Waiting'
  | 'In Progress'
  | 'Completed'
  | 'Signed'
  | 'Amended'
  | 'Cancelled'
  | 'No Show';

export type RecordSignStatus = 'Draft' | 'Signed' | 'Amended' | 'Addendum Appended';

export type DiagnosisType = 'Primary' | 'Secondary' | 'Differential' | 'Chronic' | 'Admitting' | 'Discharge';

export type DiagnosisCertainty = 'Confirmed' | 'Presumptive' | 'Suspected' | 'Ruled Out';

export interface ICD10Diagnosis {
  id: string;
  code: string;
  description: string;
  type: DiagnosisType;
  certainty: DiagnosisCertainty;
  onsetDate?: string;
  notes?: string;
  diagnosedBy: string;
  diagnosedAt: string;
}

export interface PatientAllergy {
  id: string;
  patientId: string;
  allergen: string;
  category: 'Medication' | 'Food' | 'Environmental' | 'Biological' | 'Other';
  reaction: string;
  severity: 'Mild' | 'Moderate' | 'Severe' | 'Life Threatening / Anaphylaxis';
  verifiedDate: string;
  verifiedBy: string;
  status: 'Active' | 'Resolved' | 'Suspected';
}

export interface ClinicalVitals {
  systolicBp: number;
  diastolicBp: number;
  heartRate: number;
  respiratoryRate: number;
  spo2: number;
  temperature: number; // in Fahrenheit or Celsius
  tempUnit: 'F' | 'C';
  painScore: number; // 0 to 10 scale
  weightKg?: number;
  heightCm?: number;
  bmi?: number;
  gcsScore?: number; // Glasgow Coma Scale (3-15)
  bloodGlucoseMgDl?: number;
  recordedAt: string;
  recordedBy: string;
}

export interface PhysicalExamination {
  generalAppearance?: string;
  heent?: string; // Head, Eyes, Ears, Nose, Throat
  cardiovascular?: string;
  respiratory?: string;
  abdomen?: string;
  neurological?: string;
  musculoskeletal?: string;
  skinLympatics?: string;
  notes?: string;
}

export interface ClinicalAmendment {
  id: string;
  encounterId: string;
  version: number;
  amendmentType: 'Addendum' | 'Correction' | 'Clarification';
  amendedBy: string;
  amendedByRole: HospitalRole;
  amendedAt: string;
  reasonForAmendment: string;
  amendmentContent: string;
  previousContentSnapshot?: string;
  digitalSignatureHash: string;
}

export interface ClinicalEncounter {
  id: string; // e.g. "ENC-2026-1049"
  patientId: string;
  patientMrn: string;
  patientName: string;
  patientAge: number;
  patientGender: string;
  doctorId: string;
  doctorName: string;
  department: DepartmentType;
  encounterType: EncounterType;
  encounterDate: string;
  startTime: string;
  endTime?: string;
  status: EncounterStatus;
  signStatus: RecordSignStatus;
  
  // Clinical Documentation
  chiefComplaint: string;
  historyOfPresentIllness: string;
  pastMedicalHistory?: string;
  familyHistory?: string;
  socialHistory?: string;
  reviewOfSystems?: string;
  
  // Triage & Examination
  vitals?: ClinicalVitals;
  examination?: PhysicalExamination;
  
  // Clinical Assessment & SOAP
  subjectiveNotes: string;
  objectiveNotes: string;
  assessmentNotes: string;
  planNotes: string;
  
  // Codified clinical data
  diagnoses: ICD10Diagnosis[];
  allergiesSnapshot: string[];
  
  // Associated Clinical Orders
  prescriptionIds: string[];
  labOrderIds: string[];
  radiologyScanIds: string[];
  
  // Plan & Disposition
  treatmentPlan: string;
  patientInstructions: string;
  followUpDate?: string;
  referralId?: string;
  
  // Authorship & Immutability
  signedBy?: string;
  signedAt?: string;
  digitalSignatureHash?: string;
  amendments: ClinicalAmendment[];
  hospitalId: string;
}

/**
 * ELECTRONIC PRESCRIPTION TYPES (e-Prescription / CPOE)
 */
export interface PrescriptionItem {
  id: string;
  medicineId: string;
  medicineName: string;
  genericName: string;
  dosage: string;
  route: 'Oral' | 'IVPB Infusion' | 'IV Push' | 'Subcutaneous' | 'Inhalation' | 'Intramuscular' | 'Topical' | 'Ophthalmic';
  frequency: 'QD (Once Daily)' | 'BID (Twice Daily)' | 'TID (Three times daily)' | 'QID (Four times daily)' | 'PRN (As Needed)' | 'Q8H (Every 8 hours)' | 'Q12H (Every 12 hours)' | 'STAT (Immediately)';
  durationDays: number;
  quantity: number;
  instructions: string;
  indication: string;
  dispenseStatus: 'Pending' | 'Dispensed' | 'Substituted' | 'Cancelled';
  contraindicationFlag?: boolean;
  contraindicationNotes?: string;
}

export interface ElectronicPrescription {
  id: string; // e.g. "RX-88401"
  encounterId?: string;
  patientId: string;
  patientName: string;
  patientMrn: string;
  patientAge: number;
  doctorId: string;
  doctorName: string;
  doctorLicense: string;
  department: DepartmentType;
  prescribedDate: string;
  status: 'Pending' | 'Verified' | 'Dispensed' | 'Partially Dispensed' | 'Cancelled';
  items: PrescriptionItem[];
  clinicalIndication: string;
  allergiesChecked: boolean;
  knownAllergies: string[];
  refillsAllowed: number;
  digitalSignature: string;
  hospitalId: string;
}

/**
 * NURSING RECORDS & OBSERVATION CHARTS
 */
export interface MEWSCalculation {
  score: number; // 0 to 14
  riskCategory: 'Low Risk (0-1)' | 'Medium Risk (2-3)' | 'High Alert (4-5)' | 'Critical Deterioration (>=6)';
  actionRequired: string;
}

export interface NursingObservation {
  id: string;
  patientId: string;
  patientName: string;
  mrn: string;
  ward: string;
  bed: string;
  timestamp: string;
  nurseId: string;
  nurseName: string;
  
  // Vitals
  systolicBp: number;
  diastolicBp: number;
  heartRate: number;
  respiratoryRate: number;
  spo2: number;
  temperature: number;
  painScore: number;
  gcsScore: number; // 3-15
  avpuConsciousness: 'Alert' | 'Voice' | 'Pain' | 'Unresponsive';
  bloodSugarMgDl?: number;
  oxygenDevice?: 'Room Air' | 'Nasal Cannula 2L' | 'Venturi Mask' | 'Non-Rebreather' | 'BiPAP' | 'Mechanical Ventilator';
  
  // Scoring
  mews: MEWSCalculation;
  
  // Clinical Notes
  nursingInterventions: string;
  telemetryRhythm?: 'Normal Sinus' | 'Sinus Tachycardia' | 'Sinus Bradycardia' | 'Atrial Fibrillation' | 'Paced';
  fallRiskScore?: number; // Morse Fall Scale
  bradenSkinScore?: number; // Pressure injury risk
}

export interface FluidBalanceRecord {
  id: string;
  patientId: string;
  patientName: string;
  ward: string;
  bed: string;
  timestamp: string;
  nurseName: string;
  
  // Intake (mL)
  oralIntakeMl: number;
  ivInfusionMl: number;
  enteralFeedMl: number;
  bloodProductMl: number;
  totalIntakeMl: number;
  
  // Output (mL)
  urineOutputMl: number;
  surgicalDrainMl: number;
  ngAspirateMl: number;
  emesisMl: number;
  totalOutputMl: number;
  
  // Balance
  netBalanceMl: number; // totalIntake - totalOutput
  shift: 'Day' | 'Evening' | 'Night';
  cumulative24hBalanceMl: number;
  notes?: string;
}

export interface EMARRecord {
  id: string;
  patientId: string;
  prescriptionId: string;
  medicineName: string;
  dosage: string;
  route: string;
  scheduledTime: string;
  administeredTime?: string;
  administeredBy?: string;
  witnessNurse?: string;
  status: 'Due' | 'Administered' | 'Held' | 'Refused' | 'Omitted';
  notes?: string;
  vitalsBeforeAdmin?: string; // e.g., "HR 74, BP 124/82 before beta-blocker"
}

export interface SBARHandoverNote {
  id: string;
  patientId: string;
  patientName: string;
  ward: string;
  bed: string;
  createdDate: string;
  fromNurse: string;
  toNurse: string;
  shift: 'Day to Evening' | 'Evening to Night' | 'Night to Day';
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
  codeStatus: 'Full Code' | 'DNR / DNI' | 'Modified Code';
  keyTasksForNextShift: string[];
}

/**
 * DISCHARGE SUMMARIES (IPD)
 */
export interface DischargeSummary {
  id: string;
  admissionId: string;
  patientId: string;
  patientName: string;
  mrn: string;
  age: number;
  gender: string;
  ward: string;
  bed: string;
  admissionDate: string;
  dischargeDate: string;
  admittingDiagnosis: string;
  dischargeDiagnosis: string;
  secondaryDiagnoses: string[];
  
  // Clinical Narrative
  hospitalCourse: string;
  proceduresPerformed: string[];
  significantFindings: string;
  conditionAtDischarge: 'Stable / Improved' | 'Good' | 'Fair' | 'Transferred to Specialized Facility' | 'Against Medical Advice (AMA)';
  
  // Post-discharge Care
  dischargeMedications: {
    medicineName: string;
    dosage: string;
    frequency: string;
    duration: string;
    specialInstructions: string;
  }[];
  dietInstructions: string;
  activityRestrictions: string;
  woundCareInstructions?: string;
  warningSignsRedFlags: string[];
  followUpAppointments: {
    department: DepartmentType;
    doctorName: string;
    scheduledDate: string;
    instructions: string;
  }[];
  
  // Attending Physician Sign-Off
  attendingDoctorId: string;
  attendingDoctorName: string;
  signedAt: string;
  digitalSignature: string;
  status: 'Draft' | 'Final Signed';
  hospitalId: string;
}

/**
 * CLINICAL REFERRAL WORKFLOW
 */
export interface ClinicalReferral {
  id: string;
  patientId: string;
  patientName: string;
  mrn: string;
  encounterId?: string;
  referringDoctorId: string;
  referringDoctorName: string;
  referringDepartment: DepartmentType;
  targetDepartment: DepartmentType;
  targetDoctorName?: string;
  urgency: 'Routine' | 'Urgent (<24h)' | 'Emergency / Stat';
  referralReason: string;
  clinicalSummary: string;
  requestedInvestigations: string[];
  status: 'Draft' | 'Submitted' | 'Accepted' | 'In Consultation' | 'Completed' | 'Declined';
  scheduledDate?: string;
  consultantNotes?: string;
  createdAt: string;
  updatedAt: string;
  hospitalId: string;
}

/**
 * CLINICAL DOCUMENTATION TEMPLATES
 */
export interface ClinicalTemplate {
  id: string;
  title: string;
  department: DepartmentType;
  encounterType: EncounterType;
  description: string;
  defaultChiefComplaint: string;
  subjectiveTemplate: string;
  objectiveTemplate: string;
  assessmentTemplate: string;
  planTemplate: string;
  commonDiagnoses: { code: string; desc: string }[];
}
