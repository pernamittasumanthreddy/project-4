import React, { useState } from 'react';
import { ReconciliationRecord } from '../types/finance';
import { StatusBadge } from '../components/StatusBadge';
import { GitCompare, Play, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface PaymentReconciliationViewProps {
  reconciliations: ReconciliationRecord[];
  onRunReconciliation: () => Promise<void>;
}

export const PaymentReconciliationView: React.FC<PaymentReconciliationViewProps> = ({
  reconciliations,
  onRunReconciliation
}) => {
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = async () => {
    setIsRunning(true);
    try {
      await onRunReconciliation();
    } catch (err: any) {
      alert(`Reconciliation error: ${err.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Smart Payment Reconciliation</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Unique Feature B: Automated Settlement Matching & Bank Discrepancy Detection
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleRun} disabled={isRunning}>
          <Play size={16} /> {isRunning ? 'Scanning Statements...' : 'Run Automated Bank Reconciliation'}
        </button>
      </div>

      {/* Explanatory Banner */}
      <div
        className="card"
        style={{
          background: 'rgba(2, 132, 199, 0.08)',
          border: '1px solid rgba(2, 132, 199, 0.25)',
          marginBottom: '20px',
          padding: '16px 20px'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <GitCompare size={20} color="#38bdf8" />
          <div>
            <div style={{ fontWeight: 600, color: '#38bdf8', fontSize: '0.875rem' }}>
              Automated Bank & POS Settlement Audit Invariant
            </div>
            <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
              Cross-references bank settlement files with recorded hospital POS/UPI receipts.
              Flags unlinked gateway payouts, double-settlements, and merchant fee discrepancies.
            </div>
          </div>
        </div>
      </div>

      {/* Reconciliation Batches Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Settlement Batch #</th>
              <th>Statement Date</th>
              <th>Total Txns</th>
              <th>Matched Items</th>
              <th>Discrepancies</th>
              <th style={{ textAlign: 'right' }}>Statement Sum (₹)</th>
              <th style={{ textAlign: 'right' }}>System Recorded (₹)</th>
              <th>Status</th>
              <th>Audit Narrative & Notes</th>
            </tr>
          </thead>
          <tbody>
            {reconciliations.length === 0 ? (
              <tr>
                <td colSpan={9} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No settlement reconciliation batches recorded. Run automated reconciliation above.
                </td>
              </tr>
            ) : (
              reconciliations.map((r) => (
                <tr key={r.id}>
                  <td><strong style={{ color: '#38bdf8' }}>{r.batch_number}</strong></td>
                  <td style={{ fontSize: '0.8125rem' }}>{r.statement_date}</td>
                  <td className="mono-num">{r.total_records}</td>
                  <td className="mono-num" style={{ color: '#34d399', fontWeight: 600 }}>{r.matched_records}</td>
                  <td className="mono-num" style={{ color: r.discrepancy_count > 0 ? '#f87171' : '#34d399', fontWeight: 700 }}>
                    {r.discrepancy_count}
                  </td>
                  <td className="mono-num" style={{ textAlign: 'right' }}>₹{r.total_statement_amount}</td>
                  <td className="mono-num" style={{ textAlign: 'right', fontWeight: 600 }}>₹{r.total_system_amount}</td>
                  <td><StatusBadge status={r.status} /></td>
                  <td style={{ fontSize: '0.8125rem', maxWidth: '300px' }}>{r.notes}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
