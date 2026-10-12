import React, { useState, useEffect } from 'react';
import { Invoice, InvoiceTimelineResponse } from '../types/finance';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { Printer, ArrowLeft, Clock, ShieldCheck, IndianRupee } from 'lucide-react';

interface InvoiceDetailsTimelineViewProps {
  invoices: Invoice[];
  selectedInvoice: Invoice | null;
  onSelectInvoice: (inv: Invoice) => void;
  onPrintInvoice: (inv: Invoice) => void;
  onBackToInvoices: () => void;
}

export const InvoiceDetailsTimelineView: React.FC<InvoiceDetailsTimelineViewProps> = ({
  invoices,
  selectedInvoice,
  onSelectInvoice,
  onPrintInvoice,
  onBackToInvoices
}) => {
  const [activeInvoice, setActiveInvoice] = useState<Invoice>(selectedInvoice || invoices[0]);
  const [timelineData, setTimelineData] = useState<InvoiceTimelineResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (selectedInvoice) {
      setActiveInvoice(selectedInvoice);
    }
  }, [selectedInvoice]);

  useEffect(() => {
    if (activeInvoice?.id) {
      loadTimeline(activeInvoice.id);
    }
  }, [activeInvoice?.id]);

  const loadTimeline = async (id: string) => {
    setIsLoading(true);
    try {
      const data = await api.getInvoiceTimeline(id);
      setTimelineData(data);
    } catch (err) {
      console.error('Timeline fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (!activeInvoice) {
    return (
      <div className="card" style={{ padding: '40px', textAlign: 'center' }}>
        <h3>No invoice selected.</h3>
        <button className="btn btn-primary" style={{ marginTop: '16px' }} onClick={onBackToInvoices}>
          Return to Invoice List
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Top Header & Selector */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button className="btn btn-outline btn-sm" onClick={onBackToInvoices}>
            <ArrowLeft size={16} /> Back
          </button>
          <div>
            <h1>Invoice Details & Financial Timeline</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8125rem' }}>
              Unique Feature A: Chronological Audit Trail of Invoices, Payments, Concessions & Claims
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <select
            className="form-control"
            style={{ width: 'auto' }}
            value={activeInvoice.id}
            onChange={(e) => {
              const inv = invoices.find((i) => i.id === e.target.value);
              if (inv) {
                setActiveInvoice(inv);
                onSelectInvoice(inv);
              }
            }}
          >
            {invoices.map((i) => (
              <option key={i.id} value={i.id}>
                {i.invoice_number} ({i.patient_name})
              </option>
            ))}
          </select>

          <button className="btn btn-primary btn-sm" onClick={() => onPrintInvoice(activeInvoice)}>
            <Printer size={14} /> Print Bill
          </button>
        </div>
      </div>

      {/* Invoice Key Header Box */}
      <div
        className="card"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(5, 1fr)',
          gap: '16px',
          marginBottom: '24px',
          background: 'linear-gradient(180deg, #1e293b 0%, #152238 100%)'
        }}
      >
        <div>
          <div className="kpi-label">Invoice Number</div>
          <div style={{ fontWeight: 700, fontSize: '1.1rem', color: '#38bdf8' }}>{activeInvoice.invoice_number}</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '2px' }}>
            Issued: {activeInvoice.issue_date}
          </div>
        </div>

        <div>
          <div className="kpi-label">Patient & MRN</div>
          <div style={{ fontWeight: 600 }}>{activeInvoice.patient_name}</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{activeInvoice.patient_mrn}</div>
        </div>

        <div>
          <div className="kpi-label">Net Bill Amount</div>
          <div className="mono-num" style={{ fontWeight: 700, fontSize: '1.25rem', color: '#ffffff' }}>
            ₹{activeInvoice.total_net}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Tax: ₹{activeInvoice.total_tax}</div>
        </div>

        <div>
          <div className="kpi-label">Settled / Balance Due</div>
          <div className="mono-num" style={{ fontWeight: 700, fontSize: '1.25rem', color: parseFloat(activeInvoice.balance_due) > 0 ? '#f87171' : '#34d399' }}>
            ₹{activeInvoice.balance_due}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#34d399' }}>Paid: ₹{activeInvoice.paid_amount}</div>
        </div>

        <div>
          <div className="kpi-label">Status & State</div>
          <div style={{ marginTop: '2px' }}>
            <StatusBadge status={activeInvoice.status} />
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '6px' }}>
            {activeInvoice.is_interstate ? 'Inter-State (IGST)' : 'Intra-State (CGST+SGST)'}
          </div>
        </div>
      </div>

      {/* Two Column Layout: Lines vs Timeline */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px' }}>
        {/* Left Column: Itemized Line Items Table */}
        <div className="card">
          <div className="card-header">
            <h3>Itemized Clinical Lines</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
              {activeInvoice.lines?.length || 0} billable items
            </span>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Service</th>
                  <th>Dept</th>
                  <th style={{ textAlign: 'right' }}>Qty</th>
                  <th style={{ textAlign: 'right' }}>Rate (₹)</th>
                  <th style={{ textAlign: 'right' }}>Tax (₹)</th>
                  <th style={{ textAlign: 'right' }}>Net (₹)</th>
                </tr>
              </thead>
              <tbody>
                {activeInvoice.lines?.map((line, idx) => (
                  <tr key={idx}>
                    <td>
                      <div style={{ fontWeight: 600 }}>{line.service_name}</div>
                      <div style={{ fontSize: '0.6875rem', color: 'var(--text-dim)' }}>
                        SAC: {line.hsn_sac_code} | Code: {line.service_code}
                      </div>
                    </td>
                    <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{line.department}</td>
                    <td className="mono-num" style={{ textAlign: 'right' }}>{line.quantity}</td>
                    <td className="mono-num" style={{ textAlign: 'right' }}>₹{line.unit_price}</td>
                    <td className="mono-num" style={{ textAlign: 'right', color: '#94a3b8' }}>₹{line.tax_amount || '0.00'}</td>
                    <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#ffffff' }}>
                      ₹{line.net_amount}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Tax Breakdown Subcard */}
          <div
            style={{
              marginTop: '16px',
              padding: '14px 18px',
              background: 'rgba(0, 0, 0, 0.2)',
              borderRadius: '6px',
              fontSize: '0.8125rem',
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '12px'
            }}
          >
            <div>
              <span style={{ color: 'var(--text-dim)' }}>Taxable Value:</span>
              <div className="mono-num" style={{ fontWeight: 600 }}>₹{activeInvoice.total_taxable}</div>
            </div>
            <div>
              <span style={{ color: 'var(--text-dim)' }}>CGST Amount:</span>
              <div className="mono-num" style={{ fontWeight: 600 }}>₹{activeInvoice.total_cgst}</div>
            </div>
            <div>
              <span style={{ color: 'var(--text-dim)' }}>SGST Amount:</span>
              <div className="mono-num" style={{ fontWeight: 600 }}>₹{activeInvoice.total_sgst}</div>
            </div>
            <div>
              <span style={{ color: 'var(--text-dim)' }}>IGST Amount:</span>
              <div className="mono-num" style={{ fontWeight: 600 }}>₹{activeInvoice.total_igst}</div>
            </div>
          </div>
        </div>

        {/* Right Column: Unified Financial Timeline */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Clock size={18} color="#38bdf8" />
              <h3>Unified Financial Timeline</h3>
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
              {timelineData?.events?.length || 0} Events Logged
            </span>
          </div>

          {isLoading ? (
            <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-dim)' }}>
              Loading chronological financial audit events...
            </div>
          ) : (
            <div className="timeline">
              {timelineData?.events?.map((ev, idx) => (
                <div key={idx} className="timeline-item">
                  <div className="timeline-dot" />
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div className="timeline-title">{ev.title}</div>
                    <span className="mono-num" style={{ fontWeight: 700, fontSize: '0.875rem', color: '#38bdf8' }}>
                      ₹{ev.amount}
                    </span>
                  </div>
                  <div className="timeline-time">
                    {new Date(ev.timestamp).toLocaleString()} • Actor: <strong>{ev.actor}</strong>
                  </div>
                  <div className="timeline-desc">{ev.details}</div>
                  <div style={{ marginTop: '6px' }}>
                    <StatusBadge status={ev.status} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
