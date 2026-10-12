import React, { useState, useEffect } from 'react';
import { TaxConfiguration } from '../types/finance';
import { api } from '../services/api';
import { Percent, ShieldCheck, FileSpreadsheet } from 'lucide-react';

interface GSTTaxConfigurationViewProps {
  taxConfigs: TaxConfiguration[];
}

export const GSTTaxConfigurationView: React.FC<GSTTaxConfigurationViewProps> = ({
  taxConfigs
}) => {
  const [taxSummary, setTaxSummary] = useState<any>(null);

  useEffect(() => {
    api.getTaxSummary().then(setTaxSummary).catch(console.error);
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>GST & Healthcare Tax Configuration</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Module 6.4: Indian GST Compliance, CGST / SGST / IGST Slabs, HSN/SAC Mappings & GSTR-1 Summary
          </p>
        </div>
      </div>

      {/* GSTR-1 Summary KPI Grid */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-label">Taxable Turnover (Billed)</div>
          <div className="kpi-value">₹{taxSummary?.taxable_turnover || '0.00'}</div>
          <div className="kpi-sub">Total eligible taxable base</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">CGST Output Collected</div>
          <div className="kpi-value" style={{ color: '#38bdf8' }}>₹{taxSummary?.cgst_collected || '0.00'}</div>
          <div className="kpi-sub">Central GST liability</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">SGST Output Collected</div>
          <div className="kpi-value" style={{ color: '#38bdf8' }}>₹{taxSummary?.sgst_collected || '0.00'}</div>
          <div className="kpi-sub">State GST liability</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-label">IGST Output Collected</div>
          <div className="kpi-value" style={{ color: '#fbbf24' }}>₹{taxSummary?.igst_collected || '0.00'}</div>
          <div className="kpi-sub">Inter-State GST liability</div>
        </div>
      </div>

      {/* GST Slabs Table */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3>Configured Hospital Tax Slabs & HSN/SAC Codes</h3>
        </div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Slab Code</th>
                <th>Classification Name</th>
                <th style={{ textAlign: 'center' }}>Total GST Rate</th>
                <th style={{ textAlign: 'center' }}>CGST Split</th>
                <th style={{ textAlign: 'center' }}>SGST Split</th>
                <th style={{ textAlign: 'center' }}>IGST Split</th>
                <th>HSN / SAC Code</th>
                <th>Default Status</th>
              </tr>
            </thead>
            <tbody>
              {taxConfigs.map((tc) => (
                <tr key={tc.id}>
                  <td><strong style={{ color: '#38bdf8' }}>{tc.code}</strong></td>
                  <td style={{ fontWeight: 600 }}>{tc.name}</td>
                  <td style={{ textAlign: 'center', fontWeight: 700 }} className="mono-num">{tc.rate_percentage}%</td>
                  <td style={{ textAlign: 'center' }} className="mono-num">{tc.cgst_rate}%</td>
                  <td style={{ textAlign: 'center' }} className="mono-num">{tc.sgst_rate}%</td>
                  <td style={{ textAlign: 'center' }} className="mono-num">{tc.igst_rate}%</td>
                  <td className="mono-num" style={{ color: 'var(--text-muted)' }}>{tc.hsn_sac_code}</td>
                  <td>
                    {tc.is_default ? (
                      <span className="badge badge-success">DEFAULT</span>
                    ) : (
                      <span className="badge badge-neutral">CONFIGURED</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Compliance Note */}
      <div className="card" style={{ background: 'rgba(255, 255, 255, 0.02)' }}>
        <h4 style={{ fontSize: '0.875rem', fontWeight: 600, marginBottom: '6px', color: '#cbd5e1' }}>
          Indian GST Healthcare Statutory Framework Notice
        </h4>
        <p style={{ fontSize: '0.8125rem', color: 'var(--text-dim)' }}>
          Clinical healthcare services rendered by hospital clinical establishments and medical doctors are generally exempt under SAC 9993.
          Diagnostic technical services, non-exempt room tariffs exceeding threshold limits, and retail pharmaceutical sales require separate GST slab attribution (5%, 12%, 18%).
          Intra-state transactions split tax equally between CGST and SGST; inter-state supplies apply IGST.
        </p>
      </div>
    </div>
  );
};
