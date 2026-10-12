'use client';
import React, { useState } from 'react';
import { Patient } from '@/lib/types/hms';
import { StatusBadge } from './StatusBadge';
import { 
  X, User, Calendar, Activity, Pill, FlaskConical, 
  Scan, FileText, CreditCard, ShieldCheck, Clock, 
  AlertTriangle, Plus, Download, Printer, Heart, 
  Thermometer, Stethoscope, ChevronRight, CheckCircle2 
} from 'lucide-react';

interface PatientWorkspaceModalProps {
  patient: Patient | null;
  isOpen: boolean;
  onClose: () => void;
  onOpenDoc?: (doc: any) => void;
  onOpenRAG?: () => void;
}

export const PatientWorkspaceModal: React.FC<PatientWorkspaceModalProps> = ({
  patient,
  isOpen,
  onClose,
  onOpenDoc,
  onOpenRAG,
}) => {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'notes' | 'appointments' | 'meds' | 'labs' | 'radiology' | 'docs' | 'billing' | 'timeline'
  >('overview');

  const [clinicalNotes, setClinicalNotes] = useState([
    {
      id: 'NOTE-1',
      date: '2026-10-04 08:30',
      author: 'Dr. Marcus Vance, MD (Attending Cardiologist)',
      type: 'SOAP Progress Note',
      subjective: 'Patient reports mild substernal tightness on exertion. No dyspnea at rest, denies orthopnea or PND.',
      objective: 'BP 132/84 mmHg, HR 74 bpm regular, SpO2 98% room air. S1/S2 normal without gallop or rub. Lungs clear bilaterally.',
      assessment: '1. CAD with exertional angina - stable on beta blocker.\n2. Essential hypertension - controlled.\n3. Type 2 DM - well managed.',
      plan: 'Continue Metoprolol Succinate 50mg daily and Atorvastatin 40mg. Repeat fasting lipid panel and troponin I in 4 weeks. Cardiac rehab referral initiated.',
    },
    {
      id: 'NOTE-2',
      date: '2026-10-03 14:15',
      author: 'Sarah Jenkins, RN (Telemetry)',
      type: 'Nursing Clinical Note',
      subjective: 'Patient ambulated 150 feet in corridor without lightheadedness.',
      objective: 'Post-ambulation vitals: BP 128/80, HR 82 bpm, SpO2 99%. Sinus rhythm on telemetry.',
      assessment: 'Tolerating progressive physical activity well.',
      plan: 'Encourage incentive spirometry q2h while awake.',
    },
  ]);

  const [newNoteText, setNewNoteText] = useState('');
  const [isAddingNote, setIsAddingNote] = useState(false);

  if (!isOpen || !patient) return null;

  const handleAddNote = () => {
    if (!newNoteText.trim()) return;
    setClinicalNotes(prev => [
      {
        id: `NOTE-${Date.now()}`,
        date: new Date().toLocaleString(),
        author: 'Current Clinician',
        type: 'Clinical Progress Note',
        subjective: newNoteText,
        objective: 'Vitals documented in telemetry flow sheet.',
        assessment: 'Clinical stability maintained.',
        plan: 'Continue current inpatient plan of care.',
      },
      ...prev,
    ]);
    setNewNoteText('');
    setIsAddingNote(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-3 md:p-6 animate-in fade-in duration-150">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-5xl max-h-[92vh] flex flex-col overflow-hidden text-slate-800">
        
        {/* EMR Banner / Patient Header */}
        <div className="bg-slate-900 text-white p-5 shrink-0 border-b border-slate-800">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            
            {/* Patient Demographics */}
            <div className="flex items-start gap-3.5">
              <div className="w-12 h-12 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-lg shadow-sm shrink-0">
                {patient.firstName[0]}{patient.lastName[0]}
              </div>
              <div>
                <div className="flex items-center gap-2.5 flex-wrap">
                  <h2 className="text-xl font-bold tracking-tight text-white">
                    {patient.firstName} {patient.lastName}
                  </h2>
                  <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-blue-300 border border-slate-700 font-bold">
                    {patient.mrn}
                  </span>
                  <StatusBadge status={patient.admissionStatus} size="sm" />
                </div>
                
                <div className="flex items-center gap-3 text-xs text-slate-300 mt-1 flex-wrap">
                  <span><strong>Age:</strong> {patient.age} yrs</span>
                  <span>•</span>
                  <span><strong>Gender:</strong> {patient.gender}</span>
                  <span>•</span>
                  <span><strong>Blood:</strong> <span className="text-rose-400 font-bold">{patient.bloodType}</span></span>
                  <span>•</span>
                  <span><strong>Ward/Bed:</strong> {patient.currentWard || 'Outpatient'} - {patient.currentBed || 'Ambulatory'}</span>
                  <span>•</span>
                  <span><strong>Attending:</strong> {patient.assignedDoctorName}</span>
                </div>
              </div>
            </div>

            {/* Quick Actions & Close */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => alert(`Printing Summary for ${patient.firstName} ${patient.lastName} (${patient.mrn})`)}
                className="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors"
                title="Print Patient Summary"
              >
                <Printer className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Print</span>
              </button>
              
              <button
                onClick={onClose}
                className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
                title="Close Chart"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Clinical Alert Strip */}
          <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="font-bold text-rose-400 uppercase tracking-wider text-[11px] flex items-center gap-1">
                <AlertTriangle className="w-3.5 h-3.5" /> Allergies:
              </span>
              {patient.allergies && patient.allergies.length > 0 ? (
                <div className="flex items-center gap-1.5">
                  {patient.allergies.map((allergy, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-rose-950/80 text-rose-200 border border-rose-800 text-[11px] font-semibold">
                      {allergy}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-emerald-400 font-semibold">NKDA (No Known Drug Allergies)</span>
              )}
            </div>

            <div className="flex items-center gap-2 text-slate-400">
              <span>Code Status: <strong className="text-white font-mono">FULL CODE</strong></span>
              <span>•</span>
              <span>Payer: <strong className="text-blue-300">{patient.insuranceProvider} ({patient.insurancePolicyNumber})</strong></span>
            </div>
          </div>
        </div>

        {/* EMR Navigation Tabs */}
        <div className="bg-slate-50 border-b border-slate-200 px-5 flex items-center gap-1 overflow-x-auto shrink-0 scrollbar-none text-xs font-semibold">
          {[
            { id: 'overview', label: 'Overview & Vitals', icon: Activity },
            { id: 'notes', label: 'Clinical Notes', icon: FileText },
            { id: 'appointments', label: 'Appointments', icon: Calendar },
            { id: 'meds', label: 'Medications', icon: Pill },
            { id: 'labs', label: 'Lab Results', icon: FlaskConical },
            { id: 'radiology', label: 'Radiology / PACS', icon: Scan },
            { id: 'docs', label: 'Documents & Consent', icon: ShieldCheck },
            { id: 'billing', label: 'Billing & Claims', icon: CreditCard },
            { id: 'timeline', label: 'Clinical Timeline', icon: Clock },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-3 px-3 flex items-center gap-1.5 border-b-2 whitespace-nowrap transition-all ${
                  isActive
                    ? 'border-blue-600 text-blue-700 bg-white shadow-2xs font-bold'
                    : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-100/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/50">
          
          {/* TAB: OVERVIEW & VITALS */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Vitals Telemetry Row */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-1.5">
                  <Activity className="w-4 h-4 text-blue-600" /> Bedside Vitals Telemetry (Last Recorded: Today 08:00)
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
                  <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs">
                    <span className="text-[11px] text-slate-500 block font-medium">Blood Pressure</span>
                    <strong className="text-base text-slate-900 font-mono block mt-0.5">124 / 82</strong>
                    <span className="text-[10px] text-emerald-600 font-semibold">Normal (mmHg)</span>
                  </div>
                  <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs">
                    <span className="text-[11px] text-slate-500 block font-medium">Heart Rate</span>
                    <strong className="text-base text-slate-900 font-mono block mt-0.5">72 bpm</strong>
                    <span className="text-[10px] text-emerald-600 font-semibold">Normal sinus</span>
                  </div>
                  <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs">
                    <span className="text-[11px] text-slate-500 block font-medium">Oxygen Sat (SpO₂)</span>
                    <strong className="text-base text-slate-900 font-mono block mt-0.5">98%</strong>
                    <span className="text-[10px] text-emerald-600 font-semibold">Room air</span>
                  </div>
                  <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs">
                    <span className="text-[11px] text-slate-500 block font-medium">Temperature</span>
                    <strong className="text-base text-slate-900 font-mono block mt-0.5">98.6 °F</strong>
                    <span className="text-[10px] text-emerald-600 font-semibold">Afebrile (37.0 °C)</span>
                  </div>
                  <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs">
                    <span className="text-[11px] text-slate-500 block font-medium">Respiratory Rate</span>
                    <strong className="text-base text-slate-900 font-mono block mt-0.5">16 / min</strong>
                    <span className="text-[10px] text-emerald-600 font-semibold">Eupneic</span>
                  </div>
                  <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-2xs">
                    <span className="text-[11px] text-slate-500 block font-medium">Pain Score</span>
                    <strong className="text-base text-slate-900 font-mono block mt-0.5">1 / 10</strong>
                    <span className="text-[10px] text-emerald-600 font-semibold">Mild / Managed</span>
                  </div>
                </div>
              </div>

              {/* Clinical Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Active Diagnoses & Chronic Conditions */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-3">
                  <h4 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100 flex items-center justify-between">
                    <span>Chronic Conditions & Diagnoses</span>
                    <span className="text-xs text-slate-500 font-mono font-normal">ICD-10 Mapped</span>
                  </h4>
                  <div className="space-y-2 text-xs">
                    {patient.chronicConditions && patient.chronicConditions.map((cond, idx) => (
                      <div key={idx} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                        <span className="font-semibold text-slate-800">{cond}</span>
                        <span className="text-blue-700 bg-blue-50 px-2 py-0.5 rounded text-[10px] font-bold border border-blue-100">
                          Active Monitoring
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Emergency Contact & Social History */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-3">
                  <h4 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100">
                    Emergency Contact & Address
                  </h4>
                  <div className="text-xs space-y-2 text-slate-700">
                    <div className="flex justify-between py-1 border-b border-slate-50">
                      <span className="text-slate-500">Contact Person</span>
                      <strong className="text-slate-900">{patient.emergencyContact.name} ({patient.emergencyContact.relationship})</strong>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-50">
                      <span className="text-slate-500">Emergency Phone</span>
                      <strong className="font-mono text-slate-900">{patient.emergencyContact.phone}</strong>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-50">
                      <span className="text-slate-500">Patient Phone</span>
                      <strong className="font-mono text-slate-900">{patient.phone}</strong>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-50">
                      <span className="text-slate-500">Email</span>
                      <strong className="text-slate-900">{patient.email}</strong>
                    </div>
                    <div className="flex justify-between py-1">
                      <span className="text-slate-500">Home Address</span>
                      <strong className="text-slate-900 text-right">{patient.address}</strong>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB: CLINICAL NOTES */}
          {activeTab === 'notes' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Physician & Nursing Clinical Documentation</h3>
                  <p className="text-xs text-slate-500">Chronological SOAP notes, attending consultations, and multidisciplinary rounds</p>
                </div>
                <button
                  onClick={() => setIsAddingNote(!isAddingNote)}
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-2xs"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Add Progress Note</span>
                </button>
              </div>

              {isAddingNote && (
                <div className="p-4 bg-white rounded-xl border border-blue-200 shadow-sm space-y-3">
                  <label className="text-xs font-bold text-slate-800 block">New Clinical Progress Note (SOAP)</label>
                  <textarea
                    rows={4}
                    value={newNoteText}
                    onChange={(e) => setNewNoteText(e.target.value)}
                    placeholder="Enter clinical assessment, subjective findings, and management plan..."
                    className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-600"
                  />
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => setIsAddingNote(false)}
                      className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-medium"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleAddNote}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold"
                    >
                      Sign & Post to Chart
                    </button>
                  </div>
                </div>
              )}

              <div className="space-y-3">
                {clinicalNotes.map((note) => (
                  <div key={note.id} className="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs space-y-2.5">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                      <div>
                        <strong className="text-slate-900 text-xs block">{note.type}</strong>
                        <span className="text-[11px] text-slate-500">{note.author}</span>
                      </div>
                      <span className="font-mono text-[11px] text-slate-400">{note.date}</span>
                    </div>
                    <div className="text-xs space-y-1.5 text-slate-700">
                      <p><strong>S (Subjective):</strong> {note.subjective}</p>
                      <p><strong>O (Objective):</strong> {note.objective}</p>
                      <p><strong>A (Assessment):</strong> {note.assessment}</p>
                      <p><strong>P (Plan):</strong> {note.plan}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB: MEDICATIONS */}
          {activeTab === 'meds' && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Active Inpatient & Outpatient Medications</h3>
                  <p className="text-xs text-slate-500">CPOE verified orders with dosage schedule and administration guidelines</p>
                </div>
                <button
                  onClick={() => alert('Opening CPOE Prescription Writer')}
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Prescribe Medication</span>
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                    <tr>
                      <th className="p-2.5">Medication & Form</th>
                      <th className="p-2.5">Dose & Route</th>
                      <th className="p-2.5">Frequency</th>
                      <th className="p-2.5">Indication</th>
                      <th className="p-2.5">Prescriber</th>
                      <th className="p-2.5">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Metoprolol Succinate</td>
                      <td className="p-2.5 font-mono">50 mg PO (Oral)</td>
                      <td className="p-2.5">Once daily (Morning)</td>
                      <td className="p-2.5 text-slate-600">Rate control / Angina</td>
                      <td className="p-2.5">{patient.assignedDoctorName}</td>
                      <td className="p-2.5"><StatusBadge status="Active" size="sm" /></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Atorvastatin Calcium</td>
                      <td className="p-2.5 font-mono">40 mg PO (Oral)</td>
                      <td className="p-2.5">Once daily at bedtime</td>
                      <td className="p-2.5 text-slate-600">Hyperlipidemia</td>
                      <td className="p-2.5">{patient.assignedDoctorName}</td>
                      <td className="p-2.5"><StatusBadge status="Active" size="sm" /></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Aspirin (Enteric Coated)</td>
                      <td className="p-2.5 font-mono">81 mg PO (Oral)</td>
                      <td className="p-2.5">Once daily</td>
                      <td className="p-2.5 text-slate-600">Antiplatelet prophylaxis</td>
                      <td className="p-2.5">{patient.assignedDoctorName}</td>
                      <td className="p-2.5"><StatusBadge status="Active" size="sm" /></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Lisinopril</td>
                      <td className="p-2.5 font-mono">10 mg PO (Oral)</td>
                      <td className="p-2.5">Once daily</td>
                      <td className="p-2.5 text-slate-600">Hypertension</td>
                      <td className="p-2.5">{patient.assignedDoctorName}</td>
                      <td className="p-2.5"><StatusBadge status="Active" size="sm" /></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB: LAB RESULTS */}
          {activeTab === 'labs' && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Pathology & Diagnostic Laboratory Reports</h3>
                  <p className="text-xs text-slate-500">CLIA certified test results with standard clinical reference intervals</p>
                </div>
                <button
                  onClick={() => alert('Order New Laboratory Test')}
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Order Lab Test</span>
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                    <tr>
                      <th className="p-2.5">Test Panel</th>
                      <th className="p-2.5">Result</th>
                      <th className="p-2.5">Reference Range</th>
                      <th className="p-2.5">Flag</th>
                      <th className="p-2.5">Collected Date</th>
                      <th className="p-2.5">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Serum Troponin I (High Sens)</td>
                      <td className="p-2.5 font-mono font-bold text-slate-900">0.012 ng/mL</td>
                      <td className="p-2.5 text-slate-500">&lt; 0.040 ng/mL</td>
                      <td className="p-2.5"><span className="text-emerald-700 font-bold">NORMAL</span></td>
                      <td className="p-2.5 text-slate-600">Today 06:15</td>
                      <td className="p-2.5"><StatusBadge status="Completed" size="sm" /></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Hemoglobin A1c</td>
                      <td className="p-2.5 font-mono font-bold text-amber-700">6.8 %</td>
                      <td className="p-2.5 text-slate-500">4.0 - 5.6 %</td>
                      <td className="p-2.5"><span className="text-amber-700 font-bold">ELEVATED (H)</span></td>
                      <td className="p-2.5 text-slate-600">Yesterday 08:30</td>
                      <td className="p-2.5"><StatusBadge status="Completed" size="sm" /></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Serum Potassium (K+)</td>
                      <td className="p-2.5 font-mono font-bold text-slate-900">4.3 mmol/L</td>
                      <td className="p-2.5 text-slate-500">3.5 - 5.0 mmol/L</td>
                      <td className="p-2.5"><span className="text-emerald-700 font-bold">NORMAL</span></td>
                      <td className="p-2.5 text-slate-600">Today 06:15</td>
                      <td className="p-2.5"><StatusBadge status="Completed" size="sm" /></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">Estimated GFR (eGFR)</td>
                      <td className="p-2.5 font-mono font-bold text-slate-900">82 mL/min/1.73m²</td>
                      <td className="p-2.5 text-slate-500">&gt; 60 mL/min</td>
                      <td className="p-2.5"><span className="text-emerald-700 font-bold">NORMAL</span></td>
                      <td className="p-2.5 text-slate-600">Today 06:15</td>
                      <td className="p-2.5"><StatusBadge status="Completed" size="sm" /></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB: RADIOLOGY */}
          {activeTab === 'radiology' && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Diagnostic Imaging & Radiology Worklist</h3>
                  <p className="text-xs text-slate-500">PACS archived studies with board-certified radiologist impressions</p>
                </div>
                <button
                  onClick={() => alert('Order Radiology Imaging Study')}
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Order Imaging</span>
                </button>
              </div>

              <div className="space-y-3">
                <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <strong className="text-slate-900 text-sm">Chest Radiograph 2-Views (PA & Lateral)</strong>
                      <span className="text-xs text-slate-500 block">Modality: X-Ray • Radiologist: Dr. Jonathan Blake, MD</span>
                    </div>
                    <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                      Final Impression Signed
                    </span>
                  </div>
                  <div className="p-3 bg-white rounded-lg border border-slate-200 text-xs text-slate-700">
                    <p className="font-semibold text-slate-900 mb-1">IMPRESSION:</p>
                    <p>1. Heart size within normal limits. Mediastinal contours unremarkable.</p>
                    <p>2. Lungs are clear without focal consolidation, pneumothorax, or large pleural effusion.</p>
                    <p>3. Normal osseous thoracic cage.</p>
                  </div>
                  <div className="flex items-center justify-between pt-1 text-[11px] text-slate-500">
                    <span>Study Date: Oct 02, 2026 11:20</span>
                    <button
                      onClick={() => alert('Opening DICOM Web Viewer (PACS)')}
                      className="text-blue-700 hover:text-blue-800 font-semibold flex items-center gap-1"
                    >
                      <Scan className="w-3.5 h-3.5" /> View PACS DICOM Images
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB: TIMELINE */}
          {activeTab === 'timeline' && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <h3 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100">
                Clinical Encounter Timeline
              </h3>
              <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
                <div className="relative">
                  <div className="absolute -left-6 top-1 w-3.5 h-3.5 rounded-full bg-blue-600 ring-4 ring-white" />
                  <span className="text-[11px] text-slate-400 font-mono">Today 08:30</span>
                  <h4 className="text-xs font-bold text-slate-900 mt-0.5">Cardiology Attending Morning Rounds</h4>
                  <p className="text-xs text-slate-600">Dr. Marcus Vance documented progress note; patient cleared for cardiac telemetry step-down transfer.</p>
                </div>
                <div className="relative">
                  <div className="absolute -left-6 top-1 w-3.5 h-3.5 rounded-full bg-emerald-600 ring-4 ring-white" />
                  <span className="text-[11px] text-slate-400 font-mono">Today 06:15</span>
                  <h4 className="text-xs font-bold text-slate-900 mt-0.5">Laboratory Specimen Run Completed</h4>
                  <p className="text-xs text-slate-600">CBC, BMP, and cardiac troponin resulted within reference limits.</p>
                </div>
                <div className="relative">
                  <div className="absolute -left-6 top-1 w-3.5 h-3.5 rounded-full bg-slate-400 ring-4 ring-white" />
                  <span className="text-[11px] text-slate-400 font-mono">Oct 01, 2026 14:00</span>
                  <h4 className="text-xs font-bold text-slate-900 mt-0.5">Inpatient Admission via ED</h4>
                  <p className="text-xs text-slate-600">Admitted to Cardiac Step-Down Unit for evaluation of chest discomfort.</p>
                </div>
              </div>
            </div>
          )}

          {/* TAB: BILLING & INSURANCE */}
          {activeTab === 'billing' && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <h3 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100">
                Billing Account Ledger & Insurance Pre-Authorization
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-slate-500 block">Total Hospital Charges</span>
                  <strong className="text-base text-slate-900 font-mono block mt-0.5">$3,450.00</strong>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-slate-500 block">Insurance Paid / Approved</span>
                  <strong className="text-base text-emerald-700 font-mono block mt-0.5">$2,800.00</strong>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-slate-500 block">Patient Co-Insurance Balance</span>
                  <strong className="text-base text-blue-700 font-mono block mt-0.5">$650.00</strong>
                </div>
              </div>
              <p className="text-xs text-slate-500">
                Pre-authorization ref: <strong className="font-mono text-slate-800">PA-99201-BCBS</strong> • Claim status: <strong className="text-emerald-700">Adjudicated & Covered</strong>
              </p>
            </div>
          )}

          {/* TAB: APPOINTMENTS & DOCS */}
          {(activeTab === 'appointments' || activeTab === 'docs') && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4 text-xs text-slate-600">
              <h3 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100 capitalize">
                Patient {activeTab}
              </h3>
              <p>Upcoming follow-up visit scheduled with {patient.assignedDoctorName} on Oct 14, 2026 at 10:30 AM in Cardiology Pavilion Room 304.</p>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
                <span>General Admission Consent & HIPAA Disclosure</span>
                <span className="text-emerald-700 font-bold">Electronically Signed</span>
              </div>
            </div>
          )}
        </div>

        {/* EMR Footer Bar */}
        <div className="p-3.5 bg-slate-100 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600 shrink-0">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>EMR Chart Connected: <strong>CityCare Inpatient Records</strong></span>
          </div>

          <div className="flex items-center gap-2">
            {onOpenRAG && (
              <button
                onClick={onOpenRAG}
                className="px-3 py-1 bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 rounded-md font-semibold flex items-center gap-1 transition-colors"
              >
                <Stethoscope className="w-3.5 h-3.5" />
                <span>Ask Clinical Assistant about Patient</span>
              </button>
            )}
            <button
              onClick={onClose}
              className="px-3 py-1 bg-white hover:bg-slate-200 text-slate-800 border border-slate-300 rounded-md font-semibold transition-colors"
            >
              Close Chart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
