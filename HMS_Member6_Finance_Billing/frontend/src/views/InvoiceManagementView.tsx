import React, { useState } from 'react';
import { Invoice } from '../types/finance';
import { StatusBadge } from '../components/StatusBadge';
import { Search, Plus, Printer, Clock, CreditCard } from 'lucide-react';

interface InvoiceManagementViewProps {
  invoices: Invoice[];
  onOpenNewInvoice: () => void;
  onViewTimeline: (inv: Invoice) => void;
  onPrintInvoice: (inv: Invoice) => void;
  onPayInvoice: (inv: Invoice) => void;
}

export const InvoiceManagementView: React.FC<InvoiceManagementViewProps> = ({
  invoices,
  onOpenNewInvoice,
  onViewTimeline,
  onPrintInvoice,
  onPayInvoice
}) => {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');

  const filtered = invoices.filter((inv) => {
    const matchStatus = statusFilter === 'ALL' || inv.status === statusFilter;
    const matchSearch =
      inv.invoice_number.toLowerCase().includes(search.toLowerCase()) ||
      inv.patient_name.toLowerCase().includes(search.toLowerCase()) ||
      inv.patient_mrn.toLowerCase().includes(search.toLowerCase());
    return matchStatus && matchSearch;
  });

  return (
    <div>
      {/* Page Title & Actions */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Invoice Management & Patient Billing</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Itemized Hospital Bills across OPD, IPD, Diagnostics & Pharmacy
          </p>
        </div>
        <button className="btn btn-primary" onClick={onOpenNewInvoice}>
          <Plus size={16} /> Generate New Bill
        </button>
      </div>

      {/* Filter Bar */}
      <div
        className="card"
        style={{
          padding: '14px 20px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '16px'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, maxWidth: '400px' }}>
          <Search size={16} color="var(--text-dim)" />
          <input
            type="text"
            className="form-control"
            placeholder="Search by Invoice #, Patient Name, MRN..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {['ALL', 'ISSUED', 'PARTIALLY_PAID', 'PAID', 'OVERDUE', 'CANCELLED'].map((st) => (
            <button
              key={st}
              className={`btn btn-sm ${statusFilter === st ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setStatusFilter(st)}
            >
              {st.replace(/_/g, ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Invoices Data Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Invoice #</th>
              <th>Issue Date</th>
              <th>Patient Details</th>
              <th>Dept</th>
              <th style={{ textAlign: 'right' }}>Gross (₹)</th>
              <th style={{ textAlign: 'right' }}>Tax (₹)</th>
              <th style={{ textAlign: 'right' }}>Net Total (₹)</th>
              <th style={{ textAlign: 'right' }}>Balance Due (₹)</th>
              <th>Status</th>
              <th style={{ textAlign: 'center' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={10} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No matching invoice records found.
                </td>
              </tr>
            ) : (
              filtered.map((inv) => (
                <tr key={inv.id}>
                  <td>
                    <strong style={{ color: '#38bdf8', cursor: 'pointer' }} onClick={() => onViewTimeline(inv)}>
                      {inv.invoice_number}
                    </strong>
                  </td>
                  <td style={{ fontSize: '0.8125rem' }}>{inv.issue_date}</td>
                  <td>
                    <div style={{ fontWeight: 600 }}>{inv.patient_name}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{inv.patient_mrn}</div>
                  </td>
                  <td>
                    <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>
                      {inv.encounter_type}
                    </span>
                  </td>
                  <td className="mono-num" style={{ textAlign: 'right' }}>₹{inv.total_gross}</td>
                  <td className="mono-num" style={{ textAlign: 'right', color: '#94a3b8' }}>₹{inv.total_tax}</td>
                  <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#ffffff' }}>
                    ₹{inv.total_net}
                  </td>
                  <td
                    className="mono-num"
                    style={{
                      textAlign: 'right',
                      fontWeight: 700,
                      color: parseFloat(inv.balance_due) > 0 ? '#f87171' : '#34d399'
                    }}
                  >
                    ₹{inv.balance_due}
                  </td>
                  <td>
                    <StatusBadge status={inv.status} />
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <div style={{ display: 'inline-flex', gap: '6px' }}>
                      <button
                        className="btn btn-outline btn-sm"
                        title="View Unified Financial Timeline"
                        onClick={() => onViewTimeline(inv)}
                      >
                        <Clock size={14} /> Timeline
                      </button>
                      <button
                        className="btn btn-outline btn-sm"
                        title="Print Official Tax Invoice"
                        onClick={() => onPrintInvoice(inv)}
                      >
                        <Printer size={14} />
                      </button>
                      {inv.status !== 'PAID' && inv.status !== 'CANCELLED' && (
                        <button
                          className="btn btn-success btn-sm"
                          title="Record Payment"
                          onClick={() => onPayInvoice(inv)}
                        >
                          <CreditCard size={14} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
