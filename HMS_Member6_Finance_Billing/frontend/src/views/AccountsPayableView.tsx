import React, { useState, useEffect } from 'react';
import { PayableRecord } from '../types/finance';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { TrendingUp, Truck, Plus } from 'lucide-react';

interface AccountsPayableViewProps {
  payables: PayableRecord[];
}

export const AccountsPayableView: React.FC<AccountsPayableViewProps> = ({
  payables: initialPayables
}) => {
  const [payables, setPayables] = useState<PayableRecord[]>(initialPayables);

  useEffect(() => {
    api.getPayableRecords().then(setPayables).catch(console.error);
  }, []);

  const totalPayables = payables.reduce((acc, p) => acc + parseFloat(p.balance_due), 0);

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Accounts Payable & Supplier Ledger</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Module 6.5: Medical Consumables, Implants, Pharmaceutical Vendors & Procurement Liabilities
          </p>
        </div>
      </div>

      {/* KPI Card */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: '20px' }}>
        <div className="kpi-card">
          <div className="kpi-label">Outstanding Trade Payables</div>
          <div className="kpi-value" style={{ color: '#fbbf24' }}>₹{totalPayables.toFixed(2)}</div>
          <div className="kpi-sub">Total procurement liabilities due</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">Active Vendor Invoices</div>
          <div className="kpi-value">{payables.length}</div>
          <div className="kpi-sub">Medical device & consumables bills</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">Credit Terms Compliance</div>
          <div className="kpi-value" style={{ color: '#34d399' }}>100%</div>
          <div className="kpi-sub">Zero vendor defaults logged</div>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Vendor / Supplier Name</th>
              <th>Bill / Invoice #</th>
              <th>Procurement Category</th>
              <th>Due Date</th>
              <th style={{ textAlign: 'right' }}>Total Bill (₹)</th>
              <th style={{ textAlign: 'right' }}>Paid (₹)</th>
              <th style={{ textAlign: 'right' }}>Balance Due (₹)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {payables.length === 0 ? (
              <tr>
                <td colSpan={8} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No accounts payable records found.
                </td>
              </tr>
            ) : (
              payables.map((p) => (
                <tr key={p.id}>
                  <td><strong style={{ color: '#38bdf8' }}>{p.vendor_name}</strong></td>
                  <td className="mono-num">{p.bill_number}</td>
                  <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{p.category}</td>
                  <td style={{ fontSize: '0.8125rem' }}>{p.due_date}</td>
                  <td className="mono-num" style={{ textAlign: 'right' }}>₹{p.total_amount}</td>
                  <td className="mono-num" style={{ textAlign: 'right', color: '#34d399' }}>₹{p.paid_amount}</td>
                  <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#fbbf24' }}>
                    ₹{p.balance_due}
                  </td>
                  <td><StatusBadge status={p.status} /></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
