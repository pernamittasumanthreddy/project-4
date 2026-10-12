import React, { useState } from 'react';
import { InsurancePayer, InsurancePolicy } from '../types/finance';
import { ShieldCheck, UserCheck, Plus } from 'lucide-react';

interface InsurancePayersPoliciesViewProps {
  payers: InsurancePayer[];
  policies: InsurancePolicy[];
}

export const InsurancePayersPoliciesView: React.FC<InsurancePayersPoliciesViewProps> = ({
  payers,
  policies
}) => {
  const [activeTab, setActiveTab] = useState<'PAYERS' | 'POLICIES'>('PAYERS');

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Insurance Payers & Patient Policies</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            TPA Registry, Turnaround Times (TAT), Government Schemes & Patient Coverage Limits
          </p>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            className={`btn btn-sm ${activeTab === 'PAYERS' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setActiveTab('PAYERS')}
          >
            Payer Registry ({payers.length})
          </button>
          <button
            className={`btn btn-sm ${activeTab === 'POLICIES' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setActiveTab('POLICIES')}
          >
            Active Policies ({policies.length})
          </button>
        </div>
      </div>

      {activeTab === 'PAYERS' ? (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Payer Code</th>
                <th>Insurance Company / TPA Name</th>
                <th>Classification</th>
                <th>Contact Email</th>
                <th>Helpdesk Helpline</th>
                <th style={{ textAlign: 'center' }}>Settlement TAT (Days)</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {payers.map((p) => (
                <tr key={p.id}>
                  <td><strong style={{ color: '#38bdf8' }}>{p.code}</strong></td>
                  <td style={{ fontWeight: 600 }}>{p.name}</td>
                  <td>
                    <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>
                      {p.payer_type_display}
                    </span>
                  </td>
                  <td style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{p.tpa_contact_email || '—'}</td>
                  <td style={{ fontSize: '0.8125rem' }}>{p.tpa_contact_phone || '—'}</td>
                  <td style={{ textAlign: 'center', fontWeight: 600 }} className="mono-num">
                    {p.settlement_tat_days} Days
                  </td>
                  <td>
                    <span className="badge badge-success">ACTIVE</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Policy Number</th>
                <th>Patient Name</th>
                <th>Insurer / TPA</th>
                <th>Health Card #</th>
                <th style={{ textAlign: 'right' }}>Sum Insured (₹)</th>
                <th style={{ textAlign: 'center' }}>Co-pay %</th>
                <th>Validity Period</th>
              </tr>
            </thead>
            <tbody>
              {policies.map((pol) => (
                <tr key={pol.id}>
                  <td><strong style={{ color: '#fbbf24' }}>{pol.policy_number}</strong></td>
                  <td style={{ fontWeight: 600 }}>{pol.patient_name}</td>
                  <td>{pol.payer_name || 'Insurance Provider'}</td>
                  <td className="mono-num" style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                    {pol.card_number || 'N/A'}
                  </td>
                  <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }}>
                    ₹{pol.sum_insured}
                  </td>
                  <td style={{ textAlign: 'center', fontWeight: 600 }}>{pol.copay_percentage}%</td>
                  <td style={{ fontSize: '0.8125rem' }}>
                    {pol.valid_from} to {pol.valid_to}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
