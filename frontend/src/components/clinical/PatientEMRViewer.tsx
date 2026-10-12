'use client';
import React, { useState } from 'react';
import { 
  FileText, Activity, Pill, FlaskConical, Scan, 
  ShieldCheck, AlertTriangle, Calendar, User, 
  Clock, Plus, Printer, ShieldAlert, Heart, 
  ChevronRight, Lock, CheckCircle2, Droplets, Send 
} from 'lucide-react';
import { Patient } from '@/lib/types/hms';
import { clinicalStore } from '@/lib/data/clinicalStore';
import { StatusBadge } from '../shared/StatusBadge';
import { SAMPLE_LAB_TESTS, SAMPLE_RADIOLOGY_SCANS } from '@/lib/data/mockDatabase';

interface PatientEMRViewerProps {
  patient: Patient;
  onOpenDoc?: (doc: any) => void;
  onOpenRAG?: () => void;
}

export const PatientEMRViewer: React.FC<PatientEMRViewerProps> = ({
  patient,
  onOpenDoc,
  onOpenRAG
}) => {
  const [activeSection, setActiveSection] = useState<'encounters' | 'meds' | 'vitals' | 'allergies' | 'discharge' | 'diagnostics'>('encounters');

  const chart = clinicalStore.getPatientEMRChart(patient.id);
  const patientLabs = SAMPLE_LAB_TESTS.filter(l => l.patientId === patient.id);
  const patientScans = SAMPLE_RADIOLOGY_SCANS.filter(r => r.patientId === patient.id);

  if (!chart) {
    return <div className="p-8 text-center text-slate-500">No clinical chart records found for this patient.</div>;
  }

  return (
    <div className="space-y-6">
      {/* Top Patient Master Medical Banner */}
      <div className="bg-slate-900 text-white rounded-xl p-5 border border-slate-800 shadow-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-xl shadow-inner shrink-0">
              {patient.firstName[0]}{patient.lastName[0]}
            </div>
            <div>
              <div className="flex items-center gap-3 flex-wrap">
                <h1 className="text-xl font-bold text-white tracking-tight">
                  {patient.firstName} {patient.lastName}
                </h1>
                <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-blue-300 border border-slate-700 font-bold">
                  {patient.mrn}
                </span>
                <StatusBadge status={patient.admissionStatus} size="sm" />
              </div>

              <div className="text-xs text-slate-300 mt-1 flex flex-wrap items-center gap-4">
                <span>Age: <strong>{patient.age}y</strong></span>
                <span>Gender: <strong>{patient.gender}</strong></span>
                <span>Blood Type: <strong className="text-red-400 font-mono">{patient.bloodType}</strong></span>
                <span>DOB: <strong>{patient.dateOfBirth}</strong></span>
                <span>Attending: <strong>{patient.assignedDoctorName || 'Dr. Marcus Vance, MD'}</strong></span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => window.print()}
              className="px-3 py-1.5 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 flex items-center gap-1.5 transition-all"
            >
              <Printer className="w-3.5 h-3.5" /> Print EMR Chart
            </button>
          </div>
        </div>

        {/* Allergy Red-Flag Alert Strip */}
        {chart.allergies.length > 0 && (
          <div className="mt-4 bg-red-950/70 border border-red-800/80 rounded-lg p-2.5 text-xs text-red-200 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
              <div>
                <strong>Active Allergies:</strong>{' '}
                {chart.allergies.map(a => `${a.allergen} (${a.severity})`).join(' • ')}
              </div>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-red-900 text-red-100 font-bold uppercase">
              Allergy Warning
            </span>
          </div>
        )}
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex border-b border-slate-200 bg-white rounded-t-xl px-4 gap-2 text-xs overflow-x-auto shadow-2xs">
        {[
          { id: 'encounters', label: `Clinical Encounters (${chart.encounters.length})`, icon: FileText },
          { id: 'meds', label: `e-Prescriptions (${chart.prescriptions.length})`, icon: Pill },
          { id: 'vitals', label: `Bedside Vitals & MEWS (${chart.observations.length})`, icon: Activity },
          { id: 'diagnostics', label: `Diagnostic Labs & Scans (${patientLabs.length + patientScans.length})`, icon: FlaskConical },
          { id: 'discharge', label: `Discharge Summaries (${chart.dischargeSummaries.length})`, icon: ShieldCheck },
          { id: 'allergies', label: `Allergies & Adverse Reactions (${chart.allergies.length})`, icon: AlertTriangle },
        ].map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveSection(tab.id as any)}
              className={`py-3 px-3 font-semibold border-b-2 flex items-center gap-1.5 whitespace-nowrap transition-all ${
                activeSection === tab.id
                  ? 'border-blue-600 text-blue-700 bg-blue-50/40'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Main Longitudinal Content Sections */}
      <div className="bg-white rounded-b-xl border border-t-0 border-slate-200 p-6 shadow-2xs">
        
        {/* Section 1: Clinical Encounters & SOAP Notes */}
        {activeSection === 'encounters' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900 text-sm">Longitudinal Encounter History</h3>
              <span className="text-xs text-slate-500">{chart.encounters.length} Encounters Documented</span>
            </div>

            <div className="space-y-4">
              {chart.encounters.map(enc => (
                <div key={enc.id} className="p-5 rounded-xl border border-slate-200 bg-white shadow-2xs space-y-3">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b pb-3 border-slate-100">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 font-bold">
                        {enc.id}
                      </span>
                      <h4 className="font-bold text-sm text-slate-900">{enc.encounterType}</h4>
                      <span className="text-xs text-slate-500">• {enc.department}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-slate-500">{enc.encounterDate} {enc.startTime}</span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 flex items-center gap-1">
                        <Lock className="w-3 h-3" /> {enc.signStatus}
                      </span>
                    </div>
                  </div>

                  <div className="text-xs text-slate-700">
                    <strong className="text-slate-900">Chief Complaint:</strong> {enc.chiefComplaint}
                  </div>

                  {/* SOAP Breakdown */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-50 p-3.5 rounded-lg border border-slate-200">
                    <div>
                      <strong className="text-blue-900 block">Subjective (S):</strong>
                      <p className="text-slate-700 mt-0.5">{enc.subjectiveNotes || 'N/A'}</p>
                    </div>
                    <div>
                      <strong className="text-blue-900 block">Objective (O):</strong>
                      <p className="text-slate-700 mt-0.5">{enc.objectiveNotes || 'N/A'}</p>
                    </div>
                    <div>
                      <strong className="text-blue-900 block">Assessment (A):</strong>
                      <p className="text-slate-700 mt-0.5 whitespace-pre-wrap">{enc.assessmentNotes || 'N/A'}</p>
                    </div>
                    <div>
                      <strong className="text-blue-900 block">Plan (P):</strong>
                      <p className="text-slate-700 mt-0.5 whitespace-pre-wrap">{enc.planNotes || 'N/A'}</p>
                    </div>
                  </div>

                  {/* Codified Diagnoses */}
                  {enc.diagnoses.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {enc.diagnoses.map(d => (
                        <span key={d.id} className="px-2 py-0.5 rounded font-mono text-[11px] bg-slate-100 text-slate-800 border border-slate-200">
                          <strong>{d.code}</strong> - {d.description} ({d.type})
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Amendments */}
                  {enc.amendments.length > 0 && (
                    <div className="pt-2 border-t border-slate-100 space-y-2">
                      <strong className="text-xs text-amber-900 flex items-center gap-1">
                        <ShieldCheck className="w-3.5 h-3.5 text-amber-600" /> Authorized Addenda ({enc.amendments.length}):
                      </strong>
                      {enc.amendments.map(amd => (
                        <div key={amd.id} className="p-2.5 rounded bg-amber-50/60 border border-amber-200 text-xs">
                          <div className="flex items-center justify-between text-[11px] text-amber-900 font-semibold mb-1">
                            <span>{amd.amendedBy} ({amd.amendmentType} v{amd.version})</span>
                            <span className="font-mono text-slate-500">{amd.amendedAt}</span>
                          </div>
                          <p className="text-slate-800">{amd.amendmentContent}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-[11px] text-slate-500">
                    <span>Signed by: <strong>{enc.signedBy || enc.doctorName}</strong></span>
                    <span className="font-mono">{enc.digitalSignatureHash}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Section 2: e-Prescriptions */}
        {activeSection === 'meds' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm">Active & Past Electronic Prescriptions</h3>
            <div className="space-y-3">
              {chart.prescriptions.map(rx => (
                <div key={rx.id} className="p-4 rounded-xl border border-slate-200 bg-white space-y-2 text-xs">
                  <div className="flex items-center justify-between border-b pb-2">
                    <span className="font-mono font-bold text-blue-700">{rx.id}</span>
                    <span className="text-slate-500">{rx.prescribedDate}</span>
                  </div>

                  <div className="divide-y divide-slate-100">
                    {rx.items.map(it => (
                      <div key={it.id} className="py-2 flex items-center justify-between">
                        <div>
                          <strong className="text-slate-900 text-sm">{it.medicineName}</strong>
                          <div className="text-slate-600">
                            {it.dosage} • {it.route} • {it.frequency} for {it.durationDays} days
                          </div>
                          <div className="text-slate-500 italic mt-0.5">&ldquo;{it.instructions}&rdquo;</div>
                        </div>
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                          {it.dispenseStatus}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Section 3: Vitals & MEWS */}
        {activeSection === 'vitals' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-900 text-sm">Bedside Vitals & Early Warning Score Flowsheet</h3>
            <div className="overflow-x-auto border border-slate-200 rounded-lg text-xs">
              <table className="w-full text-left">
                <thead className="bg-slate-50 text-slate-700 font-bold border-b">
                  <tr>
                    <th className="p-2.5">Time</th>
                    <th className="p-2.5">BP</th>
                    <th className="p-2.5">HR</th>
                    <th className="p-2.5">RR</th>
                    <th className="p-2.5">SpO2</th>
                    <th className="p-2.5">Temp</th>
                    <th className="p-2.5">Pain</th>
                    <th className="p-2.5">MEWS Score</th>
                    <th className="p-2.5">Nurse</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {chart.observations.map(obs => (
                    <tr key={obs.id}>
                      <td className="p-2.5 font-mono text-slate-500">{new Date(obs.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
                      <td className="p-2.5 font-semibold text-slate-900">{obs.systolicBp}/{obs.diastolicBp}</td>
                      <td className="p-2.5 text-slate-900">{obs.heartRate} bpm</td>
                      <td className="p-2.5 text-slate-700">{obs.respiratoryRate}/min</td>
                      <td className="p-2.5 font-bold text-teal-700">{obs.spo2}%</td>
                      <td className="p-2.5 text-slate-700">{obs.temperature}°F</td>
                      <td className="p-2.5 text-slate-700">{obs.painScore}/10</td>
                      <td className="p-2.5">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                          {obs.mews.score}
                        </span>
                      </td>
                      <td className="p-2.5 text-slate-600">{obs.nurseName}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Section 4: Diagnostics (Labs & Scans) */}
        {activeSection === 'diagnostics' && (
          <div className="space-y-4 text-xs">
            <h3 className="font-bold text-slate-900 text-sm">Diagnostic Investigations & Reports</h3>
            
            <div className="space-y-3">
              <h4 className="font-bold text-slate-800">Laboratory Panels:</h4>
              {patientLabs.map(lab => (
                <div key={lab.id} className="p-3.5 rounded-lg border border-slate-200 bg-white">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-bold text-slate-900">{lab.testName} ({lab.category})</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">{lab.status}</span>
                  </div>
                  {lab.results && (
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2 pt-2 border-t border-slate-100">
                      {lab.results.map((r, i) => (
                        <div key={i} className="p-2 bg-slate-50 rounded">
                          <span className="text-slate-500 text-[10px] block">{r.parameter}</span>
                          <strong className="text-slate-900 text-xs">{r.value} {r.unit}</strong>
                          <span className="text-[10px] text-slate-500 block">Ref: {r.referenceRange}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="space-y-3 pt-3">
              <h4 className="font-bold text-slate-800">Radiology & PACS Scans:</h4>
              {patientScans.map(scan => (
                <div key={scan.id} className="p-3.5 rounded-lg border border-slate-200 bg-white space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900">{scan.modality} - {scan.anatomy}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{scan.status}</span>
                  </div>
                  <p className="text-slate-600">Findings: {scan.findings}</p>
                  <p className="text-slate-800 font-semibold">Impression: {scan.impression}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Section 5: Discharge Summaries */}
        {activeSection === 'discharge' && (
          <div className="space-y-4 text-xs">
            <h3 className="font-bold text-slate-900 text-sm">Final Inpatient Discharge Summaries</h3>
            {chart.dischargeSummaries.map(ds => (
              <div key={ds.id} className="p-5 rounded-xl border border-slate-300 bg-white space-y-3">
                <div className="flex items-center justify-between border-b pb-2">
                  <span className="font-mono font-bold text-blue-700">{ds.id}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">{ds.status}</span>
                </div>
                <div><strong>Discharge Diagnosis:</strong> {ds.dischargeDiagnosis}</div>
                <div><strong>Hospital Course:</strong> <div className="p-2 bg-slate-50 rounded mt-1 whitespace-pre-wrap">{ds.hospitalCourse}</div></div>
                <div><strong>Signed by:</strong> {ds.attendingDoctorName} ({ds.signedAt})</div>
              </div>
            ))}
          </div>
        )}

        {/* Section 6: Allergies */}
        {activeSection === 'allergies' && (
          <div className="space-y-3 text-xs">
            <h3 className="font-bold text-slate-900 text-sm">Verified Patient Allergies</h3>
            {chart.allergies.map(alg => (
              <div key={alg.id} className="p-3 rounded-lg border border-red-200 bg-red-50/40 flex items-center justify-between">
                <div>
                  <div className="font-bold text-red-950 flex items-center gap-2">
                    {alg.allergen}
                    <span className="px-2 py-0.5 rounded text-[10px] bg-red-200/80 text-red-900 font-bold">
                      {alg.severity}
                    </span>
                  </div>
                  <p className="text-slate-600 mt-0.5">Reaction: {alg.reaction}</p>
                </div>
                <span className="text-[11px] text-slate-500 font-mono">Verified: {alg.verifiedDate}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
