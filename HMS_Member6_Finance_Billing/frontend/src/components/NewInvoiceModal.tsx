import React, { useState } from 'react';
import { Modal } from './Modal';
import { BillingEntity, ServicePrice, TaxConfiguration, Invoice } from '../types/finance';
import { Plus, Trash2 } from 'lucide-react';

interface NewInvoiceModalProps {
  isOpen: boolean;
  onClose: () => void;
  billingEntities: BillingEntity[];
  services: ServicePrice[];
  taxConfigs: TaxConfiguration[];
  onSubmit: (data: any) => Promise<Invoice>;
}

export const NewInvoiceModal: React.FC<NewInvoiceModalProps> = ({
  isOpen,
  onClose,
  billingEntities,
  services,
  taxConfigs,
  onSubmit
}) => {
  const [billingEntityId, setBillingEntityId] = useState(billingEntities[0]?.id || '');
  const [patientId, setPatientId] = useState('PAT-1001');
  const [patientName, setPatientName] = useState('Aarav Sharma');
  const [patientMrn, setPatientMrn] = useState('MRN-2026-00891');
  const [patientStateCode, setPatientStateCode] = useState('07'); // Delhi
  const [encounterType, setEncounterType] = useState<'OPD' | 'IPD' | 'EMERGENCY' | 'DAYCARE'>('OPD');
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [lines, setLines] = useState<Array<{
    service_code: string;
    service_name: string;
    department: string;
    quantity: number;
    unit_price: number;
    discount_amount: number;
    tax_config_id: string;
    hsn_sac_code: string;
  }>>([
    {
      service_code: services[0]?.code || 'SRV-OPD-01',
      service_name: services[0]?.name || 'Senior Consultant OPD Consultation',
      department: services[0]?.department || 'OPD',
      quantity: 1,
      unit_price: parseFloat(services[0]?.base_amount || '1200'),
      discount_amount: 0,
      tax_config_id: taxConfigs[0]?.id || '',
      hsn_sac_code: '999312'
    }
  ]);

  const handleAddLine = () => {
    const s = services[0] || { code: 'SRV-01', name: 'General Consult', department: 'OPD', base_amount: '800' };
    setLines([
      ...lines,
      {
        service_code: s.code,
        service_name: s.name,
        department: s.department,
        quantity: 1,
        unit_price: parseFloat(s.base_amount),
        discount_amount: 0,
        tax_config_id: taxConfigs[0]?.id || '',
        hsn_sac_code: '999312'
      }
    ]);
  };

  const handleRemoveLine = (idx: number) => {
    if (lines.length > 1) {
      setLines(lines.filter((_, i) => i !== idx));
    }
  };

  const handleServiceSelect = (idx: number, serviceCode: string) => {
    const s = services.find((x) => x.code === serviceCode);
    if (!s) return;
    const updated = [...lines];
    updated[idx] = {
      ...updated[idx],
      service_code: s.code,
      service_name: s.name,
      department: s.department,
      unit_price: parseFloat(s.base_amount),
      hsn_sac_code: s.hsn_sac_code || '999312',
      tax_config_id: s.tax_config || taxConfigs[0]?.id || ''
    };
    setLines(updated);
  };

  const calculateTotalGross = () =>
    lines.reduce((acc, l) => acc + l.quantity * l.unit_price, 0);

  const calculateTotalDiscount = () =>
    lines.reduce((acc, l) => acc + (l.discount_amount || 0), 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const today = new Date().toISOString().split('T')[0];
      const dueDate = new Date(Date.now() + 7 * 86400000).toISOString().split('T')[0];
      await onSubmit({
        billing_entity: billingEntityId || billingEntities[0]?.id,
        patient_id: patientId,
        patient_name: patientName,
        patient_mrn: patientMrn,
        patient_state_code: patientStateCode,
        encounter_type: encounterType,
        issue_date: today,
        due_date: dueDate,
        notes: notes,
        lines: lines
      });
      onClose();
    } catch (err: any) {
      alert(`Invoice generation failed: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Generate Itemized Hospital Invoice"
      maxWidth="860px"
    >
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '16px' }}>
          <div className="form-group">
            <label className="form-label">Hospital Billing Entity</label>
            <select
              className="form-control"
              value={billingEntityId}
              onChange={(e) => setBillingEntityId(e.target.value)}
              required
            >
              {billingEntities.map((be) => (
                <option key={be.id} value={be.id}>
                  {be.name} (GST: {be.gstin})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Patient Name (Contract Ref)</label>
            <input
              type="text"
              className="form-control"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Patient State Code (GST Check)</label>
            <select
              className="form-control"
              value={patientStateCode}
              onChange={(e) => setPatientStateCode(e.target.value)}
            >
              <option value="07">07 — Delhi (Intra-State)</option>
              <option value="27">27 — Maharashtra (Inter-State IGST)</option>
              <option value="36">36 — Telangana (Inter-State IGST)</option>
              <option value="19">19 — West Bengal (Inter-State IGST)</option>
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px', marginBottom: '16px' }}>
          <div className="form-group">
            <label className="form-label">Patient MRN</label>
            <input
              type="text"
              className="form-control"
              value={patientMrn}
              onChange={(e) => setPatientMrn(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Encounter Department</label>
            <select
              className="form-control"
              value={encounterType}
              onChange={(e) => setEncounterType(e.target.value as any)}
            >
              <option value="OPD">OPD Consultation</option>
              <option value="IPD">Inpatient Admission</option>
              <option value="EMERGENCY">Emergency / Trauma</option>
              <option value="DAYCARE">Day Care Surgery</option>
            </select>
          </div>
        </div>

        {/* Line Items Table */}
        <div style={{ marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <h4 style={{ fontSize: '0.875rem', fontWeight: 600, color: '#ffffff' }}>Billable Items & Clinical Services</h4>
            <button
              type="button"
              className="btn btn-outline btn-sm"
              onClick={handleAddLine}
            >
              <Plus size={14} /> Add Service
            </button>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Service / Tariff</th>
                  <th>Dept</th>
                  <th style={{ width: '80px' }}>Qty</th>
                  <th style={{ width: '120px' }}>Rate (₹)</th>
                  <th style={{ width: '100px' }}>Disc (₹)</th>
                  <th style={{ width: '140px' }}>Tax Slab</th>
                  <th style={{ width: '40px' }}></th>
                </tr>
              </thead>
              <tbody>
                {lines.map((l, idx) => (
                  <tr key={idx}>
                    <td>
                      <select
                        className="form-control"
                        style={{ fontSize: '0.8125rem', padding: '6px' }}
                        value={l.service_code}
                        onChange={(e) => handleServiceSelect(idx, e.target.value)}
                      >
                        {services.map((s) => (
                          <option key={s.code} value={s.code}>
                            [{s.department}] {s.name} (₹{s.base_amount})
                          </option>
                        ))}
                      </select>
                    </td>
                    <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{l.department}</td>
                    <td>
                      <input
                        type="number"
                        min="1"
                        className="form-control"
                        style={{ padding: '6px' }}
                        value={l.quantity}
                        onChange={(e) => {
                          const updated = [...lines];
                          updated[idx].quantity = parseFloat(e.target.value) || 1;
                          setLines(updated);
                        }}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        step="0.01"
                        className="form-control mono-num"
                        style={{ padding: '6px' }}
                        value={l.unit_price}
                        onChange={(e) => {
                          const updated = [...lines];
                          updated[idx].unit_price = parseFloat(e.target.value) || 0;
                          setLines(updated);
                        }}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        step="0.01"
                        className="form-control mono-num"
                        style={{ padding: '6px' }}
                        value={l.discount_amount}
                        onChange={(e) => {
                          const updated = [...lines];
                          updated[idx].discount_amount = parseFloat(e.target.value) || 0;
                          setLines(updated);
                        }}
                      />
                    </td>
                    <td>
                      <select
                        className="form-control"
                        style={{ fontSize: '0.75rem', padding: '6px' }}
                        value={l.tax_config_id}
                        onChange={(e) => {
                          const updated = [...lines];
                          updated[idx].tax_config_id = e.target.value;
                          setLines(updated);
                        }}
                      >
                        {taxConfigs.map((tc) => (
                          <option key={tc.id} value={tc.id}>
                            {tc.name} ({tc.rate_percentage}%)
                          </option>
                        ))}
                      </select>
                    </td>
                    <td>
                      {lines.length > 1 && (
                        <button
                          type="button"
                          className="btn btn-danger btn-sm"
                          style={{ padding: '4px' }}
                          onClick={() => handleRemoveLine(idx)}
                        >
                          <Trash2 size={14} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Total Calculations Summary */}
        <div
          style={{
            background: 'rgba(0, 0, 0, 0.25)',
            padding: '14px 18px',
            borderRadius: '8px',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '24px',
            marginBottom: '16px',
            fontSize: '0.875rem'
          }}
        >
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Estimated Gross:</span>{' '}
            <strong className="mono-num">₹{calculateTotalGross().toFixed(2)}</strong>
          </div>
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Discounts:</span>{' '}
            <strong className="mono-num" style={{ color: '#fbbf24' }}>-₹{calculateTotalDiscount().toFixed(2)}</strong>
          </div>
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Estimated Net:</span>{' '}
            <strong className="mono-num" style={{ color: '#38bdf8', fontSize: '1rem' }}>
              ₹{(calculateTotalGross() - calculateTotalDiscount()).toFixed(2)}
            </strong>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Clinical / Billing Remarks</label>
          <input
            type="text"
            className="form-control"
            placeholder="e.g. Authorized under corporate insurance pre-auth schedule"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
            {isSubmitting ? 'Generating Invoice...' : 'Generate & Issue Invoice'}
          </button>
        </div>
      </form>
    </Modal>
  );
};
