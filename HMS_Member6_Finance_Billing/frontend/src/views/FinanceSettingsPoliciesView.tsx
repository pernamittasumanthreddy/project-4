import React, { useState } from 'react';
import { BillingEntity } from '../types/finance';
import { Sliders, Save, CheckCircle2 } from 'lucide-react';

interface FinanceSettingsPoliciesViewProps {
  billingEntities: BillingEntity[];
}

export const FinanceSettingsPoliciesView: React.FC<FinanceSettingsPoliciesViewProps> = ({
  billingEntities
}) => {
  const [refundThreshold, setRefundThreshold] = useState('5000');
  const [creditNoteThreshold, setCreditNoteThreshold] = useState('10000');
  const [opdGraceDays, setOpdGraceDays] = useState('7');
  const [ipdGraceDays, setIpdGraceDays] = useState('14');
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  const activeEntity = billingEntities[0];

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Finance Governance Settings & Approval Policies</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Unique Feature G: Configurable Financial Approval Limits, Invoicing Sequences & Payment Policies
          </p>
        </div>
      </div>

      <form onSubmit={handleSave}>
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px' }}>
          {/* Approval Thresholds Card */}
          <div className="card">
            <div className="card-header">
              <h3>Multi-Tier Approval Policy Thresholds</h3>
            </div>

            <div className="form-group">
              <label className="form-label">Refund Executive Approval Limit (₹)</label>
              <input
                type="number"
                className="form-control mono-num"
                value={refundThreshold}
                onChange={(e) => setRefundThreshold(e.target.value)}
                required
              />
              <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                Refunds exceeding this amount mandate two-tier sign-off by the Chief Financial Officer.
              </span>
            </div>

            <div className="form-group">
              <label className="form-label">Credit Note Concession Limit (₹)</label>
              <input
                type="number"
                className="form-control mono-num"
                value={creditNoteThreshold}
                onChange={(e) => setCreditNoteThreshold(e.target.value)}
                required
              />
              <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                Concessions above this limit require Medical Superintendent authorization.
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">OPD Payment Terms (Days)</label>
                <input
                  type="number"
                  className="form-control mono-num"
                  value={opdGraceDays}
                  onChange={(e) => setOpdGraceDays(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">IPD Payment Terms (Days)</label>
                <input
                  type="number"
                  className="form-control mono-num"
                  value={ipdGraceDays}
                  onChange={(e) => setIpdGraceDays(e.target.value)}
                  required
                />
              </div>
            </div>

            <button type="submit" className="btn btn-primary" style={{ marginTop: '8px' }}>
              <Save size={16} /> Save Policy Configurations
            </button>

            {isSaved && (
              <span style={{ marginLeft: '12px', fontSize: '0.8125rem', color: '#34d399', fontWeight: 600 }}>
                Policies updated successfully!
              </span>
            )}
          </div>

          {/* Legal Entity Registration Details */}
          <div className="card">
            <div className="card-header">
              <h3>Hospital Legal Billing Entity</h3>
            </div>

            {activeEntity && (
              <div style={{ fontSize: '0.875rem', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    Entity Legal Name:
                  </span>
                  <div style={{ fontWeight: 600, color: '#ffffff' }}>{activeEntity.legal_name}</div>
                </div>

                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    GST Identification Number (GSTIN):
                  </span>
                  <div className="mono-num" style={{ fontWeight: 700, color: '#38bdf8' }}>{activeEntity.gstin}</div>
                </div>

                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    Permanent Account Number (PAN):
                  </span>
                  <div className="mono-num">{activeEntity.pan}</div>
                </div>

                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    Hospital Registered Address:
                  </span>
                  <div style={{ color: 'var(--text-muted)' }}>{activeEntity.address}</div>
                </div>

                <div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    Invoice Numbering Pattern:
                  </span>
                  <div className="mono-num" style={{ color: '#fbbf24' }}>
                    {activeEntity.invoice_prefix}-00000 (Next: {activeEntity.invoice_next_seq})
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </form>
    </div>
  );
};
