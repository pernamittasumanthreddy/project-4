// Member 6 Finance & Billing TypeScript Domain Definitions

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  domain?: string;
  subscription_tier: 'STARTER' | 'PRO' | 'ENTERPRISE';
  default_currency: string;
  is_active: boolean;
  branches: Branch[];
}

export interface Branch {
  id: string;
  name: string;
  code: string;
  city: string;
  state_code: string;
  gstin?: string;
  address?: string;
  phone?: string;
}

export interface BillingEntity {
  id: string;
  name: string;
  legal_name: string;
  gstin: string;
  pan: string;
  state_code: string;
  state_name: string;
  address: string;
  contact_phone: string;
  contact_email: string;
  invoice_prefix: string;
  invoice_next_seq: number;
}

export interface TaxConfiguration {
  id: string;
  code: string;
  name: string;
  rate_percentage: string;
  cgst_rate: string;
  sgst_rate: string;
  igst_rate: string;
  hsn_sac_code: string;
  is_default: boolean;
  is_active: boolean;
  description?: string;
}

export interface ServicePrice {
  id: string;
  code: string;
  name: string;
  department: 'OPD' | 'IPD' | 'LAB' | 'RAD' | 'PHARM' | 'SURG' | 'PROC';
  department_display: string;
  base_amount: string;
  hsn_sac_code: string;
  tax_config?: string;
  tax_rate?: string;
}

export interface InvoiceLine {
  id?: string;
  service_code: string;
  service_name: string;
  department: string;
  quantity: string | number;
  unit_price: string | number;
  discount_amount: string | number;
  hsn_sac_code: string;
  tax_config?: string;
  tax_rate?: string;
  gross_amount?: string;
  taxable_amount?: string;
  cgst_amount?: string;
  sgst_amount?: string;
  igst_amount?: string;
  tax_amount?: string;
  net_amount?: string;
}

export interface CreditNote {
  id: string;
  credit_note_number: string;
  invoice: string;
  invoice_number?: string;
  amount: string;
  reason: string;
  status: 'DRAFT' | 'APPROVED' | 'APPLIED' | 'VOID';
  approved_by: string;
  created_at: string;
}

export interface Invoice {
  id: string;
  invoice_number: string;
  billing_entity: string;
  billing_entity_name?: string;
  billing_entity_gstin?: string;
  patient_id: string;
  patient_name: string;
  patient_mrn: string;
  patient_state_code: string;
  encounter_id?: string;
  encounter_type: 'OPD' | 'IPD' | 'EMERGENCY' | 'DAYCARE';
  status: 'DRAFT' | 'ISSUED' | 'PARTIALLY_PAID' | 'PAID' | 'OVERDUE' | 'CANCELLED';
  issue_date: string;
  due_date: string;
  total_gross: string;
  total_discount: string;
  total_taxable: string;
  total_cgst: string;
  total_sgst: string;
  total_igst: string;
  total_tax: string;
  total_net: string;
  paid_amount: string;
  balance_due: string;
  is_interstate: boolean;
  notes?: string;
  terms?: string;
  lines: InvoiceLine[];
  credit_notes?: CreditNote[];
  created_at: string;
}

export interface TimelineEvent {
  event_type: string;
  title: string;
  timestamp: string;
  amount: string;
  actor: string;
  status: string;
  details: string;
}

export interface InvoiceTimelineResponse {
  invoice_number: string;
  patient_name: string;
  total_net: string;
  paid_amount: string;
  balance_due: string;
  status: string;
  events: TimelineEvent[];
}

export interface Payment {
  id: string;
  payment_number: string;
  invoice: string;
  invoice_number?: string;
  patient_name?: string;
  amount: string;
  method: 'CASH' | 'CARD' | 'UPI' | 'WIRE_TRANSFER' | 'CHEQUE' | 'INSURANCE_SETTLEMENT';
  method_display: string;
  status: 'SUCCESS' | 'PENDING' | 'FAILED' | 'REFUNDED' | 'PARTIALLY_REFUNDED';
  idempotency_key?: string;
  transaction_reference?: string;
  received_by: string;
  notes?: string;
  created_at: string;
}

export interface Refund {
  id: string;
  refund_number: string;
  payment: string;
  payment_number?: string;
  invoice_number?: string;
  amount: string;
  reason: string;
  status: 'REQUESTED' | 'APPROVED' | 'PROCESSED' | 'REJECTED';
  requested_by: string;
  approved_by?: string;
  processed_at?: string;
  created_at: string;
}

export interface ReconciliationRecord {
  id: string;
  batch_number: string;
  statement_date: string;
  total_records: number;
  matched_records: number;
  discrepancy_count: number;
  total_statement_amount: string;
  total_system_amount: string;
  status: 'RECONCILED' | 'DISCREPANCY_DETECTED' | 'IN_REVIEW';
  notes: string;
  created_at: string;
}

export interface InsurancePayer {
  id: string;
  code: string;
  name: string;
  payer_type: 'PRIVATE_INSURER' | 'GOVERNMENT_SCHEME' | 'CORPORATE_TPA';
  payer_type_display: string;
  tpa_contact_email?: string;
  tpa_contact_phone?: string;
  settlement_tat_days: number;
  is_active: boolean;
}

export interface InsurancePolicy {
  id: string;
  patient_id: string;
  patient_name: string;
  payer: string;
  payer_name?: string;
  policy_number: string;
  card_number?: string;
  sum_insured: string;
  copay_percentage: string;
  valid_from: string;
  valid_to: string;
}

export interface DenialLog {
  id: string;
  claim: string;
  denial_code: string;
  denial_code_display: string;
  denial_reason: string;
  corrective_action_taken?: string;
  resubmitted_claim_reference?: string;
  logged_at: string;
  resolved: boolean;
}

export interface InsuranceClaim {
  id: string;
  claim_number: string;
  invoice: string;
  invoice_number?: string;
  patient_name?: string;
  payer: string;
  payer_name?: string;
  policy?: string;
  pre_auth_number?: string;
  claim_amount: string;
  approved_amount: string;
  patient_copay_amount: string;
  deductible_amount: string;
  settled_amount: string;
  status: 'PREPARING' | 'PRE_AUTH_PENDING' | 'SUBMITTED' | 'PENDING_REVIEW' | 'APPROVED' | 'PARTIALLY_APPROVED' | 'REJECTED' | 'RESUBMITTED' | 'SETTLED';
  status_display: string;
  submission_date: string;
  adjudication_date?: string;
  denial_reason?: string;
  denial_logs: DenialLog[];
  created_at: string;
}

export interface ChartOfAccount {
  id: string;
  account_code: string;
  account_name: string;
  account_type: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'EXPENSE';
  account_type_display: string;
  current_balance: string;
  is_active: boolean;
}

export interface JournalLine {
  id?: string;
  account: string;
  account_code?: string;
  account_name?: string;
  debit_amount: string;
  credit_amount: string;
  description?: string;
}

export interface JournalEntry {
  id: string;
  entry_number: string;
  entry_date: string;
  description: string;
  source_document_type: string;
  source_type_display: string;
  status: 'DRAFT' | 'POSTED' | 'REVERSED';
  status_display: string;
  total_debit: string;
  total_credit: string;
  posted_by: string;
  posted_at: string;
  lines: JournalLine[];
}

export interface FinancialPeriod {
  id: string;
  period_name: string;
  start_date: string;
  end_date: string;
  is_closed: boolean;
  closed_at?: string;
  closed_by?: string;
  closing_notes?: string;
}

export interface PayableRecord {
  id: string;
  vendor_name: string;
  bill_number: string;
  category: string;
  due_date: string;
  total_amount: string;
  paid_amount: string;
  balance_due: string;
  status: 'PENDING' | 'PARTIALLY_PAID' | 'PAID' | 'OVERDUE';
  status_display: string;
  created_at: string;
}

export interface ARAgingSummary {
  current_0_30: string;
  aging_31_60: string;
  aging_61_90: string;
  overdue_90_plus: string;
  total_outstanding: string;
}

export interface ARAgingResponse {
  summary: ARAgingSummary;
  invoices: Array<{
    invoice_number: string;
    patient_name: string;
    patient_mrn: string;
    due_date: string;
    days_overdue: number;
    balance_due: string;
    status: string;
  }>;
}

export interface DashboardKPIs {
  total_billed: string;
  total_collected: string;
  outstanding_receivables: string;
  collection_efficiency_percentage: string;
  insurance_kpis: {
    total_claims: number;
    pending_claims: number;
    pending_amount: string;
    approved_claims: number;
    rejected_claims: number;
  };
  department_revenue: Record<string, string>;
  recent_invoices_count: number;
  recent_payments_count: number;
}

export interface IntegrityIssue {
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM';
  category: string;
  record_id: string;
  message: string;
  remediation: string;
}

export interface IntegrityReport {
  integrity_score: number;
  status: 'HEALTHY' | 'NEEDS_ATTENTION' | 'ACTION_REQUIRED';
  total_checks_run: number;
  flagged_issues_count: number;
  issues: IntegrityIssue[];
}

export interface FinancialAuditEvent {
  id: string;
  actor_username: string;
  action_type: string;
  entity_name: string;
  entity_id: string;
  summary: string;
  changes_json: Record<string, any>;
  ip_address?: string;
  created_at: string;
}
