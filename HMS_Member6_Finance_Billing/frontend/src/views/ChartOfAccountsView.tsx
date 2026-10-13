import React, { useState } from 'react';
import { ChartOfAccount } from '../types/finance';
import { api } from '../services/api';
import { BookOpen, Scale, CheckCircle2, AlertCircle } from 'lucide-react';
import { Modal } from '../components/Modal';

interface ChartOfAccountsViewProps {
  accounts: ChartOfAccount[];
}

export const ChartOfAccountsView: React.FC<ChartOfAccountsViewProps> = ({
  accounts
}) => {
  const [filterType, setFilterType] = useState('ALL');
  const [trialBalanceData, setTrialBalanceData] = useState<any>(null);
  const [isCalculating, setIsCalculating] = useState(false);

  const filtered = accounts.filter((a) => {
    return filterType === 'ALL' || a.account_type === filterType;
  });

  const handleGenerateTrialBalance = async () => {
    setIsCalculating(true);
    try {
      const data = await api.getTrialBalance();
      setTrialBalanceData(data);
    } catch (err: any) {
      alert(`Trial balance error: ${err.message}`);
    } finally {
      setIsCalculating(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Chart of Accounts & General Ledger Directory</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Module 6.5: 5-Category Standard Chart of Accounts (Assets, Liabilities, Equity, Revenue, Expenses)
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleGenerateTrialBalance} disabled={isCalculating}>
          <Scale size={16} /> {isCalculating ? 'Computing Ledger...' : 'Generate Live Trial Balance'}
        </button>
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        {['ALL', 'ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE'].map((t) => (
          <button
            key={t}
            className={`btn btn-sm ${filterType === t ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setFilterType(t)}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Chart of Accounts Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Account Code</th>
              <th>Account Title</th>
              <th>Classification</th>
              <th>Category Normal Balance</th>
              <th style={{ textAlign: 'right' }}>Current Balance (₹)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((acct) => (
              <tr key={acct.id}>
                <td><strong style={{ color: '#38bdf8' }}>{acct.account_code}</strong></td>
                <td style={{ fontWeight: 600 }}>{acct.account_name}</td>
                <td>
                  <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>
                    {acct.account_type_display}
                  </span>
                </td>
                <td style={{ fontSize: '0.8125rem', color: 'var(--text-dim)' }}>
                  {acct.account_type === 'ASSET' || acct.account_type === 'EXPENSE' ? 'Debit (Dr)' : 'Credit (Cr)'}
                </td>
                <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#ffffff' }}>
                  ₹{acct.current_balance}
                </td>
                <td>
                  <span className="badge badge-success">ACTIVE</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Trial Balance Modal */}
      <Modal
        isOpen={!!trialBalanceData}
        onClose={() => setTrialBalanceData(null)}
        title="General Ledger — Official Trial Balance Statement"
        maxWidth="760px"
      >
        {trialBalanceData && (
          <div>
            <div
              style={{
                background: trialBalanceData.is_balanced ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                border: `1px solid ${trialBalanceData.is_balanced ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                borderRadius: '6px',
                padding: '12px 16px',
                marginBottom: '16px',
                display: 'flex',
                alignItems: 'center',
                gap: '10px'
              }}
            >
              {trialBalanceData.is_balanced ? (
                <CheckCircle2 size={20} color="#34d399" />
              ) : (
                <AlertCircle size={20} color="#f87171" />
              )}
              <div>
                <div style={{ fontWeight: 600, color: trialBalanceData.is_balanced ? '#34d399' : '#f87171' }}>
                  {trialBalanceData.is_balanced
                    ? 'Trial Balance Balanced: Total Debit Equals Total Credit'
                    : 'Unbalanced Ledger Discrepancy Detected'}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Proof of mathematical integrity for double-entry bookkeeping.
                </div>
              </div>
            </div>

            <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto', marginBottom: '16px' }}>
              <table>
                <thead>
                  <tr>
                    <th>Code</th>
                    <th>Account Name</th>
                    <th>Type</th>
                    <th style={{ textAlign: 'right' }}>Debit (₹)</th>
                    <th style={{ textAlign: 'right' }}>Credit (₹)</th>
                  </tr>
                </thead>
                <tbody>
                  {trialBalanceData.accounts.map((row: any, i: number) => (
                    <tr key={i}>
                      <td><strong style={{ color: '#38bdf8' }}>{row.account_code}</strong></td>
                      <td>{row.account_name}</td>
                      <td style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{row.account_type}</td>
                      <td className="mono-num" style={{ textAlign: 'right' }}>
                        {parseFloat(row.debit) > 0 ? `₹${row.debit}` : '—'}
                      </td>
                      <td className="mono-num" style={{ textAlign: 'right' }}>
                        {parseFloat(row.credit) > 0 ? `₹${row.credit}` : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div
              style={{
                display: 'flex',
                justifyContent: 'flex-end',
                gap: '24px',
                padding: '12px 16px',
                background: 'rgba(0, 0, 0, 0.25)',
                borderRadius: '6px',
                fontWeight: 700,
                fontSize: '1rem'
              }}
            >
              <div>
                <span style={{ color: 'var(--text-dim)' }}>Total Debits:</span>{' '}
                <span className="mono-num" style={{ color: '#ffffff' }}>₹{trialBalanceData.total_debit}</span>
              </div>
              <div>
                <span style={{ color: 'var(--text-dim)' }}>Total Credits:</span>{' '}
                <span className="mono-num" style={{ color: '#ffffff' }}>₹{trialBalanceData.total_credit}</span>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};
