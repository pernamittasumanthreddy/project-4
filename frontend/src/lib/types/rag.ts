import { HospitalRole, DepartmentType } from './roles';

export type DocumentCategory =
  | 'A. Hospital Policies'
  | 'B. Department Information'
  | 'C. Admission Procedures'
  | 'D. Discharge Procedures'
  | 'E. Emergency Procedures'
  | 'F. Clinical Guidelines'
  | 'G. Medicine Information'
  | 'H. Pharmacy Policies'
  | 'I. Laboratory Guidelines'
  | 'J. Radiology Guidelines'
  | 'K. Insurance Policies'
  | 'L. Billing Policies'
  | 'M. Patient Education'
  | 'N. Staff Policies'
  | 'O. HR Policies'
  | 'P. Employee Handbook'
  | 'Q. Infection Control'
  | 'R. Safety Procedures'
  | 'S. Hospital SOPs'
  | 'T. Appointment Policies'
  | 'U. Visiting Policies'
  | 'V. Consent Forms'
  | 'W. Privacy Policies'
  | 'X. Data Protection Policies'
  | 'Y. Equipment Manuals'
  | 'Z. Hospital Announcements'
  | 'Patient Medical Records'
  | 'Prescription Records'
  | 'Lab Test Reports'
  | 'Radiology Reports'
  | 'Discharge Summaries';

export type ConfidentialityLevel = 'PUBLIC' | 'INTERNAL' | 'RESTRICTED' | 'CONFIDENTIAL' | 'STRICTLY_CONFIDENTIAL';

export interface HospitalDocument {
  id: string; // e.g. "DOC-ADMIT-01"
  title: string;
  category: DocumentCategory;
  department: DepartmentType | 'General Hospital';
  version: string; // "v2.1"
  effectiveDate: string;
  lastUpdated: string;
  confidentiality: ConfidentialityLevel;
  roleAccess: HospitalRole[];
  patientId?: string; // If patient-specific document
  fileType: 'PDF' | 'DOCX' | 'TXT' | 'XLSX';
  fileSize: string;
  sourceUri: string;
  isArchived: boolean;
  content: string; // Full text content
  sections?: {
    heading: string;
    page: number;
    text: string;
  }[];
}

export interface DocumentChunk {
  id: string;
  documentId: string;
  documentTitle: string;
  category: DocumentCategory;
  department: DepartmentType | 'General Hospital';
  roleAccess: HospitalRole[];
  confidentiality: ConfidentialityLevel;
  patientId?: string;
  lastUpdated: string;
  version: string;
  pageNumber: number;
  section: string;
  content: string;
  tags: string[];
  embedding?: number[];
}

export interface RAGRoleConfig {
  role: HospitalRole;
  displayName: string;
  ragTitle: string; // e.g., "Clinical & Patient Knowledge Assistant"
  knowledgeScopeDescription: string;
  allowedCategories: DocumentCategory[];
  allowedPatientScope: 'ALL' | 'ASSIGNED_ONLY' | 'OWN_RECORD_ONLY' | 'NONE';
  allowedConfidentiality: ConfidentialityLevel[];
  systemPrompt: string;
  suggestedQuestions: string[];
  responseRules: string[];
  citationRules: string[];
}

export interface Citation {
  documentId: string;
  documentTitle: string;
  category: DocumentCategory;
  section: string;
  pageNumber?: number;
  lastUpdated: string;
  version: string;
  relevanceScore: number; // 0.0 - 1.0
  snippet: string;
}

export interface RAGQueryResult {
  queryId: string;
  question: string;
  role: HospitalRole;
  answer: string;
  citations: Citation[];
  confidenceScore: number; // e.g. 0.94
  confidenceLevel: 'High' | 'Moderate' | 'Low' | 'Uncertain';
  isGrounded: boolean;
  sourceCount: number;
  retrievalLatencyMs: number;
  generationLatencyMs: number;
  totalLatencyMs: number;
  verificationBadge: string; // "This answer is based on hospital documents"
  safetyNotice?: string;
  evaluatedAt: string;
}

export interface RAGEvaluationMetrics {
  retrievalAccuracy: number; // % e.g. 98.4
  precisionAtK: number; // e.g. 0.94
  recallAtK: number; // e.g. 0.91
  mrr: number; // Mean Reciprocal Rank e.g. 0.93
  faithfulnessScore: number; // % e.g. 99.2 (zero hallucinations)
  answerRelevance: number; // % e.g. 96.8
  citationAccuracy: number; // % e.g. 99.5
  hallucinationRate: number; // % e.g. 0.0%
  averageLatencyMs: number; // e.g. 340ms
  totalQueriesEvaluated: number;
  queriesPerRole: Record<string, number>;
  topQueriedCategories: { category: string; count: number }[];
  mostRetrievedDocuments: { title: string; count: number }[];
}
