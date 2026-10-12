import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import {
  FileText,
  Activity,
  CheckCircle2,
  AlertTriangle,
  Pill,
  ShieldCheck,
  Stethoscope,
  Eye,
  X
} from 'lucide-react';

export const PatientMedicalRecords: React.FC = () => {
  const { showToast } = useAuth();
  const [records, setRecords] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<'LABS' | 'RADIOLOGY' | 'PRESCRIPTIONS' | 'ENCOUNTERS' | 'ALLERGIES'>('LABS');

  // Modal inspection states
  const [selectedLabReport, setSelectedLabReport] = useState<any | null>(null);
  const [selectedRadiology, setSelectedRadiology] = useState<any | null>(null);
  const [selectedEncounter, setSelectedEncounter] = useState<any | null>(null);

  useEffect(() => {
    setLoading(true);
    api.getPatientMedicalRecords()
      .then(setRecords)
      .catch((err) => {
        console.error(err);
        showToast('Failed to load medical records.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '60px', textAlign: 'center', color: 'var(--slate-400)' }}>
        Retrieving encrypted longitudinal medical records...
      </div>
    );
  }

  if (!records) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-500)' }}>
        No medical records found for this patient.
      </div>
    );
  }

  const { allergies, medical_history, diagnoses, clinical_encounters, prescriptions, lab_reports, radiology_reports, patient_mrn, patient_name, blood_group } = records;

  return (
    <div>
      {/* Patient Banner */}
      <div className="card" style={{ marginBottom: '24px', background: 'linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="badge badge-success">Authorized Electronic Health Record</span>
              <span style={{ fontSize: '0.8rem', color: 'var(--slate-500)' }}>HIPAA Protected</span>
            </div>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--slate-900)', marginTop: '4px' }}>
              Medical Records: {patient_name}
            </h1>
            <div style={{ fontSize: '0.86rem', color: 'var(--slate-600)' }}>
              MRN: <strong>{patient_mrn}</strong> • Blood Group: <strong>{blood_group}</strong>
            </div>
          </div>

          {/* Allergy Alert Pills */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {allergies?.map((al: any) => (
              <span key={al.id} className="badge badge-danger" style={{ padding: '6px 12px', fontSize: '0.78rem' }}>
                <AlertTriangle size={14} /> Allergy: {al.allergen} ({al.severity})
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', overflowX: 'auto', paddingBottom: '6px' }}>
        {[
          { key: 'LABS', label: `Laboratory Reports (${lab_reports?.length || 0})` },
          { key: 'RADIOLOGY', label: `Diagnostic Imaging (${radiology_reports?.length || 0})` },
          { key: 'PRESCRIPTIONS', label: `Prescriptions (${prescriptions?.length || 0})` },
          { key: 'ENCOUNTERS', label: `Clinical Encounters (${clinical_encounters?.length || 0})` },
          { key: 'ALLERGIES', label: 'Allergies & Chronic History' },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`btn btn-sm ${activeTab === tab.key ? 'btn-primary' : 'btn-secondary'}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab 1: Laboratory Reports */}
      {activeTab === 'LABS' && (
        <div className="card">
          <h2 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
            Approved Laboratory Diagnostic Reports
          </h2>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Report #</th>
                  <th>Investigation Name</th>
                  <th>Specimen</th>
                  <th>Order Date</th>
                  <th>Pathologist Approval</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {lab_reports?.map((lr: any) => (
                  <tr key={lr.id}>
                    <td style={{ fontWeight: 700 }}>{lr.report_number}</td>
                    <td>
                      <div style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{lr.test_name}</div>
                      <div style={{ fontSize: '0.74rem', color: 'var(--slate-400)' }}>LOINC: {lr.test_code}</div>
                    </td>
                    <td>{lr.specimen_type}</td>
                    <td>{lr.order_date}</td>
                    <td style={{ fontSize: '0.8rem', color: 'var(--slate-600)' }}>
                      {lr.approved_by || 'Verified Pathologist'}
                    </td>
                    <td>
                      <span className="badge badge-success">Approved</span>
                    </td>
                    <td>
                      <button onClick={() => setSelectedLabReport(lr)} className="btn btn-sm btn-outline">
                        <Eye size={14} /> View Results
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 2: Diagnostic Imaging */}
      {activeTab === 'RADIOLOGY' && (
        <div className="card">
          <h2 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
            Radiology & Diagnostic Imaging Studies
          </h2>
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Study #</th>
                  <th>Study Description</th>
                  <th>Modality</th>
                  <th>Body Part</th>
                  <th>Study Date</th>
                  <th>Radiologist</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {radiology_reports?.map((rad: any) => (
                  <tr key={rad.id}>
                    <td style={{ fontWeight: 700 }}>{rad.study_number}</td>
                    <td style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{rad.study_name}</td>
                    <td><span className="badge badge-info">{rad.modality}</span></td>
                    <td>{rad.body_part}</td>
                    <td>{rad.study_date}</td>
                    <td style={{ fontSize: '0.8rem' }}>{rad.radiologist_name}</td>
                    <td>
                      <button onClick={() => setSelectedRadiology(rad)} className="btn btn-sm btn-outline">
                        <Eye size={14} /> View Report
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Prescriptions */}
      {activeTab === 'PRESCRIPTIONS' && (
        <div className="card">
          <h2 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
            Prescription Medications & Dispensing History
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {prescriptions?.map((rx: any) => (
              <div key={rx.id} style={{ border: '1px solid var(--slate-200)', borderRadius: 'var(--radius-md)', padding: '18px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <div>
                    <span style={{ fontWeight: 800, fontSize: '0.95rem', color: 'var(--slate-900)' }}>
                      Prescription #{rx.prescription_number}
                    </span>
                    <span style={{ marginLeft: '10px', fontSize: '0.8rem', color: 'var(--slate-500)' }}>
                      Prescribed by: {rx.doctor_name} on {rx.issued_date}
                    </span>
                  </div>
                  <span className={`badge ${rx.status === 'ACTIVE' ? 'badge-success' : 'badge-neutral'}`}>
                    {rx.status}
                  </span>
                </div>

                <div className="table-container">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Medication & Strength</th>
                        <th>Route</th>
                        <th>Dosage & Frequency</th>
                        <th>Duration</th>
                        <th>Special Instructions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {rx.items?.map((item: any, i: number) => (
                        <tr key={i}>
                          <td style={{ fontWeight: 700 }}>{item.medication_name} ({item.dosage})</td>
                          <td>{item.route}</td>
                          <td>{item.frequency}</td>
                          <td>{item.duration_days} days (Qty: {item.quantity})</td>
                          <td style={{ color: 'var(--slate-600)', fontStyle: 'italic' }}>{item.instructions || 'Take as directed'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Clinical Encounters */}
      {activeTab === 'ENCOUNTERS' && (
        <div className="card">
          <h2 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
            Finalized Clinical Consultation Summaries
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {clinical_encounters?.map((enc: any) => (
              <div key={enc.id} style={{ border: '1px solid var(--slate-200)', borderRadius: 'var(--radius-md)', padding: '18px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div>
                    <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--slate-900)' }}>
                      Encounter #{enc.encounter_number} — {enc.encounter_date}
                    </h3>
                    <div style={{ fontSize: '0.82rem', color: 'var(--slate-500)' }}>
                      Attending Physician: {enc.doctor_name} ({enc.doctor_specialization})
                    </div>
                  </div>
                  <span className="badge badge-success">Digitally Signed</span>
                </div>

                <div style={{ background: 'var(--slate-50)', padding: '12px 16px', borderRadius: 'var(--radius-sm)', marginBottom: '12px', fontSize: '0.84rem' }}>
                  <strong>Chief Complaint:</strong> {enc.chief_complaint}
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', fontSize: '0.84rem' }}>
                  <div>
                    <strong>Clinical Assessment:</strong>
                    <p style={{ color: 'var(--slate-700)', marginTop: '4px' }}>{enc.assessment || 'N/A'}</p>
                  </div>
                  <div>
                    <strong>Care Plan & Follow-Up:</strong>
                    <p style={{ color: 'var(--slate-700)', marginTop: '4px' }}>{enc.clinical_plan || 'N/A'}</p>
                  </div>
                </div>

                {enc.vitals && Object.keys(enc.vitals).length > 0 && (
                  <div style={{ marginTop: '12px', paddingTop: '10px', borderTop: '1px solid var(--slate-200)', display: 'flex', gap: '14px', flexWrap: 'wrap', fontSize: '0.78rem', color: 'var(--slate-600)' }}>
                    <span>BP: <strong>{enc.vitals.bp_systolic}/{enc.vitals.bp_diastolic} mmHg</strong></span>
                    <span>Pulse: <strong>{enc.vitals.heart_rate} bpm</strong></span>
                    <span>SpO2: <strong>{enc.vitals.spo2}%</strong></span>
                    <span>Temp: <strong>{enc.vitals.temp_c}°C</strong></span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: Allergies & Chronic Conditions */}
      {activeTab === 'ALLERGIES' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle className="text-rose-600" size={18} /> Recorded Allergies & Adverse Reactions
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {allergies?.map((al: any) => (
                <div key={al.id} style={{ padding: '12px', borderRadius: 'var(--radius-md)', background: 'var(--color-danger-light)', border: '1px solid #FECDD3' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ fontWeight: 800, color: 'var(--color-danger)' }}>{al.allergen}</span>
                    <span className="badge badge-danger">{al.severity}</span>
                  </div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--slate-700)', marginTop: '4px' }}>
                    Reaction: {al.reaction}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Activity className="text-teal-600" size={18} /> Chronic Medical Conditions
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {medical_history?.map((mh: any) => (
                <div key={mh.id} style={{ padding: '12px', borderRadius: 'var(--radius-md)', background: 'var(--slate-50)', border: '1px solid var(--slate-200)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ fontWeight: 800, color: 'var(--slate-900)' }}>{mh.condition}</span>
                    <span style={{ fontSize: '0.78rem', color: 'var(--slate-500)' }}>Onset: {mh.onset_year}</span>
                  </div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--slate-600)', marginTop: '4px' }}>
                    Status: {mh.status} • {mh.notes}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Lab Results Modal */}
      {selectedLabReport && (
        <div className="modal-overlay" onClick={() => setSelectedLabReport(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '680px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--slate-900)' }}>
                  {selectedLabReport.test_name}
                </h3>
                <div style={{ fontSize: '0.82rem', color: 'var(--slate-500)' }}>
                  Report #{selectedLabReport.report_number} • Specimen: {selectedLabReport.specimen_type}
                </div>
              </div>
              <button onClick={() => setSelectedLabReport(null)} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                <X size={22} />
              </button>
            </div>

            <div className="table-container" style={{ marginBottom: '16px' }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>Analyte Metric</th>
                    <th>Observed Value</th>
                    <th>Standard Reference Range</th>
                    <th>Flag</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedLabReport.results?.map((m: any, idx: number) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 700 }}>{m.name}</td>
                      <td style={{ fontWeight: 800, color: m.flag === 'HIGH' || m.flag === 'CRITICAL' ? 'var(--color-danger)' : 'var(--slate-900)' }}>
                        {m.value} {m.unit}
                      </td>
                      <td style={{ color: 'var(--slate-500)' }}>{m.reference_range}</td>
                      <td>
                        <span className={`badge ${m.flag === 'NORMAL' ? 'badge-success' : 'badge-danger'}`}>
                          {m.flag}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {selectedLabReport.conclusion && (
              <div style={{ padding: '14px', background: 'var(--slate-50)', borderRadius: 'var(--radius-md)', fontSize: '0.86rem', color: 'var(--slate-800)', marginBottom: '16px' }}>
                <strong>Pathologist Clinical Interpretation:</strong><br />
                {selectedLabReport.conclusion}
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem', color: 'var(--slate-500)' }}>
              <div>Approved by: <strong>{selectedLabReport.approved_by || 'Pathology Staff'}</strong></div>
              <button onClick={() => setSelectedLabReport(null)} className="btn btn-secondary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Radiology Modal */}
      {selectedRadiology && (
        <div className="modal-overlay" onClick={() => setSelectedRadiology(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '640px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--slate-900)' }}>
                  {selectedRadiology.study_name}
                </h3>
                <div style={{ fontSize: '0.82rem', color: 'var(--slate-500)' }}>
                  Study #{selectedRadiology.study_number} • Modality: {selectedRadiology.modality}
                </div>
              </div>
              <button onClick={() => setSelectedRadiology(null)} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                <X size={22} />
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', fontSize: '0.88rem' }}>
              <div>
                <strong>Clinical History:</strong>
                <p style={{ color: 'var(--slate-700)', marginTop: '2px' }}>{selectedRadiology.clinical_history || 'N/A'}</p>
              </div>

              <div>
                <strong>Radiological Findings:</strong>
                <p style={{ color: 'var(--slate-700)', marginTop: '2px', lineHeight: '1.5' }}>{selectedRadiology.findings || 'N/A'}</p>
              </div>

              <div style={{ padding: '12px', background: 'var(--color-primary-light)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--color-primary-border)' }}>
                <strong style={{ color: 'var(--color-primary-dark)' }}>Impression:</strong>
                <p style={{ color: 'var(--slate-800)', marginTop: '4px', whiteSpace: 'pre-line' }}>{selectedRadiology.impression || 'N/A'}</p>
              </div>
            </div>

            <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem', color: 'var(--slate-500)' }}>
              <div>Interpreted by: <strong>{selectedRadiology.radiologist_name}</strong></div>
              <button onClick={() => setSelectedRadiology(null)} className="btn btn-secondary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
