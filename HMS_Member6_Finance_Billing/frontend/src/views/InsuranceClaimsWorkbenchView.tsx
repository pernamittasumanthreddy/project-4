import React, { useState } from 'react';
import { InsuranceClaim } from '../types/finance';
import { StatusBadge } from '../components/StatusBadge';
import { FileCheck2, AlertOctagon, Send, CheckCircle2, RotateCw } from 'lucide-react';
import { Modal } from '../components/Modal';

interface InsuranceClaimsWorkbenchViewProps {
  claims: InsuranceClaim[];
  onAdjudicateClaim: (claimId: string, data: any) => Promise<void>;
  onResubmitClaim: (claimId: string, correctiveAction: string) => Promise<void>;
}

export const InsuranceClaimsWorkbenchView: React.FC<InsuranceClaimsWorkbenchViewProps> = ({
  claims,
  onAdjudicateClaim,
  onResubmitClaim
}) => {
  const [activeTab, setActiveTab] = useState<'ALL' | 'DENIAL_WORKBENCH'>('ALL');
  
  // Resubmission State
  const [resubmittingClaim, setResubmittingClaim] = useState<InsuranceClaim | null>(null);
  const [correctiveAction, setCorrectiveAction] = useState('');
  const [isResubmitting, setIsResubmitting] = useState(false);

  // Adjudication State
  const [adjudicatingClaim, setAdjudicatingClaim] = useState<InsuranceClaim | null>(null);
  const [adjStatus, setAdjStatus] = useState<'APPROVED' | 'PARTIALLY_APPROVED' | 'REJECTED'>('APPROVED');
  const [approvedAmt, setApprovedAmt] = useState('');
  const [denialCode, setDenialCode] = useState('DOCS_MISSING');
  const [denialReason, setDenialReason] = useState('');
  const [isAdjudicating, setIsAdjudicating] = useState(false);

  const deniedClaims = claims.filter(
    (c) => c.status === 'REJECTED' || c.status === 'PARTIALLY_APPROVED' || c.status === 'RESUBMITTED'
  );

  const displayedClaims = activeTab === 'DENIAL_WORKBENCH' ? deniedClaims : claims;

  const handleOpenResubmit = (c: InsuranceClaim) => {
    setResubmittingClaim(c);
    setCorrectiveAction('Attached signed discharge summary & clinical justification notes.');
  };

  const handleConfirmResubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resubmittingClaim) return;
    setIsResubmitting(true);
    try {
      await onResubmitClaim(resubmittingClaim.id, correctiveAction);
      setResubmittingClaim(null);
    } catch (err: any) {
      alert(`Resubmission error: ${err.message}`);
    } finally {
      setIsResubmitting(false);
    }
  };

  const handleOpenAdjudicate = (c: InsuranceClaim) => {
    setAdjudicatingClaim(c);
    setAdjStatus('APPROVED');
    setApprovedAmt(c.claim_amount);
    setDenialCode('DOCS_MISSING');
    setDenialReason('');
  };

  const handleConfirmAdjudicate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!adjudicatingClaim) return;
    setIsAdjudicating(true);
    try {
      await onAdjudicateClaim(adjudicatingClaim.id, {
        status: adjStatus,
        approved_amount: approvedAmt,
        denial_code: denialCode,
        denial_reason: denialReason
      });
      setAdjudicatingClaim(null);
    } catch (err: any) {
      alert(`Adjudication error: ${err.message}`);
    } finally {
      setIsAdjudicating(false);
    }
  };

  return (
    <div>
      {/* Title & Tab Switcher */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Insurance Claims & Denial Workbench</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Unique Feature C: Pre-Auth Tracking, TPA Adjudication & Deficiency Denial Resolution
          </p>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            className={`btn btn-sm ${activeTab === 'ALL' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setActiveTab('ALL')}
          >
            All Claims Pipeline ({claims.length})
          </button>
          <button
            className={`btn btn-sm ${activeTab === 'DENIAL_WORKBENCH' ? 'btn-danger' : 'btn-outline'}`}
            onClick={() => setActiveTab('DENIAL_WORKBENCH')}
            style={activeTab === 'DENIAL_WORKBENCH' ? {} : { color: '#f87171', borderColor: 'rgba(239, 68, 68, 0.4)' }}
          >
            <AlertOctagon size={14} /> Denial Workbench ({deniedClaims.length})
          </button>
        </div>
      </div>

      {activeTab === 'DENIAL_WORKBENCH' && (
        <div
          className="card"
          style={{
            background: 'rgba(239, 68, 68, 0.08)',
            border: '1px solid rgba(239, 68, 68, 0.25)',
            padding: '16px 20px',
            marginBottom: '20px'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <AlertOctagon size={20} color="#f87171" />
            <div>
              <div style={{ fontWeight: 600, color: '#f87171', fontSize: '0.875rem' }}>
                Active Denial Management & Deficiency Remediation Workbench
              </div>
              <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                Targeting zero revenue leakage: inspect insurer denial reason codes, review missing clinical documentation,
                attach corrections, and resubmit claims with auditable history.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Claims Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Claim Reference #</th>
              <th>Pre-Auth #</th>
              <th>Insurer / TPA</th>
              <th>Patient</th>
              <th style={{ textAlign: 'right' }}>Claimed Amount (₹)</th>
              <th style={{ textAlign: 'right' }}>Approved Amount (₹)</th>
              <th>Status</th>
              <th>Denial Reason / Deficiency</th>
              <th style={{ textAlign: 'center' }}>Workbench Actions</th>
            </tr>
          </thead>
          <tbody>
            {displayedClaims.length === 0 ? (
              <tr>
                <td colSpan={9} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No claims found in this view.
                </td>
              </tr>
            ) : (
              displayedClaims.map((c) => (
                <tr key={c.id}>
                  <td><strong style={{ color: '#38bdf8' }}>{c.claim_number}</strong></td>
                  <td className="mono-num" style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                    {c.pre_auth_number || 'N/A'}
                  </td>
                  <td style={{ fontWeight: 600 }}>{c.payer_name}</td>
                  <td>{c.patient_name || 'Patient Reference'}</td>
                  <td className="mono-num" style={{ textAlign: 'right', fontWeight: 600 }}>
                    ₹{c.claim_amount}
                  </td>
                  <td className="mono-num" style={{ textAlign: 'right', color: '#34d399', fontWeight: 700 }}>
                    ₹{c.approved_amount}
                  </td>
                  <td><StatusBadge status={c.status} /></td>
                  <td style={{ fontSize: '0.8125rem', maxWidth: '240px', color: c.status === 'REJECTED' ? '#f87171' : 'var(--text-muted)' }}>
                    {c.denial_reason || '—'}
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <div style={{ display: 'inline-flex', gap: '6px' }}>
                      {c.status === 'SUBMITTED' && (
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={() => handleOpenAdjudicate(c)}
                        >
                          Adjudicate
                        </button>
                      )}
                      {(c.status === 'REJECTED' || c.status === 'PARTIALLY_APPROVED') && (
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleOpenResubmit(c)}
                        >
                          <RotateCw size={14} /> Resubmit Claim
                        </button>
                      )}
                      {c.status === 'RESUBMITTED' && (
                        <span style={{ fontSize: '0.75rem', color: '#fbbf24', fontWeight: 600 }}>
                          Resubmitted (Awaiting TPA)
                        </span>
                      )}
                      {c.status === 'APPROVED' && (
                        <span style={{ fontSize: '0.75rem', color: '#34d399', fontWeight: 600 }}>
                          Approved
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Denial Workbench Resubmit Modal */}
      <Modal
        isOpen={!!resubmittingClaim}
        onClose={() => setResubmittingClaim(null)}
        title={`Denial Workbench — Resubmit Claim ${resubmittingClaim?.claim_number}`}
        maxWidth="620px"
      >
        <form onSubmit={handleConfirmResubmit}>
          <div style={{ background: 'rgba(239, 68, 68, 0.08)', padding: '12px 16px', borderRadius: '6px', marginBottom: '16px', fontSize: '0.8125rem' }}>
            <div style={{ color: '#f87171', fontWeight: 600 }}>Original Rejection Notice:</div>
            <div>{resubmittingClaim?.denial_reason}</div>
          </div>

          <div className="form-group">
            <label className="form-label">Corrective Action Taken & Upload Notes</label>
            <textarea
              rows={4}
              className="form-control"
              placeholder="Detail deficiency remediation (e.g. Attached surgeon signed OT notes, revised tariff breakdown, or enhanced pre-auth approval letter)..."
              value={correctiveAction}
              onChange={(e) => setCorrectiveAction(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <button type="button" className="btn btn-secondary" onClick={() => setResubmittingClaim(null)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isResubmitting}>
              {isResubmitting ? 'Submitting...' : 'Resolve Deficiencies & Resubmit'}
            </button>
          </div>
        </form>
      </Modal>

      {/* Adjudication Modal */}
      <Modal
        isOpen={!!adjudicatingClaim}
        onClose={() => setAdjudicatingClaim(null)}
        title={`Adjudicate Claim ${adjudicatingClaim?.claim_number}`}
        maxWidth="600px"
      >
        <form onSubmit={handleConfirmAdjudicate}>
          <div className="form-group">
            <label className="form-label">Adjudication Decision</label>
            <select
              className="form-control"
              value={adjStatus}
              onChange={(e) => setAdjStatus(e.target.value as any)}
            >
              <option value="APPROVED">Approve Full Claim</option>
              <option value="PARTIALLY_APPROVED">Partially Approve (Deductions Applied)</option>
              <option value="REJECTED">Reject / Deny Claim</option>
            </select>
          </div>

          {adjStatus !== 'REJECTED' && (
            <div className="form-group">
              <label className="form-label">Approved Settlement Amount (₹)</label>
              <input
                type="number"
                step="0.01"
                className="form-control mono-num"
                value={approvedAmt}
                onChange={(e) => setApprovedAmt(e.target.value)}
                required
              />
            </div>
          )}

          {adjStatus !== 'APPROVED' && (
            <>
              <div className="form-group">
                <label className="form-label">Denial Root Cause Code</label>
                <select
                  className="form-control"
                  value={denialCode}
                  onChange={(e) => setDenialCode(e.target.value)}
                >
                  <option value="DOCS_MISSING">DOCS_MISSING — Missing Clinical Discharge Summary / Documents</option>
                  <option value="NON_COVERED">NON_COVERED — Non-payable / Exclusion Items Billed</option>
                  <option value="PRE_AUTH_EXCEEDED">PRE_AUTH_EXCEEDED — Billed Amount Exceeded Approved Pre-Auth</option>
                  <option value="DIAGNOSIS_MISMATCH">DIAGNOSIS_MISMATCH — Diagnosis Mismatch with Policy Coverage</option>
                  <option value="TARIFF_DISPUTE">TARIFF_DISPUTE — Rates Exceeded Agreed Tariff Schedule</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Denial Explanation</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Specific deduction reasoning..."
                  value={denialReason}
                  onChange={(e) => setDenialReason(e.target.value)}
                  required
                />
              </div>
            </>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
            <button type="button" className="btn btn-secondary" onClick={() => setAdjudicatingClaim(null)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isAdjudicating}>
              {isAdjudicating ? 'Processing...' : 'Save Adjudication Result'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
