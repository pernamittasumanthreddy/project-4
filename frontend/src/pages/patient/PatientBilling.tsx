import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Invoice, Payment } from '../../types';
import {
  CreditCard,
  CheckCircle,
  Clock,
  AlertCircle,
  DollarSign,
  Download,
  Receipt,
  ShieldCheck,
  X
} from 'lucide-react';

export const PatientBilling: React.FC = () => {
  const { showToast } = useAuth();
  const [billingData, setBillingData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  
  // Sandbox payment modal
  const [payingInvoice, setPayingInvoice] = useState<Invoice | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<string>('CREDIT_CARD');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [paidReceipt, setPaidReceipt] = useState<Payment | null>(null);

  const loadBilling = async () => {
    setLoading(true);
    try {
      const data = await api.getPatientBilling();
      setBillingData(data);
    } catch (err: any) {
      console.error(err);
      showToast('Failed to load billing history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBilling();
  }, []);

  const handleProcessPayment = async () => {
    if (!payingInvoice) return;
    setIsProcessing(true);
    try {
      const res = await api.payInvoiceSandbox(payingInvoice.id, paymentMethod);
      showToast(res.message);
      setPaidReceipt(res.payment);
      loadBilling();
    } catch (err: any) {
      showToast(`Payment simulation failed: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '60px', textAlign: 'center', color: 'var(--slate-400)' }}>
        Retrieving patient billing statements and insurance balances...
      </div>
    );
  }

  if (!billingData) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-500)' }}>
        No billing account found for this patient.
      </div>
    );
  }

  const { financial_summary, invoices } = billingData;

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--slate-900)' }}>
            Billing Statements & Payments
          </h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--slate-500)' }}>
            Transparent itemized medical invoices with verifiable sandbox payments.
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon-box amber">
            <DollarSign size={24} />
          </div>
          <div>
            <div className="metric-value">${financial_summary.balance_due.toFixed(2)}</div>
            <div className="metric-label">Outstanding Balance Due</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box green">
            <CheckCircle size={24} />
          </div>
          <div>
            <div className="metric-value">${financial_summary.total_paid.toFixed(2)}</div>
            <div className="metric-label">Total Amount Paid</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box blue">
            <Receipt size={24} />
          </div>
          <div>
            <div className="metric-value">{financial_summary.invoice_count}</div>
            <div className="metric-label">Invoices Issued</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box teal">
            <ShieldCheck size={24} />
          </div>
          <div>
            <div style={{ fontWeight: 800, fontSize: '0.95rem', color: 'var(--slate-900)' }}>
              {financial_summary.insurance_provider}
            </div>
            <div className="metric-label">Policy: {financial_summary.insurance_policy_number}</div>
          </div>
        </div>
      </div>

      {/* Invoices List */}
      <div className="card">
        <h2 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
          Itemized Hospital Invoices
        </h2>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
          {invoices?.map((inv: Invoice) => {
            const isUnpaid = inv.status === 'UNPAID' || inv.status === 'PARTIALLY_PAID';
            return (
              <div
                key={inv.id}
                style={{
                  border: isUnpaid ? '2px solid #FDE68A' : '1px solid var(--slate-200)',
                  background: isUnpaid ? 'var(--color-warning-light)' : 'var(--surface-white)',
                  borderRadius: 'var(--radius-md)',
                  padding: '20px',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontWeight: 800, fontSize: '1rem', color: 'var(--slate-900)' }}>
                        Invoice #{inv.invoice_number}
                      </span>
                      <span className={`badge ${inv.status === 'PAID' ? 'badge-success' : 'badge-warning'}`}>
                        {inv.status}
                      </span>
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--slate-500)', marginTop: '2px' }}>
                      Issued: {inv.issue_date} • Due: {inv.due_date}
                    </div>
                  </div>

                  <div style={{ textAlign: 'right', display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--slate-500)' }}>Balance Due</div>
                      <div style={{ fontWeight: 800, fontSize: '1.2rem', color: isUnpaid ? 'var(--color-warning)' : 'var(--slate-900)' }}>
                        ${Number(inv.balance_due).toFixed(2)}
                      </div>
                    </div>

                    {isUnpaid && (
                      <button
                        onClick={() => { setPayingInvoice(inv); setPaidReceipt(null); }}
                        className="btn btn-primary"
                      >
                        <CreditCard size={16} /> Pay in Sandbox
                      </button>
                    )}
                  </div>
                </div>

                {/* Line Items Table */}
                <div className="table-container" style={{ marginBottom: '12px' }}>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Item Description</th>
                        <th>Qty</th>
                        <th>Unit Fee</th>
                        <th>Total Amount</th>
                      </tr>
                    </thead>
                    <tbody>
                      {inv.line_items?.map((item: any, i: number) => (
                        <tr key={i}>
                          <td style={{ fontWeight: 600 }}>{item.description}</td>
                          <td>{item.quantity}</td>
                          <td>${Number(item.unit_price).toFixed(2)}</td>
                          <td style={{ fontWeight: 700 }}>${Number(item.total).toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Payments History if any */}
                {inv.payments && inv.payments.length > 0 && (
                  <div style={{ background: 'var(--surface-white)', padding: '10px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--slate-200)', fontSize: '0.8rem' }}>
                    <strong>Verified Settlement Receipts:</strong>
                    {inv.payments.map((p) => (
                      <div key={p.id} style={{ display: 'flex', justifyContent: 'space-between', marginTop: '4px', color: 'var(--slate-700)' }}>
                        <span>Receipt #{p.receipt_number} via {p.payment_method} ({new Date(p.transaction_date).toLocaleDateString()})</span>
                        <span style={{ fontWeight: 700, color: 'var(--color-success)' }}>+${Number(p.amount).toFixed(2)} Paid</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Sandbox Payment Simulator Modal */}
      {payingInvoice && (
        <div className="modal-overlay" onClick={() => setPayingInvoice(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '520px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--slate-900)' }}>
                  {paidReceipt ? 'Payment Receipt' : 'Sandbox Payment Gateway'}
                </h3>
                <div style={{ fontSize: '0.82rem', color: 'var(--slate-500)' }}>
                  Invoice #{payingInvoice.invoice_number} • Amount Due: ${Number(payingInvoice.balance_due).toFixed(2)}
                </div>
              </div>
              <button onClick={() => setPayingInvoice(null)} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                <X size={22} />
              </button>
            </div>

            {paidReceipt ? (
              <div style={{ textAlign: 'center', padding: '20px 0' }}>
                <CheckCircle size={56} className="text-green-600" style={{ margin: '0 auto 16px' }} />
                <h4 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--slate-900)' }}>
                  Settlement Recorded Successfully!
                </h4>
                <p style={{ fontSize: '0.86rem', color: 'var(--slate-600)', marginTop: '6px' }}>
                  A verifiable sandbox transaction has settled this medical balance in full.
                </p>

                <div style={{ background: 'var(--slate-50)', border: '1px solid var(--slate-200)', borderRadius: 'var(--radius-md)', padding: '16px', margin: '20px 0', textAlign: 'left', fontSize: '0.84rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ color: 'var(--slate-500)' }}>Receipt Number:</span>
                    <strong style={{ color: 'var(--slate-900)' }}>{paidReceipt.receipt_number}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ color: 'var(--slate-500)' }}>Payment Reference:</span>
                    <strong style={{ color: 'var(--slate-900)' }}>{paidReceipt.payment_reference}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ color: 'var(--slate-500)' }}>Amount Paid:</span>
                    <strong style={{ color: 'var(--color-success)', fontSize: '1rem' }}>${Number(paidReceipt.amount).toFixed(2)}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--slate-500)' }}>Mode:</span>
                    <strong>{paidReceipt.payment_method} (Sandbox Adapter)</strong>
                  </div>
                </div>

                <button onClick={() => setPayingInvoice(null)} className="btn btn-primary" style={{ width: '100%' }}>
                  Done
                </button>
              </div>
            ) : (
              <div>
                <div style={{ background: 'var(--color-primary-light)', padding: '12px 16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-primary-border)', marginBottom: '18px', fontSize: '0.82rem', color: 'var(--color-primary-dark)' }}>
                  <strong>🔒 Secure Development Sandbox:</strong> Local simulated payment. No actual bank or credit card credentials will be charged.
                </div>

                <div className="form-group">
                  <label className="form-label">Select Payment Method</label>
                  <select
                    className="form-select"
                    value={paymentMethod}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                  >
                    <option value="CREDIT_CARD">Credit / Debit Card (Visa/Mastercard)</option>
                    <option value="UPI">Unified Payments Interface (UPI)</option>
                    <option value="NET_BANKING">Electronic Wire / Net Banking</option>
                    <option value="INSURANCE">Direct Insurance Adjudication</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Cardholder / Account Name</label>
                  <input
                    type="text"
                    className="form-input"
                    defaultValue="Priya Sharma"
                    disabled
                  />
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '24px' }}>
                  <button onClick={() => setPayingInvoice(null)} className="btn btn-secondary">
                    Cancel
                  </button>
                  <button
                    onClick={handleProcessPayment}
                    disabled={isProcessing}
                    className="btn btn-primary"
                  >
                    {isProcessing ? 'Simulating Settlement...' : `Authorize & Pay $${Number(payingInvoice.balance_due).toFixed(2)}`}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
