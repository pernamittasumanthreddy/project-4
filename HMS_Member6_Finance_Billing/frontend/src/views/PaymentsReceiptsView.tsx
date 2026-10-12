import React, { useState } from 'react';
import { Payment } from '../types/finance';
import { StatusBadge } from '../components/StatusBadge';
import { Plus, Search, ShieldCheck } from 'lucide-react';

interface PaymentsReceiptsViewProps {
  payments: Payment[];
  onOpenNewPayment: () => void;
  onRequestRefund: (payment: Payment) => void;
}

export const PaymentsReceiptsView: React.FC<PaymentsReceiptsViewProps> = ({
  payments,
  onOpenNewPayment,
  onRequestRefund
}) => {
  const [search, setSearch] = useState('');
  const [methodFilter, setMethodFilter] = useState('ALL');

  const filtered = payments.filter((p) => {
    const matchMethod = methodFilter === 'ALL' || p.method === methodFilter;
    const matchSearch =
      p.payment_number.toLowerCase().includes(search.toLowerCase()) ||
      (p.transaction_reference && p.transaction_reference.toLowerCase().includes(search.toLowerCase())) ||
      (p.patient_name && p.patient_name.toLowerCase().includes(search.toLowerCase()));
    return matchMethod && matchSearch;
  });

  const totalCollected = payments
    .filter((p) => p.status === 'SUCCESS')
    .reduce((acc, p) => acc + parseFloat(p.amount), 0);

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Payments & Cash Collections Desk</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Multi-Tender Cash, Card, UPI & Bank Wire Settlements with Idempotency Protection
          </p>
        </div>
        <button className="btn btn-success" onClick={onOpenNewPayment}>
          <Plus size={16} /> Record Payment Receipt
        </button>
      </div>

      {/* KPI Highlight Strip */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: '20px' }}>
        <div className="kpi-card">
          <div className="kpi-label">Total Cleared Receipts</div>
          <div className="kpi-value" style={{ color: '#34d399' }}>₹{totalCollected.toFixed(2)}</div>
          <div className="kpi-sub">Across all tenders this period</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">Transaction Volume</div>
          <div className="kpi-value">{payments.length}</div>
          <div className="kpi-sub">Cleared transactions</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">Duplicate Protection</div>
          <div className="kpi-value" style={{ color: '#38bdf8', fontSize: '1.25rem' }}>Active</div>
          <div className="kpi-sub">Idempotency-Key headers enforced</div>
        </div>
      </div>

      {/* Search & Filters */}
      <div
        className="card"
        style={{
          padding: '14px 20px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '16px'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, maxWidth: '400px' }}>
          <Search size={16} color="var(--text-dim)" />
          <input
            type="text"
            className="form-control"
            placeholder="Search by Payment #, Bank Ref, Patient..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          {['ALL', 'UPI', 'CARD', 'CASH', 'WIRE_TRANSFER'].map((m) => (
            <button
              key={m}
              className={`btn btn-sm ${methodFilter === m ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setMethodFilter(m)}
            >
              {m.replace(/_/g, ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Payments Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Receipt #</th>
              <th>Recorded At</th>
              <th>Invoice Ref</th>
              <th>Patient</th>
              <th>Tender Method</th>
              <th>Bank Ref / UTR</th>
              <th style={{ textAlign: 'right' }}>Amount (₹)</th>
              <th>Status</th>
              <th style={{ textAlign: 'center' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={9} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No payment records match criteria.
                </td>
              </tr>
            ) : (
              filtered.map((p) => (
                <tr key={p.id}>
                  <td><strong style={{ color: '#38bdf8' }}>{p.payment_number}</strong></td>
                  <td style={{ fontSize: '0.8125rem' }}>{new Date(p.created_at).toLocaleDateString()}</td>
                  <td>
                    <span style={{ fontWeight: 600 }}>{p.invoice_number || 'INV-REF'}</span>
                  </td>
                  <td>{p.patient_name || 'Hospital Patient'}</td>
                  <td>
                    <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>
                      {p.method_display}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                      {p.transaction_reference || 'N/A'}
                    </span>
                  </td>
                  <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }}>
                    ₹{p.amount}
                  </td>
                  <td>
                    <StatusBadge status={p.status} />
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    {p.status === 'SUCCESS' && (
                      <button
                        className="btn btn-outline btn-sm"
                        style={{ color: '#fbbf24', borderColor: 'rgba(245, 158, 11, 0.3)' }}
                        onClick={() => onRequestRefund(p)}
                      >
                        Refund Request
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
