import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar, ViewKey } from './components/Sidebar';
import { api } from './services/api';
import {
  Tenant, BillingEntity, ServicePrice, TaxConfiguration, Invoice,
  Payment, Refund, ReconciliationRecord, InsurancePayer, InsurancePolicy,
  InsuranceClaim, ChartOfAccount, JournalEntry, FinancialPeriod,
  PayableRecord, DashboardKPIs, IntegrityReport
} from './types/finance';

// Modals
import { NewInvoiceModal } from './components/NewInvoiceModal';
import { NewPaymentModal } from './components/NewPaymentModal';
import { InvoicePrintModal } from './components/InvoicePrintModal';
import { NewJournalEntryModal } from './components/NewJournalEntryModal';

// Views
import { FinanceDashboardView } from './views/FinanceDashboardView';
import { InvoiceManagementView } from './views/InvoiceManagementView';
import { InvoiceDetailsTimelineView } from './views/InvoiceDetailsTimelineView';
import { PaymentsReceiptsView } from './views/PaymentsReceiptsView';
import { RefundManagementView } from './views/RefundManagementView';
import { PaymentReconciliationView } from './views/PaymentReconciliationView';
import { InsurancePayersPoliciesView } from './views/InsurancePayersPoliciesView';
import { InsuranceClaimsWorkbenchView } from './views/InsuranceClaimsWorkbenchView';
import { GSTTaxConfigurationView } from './views/GSTTaxConfigurationView';
import { ChartOfAccountsView } from './views/ChartOfAccountsView';
import { JournalEntriesGLView } from './views/JournalEntriesGLView';
import { AccountsReceivableView } from './views/AccountsReceivableView';
import { AccountsPayableView } from './views/AccountsPayableView';
import { FinancialReportsAnalyticsView } from './views/FinancialReportsAnalyticsView';
import { FinancialIntegrityMonitorView } from './views/FinancialIntegrityMonitorView';
import { FinancialPeriodClosingView } from './views/FinancialPeriodClosingView';
import { FinanceAuditLogView } from './views/FinanceAuditLogView';
import { FinanceSettingsPoliciesView } from './views/FinanceSettingsPoliciesView';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewKey>('dashboard');
  const [activeTenantId, setActiveTenantId] = useState('tenant-apollo-01');
  const [isLoading, setIsLoading] = useState(false);

  // Core Data States
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [billingEntities, setBillingEntities] = useState<BillingEntity[]>([]);
  const [services, setServices] = useState<ServicePrice[]>([]);
  const [taxConfigs, setTaxConfigs] = useState<TaxConfiguration[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [refunds, setRefunds] = useState<Refund[]>([]);
  const [reconciliations, setReconciliations] = useState<ReconciliationRecord[]>([]);
  const [payers, setPayers] = useState<InsurancePayer[]>([]);
  const [policies, setPolicies] = useState<InsurancePolicy[]>([]);
  const [claims, setClaims] = useState<InsuranceClaim[]>([]);
  const [accounts, setAccounts] = useState<ChartOfAccount[]>([]);
  const [journals, setJournals] = useState<JournalEntry[]>([]);
  const [periods, setPeriods] = useState<FinancialPeriod[]>([]);
  const [payables, setPayables] = useState<PayableRecord[]>([]);
  const [kpis, setKpis] = useState<DashboardKPIs | null>(null);
  const [integrityReport, setIntegrityReport] = useState<IntegrityReport | null>(null);

  // Modal States
  const [isNewInvoiceOpen, setIsNewInvoiceOpen] = useState(false);
  const [isNewPaymentOpen, setIsNewPaymentOpen] = useState(false);
  const [paymentInvoiceId, setPaymentInvoiceId] = useState<string | undefined>(undefined);
  const [isNewJournalOpen, setIsNewJournalOpen] = useState(false);
  const [printingInvoice, setPrintingInvoice] = useState<Invoice | null>(null);
  const [selectedTimelineInvoice, setSelectedTimelineInvoice] = useState<Invoice | null>(null);

  useEffect(() => {
    loadAllData();
  }, [activeTenantId]);

  const loadAllData = async () => {
    setIsLoading(true);
    api.setTenant(activeTenantId);
    try {
      const [
        tList, beList, sList, tcList, invList, payList, refList,
        recList, payrList, polList, clmList, acctList, jList,
        perList, paybList, kpiData, intData
      ] = await Promise.allSettled([
        api.getTenants(),
        api.getBillingEntities(),
        api.getServices(),
        api.getTaxConfigs(),
        api.getInvoices(),
        api.getPayments(),
        api.getRefunds(),
        api.getReconciliations(),
        api.getInsurancePayers(),
        api.getInsurancePolicies(),
        api.getInsuranceClaims(),
        api.getChartOfAccounts(),
        api.getJournalEntries(),
        api.getFinancialPeriods(),
        api.getPayableRecords(),
        api.getDashboardKPIs(),
        api.getIntegrityReport()
      ]);

      if (tList.status === 'fulfilled' && tList.value.length > 0) setTenants(tList.value);
      if (beList.status === 'fulfilled') setBillingEntities(beList.value);
      if (sList.status === 'fulfilled') setServices(sList.value);
      if (tcList.status === 'fulfilled') setTaxConfigs(tcList.value);
      if (invList.status === 'fulfilled') setInvoices(invList.value);
      if (payList.status === 'fulfilled') setPayments(payList.value);
      if (refList.status === 'fulfilled') setRefunds(refList.value);
      if (recList.status === 'fulfilled') setReconciliations(recList.value);
      if (payrList.status === 'fulfilled') setPayers(payrList.value);
      if (polList.status === 'fulfilled') setPolicies(polList.value);
      if (clmList.status === 'fulfilled') setClaims(clmList.value);
      if (acctList.status === 'fulfilled') setAccounts(acctList.value);
      if (jList.status === 'fulfilled') setJournals(jList.value);
      if (perList.status === 'fulfilled') setPeriods(perList.value);
      if (paybList.status === 'fulfilled') setPayables(paybList.value);
      if (kpiData.status === 'fulfilled') setKpis(kpiData.value);
      if (intData.status === 'fulfilled') setIntegrityReport(intData.value);
    } catch (err) {
      console.error('Data loading error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handlers
  const handleTenantChange = (tenantId: string) => {
    setActiveTenantId(tenantId);
  };

  const handleCreateInvoice = async (data: any) => {
    const newInv = await api.createInvoice(data);
    await loadAllData();
    return newInv;
  };

  const handleCreatePayment = async (data: any) => {
    const newPay = await api.createPayment(data);
    await loadAllData();
    return newPay;
  };

  const handleCreateJournal = async (data: any) => {
    const newJ = await api.createJournalEntry(data);
    await loadAllData();
    return newJ;
  };

  const handleApproveRefund = async (refundId: string) => {
    await api.approveRefund(refundId);
    await loadAllData();
  };

  const handleProcessRefund = async (refundId: string) => {
    await api.processRefund(refundId);
    await loadAllData();
  };

  const handleRunReconciliation = async () => {
    await api.simulateBankReconciliation();
    await loadAllData();
  };

  const handleAdjudicateClaim = async (claimId: string, data: any) => {
    await api.adjudicateClaim(claimId, data);
    await loadAllData();
  };

  const handleResubmitClaim = async (claimId: string, correctiveAction: string) => {
    await api.resubmitClaim(claimId, correctiveAction);
    await loadAllData();
  };

  const handleClosePeriod = async (periodId: string, notes: string) => {
    await api.closeFinancialPeriod(periodId, notes);
    await loadAllData();
  };

  const handleViewTimeline = (inv: Invoice) => {
    setSelectedTimelineInvoice(inv);
    setCurrentView('invoice-timeline');
  };

  const handlePayInvoice = (inv: Invoice) => {
    setPaymentInvoiceId(inv.id);
    setIsNewPaymentOpen(true);
  };

  const openPeriod = periods.find((p) => !p.is_closed);

  return (
    <div className="app-container">
      {/* 18-View Sidebar */}
      <Sidebar currentView={currentView} onNavigate={(v) => setCurrentView(v)} />

      {/* Main Panel */}
      <div className="main-content">
        <Header
          tenants={tenants.length > 0 ? tenants : [
            { id: 'tenant-apollo-01', name: 'Apollo Super Speciality Hospital', slug: 'apollo-delhi', subscription_tier: 'ENTERPRISE', default_currency: 'INR', is_active: true, branches: [] },
            { id: 'tenant-max-02', name: 'Max Healthcare Institute', slug: 'max-mumbai', subscription_tier: 'ENTERPRISE', default_currency: 'INR', is_active: true, branches: [] }
          ]}
          activeTenantId={activeTenantId}
          onSelectTenant={handleTenantChange}
          integrityScore={integrityReport?.integrity_score ?? 100}
          periodName={openPeriod ? `${openPeriod.period_name} (OPEN)` : 'FY2026-M10 (OPEN)'}
          onRefresh={loadAllData}
          isLoading={isLoading}
        />

        <main className="content-body">
          {currentView === 'dashboard' && (
            <FinanceDashboardView
              kpis={kpis}
              recentInvoices={invoices}
              recentPayments={payments}
              onNavigate={(v) => setCurrentView(v)}
              onOpenNewInvoice={() => setIsNewInvoiceOpen(true)}
              onOpenNewPayment={() => {
                setPaymentInvoiceId(undefined);
                setIsNewPaymentOpen(true);
              }}
            />
          )}

          {currentView === 'invoices' && (
            <InvoiceManagementView
              invoices={invoices}
              onOpenNewInvoice={() => setIsNewInvoiceOpen(true)}
              onViewTimeline={handleViewTimeline}
              onPrintInvoice={(inv) => setPrintingInvoice(inv)}
              onPayInvoice={handlePayInvoice}
            />
          )}

          {currentView === 'invoice-timeline' && (
            <InvoiceDetailsTimelineView
              invoices={invoices}
              selectedInvoice={selectedTimelineInvoice || invoices[0]}
              onSelectInvoice={(inv) => setSelectedTimelineInvoice(inv)}
              onPrintInvoice={(inv) => setPrintingInvoice(inv)}
              onBackToInvoices={() => setCurrentView('invoices')}
            />
          )}

          {currentView === 'payments' && (
            <PaymentsReceiptsView
              payments={payments}
              onOpenNewPayment={() => {
                setPaymentInvoiceId(undefined);
                setIsNewPaymentOpen(true);
              }}
              onRequestRefund={(p) => {
                setCurrentView('refunds');
              }}
            />
          )}

          {currentView === 'refunds' && (
            <RefundManagementView
              refunds={refunds}
              onApproveRefund={handleApproveRefund}
              onProcessRefund={handleProcessRefund}
            />
          )}

          {currentView === 'reconciliation' && (
            <PaymentReconciliationView
              reconciliations={reconciliations}
              onRunReconciliation={handleRunReconciliation}
            />
          )}

          {currentView === 'insurance-payers' && (
            <InsurancePayersPoliciesView
              payers={payers}
              policies={policies}
            />
          )}

          {currentView === 'claims-workbench' && (
            <InsuranceClaimsWorkbenchView
              claims={claims}
              onAdjudicateClaim={handleAdjudicateClaim}
              onResubmitClaim={handleResubmitClaim}
            />
          )}

          {currentView === 'gst-tax' && (
            <GSTTaxConfigurationView
              taxConfigs={taxConfigs}
            />
          )}

          {currentView === 'chart-of-accounts' && (
            <ChartOfAccountsView
              accounts={accounts}
            />
          )}

          {currentView === 'journal-entries' && (
            <JournalEntriesGLView
              journals={journals}
              onOpenNewJournal={() => setIsNewJournalOpen(true)}
            />
          )}

          {currentView === 'accounts-receivable' && (
            <AccountsReceivableView />
          )}

          {currentView === 'accounts-payable' && (
            <AccountsPayableView
              payables={payables}
            />
          )}

          {currentView === 'financial-reports' && (
            <FinancialReportsAnalyticsView
              kpis={kpis}
              invoices={invoices}
              payments={payments}
            />
          )}

          {currentView === 'integrity-monitor' && (
            <FinancialIntegrityMonitorView
              report={integrityReport}
              onRefresh={loadAllData}
            />
          )}

          {currentView === 'period-closing' && (
            <FinancialPeriodClosingView
              periods={periods}
              onClosePeriod={handleClosePeriod}
            />
          )}

          {currentView === 'audit-log' && (
            <FinanceAuditLogView />
          )}

          {currentView === 'settings-policies' && (
            <FinanceSettingsPoliciesView
              billingEntities={billingEntities}
            />
          )}
        </main>
      </div>

      {/* Global Interactive Modals */}
      <NewInvoiceModal
        isOpen={isNewInvoiceOpen}
        onClose={() => setIsNewInvoiceOpen(false)}
        billingEntities={billingEntities}
        services={services}
        taxConfigs={taxConfigs}
        onSubmit={handleCreateInvoice}
      />

      <NewPaymentModal
        isOpen={isNewPaymentOpen}
        onClose={() => setIsNewPaymentOpen(false)}
        invoices={invoices}
        initialInvoiceId={paymentInvoiceId}
        onSubmit={handleCreatePayment}
      />

      <NewJournalEntryModal
        isOpen={isNewJournalOpen}
        onClose={() => setIsNewJournalOpen(false)}
        accounts={accounts}
        onSubmit={handleCreateJournal}
      />

      <InvoicePrintModal
        isOpen={!!printingInvoice}
        onClose={() => setPrintingInvoice(null)}
        invoice={printingInvoice}
      />
    </div>
  );
};

export default App;
