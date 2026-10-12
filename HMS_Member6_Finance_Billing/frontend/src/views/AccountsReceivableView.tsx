import React, { useState, useEffect } from 'react';
import { ARAgingResponse } from '../types/finance';
import { api } from '../services/api';
import { TrendingDown, AlertTriangle, Clock, Mail } from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';

export const AccountsReceivableView: React.FC = () => {
  const [arData, setArData] = useState<ARAgingResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.getAccountsReceivable()
      .then(setArData)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Accounts Receivable Aging & Debtors Ledger</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Unique Feature E: Revenue Leakage Tracker across 0-30, 31-60, 61-90, and 90+ Overdue Aging Buckets
          </p>
        </div>
      </div>

      {/* Aging Summary KPI Grid */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-label">Current (0 - 30 Days)</div>
          <div className="kpi-value" style={{ color: '#34d399' }}>
            ₹{arData?.summary?.current_0_30 || '0.00'}
          </div>
          <div className="kpi-sub">Within standard hospital credit terms</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Aging (31 - 60 Days)</div>
          <div className="kpi-value" style={{ color: '#fbbf24' }}>
            ₹{arData?.summary?.aging_31_60 || '0.00'}
          </div>
          <div className="kpi-sub">Follow-up reminder stage</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">Aging (61 - 90 Days)</div>
          <div className="kpi-value" style={{ color: '#f97316' }}>
            ₹{arData?.summary?.aging_61_90 || '0.00'}
          </div>
          <div className="kpi-sub">Escalated collection inquiry</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-label">High Risk (90+ Days Overdue)</div>
          <div className="kpi-value" style={{ color: '#f87171' }}>
            ₹{arData?.summary?.overdue_90_plus || '0.00'}
          </div>
          <div className="kpi-sub">Critical delinquency risk</div>
        </div>
      </div>

      {/* Outstanding Invoices Aging Table */}
      <div className="card">
        <div className="card-header">
          <h3>Outstanding Patient & TPA Debtor Balances</h3>
          <span style={{ fontSize: '0.8125rem', color: '#f87171', fontWeight: 600 }}>
            Total Overdue: ₹{arData?.summary?.total_outstanding || '0.00'}
          </span>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Patient Name</th>
                <th>MRN</th>
                <th>Due Date</th>
                <th style={{ textAlign: 'center' }}>Overdue Age (Days)</th>
                <th style={{ textAlign: 'right' }}>Outstanding Balance (₹)</th>
                <th>Status</th>
                <th style={{ textAlign: 'center' }}>Follow-up</th>
              </tr>
            </thead>
            <tbody>
              {arData?.invoices?.length === 0 ? (
                <tr>
                  <td colSpan={8} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                    No unsettled receivables currently overdue.
                  </td>
                </tr>
              ) : (
                arData?.invoices?.map((row, idx) => (
                  <tr key={idx}>
                    <td><strong style={{ color: '#38bdf8' }}>{row.invoice_number}</strong></td>
                    <td style={{ fontWeight: 600 }}>{row.patient_name}</td>
                    <td className="mono-num" style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{row.patient_mrn}</td>
                    <td style={{ fontSize: '0.8125rem' }}>{row.due_date}</td>
                    <td style={{ textAlign: 'center', fontWeight: 700 }} className="mono-num">
                      <span
                        className="badge"
                        style={{
                          background: row.days_overdue > 60 ? 'rgba(239, 68, 68, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                          color: row.days_overdue > 60 ? '#f87171' : '#fbbf24'
                        }}
                      >
                        {row.days_overdue} Days
                      </span>
                    </td>
                    <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#f87171' }}>
                      ₹{row.balance_due}
                    </td>
                    <td><StatusBadge status={row.status} /></td>
                    <td style={{ textAlign: 'center' }}>
                      <button
                        className="btn btn-outline btn-sm"
                        onClick={() => alert(`Payment reminder dispatch triggered for ${row.patient_name} (${row.invoice_number})`)}
                      >
                        <Mail size={12} /> Send Statement
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
