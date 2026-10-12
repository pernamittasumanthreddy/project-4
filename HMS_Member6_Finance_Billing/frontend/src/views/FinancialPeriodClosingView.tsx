import React, { useState } from 'react';
import { FinancialPeriod } from '../types/finance';
import { StatusBadge } from '../components/StatusBadge';
import { Lock, Unlock, CheckCircle2, AlertCircle } from 'lucide-react';
import { Modal } from '../components/Modal';

interface FinancialPeriodClosingViewProps {
  periods: FinancialPeriod[];
  onClosePeriod: (periodId: string, notes: string) => Promise<void>;
}

export const FinancialPeriodClosingView: React.FC<FinancialPeriodClosingViewProps> = ({
  periods,
  onClosePeriod
}) => {
  const [closingPeriod, setClosingPeriod] = useState<FinancialPeriod | null>(null);
  const [closingNotes, setClosingNotes] = useState('');
  const [isClosing, setIsClosing] = useState(false);

  const openPeriods = periods.filter((p) => !p.is_closed);
  const closedPeriods = periods.filter((p) => p.is_closed);

  const handleOpenCloseModal = (p: FinancialPeriod) => {
    setClosingPeriod(p);
    setClosingNotes('September monthly ledger audit clearance finalized. All journals posted.');
  };

  const handleConfirmClose = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!closingPeriod) return;
    setIsClosing(true);
    try {
      await onClosePeriod(closingPeriod.id, closingNotes);
      setClosingPeriod(null);
    } catch (err: any) {
      alert(`Period close failed: ${err.message}`);
    } finally {
      setIsClosing(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Financial Period Closing & Audit Locks</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Unique Feature H: Pre-Closing Reconciliation Clearance & Immutability Locks for Historical Ledgers
          </p>
        </div>
      </div>

      {/* Active Operational Period */}
      <div className="card" style={{ marginBottom: '24px', borderLeft: '4px solid #38bdf8' }}>
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Unlock size={18} color="#38bdf8" />
            <h3>Active Operational Financial Period</h3>
          </div>
        </div>

        {openPeriods.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>No open operational financial period.</p>
        ) : (
          openPeriods.map((p) => (
            <div key={p.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#ffffff' }}>
                  {p.period_name}
                </div>
                <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                  Effective Range: <strong>{p.start_date}</strong> through <strong>{p.end_date}</strong>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                  Status: <strong>Open for live patient billing, payment receipts, and journal vouchers</strong>
                </div>
              </div>
              <button
                className="btn btn-primary"
                onClick={() => handleOpenCloseModal(p)}
              >
                <Lock size={16} /> Execute Period Close & Lock
              </button>
            </div>
          ))
        )}
      </div>

      {/* Historical Closed Periods */}
      <div className="card">
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Lock size={18} color="#10b981" />
            <h3>Historical Closed & Locked Periods</h3>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
            Tamper-proof historical ledgers
          </span>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Period Code</th>
                <th>Calendar Duration</th>
                <th>Locked At</th>
                <th>Auditor / Closed By</th>
                <th>Closing Governance Notes</th>
                <th>Ledger Lock State</th>
              </tr>
            </thead>
            <tbody>
              {closedPeriods.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                    No historical periods closed yet.
                  </td>
                </tr>
              ) : (
                closedPeriods.map((p) => (
                  <tr key={p.id}>
                    <td><strong style={{ color: '#38bdf8' }}>{p.period_name}</strong></td>
                    <td style={{ fontSize: '0.8125rem' }}>{p.start_date} to {p.end_date}</td>
                    <td style={{ fontSize: '0.8125rem' }}>{p.closed_at ? new Date(p.closed_at).toLocaleString() : '—'}</td>
                    <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{p.closed_by || 'Chief Auditor'}</td>
                    <td style={{ fontSize: '0.8125rem' }}>{p.closing_notes || 'Period closed without exceptions.'}</td>
                    <td>
                      <span className="badge badge-success">LOCKED (IMMUTABLE)</span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Period Close Wizard Modal */}
      <Modal
        isOpen={!!closingPeriod}
        onClose={() => setClosingPeriod(null)}
        title={`Execute Financial Close for Period ${closingPeriod?.period_name}`}
        maxWidth="600px"
      >
        <form onSubmit={handleConfirmClose}>
          <div
            style={{
              background: 'rgba(2, 132, 199, 0.08)',
              border: '1px solid rgba(2, 132, 199, 0.25)',
              borderRadius: '6px',
              padding: '14px',
              marginBottom: '16px',
              fontSize: '0.8125rem'
            }}
          >
            <div style={{ fontWeight: 600, color: '#38bdf8', marginBottom: '6px' }}>
              Automated Pre-Closing Audit Checks:
            </div>
            <ul style={{ paddingLeft: '18px', color: 'var(--text-muted)' }}>
              <li>Verifies all Draft Journal entries are finalized and posted.</li>
              <li>Validates that Double-Entry General Ledger is strictly balanced ($\sum Dr == \sum Cr$).</li>
              <li>Applies an immutable write-lock preventing retroactive voucher alterations.</li>
            </ul>
          </div>

          <div className="form-group">
            <label className="form-label">CFO / Chief Auditor Closing Governance Notes</label>
            <textarea
              rows={3}
              className="form-control"
              value={closingNotes}
              onChange={(e) => setClosingNotes(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <button type="button" className="btn btn-secondary" onClick={() => setClosingPeriod(null)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isClosing}>
              {isClosing ? 'Executing Close & Lock...' : 'Confirm Period Close & Apply Lock'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
