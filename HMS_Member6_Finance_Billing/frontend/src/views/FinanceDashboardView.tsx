import React from 'react';
import { DashboardKPIs, Invoice, Payment } from '../types/finance';
import { IndianRupee, ArrowUpRight, TrendingUp, ShieldAlert, FileText, CheckCircle2 } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

interface FinanceDashboardViewProps {
  kpis: DashboardKPIs | null;
  recentInvoices: Invoice[];
  recentPayments: Payment[];
  onNavigate: (view: any) => void;
  onOpenNewInvoice: () => void;
  onOpenNewPayment: () => void;
}

export const FinanceDashboardView: React.FC<FinanceDashboardViewProps> = ({
  kpis,
  recentInvoices,
  recentPayments,
  onNavigate,
  onOpenNewInvoice,
  onOpenNewPayment
}) => {
  const deptLabels: Record<string, string> = {
    OPD: 'Outpatient Consultations',
    IPD: 'Inpatient Ward & Bed',
    LAB: 'Laboratory Pathology',
    RAD: 'Radiology & Imaging',
    PHARM: 'Pharmacy & Drug Sales',
    SURG: 'Surgical & Operation Theatre'
  };

  return (
    <div>
      {/* Top Banner & Quick Action Buttons */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1>Hospital Finance & Billing Dashboard</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Multi-Tenant Healthcare Revenue Cycle, Payment Reconciliation & General Ledger
          </p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn btn-primary" onClick={onOpenNewInvoice}>
            <FileText size={16} /> New Patient Bill
          </button>
          <button className="btn btn-success" onClick={onOpenNewPayment}>
            <IndianRupee size={16} /> Record Payment
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-label">Gross Billed Turnover</div>
          <div className="kpi-value">₹{kpis?.total_billed || '0.00'}</div>
          <div className="kpi-sub">Total itemized invoices issued</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Realized Collections</div>
          <div className="kpi-value" style={{ color: '#34d399' }}>₹{kpis?.total_collected || '0.00'}</div>
          <div className="kpi-sub">Verified cash, UPI & card receipts</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Accounts Receivable</div>
          <div className="kpi-value" style={{ color: '#f87171' }}>₹{kpis?.outstanding_receivables || '0.00'}</div>
          <div className="kpi-sub">Unsettled patient & TPA balances</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Collection Efficiency</div>
          <div className="kpi-value" style={{ color: '#38bdf8' }}>{kpis?.collection_efficiency_percentage || '0.00'}%</div>
          <div className="kpi-sub">Realized vs. Billed conversion rate</div>
        </div>
      </div>

      {/* Department Breakdown & Insurance Highlights */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '24px', marginBottom: '28px' }}>
        {/* Department Revenue Breakdown */}
        <div className="card">
          <div className="card-header">
            <h3>Departmental Revenue Attribution</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>From Linked Invoice Lines</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {Object.entries(kpis?.department_revenue || {}).map(([dept, rev]) => {
              const numRev = parseFloat(rev);
              const maxRev = Math.max(...Object.values(kpis?.department_revenue || {}).map((v) => parseFloat(v) || 1));
              const pct = maxRev > 0 ? (numRev / maxRev) * 100 : 0;

              return (
                <div key={dept}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600 }}>{deptLabels[dept] || dept}</span>
                    <strong className="mono-num">₹{rev}</strong>
                  </div>
                  <div style={{ background: 'rgba(255, 255, 255, 0.05)', borderRadius: '4px', height: '6px', overflow: 'hidden' }}>
                    <div style={{ background: '#0284c7', width: `${pct}%`, height: '100%', borderRadius: '4px' }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Insurance Claims Status Summary */}
        <div className="card">
          <div className="card-header">
            <h3>Insurance & TPA Claims Desk</h3>
            <button
              className="btn btn-outline btn-sm"
              onClick={() => onNavigate('claims-workbench')}
            >
              Claims Workbench <ArrowUpRight size={14} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '6px' }}>
              <span style={{ fontSize: '0.875rem' }}>Total Claims Filed:</span>
              <strong className="mono-num">{kpis?.insurance_kpis?.total_claims || 0}</strong>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(245, 158, 11, 0.08)', borderRadius: '6px', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
              <span style={{ fontSize: '0.875rem', color: '#fbbf24' }}>Under Review / Pending:</span>
              <strong className="mono-num" style={{ color: '#fbbf24' }}>
                {kpis?.insurance_kpis?.pending_claims || 0} (₹{kpis?.insurance_kpis?.pending_amount || '0.00'})
              </strong>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '6px', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
              <span style={{ fontSize: '0.875rem', color: '#34d399' }}>Approved & Settled:</span>
              <strong className="mono-num" style={{ color: '#34d399' }}>{kpis?.insurance_kpis?.approved_claims || 0}</strong>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: 'rgba(239, 68, 68, 0.08)', borderRadius: '6px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
              <span style={{ fontSize: '0.875rem', color: '#f87171' }}>Rejected on Denial Workbench:</span>
              <strong className="mono-num" style={{ color: '#f87171' }}>{kpis?.insurance_kpis?.rejected_claims || 0}</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity: Invoices & Payments */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px' }}>
        {/* Recent Invoices */}
        <div className="card">
          <div className="card-header">
            <h3>Recent Patient Invoices</h3>
            <button className="btn btn-outline btn-sm" onClick={() => onNavigate('invoices')}>
              View All Invoices
            </button>
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Invoice #</th>
                  <th>Patient</th>
                  <th>Net Total</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentInvoices.slice(0, 5).map((inv) => (
                  <tr key={inv.id}>
                    <td><strong style={{ color: '#38bdf8' }}>{inv.invoice_number}</strong></td>
                    <td>{inv.patient_name}</td>
                    <td className="mono-num">₹{inv.total_net}</td>
                    <td><StatusBadge status={inv.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Payments */}
        <div className="card">
          <div className="card-header">
            <h3>Recent Collections</h3>
            <button className="btn btn-outline btn-sm" onClick={() => onNavigate('payments')}>
              View All Receipts
            </button>
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Receipt #</th>
                  <th>Method</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentPayments.slice(0, 5).map((p) => (
                  <tr key={p.id}>
                    <td><strong>{p.payment_number}</strong></td>
                    <td>{p.method_display}</td>
                    <td className="mono-num" style={{ color: '#34d399', fontWeight: 600 }}>₹{p.amount}</td>
                    <td><StatusBadge status={p.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
