import React, { useState } from 'react';
import { Modal } from './Modal';
import { Invoice, Payment } from '../types/finance';

interface NewPaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  invoices: Invoice[];
  initialInvoiceId?: string;
  onSubmit: (data: any) => Promise<Payment>;
}

export const NewPaymentModal: React.FC<NewPaymentModalProps> = ({
  isOpen,
  onClose,
  invoices,
  initialInvoiceId,
  onSubmit
}) => {
  const eligibleInvoices = invoices.filter((i) => i.status !== 'PAID' && i.status !== 'CANCELLED');
  const [selectedInvoiceId, setSelectedInvoiceId] = useState(initialInvoiceId || eligibleInvoices[0]?.id || '');
  
  const selectedInv = invoices.find((i) => i.id === selectedInvoiceId) || eligibleInvoices[0];
  const [amount, setAmount] = useState(selectedInv ? selectedInv.balance_due : '0.00');
  const [method, setMethod] = useState<'CASH' | 'CARD' | 'UPI' | 'WIRE_TRANSFER' | 'CHEQUE'>('UPI');
  const [refNumber, setRefNumber] = useState('');
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Auto-generate UUID idempotency token for duplicate charge protection
  const [idempotencyKey] = useState(`idemp-${Math.random().toString(36).substring(2, 12)}`);

  const handleInvoiceChange = (id: string) => {
    setSelectedInvoiceId(id);
    const inv = invoices.find((i) => i.id === id);
    if (inv) {
      setAmount(inv.balance_due);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onSubmit({
        invoice: selectedInvoiceId,
        amount: amount,
        method: method,
        transaction_reference: refNumber,
        idempotency_key: idempotencyKey,
        notes: notes
      });
      onClose();
    } catch (err: any) {
      alert(`Payment recording error: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Record Payment & Generate Official Receipt"
      maxWidth="600px"
    >
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Target Patient Bill / Invoice</label>
          <select
            className="form-control"
            value={selectedInvoiceId}
            onChange={(e) => handleInvoiceChange(e.target.value)}
            required
          >
            {eligibleInvoices.map((inv) => (
              <option key={inv.id} value={inv.id}>
                {inv.invoice_number} — {inv.patient_name} (Balance Due: ₹{inv.balance_due})
              </option>
            ))}
          </select>
        </div>

        {selectedInv && (
          <div
            style={{
              background: 'rgba(2, 132, 199, 0.08)',
              border: '1px solid rgba(2, 132, 199, 0.2)',
              borderRadius: '6px',
              padding: '12px 16px',
              marginBottom: '16px',
              fontSize: '0.8125rem',
              display: 'flex',
              justifyContent: 'space-between'
            }}
          >
            <div>Total Billed: <strong className="mono-num">₹{selectedInv.total_net}</strong></div>
            <div>Already Paid: <strong className="mono-num" style={{ color: '#34d399' }}>₹{selectedInv.paid_amount}</strong></div>
            <div>Outstanding: <strong className="mono-num" style={{ color: '#f87171' }}>₹{selectedInv.balance_due}</strong></div>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
          <div className="form-group">
            <label className="form-label">Payment Amount (₹)</label>
            <input
              type="number"
              step="0.01"
              max={selectedInv ? selectedInv.balance_due : undefined}
              className="form-control mono-num"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Tender Method</label>
            <select
              className="form-control"
              value={method}
              onChange={(e) => setMethod(e.target.value as any)}
            >
              <option value="UPI">UPI / QR Code Digital</option>
              <option value="CARD">Credit / Debit Card (POS)</option>
              <option value="CASH">Cash Counter Till</option>
              <option value="WIRE_TRANSFER">Bank Wire / NEFT / RTGS</option>
              <option value="CHEQUE">Cheque / Demand Draft</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Bank Transaction Reference / UTR / Auth Code</label>
          <input
            type="text"
            className="form-control"
            placeholder="e.g. UTR-20261012-9901842"
            value={refNumber}
            onChange={(e) => setRefNumber(e.target.value)}
          />
        </div>

        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '16px' }}>
          Idempotency Protection Token: <code className="mono-num">{idempotencyKey}</code>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="btn btn-success" disabled={isSubmitting}>
            {isSubmitting ? 'Recording & Balancing GL...' : 'Confirm Payment & Print Receipt'}
          </button>
        </div>
      </form>
    </Modal>
  );
};
