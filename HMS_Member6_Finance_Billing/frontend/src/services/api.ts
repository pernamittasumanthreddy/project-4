import {
  Tenant, Branch, BillingEntity, TaxConfiguration, ServicePrice, Invoice,
  InvoiceTimelineResponse, Payment, Refund, ReconciliationRecord,
  InsurancePayer, InsurancePolicy, InsuranceClaim, ChartOfAccount,
  JournalEntry, FinancialPeriod, PayableRecord, ARAgingResponse,
  DashboardKPIs, IntegrityReport, FinancialAuditEvent
} from '../types/finance';

const BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
  private currentTenantId: string = 'tenant-apollo-01';

  setTenant(tenantId: string) {
    this.currentTenantId = tenantId;
  }

  getTenantId() {
    return this.currentTenantId;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers = {
      'Content-Type': 'application/json',
      'X-Tenant-ID': this.currentTenantId,
      ...(options.headers || {})
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(err.detail || JSON.stringify(err));
    }

    return response.json();
  }

  // Tenants
  async getTenants(): Promise<Tenant[]> {
    const res = await this.request<any>('/tenants/');
    return res.results || res;
  }

  async getBranches(): Promise<Branch[]> {
    const res = await this.request<any>('/branches/');
    return res.results || res;
  }

  // Dashboard & Analytics
  async getDashboardKPIs(): Promise<DashboardKPIs> {
    return this.request<DashboardKPIs>('/analytics/dashboard/');
  }

  async getIntegrityReport(): Promise<IntegrityReport> {
    return this.request<IntegrityReport>('/analytics/integrity-monitor/');
  }

  async getAuditEvents(): Promise<FinancialAuditEvent[]> {
    const res = await this.request<any>('/analytics/audit-events/');
    return res.results || res;
  }

  // Billing
  async getBillingEntities(): Promise<BillingEntity[]> {
    const res = await this.request<any>('/billing/entities/');
    return res.results || res;
  }

  async getServices(): Promise<ServicePrice[]> {
    const res = await this.request<any>('/billing/services/');
    return res.results || res;
  }

  async getInvoices(search?: string, statusFilter?: string): Promise<Invoice[]> {
    let url = '/billing/invoices/?';
    if (search) url += `search=${encodeURIComponent(search)}&`;
    if (statusFilter && statusFilter !== 'ALL') url += `status=${statusFilter}&`;
    const res = await this.request<any>(url);
    return res.results || res;
  }

  async createInvoice(data: any): Promise<Invoice> {
    return this.request<Invoice>('/billing/invoices/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async getInvoiceTimeline(invoiceId: string): Promise<InvoiceTimelineResponse> {
    return this.request<InvoiceTimelineResponse>(`/billing/invoices/${invoiceId}/timeline/`);
  }

  // Payments
  async getPayments(): Promise<Payment[]> {
    const res = await this.request<any>('/payments/records/');
    return res.results || res;
  }

  async createPayment(data: { invoice: string; amount: string; method: string; transaction_reference?: string; notes?: string; idempotency_key?: string }): Promise<Payment> {
    const headers: Record<string, string> = {};
    if (data.idempotency_key) {
      headers['Idempotency-Key'] = data.idempotency_key;
    }
    return this.request<Payment>('/payments/records/', {
      method: 'POST',
      headers,
      body: JSON.stringify(data)
    });
  }

  async getRefunds(): Promise<Refund[]> {
    const res = await this.request<any>('/payments/refunds/');
    return res.results || res;
  }

  async createRefund(data: { payment: string; amount: string; reason: string }): Promise<Refund> {
    return this.request<Refund>('/payments/refunds/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async approveRefund(refundId: string): Promise<Refund> {
    return this.request<Refund>(`/payments/refunds/${refundId}/approve/`, {
      method: 'POST'
    });
  }

  async processRefund(refundId: string): Promise<Refund> {
    return this.request<Refund>(`/payments/refunds/${refundId}/process/`, {
      method: 'POST'
    });
  }

  async getReconciliations(): Promise<ReconciliationRecord[]> {
    const res = await this.request<any>('/payments/reconciliation/');
    return res.results || res;
  }

  async simulateBankReconciliation(): Promise<ReconciliationRecord> {
    return this.request<ReconciliationRecord>('/payments/reconciliation/simulate_bank_reconciliation/', {
      method: 'POST'
    });
  }

  // Insurance
  async getInsurancePayers(): Promise<InsurancePayer[]> {
    const res = await this.request<any>('/insurance/payers/');
    return res.results || res;
  }

  async getInsurancePolicies(): Promise<InsurancePolicy[]> {
    const res = await this.request<any>('/insurance/policies/');
    return res.results || res;
  }

  async getInsuranceClaims(): Promise<InsuranceClaim[]> {
    const res = await this.request<any>('/insurance/claims/');
    return res.results || res;
  }

  async getDenialWorkbench(): Promise<InsuranceClaim[]> {
    return this.request<InsuranceClaim[]>('/insurance/denial-workbench/');
  }

  async adjudicateClaim(claimId: string, data: any): Promise<InsuranceClaim> {
    return this.request<InsuranceClaim>(`/insurance/claims/${claimId}/adjudicate/`, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async resubmitClaim(claimId: string, correctiveAction: string): Promise<InsuranceClaim> {
    return this.request<InsuranceClaim>(`/insurance/claims/${claimId}/resubmit/`, {
      method: 'POST',
      body: JSON.stringify({ corrective_action: correctiveAction })
    });
  }

  // Taxes
  async getTaxConfigs(): Promise<TaxConfiguration[]> {
    const res = await this.request<any>('/taxes/configurations/');
    return res.results || res;
  }

  async getTaxSummary(): Promise<any> {
    return this.request<any>('/taxes/summary/');
  }

  // Accounting
  async getChartOfAccounts(): Promise<ChartOfAccount[]> {
    const res = await this.request<any>('/accounting/accounts/');
    return res.results || res;
  }

  async getTrialBalance(): Promise<any> {
    return this.request<any>('/accounting/accounts/trial_balance/');
  }

  async getJournalEntries(): Promise<JournalEntry[]> {
    const res = await this.request<any>('/accounting/journals/');
    return res.results || res;
  }

  async createJournalEntry(data: any): Promise<JournalEntry> {
    return this.request<JournalEntry>('/accounting/journals/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async getFinancialPeriods(): Promise<FinancialPeriod[]> {
    const res = await this.request<any>('/accounting/periods/');
    return res.results || res;
  }

  async closeFinancialPeriod(periodId: string, notes: string): Promise<FinancialPeriod> {
    return this.request<FinancialPeriod>(`/accounting/periods/${periodId}/close_period/`, {
      method: 'POST',
      body: JSON.stringify({ notes })
    });
  }

  async getAccountsReceivable(): Promise<ARAgingResponse> {
    return this.request<ARAgingResponse>('/accounting/receivables/');
  }

  async getPayableRecords(): Promise<PayableRecord[]> {
    const res = await this.request<any>('/accounting/payables/');
    return res.results || res;
  }
}

export const api = new ApiService();
