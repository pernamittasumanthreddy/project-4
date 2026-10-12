import React from 'react';
import { Modal } from './Modal';
import { Invoice } from '../types/finance';
import { Printer } from 'lucide-react';
import { StatusBadge } from './StatusBadge';

interface InvoicePrintModalProps {
  isOpen: boolean;
  onClose: () => void;
  invoice: Invoice | null;
}

export const InvoicePrintModal: React.FC<InvoicePrintModalProps> = ({
  isOpen,
  onClose,
  invoice
}) => {
  if (!invoice) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Tax Invoice — ${invoice.invoice_number}`}
      maxWidth="800px"
      footer={
        <button className="btn btn-primary" onClick={handlePrint}>
          <Printer size={16} /> Print Official Document
        </button>
      }
    >
      <div
        id="printable-invoice"
        style={{
          background: '#ffffff',
          color: '#0f172a',
          padding: '28px',
          borderRadius: '8px',
          fontFamily: 'Inter, sans-serif'
        }}
      >
        {/* Hospital Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '2px solid #0284c7', paddingBottom: '16px', marginBottom: '20px' }}>
          <div>
            <h2 style={{ color: '#0369a1', fontSize: '1.35rem', fontWeight: 800 }}>
              {invoice.billing_entity_name || 'Hospital Enterprise Legal Unit'}
            </h2>
            <div style={{ fontSize: '0.8125rem', color: '#475569' }}>
              Tax Invoice & Healthcare Settlement Statement
            </div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '4px' }}>
              GSTIN: <strong>{invoice.billing_entity_gstin || '07AAAAA0000A1Z5'}</strong> | State: Delhi (07)
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#0f172a' }}>
              {invoice.invoice_number}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
              Date: <strong>{invoice.issue_date}</strong>
            </div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
              Due: <strong>{invoice.due_date}</strong>
            </div>
            <div style={{ marginTop: '6px' }}>
              <StatusBadge status={invoice.status} />
            </div>
          </div>
        </div>

        {/* Patient & Billing Address Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', background: '#f8fafc', padding: '14px', borderRadius: '6px', marginBottom: '20px', fontSize: '0.8125rem' }}>
          <div>
            <div style={{ color: '#64748b', fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase' }}>Billed To Patient:</div>
            <div style={{ fontWeight: 700, fontSize: '0.9375rem', color: '#0f172a' }}>{invoice.patient_name}</div>
            <div>MRN: <strong>{invoice.patient_mrn}</strong></div>
            <div>Patient State: <strong>State Code {invoice.patient_state_code}</strong></div>
          </div>
          <div>
            <div style={{ color: '#64748b', fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase' }}>Encounter Details:</div>
            <div>Type: <strong>{invoice.encounter_type}</strong></div>
            <div>Tax Jurisdiction: <strong>{invoice.is_interstate ? 'Inter-State (IGST Applicable)' : 'Intra-State (CGST + SGST Applicable)'}</strong></div>
          </div>
        </div>

        {/* Itemized Table */}
        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px', fontSize: '0.8125rem' }}>
          <thead>
            <tr style={{ background: '#f1f5f9', borderBottom: '1px solid #cbd5e1' }}>
              <th style={{ padding: '8px 10px', color: '#475569', textAlign: 'left' }}>#</th>
              <th style={{ padding: '8px 10px', color: '#475569', textAlign: 'left' }}>Service Description</th>
              <th style={{ padding: '8px 10px', color: '#475569', textAlign: 'left' }}>HSN/SAC</th>
              <th style={{ padding: '8px 10px', color: '#475569', textAlign: 'right' }}>Qty</th>
              <th style={{ padding: '8px 10px', color: '#475569', textAlign: 'right' }}>Rate (₹)</th>
              <th style={{ padding: '8px 10px', color: '#475569', textAlign: 'right' }}>Tax (₹)</th>
              <th style={{ padding: '8px 10px', color: '#475569', textAlign: 'right' }}>Amount (₹)</th>
            </tr>
          </thead>
          <tbody>
            {invoice.lines?.map((line, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid #e2e8f0' }}>
                <td style={{ padding: '8px 10px', color: '#64748b' }}>{idx + 1}</td>
                <td style={{ padding: '8px 10px', color: '#0f172a', fontWeight: 600 }}>{line.service_name}</td>
                <td style={{ padding: '8px 10px', color: '#64748b' }}>{line.hsn_sac_code}</td>
                <td style={{ padding: '8px 10px', textAlign: 'right', color: '#0f172a' }}>{line.quantity}</td>
                <td style={{ padding: '8px 10px', textAlign: 'right', color: '#0f172a' }}>₹{line.unit_price}</td>
                <td style={{ padding: '8px 10px', textAlign: 'right', color: '#64748b' }}>₹{line.tax_amount || '0.00'}</td>
                <td style={{ padding: '8px 10px', textAlign: 'right', color: '#0f172a', fontWeight: 700 }}>₹{line.net_amount}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Financial Summary */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px' }}>
          <div style={{ width: '280px', fontSize: '0.8125rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#475569' }}>
              <span>Gross Total:</span>
              <span style={{ fontWeight: 600 }}>₹{invoice.total_gross}</span>
            </div>
            {parseFloat(invoice.total_discount) > 0 && (
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#d97706' }}>
                <span>Discounts / Concessions:</span>
                <span style={{ fontWeight: 600 }}>-₹{invoice.total_discount}</span>
              </div>
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#475569' }}>
              <span>Taxable Turnover:</span>
              <span style={{ fontWeight: 600 }}>₹{invoice.total_taxable}</span>
            </div>
            {!invoice.is_interstate ? (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#475569' }}>
                  <span>CGST Total:</span>
                  <span style={{ fontWeight: 600 }}>₹{invoice.total_cgst}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#475569' }}>
                  <span>SGST Total:</span>
                  <span style={{ fontWeight: 600 }}>₹{invoice.total_sgst}</span>
                </div>
              </>
            ) : (
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#475569' }}>
                <span>IGST Total:</span>
                <span style={{ fontWeight: 600 }}>₹{invoice.total_igst}</span>
              </div>
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderTop: '2px solid #0f172a', color: '#0f172a', fontSize: '1rem', fontWeight: 800 }}>
              <span>Net Payable:</span>
              <span style={{ color: '#0284c7' }}>₹{invoice.total_net}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#059669', fontWeight: 600 }}>
              <span>Paid To Date:</span>
              <span>₹{invoice.paid_amount}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', color: '#dc2626', fontWeight: 700, borderTop: '1px dashed #cbd5e1' }}>
              <span>Balance Due:</span>
              <span>₹{invoice.balance_due}</span>
            </div>
          </div>
        </div>

        {/* Declarations & Signature */}
        <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '16px', fontSize: '0.6875rem', color: '#64748b', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <div>
            <p><strong>Declaration:</strong> This is an authenticated computer-generated hospital tax invoice.</p>
            <p>Healthcare services are categorized under SAC 9993 in accordance with Indian GST regulations.</p>
          </div>
          <div style={{ textAlign: 'center', width: '180px', borderTop: '1px solid #475569', paddingTop: '6px' }}>
            Authorized Financial Signatory
          </div>
        </div>
      </div>
    </Modal>
  );
};
