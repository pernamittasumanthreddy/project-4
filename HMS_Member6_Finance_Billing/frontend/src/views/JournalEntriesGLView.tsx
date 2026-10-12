import React, { useState } from 'react';
import { JournalEntry } from '../types/finance';
import { StatusBadge } from '../components/StatusBadge';
import { Plus, Scale, ChevronDown, ChevronRight } from 'lucide-react';

interface JournalEntriesGLViewProps {
  journals: JournalEntry[];
  onOpenNewJournal: () => void;
}

export const JournalEntriesGLView: React.FC<JournalEntriesGLViewProps> = ({
  journals,
  onOpenNewJournal
}) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Double-Entry Journal Vouchers & General Ledger</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Auditable Accounting Transactions Guaranteed Balanced (Sum Debit == Sum Credit)
          </p>
        </div>
        <button className="btn btn-primary" onClick={onOpenNewJournal}>
          <Plus size={16} /> New Journal Voucher
        </button>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th style={{ width: '40px' }}></th>
              <th>Voucher #</th>
              <th>Posting Date</th>
              <th>Narrative / Description</th>
              <th>Source Transaction</th>
              <th style={{ textAlign: 'right' }}>Total Debit (₹)</th>
              <th style={{ textAlign: 'right' }}>Total Credit (₹)</th>
              <th>Posted By</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {journals.length === 0 ? (
              <tr>
                <td colSpan={9} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No journal vouchers recorded.
                </td>
              </tr>
            ) : (
              journals.map((j) => (
                <React.Fragment key={j.id}>
                  <tr style={{ cursor: 'pointer' }} onClick={() => toggleExpand(j.id)}>
                    <td style={{ textAlign: 'center' }}>
                      {expandedId === j.id ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                    </td>
                    <td><strong style={{ color: '#38bdf8' }}>{j.entry_number}</strong></td>
                    <td style={{ fontSize: '0.8125rem' }}>{j.entry_date}</td>
                    <td style={{ fontWeight: 600 }}>{j.description}</td>
                    <td>
                      <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>
                        {j.source_type_display}
                      </span>
                    </td>
                    <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#ffffff' }}>
                      ₹{j.total_debit}
                    </td>
                    <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#ffffff' }}>
                      ₹{j.total_credit}
                    </td>
                    <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{j.posted_by}</td>
                    <td><StatusBadge status={j.status} /></td>
                  </tr>

                  {/* Expanded Line Items Leg Drawer */}
                  {expandedId === j.id && (
                    <tr style={{ background: '#0f172a' }}>
                      <td colSpan={9} style={{ padding: '16px 24px' }}>
                        <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '8px' }}>
                          Distribution Legs for Voucher {j.entry_number}
                        </div>
                        <table style={{ background: '#1e293b', borderRadius: '6px' }}>
                          <thead>
                            <tr>
                              <th>Account</th>
                              <th>Leg Memo</th>
                              <th style={{ textAlign: 'right' }}>Debit Leg (₹)</th>
                              <th style={{ textAlign: 'right' }}>Credit Leg (₹)</th>
                            </tr>
                          </thead>
                          <tbody>
                            {j.lines?.map((leg, lIdx) => (
                              <tr key={lIdx}>
                                <td>
                                  <strong style={{ color: '#38bdf8' }}>{leg.account_code}</strong> — {leg.account_name}
                                </td>
                                <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{leg.description || '—'}</td>
                                <td className="mono-num" style={{ textAlign: 'right', color: parseFloat(leg.debit_amount) > 0 ? '#34d399' : 'inherit' }}>
                                  {parseFloat(leg.debit_amount) > 0 ? `₹${leg.debit_amount}` : '—'}
                                </td>
                                <td className="mono-num" style={{ textAlign: 'right', color: parseFloat(leg.credit_amount) > 0 ? '#38bdf8' : 'inherit' }}>
                                  {parseFloat(leg.credit_amount) > 0 ? `₹${leg.credit_amount}` : '—'}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
