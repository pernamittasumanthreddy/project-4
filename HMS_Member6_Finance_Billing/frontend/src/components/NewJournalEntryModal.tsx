import React, { useState } from 'react';
import { Modal } from './Modal';
import { ChartOfAccount, JournalEntry } from '../types/finance';
import { Plus, Trash2, AlertCircle, CheckCircle2 } from 'lucide-react';

interface NewJournalEntryModalProps {
  isOpen: boolean;
  onClose: () => void;
  accounts: ChartOfAccount[];
  onSubmit: (data: any) => Promise<JournalEntry>;
}

export const NewJournalEntryModal: React.FC<NewJournalEntryModalProps> = ({
  isOpen,
  onClose,
  accounts,
  onSubmit
}) => {
  const [entryDate, setEntryDate] = useState(new Date().toISOString().split('T')[0]);
  const [description, setDescription] = useState('');
  const [sourceType, setSourceType] = useState('MANUAL');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [lines, setLines] = useState<Array<{
    account_id: string;
    debit_amount: number;
    credit_amount: number;
    description: string;
  }>>([
    {
      account_id: accounts[0]?.id || '',
      debit_amount: 5000,
      credit_amount: 0,
      description: 'Debit Leg'
    },
    {
      account_id: accounts[1]?.id || '',
      debit_amount: 0,
      credit_amount: 5000,
      description: 'Credit Leg'
    }
  ]);

  const totalDebit = lines.reduce((acc, l) => acc + (l.debit_amount || 0), 0);
  const totalCredit = lines.reduce((acc, l) => acc + (l.credit_amount || 0), 0);
  const isBalanced = Math.abs(totalDebit - totalCredit) < 0.001 && totalDebit > 0;
  const discrepancy = Math.abs(totalDebit - totalCredit);

  const handleAddLine = () => {
    setLines([
      ...lines,
      {
        account_id: accounts[0]?.id || '',
        debit_amount: 0,
        credit_amount: 0,
        description: ''
      }
    ]);
  };

  const handleRemoveLine = (idx: number) => {
    if (lines.length > 2) {
      setLines(lines.filter((_, i) => i !== idx));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isBalanced) {
      alert(`Cannot post unbalanced entry. Discrepancy: ₹${discrepancy.toFixed(2)}`);
      return;
    }
    setIsSubmitting(true);
    try {
      await onSubmit({
        entry_date: entryDate,
        description,
        source_document_type: sourceType,
        lines
      });
      onClose();
    } catch (err: any) {
      alert(`Journal entry failed: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Create Double-Entry Accounting Journal Voucher"
      maxWidth="840px"
    >
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 1fr', gap: '16px', marginBottom: '16px' }}>
          <div className="form-group">
            <label className="form-label">Posting Date</label>
            <input
              type="date"
              className="form-control"
              value={entryDate}
              onChange={(e) => setEntryDate(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Voucher Description / Narrative</label>
            <input
              type="text"
              className="form-control"
              placeholder="e.g. Monthly diagnostic equipment depreciation or adjustment"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Voucher Source Type</label>
            <select
              className="form-control"
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value)}
            >
              <option value="MANUAL">Manual Adjustment</option>
              <option value="INVOICE">Invoicing Revenue</option>
              <option value="PAYMENT">Cash / Settlement</option>
              <option value="PERIOD_CLOSE">Year-End Allocation</option>
            </select>
          </div>
        </div>

        {/* Double Entry Lines */}
        <div style={{ marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <h4 style={{ fontSize: '0.875rem', fontWeight: 600, color: '#ffffff' }}>General Ledger Distribution Legs</h4>
            <button type="button" className="btn btn-outline btn-sm" onClick={handleAddLine}>
              <Plus size={14} /> Add GL Leg
            </button>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th style={{ width: '280px' }}>GL Account</th>
                  <th>Leg Description</th>
                  <th style={{ width: '130px' }}>Debit (₹)</th>
                  <th style={{ width: '130px' }}>Credit (₹)</th>
                  <th style={{ width: '40px' }}></th>
                </tr>
              </thead>
              <tbody>
                {lines.map((l, idx) => (
                  <tr key={idx}>
                    <td>
                      <select
                        className="form-control"
                        style={{ fontSize: '0.8125rem', padding: '6px' }}
                        value={l.account_id}
                        onChange={(e) => {
                          const updated = [...lines];
                          updated[idx].account_id = e.target.value;
                          setLines(updated);
                        }}
                        required
                      >
                        {accounts.map((a) => (
                          <option key={a.id} value={a.id}>
                            [{a.account_code}] {a.account_name} ({a.account_type})
                          </option>
                        ))}
                      </select>
                    </td>
                    <td>
                      <input
                        type="text"
                        className="form-control"
                        style={{ padding: '6px' }}
                        placeholder="Memo..."
                        value={l.description}
                        onChange={(e) => {
                          const updated = [...lines];
                          updated[idx].description = e.target.value;
                          setLines(updated);
                        }}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        step="0.01"
                        className="form-control mono-num"
                        style={{ padding: '6px' }}
                        value={l.debit_amount}
                        onChange={(e) => {
                          const val = parseFloat(e.target.value) || 0;
                          const updated = [...lines];
                          updated[idx].debit_amount = val;
                          if (val > 0) updated[idx].credit_amount = 0;
                          setLines(updated);
                        }}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        step="0.01"
                        className="form-control mono-num"
                        style={{ padding: '6px' }}
                        value={l.credit_amount}
                        onChange={(e) => {
                          const val = parseFloat(e.target.value) || 0;
                          const updated = [...lines];
                          updated[idx].credit_amount = val;
                          if (val > 0) updated[idx].debit_amount = 0;
                          setLines(updated);
                        }}
                      />
                    </td>
                    <td>
                      {lines.length > 2 && (
                        <button
                          type="button"
                          className="btn btn-danger btn-sm"
                          style={{ padding: '4px' }}
                          onClick={() => handleRemoveLine(idx)}
                        >
                          <Trash2 size={14} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Balancing Invariant Status Box */}
        <div
          style={{
            background: isBalanced ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
            border: `1px solid ${isBalanced ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
            borderRadius: '8px',
            padding: '14px 18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '16px'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {isBalanced ? (
              <CheckCircle2 size={20} color="#34d399" />
            ) : (
              <AlertCircle size={20} color="#f87171" />
            )}
            <div>
              <div style={{ fontWeight: 600, color: isBalanced ? '#34d399' : '#f87171', fontSize: '0.875rem' }}>
                {isBalanced ? 'Entry Perfectly Balanced (Debit == Credit)' : 'Unbalanced Entry (Double-Entry Violation)'}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {isBalanced
                  ? 'Ready to post into general ledger with audit timestamp.'
                  : `Discrepancy: ₹${discrepancy.toFixed(2)}. Total Debits and Total Credits must balance.`}
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '24px', fontSize: '0.875rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Total Debit:</span>{' '}
              <strong className="mono-num" style={{ color: '#ffffff' }}>₹{totalDebit.toFixed(2)}</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Total Credit:</span>{' '}
              <strong className="mono-num" style={{ color: '#ffffff' }}>₹{totalCredit.toFixed(2)}</strong>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={!isBalanced || isSubmitting}>
            {isSubmitting ? 'Posting to GL...' : 'Post Balanced Journal Entry'}
          </button>
        </div>
      </form>
    </Modal>
  );
};
