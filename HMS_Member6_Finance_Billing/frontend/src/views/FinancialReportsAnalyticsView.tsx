import React, { useState } from 'react';
import { DashboardKPIs, Invoice, Payment } from '../types/finance';
import { Download, Printer, BarChart3, FileSpreadsheet } from 'lucide-react';

interface FinancialReportsAnalyticsViewProps {
  kpis: DashboardKPIs | null;
  invoices: Invoice[];
  payments: Payment[];
}

export const FinancialReportsAnalyticsView: React.FC<FinancialReportsAnalyticsViewProps> = ({
  kpis,
  invoices,
  payments
}) => {
  const [selectedReport, setSelectedReport] = useState<'REVENUE' | 'TAX' | 'COLLECTIONS'>('REVENUE');

  const exportCSV = () => {
    let headers: string[] = [];
    let rows: string[][] = [];

    if (selectedReport === 'REVENUE') {
      headers = ['Invoice Number', 'Patient Name', 'MRN', 'Date', 'Gross', 'Tax', 'Net', 'Status'];
      rows = invoices.map((inv) => [
        inv.invoice_number,
        `"${inv.patient_name}"`,
        inv.patient_mrn,
        inv.issue_date,
        inv.total_gross,
        inv.total_tax,
        inv.total_net,
        inv.status
      ]);
    } else {
      headers = ['Receipt Number', 'Date', 'Method', 'Bank Reference', 'Amount', 'Status'];
      rows = payments.map((p) => [
        p.payment_number,
        new Date(p.created_at).toLocaleDateString(),
        p.method_display,
        p.transaction_reference || 'N/A',
        p.amount,
        p.status
      ]);
    }

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `hms_financial_report_${selectedReport.toLowerCase()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Financial Reports & Regulatory Statements</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Module 6.6: Exportable CSV / PDF Financial Statements Derived from Persisted Records
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn btn-outline" onClick={() => window.print()}>
            <Printer size={16} /> Print Statement
          </button>
          <button className="btn btn-primary" onClick={exportCSV}>
            <Download size={16} /> Export CSV
          </button>
        </div>
      </div>

      {/* Report Type Selector */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        <button
          className={`btn btn-sm ${selectedReport === 'REVENUE' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setSelectedReport('REVENUE')}
        >
          Departmental Revenue Statement
        </button>
        <button
          className={`btn btn-sm ${selectedReport === 'TAX' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setSelectedReport('TAX')}
        >
          GST Tax Compliance Summary
        </button>
        <button
          className={`btn btn-sm ${selectedReport === 'COLLECTIONS' ? 'btn-primary' : 'btn-outline'}`}
          onClick={() => setSelectedReport('COLLECTIONS')}
        >
          Cash Collections by Tender
        </button>
      </div>

      {/* Selected Report Content */}
      <div className="card">
        {selectedReport === 'REVENUE' && (
          <div>
            <div className="card-header">
              <h3>Departmental Revenue Recognition Schedule</h3>
              <span className="mono-num" style={{ fontWeight: 700, color: '#38bdf8' }}>
                Total Billed: ₹{kpis?.total_billed || '0.00'}
              </span>
            </div>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Department</th>
                    <th style={{ textAlign: 'right' }}>Recognized Revenue (₹)</th>
                    <th style={{ textAlign: 'right' }}>Revenue Share %</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(kpis?.department_revenue || {}).map(([dept, rev]) => {
                    const total = parseFloat(kpis?.total_billed || '1');
                    const share = total > 0 ? ((parseFloat(rev) / total) * 100).toFixed(1) : '0';
                    return (
                      <tr key={dept}>
                        <td style={{ fontWeight: 600 }}>{dept}</td>
                        <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700 }}>₹{rev}</td>
                        <td className="mono-num" style={{ textAlign: 'right', color: '#38bdf8' }}>{share}%</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {selectedReport === 'TAX' && (
          <div>
            <div className="card-header">
              <h3>GSTR Statutory Healthcare Tax Statement</h3>
            </div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
              Statutory reconciliation of Output CGST, SGST, and IGST for state tax filings.
            </p>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Invoice #</th>
                    <th>Patient</th>
                    <th>State Code</th>
                    <th style={{ textAlign: 'right' }}>Taxable Value (₹)</th>
                    <th style={{ textAlign: 'right' }}>CGST (₹)</th>
                    <th style={{ textAlign: 'right' }}>SGST (₹)</th>
                    <th style={{ textAlign: 'right' }}>IGST (₹)</th>
                    <th style={{ textAlign: 'right' }}>Total Tax (₹)</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map((inv) => (
                    <tr key={inv.id}>
                      <td><strong style={{ color: '#38bdf8' }}>{inv.invoice_number}</strong></td>
                      <td>{inv.patient_name}</td>
                      <td>{inv.patient_state_code}</td>
                      <td className="mono-num" style={{ textAlign: 'right' }}>₹{inv.total_taxable}</td>
                      <td className="mono-num" style={{ textAlign: 'right' }}>₹{inv.total_cgst}</td>
                      <td className="mono-num" style={{ textAlign: 'right' }}>₹{inv.total_sgst}</td>
                      <td className="mono-num" style={{ textAlign: 'right' }}>₹{inv.total_igst}</td>
                      <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#38bdf8' }}>
                        ₹{inv.total_tax}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {selectedReport === 'COLLECTIONS' && (
          <div>
            <div className="card-header">
              <h3>Tender Method Collection Summary</h3>
              <span className="mono-num" style={{ fontWeight: 700, color: '#34d399' }}>
                Total Cleared: ₹{kpis?.total_collected || '0.00'}
              </span>
            </div>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Payment Method</th>
                    <th style={{ textAlign: 'center' }}>Total Receipts</th>
                    <th style={{ textAlign: 'right' }}>Collected Amount (₹)</th>
                  </tr>
                </thead>
                <tbody>
                  {['UPI', 'CARD', 'CASH', 'WIRE_TRANSFER'].map((method) => {
                    const matched = payments.filter((p) => p.method === method && p.status === 'SUCCESS');
                    const sum = matched.reduce((acc, p) => acc + parseFloat(p.amount), 0);
                    return (
                      <tr key={method}>
                        <td style={{ fontWeight: 600 }}>{method.replace(/_/g, ' ')}</td>
                        <td style={{ textAlign: 'center' }} className="mono-num">{matched.length}</td>
                        <td className="mono-num" style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }}>
                          ₹{sum.toFixed(2)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
