import React, { useState } from 'react';
import { Refund } from '../types/finance';
import { StatusBadge } from '../components/StatusBadge';
import { RotateCcw, CheckCircle2, DollarSign } from 'lucide-react';

interface RefundManagementViewProps {
  refunds: Refund[];
  onApproveRefund: (id: string) => Promise<void>;
  onProcessRefund: (id: string) => Promise<void>;
}

export const RefundManagementView: React.FC<RefundManagementViewProps> = ({
  refunds,
  onApproveRefund,
  onProcessRefund
}) => {
  const [isProcessing, setIsProcessing] = useState<string | null>(null);

  const handleApprove = async (id: string) => {
    setIsProcessing(id);
    try {
      await onApproveRefund(id);
    } catch (err: any) {
      alert(`Approval failed: ${err.message}`);
    } finally {
      setIsProcessing(null);
    }
  };

  const handleProcess = async (id: string) => {
    setIsProcessing(id);
    try {
      await onProcessRefund(id);
    } catch (err: any) {
      alert(`Processing failed: ${err.message}`);
    } finally {
      setIsProcessing(null);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Refund Management & Disbursals</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Multi-Tier Financial Approval Workflow (Requested ➔ Approved ➔ Processed)
          </p>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Refund Voucher #</th>
              <th>Original Payment</th>
              <th>Invoice Ref</th>
              <th style={{ textAlign: 'right' }}>Refund Amount (₹)</th>
              <th>Justification Reason</th>
              <th>Requested By</th>
              <th>Approver</th>
              <th>Status</th>
              <th style={{ textAlign: 'center' }}>Workflow Actions</th>
            </tr>
          </thead>
          <tbody>
            {refunds.length === 0 ? (
              <tr>
                <td colSpan={9} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No refund requests on file.
                </td>
              </tr>
            ) : (
              refunds.map((r) => (
                <tr key={r.id}>
                  <td><strong style={{ color: '#fbbf24' }}>{r.refund_number}</strong></td>
                  <td className="mono-num">{r.payment_number || 'PAY-REF'}</td>
                  <td>{r.invoice_number || 'INV-REF'}</td>
                  <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#f87171' }}>
                    ₹{r.amount}
                  </td>
                  <td style={{ fontSize: '0.8125rem' }}>{r.reason}</td>
                  <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{r.requested_by}</td>
                  <td style={{ fontSize: '0.8125rem', color: '#38bdf8' }}>{r.approved_by || 'Pending'}</td>
                  <td><StatusBadge status={r.status} /></td>
                  <td style={{ textAlign: 'center' }}>
                    {r.status === 'REQUESTED' && (
                      <button
                        className="btn btn-primary btn-sm"
                        disabled={isProcessing === r.id}
                        onClick={() => handleApprove(r.id)}
                      >
                        <CheckCircle2 size={14} /> Approve Refund
                      </button>
                    )}
                    {r.status === 'APPROVED' && (
                      <button
                        className="btn btn-success btn-sm"
                        disabled={isProcessing === r.id}
                        onClick={() => handleProcess(r.id)}
                      >
                        <DollarSign size={14} /> Disburse Funds
                      </button>
                    )}
                    {r.status === 'PROCESSED' && (
                      <span style={{ fontSize: '0.75rem', color: '#34d399', fontWeight: 600 }}>
                        Disbursed
                      </span>
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
