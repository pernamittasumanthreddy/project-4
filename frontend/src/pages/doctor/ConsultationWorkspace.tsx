import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import {
  Stethoscope,
  Activity,
  AlertTriangle,
  FileCheck,
  Save,
  Lock,
  Plus,
  Video,
  ChevronLeft,
  Pill,
  CheckCircle2,
  FileText
} from 'lucide-react';

export const ConsultationWorkspace: React.FC = () => {
  const {
    selectedAppointmentId,
    setActiveTab,
    setSelectedTelemedicineSessionId,
    showToast
  } = useAuth();

  const [workspace, setWorkspace] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [signing, setSigning] = useState<boolean>(false);

  // SOAP State
  const [chiefComplaint, setChiefComplaint] = useState<string>('');
  const [subjective, setSubjective] = useState<string>('');
  const [physicalExam, setPhysicalExam] = useState<string>('');
  const [assessment, setAssessment] = useState<string>('');
  const [clinicalPlan, setClinicalPlan] = useState<string>('');

  // Vitals State
  const [bpSys, setBpSys] = useState<number>(120);
  const [bpDia, setBpDia] = useState<number>(80);
  const [heartRate, setHeartRate] = useState<number>(72);
  const [tempC, setTempC] = useState<number>(36.8);
  const [spo2, setSpo2] = useState<number>(98);
  const [weightKg, setWeightKg] = useState<number>(68);
  const [heightCm, setHeightCm] = useState<number>(170);

  // New Diagnosis Modal/Form
  const [showAddDiag, setShowAddDiag] = useState<boolean>(false);
  const [diagCode, setDiagCode] = useState<string>('I10');
  const [diagDesc, setDiagDesc] = useState<string>('Essential (primary) hypertension');
  const [diagSeverity, setDiagSeverity] = useState<string>('MODERATE');

  // New Rx Form
  const [showAddRx, setShowAddRx] = useState<boolean>(false);
  const [rxMedName, setRxMedName] = useState<string>('Lisinopril Tablets');
  const [rxDosage, setRxDosage] = useState<string>('10 mg');
  const [rxFreq, setRxFreq] = useState<string>('Once daily each morning');
  const [rxDays, setRxDays] = useState<number>(90);
  const [rxInstructions, setRxInstructions] = useState<string>('Monitor blood pressure weekly.');

  const loadWorkspace = async () => {
    if (!selectedAppointmentId) return;
    setLoading(true);
    try {
      const data = await api.getConsultationWorkspace(selectedAppointmentId);
      setWorkspace(data);

      // Populate encounter fields
      const enc = data.encounter;
      if (enc) {
        setChiefComplaint(enc.chief_complaint || '');
        setSubjective(enc.subjective_notes || '');
        setPhysicalExam(enc.physical_examination || '');
        setAssessment(enc.assessment || '');
        setClinicalPlan(enc.clinical_plan || '');

        if (enc.vitals) {
          setBpSys(enc.vitals.bp_systolic || 120);
          setBpDia(enc.vitals.bp_diastolic || 80);
          setHeartRate(enc.vitals.heart_rate || 72);
          setTempC(enc.vitals.temp_c || 36.8);
          setSpo2(enc.vitals.spo2 || 98);
          setWeightKg(enc.vitals.weight_kg || 68);
          setHeightCm(enc.vitals.height_cm || 170);
        }
      }
    } catch (err: any) {
      console.error(err);
      showToast('Failed to load consultation encounter.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkspace();
  }, [selectedAppointmentId]);

  if (!selectedAppointmentId) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
        <Stethoscope size={48} className="text-teal-600" style={{ margin: '0 auto 16px' }} />
        <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--slate-900)' }}>
          No Consultation Encounter Selected
        </h2>
        <p style={{ color: 'var(--slate-500)', fontSize: '0.88rem', margin: '8px 0 20px' }}>
          Please select an appointment from your Doctor Dashboard or Agenda schedule to document clinical notes.
        </p>
        <button onClick={() => setActiveTab('doctor-dashboard')} className="btn btn-primary">
          Go to Doctor Dashboard
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ padding: '60px', textAlign: 'center', color: 'var(--slate-400)' }}>
        Loading patient encounter chart...
      </div>
    );
  }

  if (!workspace) return null;

  const { patient_summary, allergies, active_prescriptions, lab_reports, encounter, appointment, telemedicine_session_id } = workspace;
  const isSigned = encounter?.status === 'SIGNED';

  const handleSaveDraft = async () => {
    setSaving(true);
    try {
      const payload: any = {
        chief_complaint: chiefComplaint,
        subjective_notes: subjective,
        physical_examination: physicalExam,
        assessment,
        clinical_plan: clinicalPlan,
        vitals: {
          bp_systolic: bpSys,
          bp_diastolic: bpDia,
          heart_rate: heartRate,
          temp_c: tempC,
          spo2,
          weight_kg: weightKg,
          height_cm: heightCm,
          bmi: Number((weightKg / Math.pow(heightCm / 100, 2)).toFixed(1)),
        },
      };

      if (showAddDiag) {
        payload.new_diagnosis = {
          icd10_code: diagCode,
          description: diagDesc,
          severity: diagSeverity,
          is_primary: true,
        };
      }

      if (showAddRx) {
        payload.new_prescription = {
          instructions: rxInstructions,
          medications: [
            {
              medication_name: rxMedName,
              dosage: rxDosage,
              frequency: rxFreq,
              duration_days: rxDays,
              quantity: 30,
              instructions: rxInstructions,
            },
          ],
        };
      }

      const res = await api.updateConsultationNotes(selectedAppointmentId, payload);
      showToast(res.message);
      setShowAddDiag(false);
      setShowAddRx(false);
      loadWorkspace();
    } catch (err: any) {
      showToast(`Save failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleSignEncounter = async () => {
    if (!encounter?.id) return;
    setSigning(true);
    try {
      // First save current notes
      await handleSaveDraft();
      // Then lock with digital signature
      const res = await api.signEncounter(encounter.id);
      showToast(res.message);
      loadWorkspace();
    } catch (err: any) {
      showToast(`Sign failed: ${err.message}`);
    } finally {
      setSigning(false);
    }
  };

  return (
    <div>
      {/* Navigation and Top Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
        <button
          onClick={() => setActiveTab('doctor-dashboard')}
          className="btn btn-sm btn-secondary"
        >
          <ChevronLeft size={16} /> Back to Doctor Dashboard
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {telemedicine_session_id && (
            <button
              onClick={() => {
                setSelectedTelemedicineSessionId(telemedicine_session_id);
                setActiveTab('telemedicine-room');
              }}
              className="btn btn-sm btn-primary"
              style={{ background: 'var(--color-accent)' }}
            >
              <Video size={14} /> Open Virtual Room
            </button>
          )}

          {!isSigned ? (
            <>
              <button
                onClick={handleSaveDraft}
                disabled={saving || signing}
                className="btn btn-sm btn-secondary"
              >
                <Save size={14} /> {saving ? 'Saving...' : 'Save Draft'}
              </button>
              <button
                onClick={handleSignEncounter}
                disabled={saving || signing}
                className="btn btn-sm btn-primary"
              >
                <Lock size={14} /> {signing ? 'Finalizing...' : 'Digitally Sign & Lock'}
              </button>
            </>
          ) : (
            <span className="badge badge-success" style={{ padding: '8px 14px', fontSize: '0.84rem' }}>
              <Lock size={14} /> Signed & Finalized by Clinician
            </span>
          )}
        </div>
      </div>

      {/* Patient Medical Banner */}
      <div className="card" style={{ marginBottom: '20px', background: 'var(--surface-white)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--slate-900)' }}>
                {patient_summary.name}
              </h2>
              <span style={{ fontSize: '0.85rem', color: 'var(--slate-500)' }}>
                MRN: <strong>{patient_summary.mrn}</strong>
              </span>
              <span className="badge badge-neutral">{patient_summary.gender}</span>
              <span className="badge badge-neutral">Blood: {patient_summary.blood_group}</span>
            </div>
            <div style={{ fontSize: '0.82rem', color: 'var(--slate-500)', marginTop: '4px' }}>
              Appointment #{appointment.appointment_number} • {appointment.appointment_date} at {appointment.start_time} • {appointment.appointment_type}
            </div>
          </div>

          {/* Allergy Alert Pills */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {allergies?.map((al: any) => (
              <span key={al.id} className="badge badge-danger" style={{ padding: '6px 12px', fontSize: '0.78rem' }}>
                <AlertTriangle size={14} /> CRITICAL ALLERGY: {al.allergen} ({al.severity})
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Main 2-Column Workstation Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        {/* Left Column: SOAP Notes & Vitals */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Vital Signs Strip */}
          <div className="card" style={{ padding: '18px' }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Activity className="text-teal-600" size={18} /> Vital Signs Record
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', fontSize: '0.85rem' }}>
              <div>
                <label className="form-label" style={{ fontSize: '0.76rem' }}>BP Systolic (mmHg)</label>
                <input
                  type="number"
                  disabled={isSigned}
                  className="form-input"
                  value={bpSys}
                  onChange={(e) => setBpSys(Number(e.target.value))}
                />
              </div>
              <div>
                <label className="form-label" style={{ fontSize: '0.76rem' }}>BP Diastolic (mmHg)</label>
                <input
                  type="number"
                  disabled={isSigned}
                  className="form-input"
                  value={bpDia}
                  onChange={(e) => setBpDia(Number(e.target.value))}
                />
              </div>
              <div>
                <label className="form-label" style={{ fontSize: '0.76rem' }}>Pulse (bpm)</label>
                <input
                  type="number"
                  disabled={isSigned}
                  className="form-input"
                  value={heartRate}
                  onChange={(e) => setHeartRate(Number(e.target.value))}
                />
              </div>
              <div>
                <label className="form-label" style={{ fontSize: '0.76rem' }}>SpO2 (%)</label>
                <input
                  type="number"
                  disabled={isSigned}
                  className="form-input"
                  value={spo2}
                  onChange={(e) => setSpo2(Number(e.target.value))}
                />
              </div>
            </div>
          </div>

          {/* SOAP Clinical Notes */}
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
              Clinical SOAP Documentation
            </h3>

            <div className="form-group">
              <label className="form-label">Chief Complaint & Reason for Visit</label>
              <input
                type="text"
                disabled={isSigned}
                className="form-input"
                value={chiefComplaint}
                onChange={(e) => setChiefComplaint(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Subjective (Patient Narrative & HPI)</label>
              <textarea
                rows={3}
                disabled={isSigned}
                className="form-textarea"
                placeholder="Patient reports adherence to low-sodium diet, denied acute chest pain or exertional dyspnea..."
                value={subjective}
                onChange={(e) => setSubjective(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Objective / Physical & Virtual Examination</label>
              <textarea
                rows={2}
                disabled={isSigned}
                className="form-textarea"
                placeholder="Video examination: Well appearing, fluent speech, no signs of acute respiratory distress..."
                value={physicalExam}
                onChange={(e) => setPhysicalExam(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Assessment & Clinical Impression</label>
              <textarea
                rows={2}
                disabled={isSigned}
                className="form-textarea"
                placeholder="Stage 1 essential hypertension, controlled under current therapy..."
                value={assessment}
                onChange={(e) => setAssessment(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Care Plan & Follow-Up Instructions</label>
              <textarea
                rows={2}
                disabled={isSigned}
                className="form-textarea"
                placeholder="Continue Lisinopril 10mg daily. Recheck fasting lipid panel in 6 months..."
                value={clinicalPlan}
                onChange={(e) => setClinicalPlan(e.target.value)}
              />
            </div>
          </div>

          {/* Diagnoses & Prescription Action Forms */}
          {!isSigned && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              {/* Add Diagnosis Toggle */}
              <div className="card" style={{ padding: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.88rem' }}>ICD-10 Diagnosis</span>
                  <button
                    type="button"
                    onClick={() => setShowAddDiag(!showAddDiag)}
                    className="btn btn-sm btn-secondary"
                  >
                    <Plus size={14} /> {showAddDiag ? 'Hide' : 'Add Diagnosis'}
                  </button>
                </div>

                {showAddDiag && (
                  <div style={{ marginTop: '10px' }}>
                    <div className="form-group" style={{ margin: '0 0 8px 0' }}>
                      <label className="form-label" style={{ fontSize: '0.75rem' }}>ICD-10 Code</label>
                      <input
                        type="text"
                        className="form-input"
                        value={diagCode}
                        onChange={(e) => setDiagCode(e.target.value)}
                      />
                    </div>
                    <div className="form-group" style={{ margin: '0 0 8px 0' }}>
                      <label className="form-label" style={{ fontSize: '0.75rem' }}>Diagnosis Description</label>
                      <input
                        type="text"
                        className="form-input"
                        value={diagDesc}
                        onChange={(e) => setDiagDesc(e.target.value)}
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Add Prescription Toggle */}
              <div className="card" style={{ padding: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.88rem' }}>Medication Prescription</span>
                  <button
                    type="button"
                    onClick={() => setShowAddRx(!showAddRx)}
                    className="btn btn-sm btn-secondary"
                  >
                    <Plus size={14} /> {showAddRx ? 'Hide' : 'Write Rx'}
                  </button>
                </div>

                {showAddRx && (
                  <div style={{ marginTop: '10px' }}>
                    <div className="form-group" style={{ margin: '0 0 8px 0' }}>
                      <label className="form-label" style={{ fontSize: '0.75rem' }}>Drug & Dosage</label>
                      <input
                        type="text"
                        className="form-input"
                        value={rxMedName}
                        onChange={(e) => setRxMedName(e.target.value)}
                      />
                    </div>
                    <div className="form-group" style={{ margin: '0 0 8px 0' }}>
                      <label className="form-label" style={{ fontSize: '0.75rem' }}>Directions</label>
                      <input
                        type="text"
                        className="form-input"
                        value={rxFreq}
                        onChange={(e) => setRxFreq(e.target.value)}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Longitudinal Patient Summary */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Active Prescriptions */}
          <div className="card" style={{ padding: '18px' }}>
            <h4 style={{ fontSize: '0.92rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Pill className="text-teal-600" size={16} /> Current Active Prescriptions
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.82rem' }}>
              {active_prescriptions?.map((rx: any) => (
                <div key={rx.id} style={{ background: 'var(--slate-50)', padding: '8px 10px', borderRadius: 'var(--radius-sm)' }}>
                  {rx.items?.map((item: any, i: number) => (
                    <div key={i}>
                      <strong>{item.medication_name}</strong> ({item.dosage}) — {item.frequency}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Diagnostic Lab Reports */}
          <div className="card" style={{ padding: '18px' }}>
            <h4 style={{ fontSize: '0.92rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <CheckCircle2 className="text-green-600" size={16} /> Recent Diagnostic Investigations
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.82rem' }}>
              {lab_reports?.map((lr: any) => (
                <div key={lr.id} style={{ border: '1px solid var(--slate-200)', padding: '8px 10px', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{lr.test_name}</div>
                  <div style={{ fontSize: '0.74rem', color: 'var(--slate-500)' }}>
                    Collected: {lr.order_date} • <span className={`badge ${lr.status === 'APPROVED' ? 'badge-success' : 'badge-warning'}`}>{lr.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
