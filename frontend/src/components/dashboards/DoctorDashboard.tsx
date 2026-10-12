'use client';
import React, { useState, useEffect } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Users, Calendar, FileText, Activity, Stethoscope, 
  AlertCircle, Pill, FlaskConical, Search, CheckCircle2, 
  Clock, ShieldAlert, ChevronRight, Plus, BookOpen, 
  MessageSquare, Scan, ArrowUpRight, Check, Printer 
} from 'lucide-react';
import { SEED_PATIENTS, SAMPLE_LAB_TESTS, SAMPLE_RADIOLOGY_SCANS, SAMPLE_PRESCRIPTIONS, SAMPLE_APPOINTMENTS } from '@/lib/data/mockDatabase';
import { Patient } from '@/lib/types/hms';
import { HOSPITAL_DOCUMENTS } from '@/lib/data/hospitalDocuments';
import { DoctorWorkspace } from '../clinical/DoctorWorkspace';
import { PatientEMRViewer } from '../clinical/PatientEMRViewer';

interface DoctorDashboardProps {
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
  onSelectPatient?: (patient: Patient) => void;
}

export const DoctorDashboard: React.FC<DoctorDashboardProps> = ({ 
  onOpenRAG, 
  onOpenDoc, 
  activeNav = 'dashboard',
  setActiveNav,
  onSelectPatient
}) => {
  const [selectedPatient, setSelectedPatient] = useState<Patient>(SEED_PATIENTS[0]);
  const [patientSearch, setPatientSearch] = useState('');
  const [activeTab, setActiveTab] = useState<'profile' | 'labs' | 'imaging' | 'prescriptions' | 'notes'>('profile');
  const [clinicalNotesText, setClinicalNotesText] = useState<string>(
    'Cardiology Follow-Up Oct 4, 2026: Post-percutaneous coronary intervention (DES stenting of Mid-LAD) Day 2. Patient denies recurrent angina, shortness of breath, or palpitations. Femoral/radial access site clean without hematoma or bruit. Continue dual antiplatelet therapy (Aspirin + Ticagrelor) for 12 months. Discharge anticipated tomorrow morning pending morning electrolytes.'
  );
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Sync activeNav with internal view
  useEffect(() => {
    if (activeNav === 'labs') setActiveTab('labs');
    else if (activeNav === 'patients') setActiveTab('profile');
  }, [activeNav]);

  const handleSaveNotes = () => {
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2500);
  };

  const patientLabs = SAMPLE_LAB_TESTS.filter(l => l.patientId === selectedPatient.id);
  const patientImaging = SAMPLE_RADIOLOGY_SCANS.filter(r => r.patientId === selectedPatient.id);
  const patientPrescriptions = SAMPLE_PRESCRIPTIONS.filter(p => p.patientId === selectedPatient.id);
  const clinicalGuidelines = HOSPITAL_DOCUMENTS.filter(d => d.category.includes('Clinical') || d.category.includes('Emergency') || d.category.includes('Medicine'));

  // Today's Clinical Schedule Timeline
  const scheduleTimeline = [
    { time: '08:30', patient: 'John Anderson', mrn: 'MRN-884920', type: 'Cardiology Follow-up', room: 'Consultation Room 204', status: 'In Consultation', urgency: 'routine', patientObj: SEED_PATIENTS[0] },
    { time: '09:00', patient: 'Elena Rostova', mrn: 'MRN-449182', type: 'New Consultation', room: 'Consultation Room 204', status: 'Waiting', urgency: 'routine', patientObj: SEED_PATIENTS[1] },
    { time: '09:30', patient: 'Marcus Brody', mrn: 'MRN-194029', type: 'Emergency Consultation', room: 'Trauma Bay 1', status: 'Urgent Alert', urgency: 'critical', patientObj: SEED_PATIENTS[2] },
    { time: '10:30', patient: 'Ward Rounds (4 Patients)', mrn: 'CAR-STEPDOWN', type: 'Inpatient Telemetry Rounds', room: 'Cardiac Step-Down 3A', status: 'Scheduled', urgency: 'routine', patientObj: SEED_PATIENTS[0] },
    { time: '11:15', patient: 'David Miller', mrn: 'MRN-552019', type: 'Post-PCI Stent Review', room: 'Cath Lab Recovery', status: 'Scheduled', urgency: 'routine', patientObj: SEED_PATIENTS[3] || SEED_PATIENTS[0] },
  ];

  const filteredPatients = SEED_PATIENTS.filter(p => 
    p.firstName.toLowerCase().includes(patientSearch.toLowerCase()) ||
    p.lastName.toLowerCase().includes(patientSearch.toLowerCase()) ||
    p.mrn.toLowerCase().includes(patientSearch.toLowerCase())
  );

  return (
    <div className="space-y-6 text-slate-800">
      {/* Top Clinical Header Bar */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 flex items-center gap-1">
              <Stethoscope className="w-3.5 h-3.5" /> Attending Physician Portal
            </span>
            <span className="text-xs text-slate-500">Department of Cardiology • Cath Lab 2 & Inpatient Step-Down</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-slate-900">Good morning, Dr. Marcus Vance, MD, FACC</h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Today&apos;s Schedule: <strong className="text-slate-900">8 Consultations</strong> • 4 Ward Patients • 1 Critical Alert • Active view: <span className="font-semibold text-blue-700 capitalize">{activeNav}</span>
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
              {(['dashboard', 'workspace', 'emr', 'patients', 'appointments', 'labs', 'guidelines'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all ${
                    activeNav === n ? 'bg-white text-blue-700 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'workspace' ? 'Workstation' : n === 'emr' ? 'Patient EMR' : n}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5" /> Clinical Guidelines RAG
          </button>
        </div>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <StatCard
          title="Next Appointment"
          value="08:30 AM"
          subtitle="John Anderson (Room 204)"
          icon={Clock}
          variant="blue"
        />
        <StatCard
          title="Patients Waiting"
          value="3 Patients"
          subtitle="Average wait: 12 mins"
          icon={Users}
          variant="teal"
        />
        <StatCard
          title="Consults Completed"
          value="5 / 8 Done"
          subtitle="62% Completed"
          icon={CheckCircle2}
          variant="emerald"
        />
        <StatCard
          title="Pending Lab Results"
          value="2 Reports"
          subtitle="Troponin & Lipid Panel"
          icon={FlaskConical}
          variant="amber"
        />
        <StatCard
          title="Critical Alerts"
          value="1 High Alert"
          subtitle="Trauma Bay consult req."
          icon={AlertCircle}
          variant="rose"
        />
      </div>

      {/* VIEW: DASHBOARD OVERVIEW */}
      {activeNav === 'dashboard' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left 2 Cols: Schedule Timeline & Inpatient Cards */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Timeline of Today's Consultations */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Today&apos;s Clinical Consultation Timeline</h3>
                  <p className="text-xs text-slate-500">Scheduled outpatient appointments, specialty consults, and unit rounds</p>
                </div>
                <span className="text-xs font-mono font-semibold bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-200">
                  Oct 04, 2026
                </span>
              </div>

              <div className="relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
                {scheduleTimeline.map((item, idx) => {
                  const isCritical = item.urgency === 'critical';
                  return (
                    <div key={idx} className="relative group">
                      <div className={`absolute -left-6 top-1 w-3.5 h-3.5 rounded-full ring-4 ring-white ${
                        isCritical ? 'bg-rose-600 animate-pulse' : 'bg-blue-600'
                      }`} />
                      <div className={`p-3 rounded-lg border transition-all ${
                        isCritical ? 'bg-rose-50/70 border-rose-200' : 'bg-slate-50 border-slate-200 hover:border-slate-300'
                      }`}>
                        <div className="flex items-start justify-between">
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-mono text-xs font-bold text-slate-700">{item.time}</span>
                              <strong className="text-xs text-slate-900">{item.patient}</strong>
                              <span className="font-mono text-[10px] text-slate-400 font-medium">({item.mrn})</span>
                            </div>
                            <p className="text-xs text-slate-600 mt-0.5">
                              {item.type} • <span className="font-medium text-slate-800">{item.room}</span>
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            <StatusBadge status={item.status} size="sm" />
                            {onSelectPatient && item.patientObj && (
                              <button
                                onClick={() => onSelectPatient(item.patientObj)}
                                className="px-2 py-1 bg-white hover:bg-blue-50 text-blue-700 border border-slate-200 rounded text-[11px] font-semibold transition-colors"
                              >
                                Open EMR
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Active Inpatient Cards with Quick Actions */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Assigned Inpatient Cards</h3>
                  <p className="text-xs text-slate-500">Active cardiology step-down patients under your primary service</p>
                </div>
                <span className="text-xs text-slate-500">{SEED_PATIENTS.length} Active Patients</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                {SEED_PATIENTS.map((p) => (
                  <div key={p.id} className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-white hover:border-blue-300 transition-all space-y-2.5">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-1.5">
                          <strong className="text-xs font-bold text-slate-900">{p.firstName} {p.lastName}</strong>
                          <span className="font-mono text-[10px] text-slate-500">{p.mrn}</span>
                        </div>
                        <p className="text-[11px] text-slate-500 mt-0.5">
                          {p.age}y • {p.gender} • <span className="text-slate-700 font-medium">{p.currentWard || 'Ward'} ({p.currentBed || 'Bed'})</span>
                        </p>
                      </div>
                      <StatusBadge status={p.admissionStatus} size="sm" />
                    </div>

                    <div className="p-2 rounded-lg bg-white border border-slate-200/80 text-[11px] space-y-1">
                      <div className="flex justify-between text-slate-600">
                        <span>Chief Complaint:</span>
                        <strong className="text-slate-800 font-semibold">{p.chronicConditions?.[0] || 'Chest Tightness'}</strong>
                      </div>
                      <div className="flex justify-between text-slate-600">
                        <span>Vitals:</span>
                        <span className="font-mono text-slate-800 font-medium">BP 124/82 • HR 72 • SpO₂ 98%</span>
                      </div>
                      <div className="flex justify-between text-slate-600">
                        <span>Allergies:</span>
                        <span className="text-rose-600 font-semibold">{p.allergies?.join(', ') || 'NKDA'}</span>
                      </div>
                    </div>

                    {/* Quick Clinical Actions */}
                    <div className="flex items-center justify-between pt-1 gap-1 flex-wrap">
                      <button
                        onClick={() => onSelectPatient ? onSelectPatient(p) : setSelectedPatient(p)}
                        className="px-2 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[11px] font-bold shadow-2xs transition-colors"
                      >
                        Open Full EMR
                      </button>
                      <button
                        onClick={() => alert(`Prescribing for ${p.firstName} ${p.lastName}`)}
                        className="px-2 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded text-[11px] font-semibold"
                      >
                        Rx
                      </button>
                      <button
                        onClick={() => alert(`Order Lab for ${p.firstName} ${p.lastName}`)}
                        className="px-2 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded text-[11px] font-semibold"
                      >
                        Lab
                      </button>
                      <button
                        onClick={() => alert(`Paging nurse for ${p.firstName}`)}
                        className="px-2 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded text-[11px] font-semibold"
                      >
                        Page RN
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Col: Quick Clinical Note Editor & Approved Guidelines */}
          <div className="space-y-6">
            
            {/* Quick SOAP Note Editor */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-blue-600" /> Active Progress Note
                </h3>
                <span className="text-[11px] font-mono text-slate-400">EMR Direct</span>
              </div>
              <p className="text-xs text-slate-500">
                Drafting for: <strong className="text-slate-800">{selectedPatient.firstName} {selectedPatient.lastName} ({selectedPatient.mrn})</strong>
              </p>
              <textarea
                rows={7}
                value={clinicalNotesText}
                onChange={(e) => setClinicalNotesText(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-600 font-mono leading-relaxed"
              />
              <div className="flex items-center justify-between pt-1">
                {saveSuccess ? (
                  <span className="text-emerald-700 text-xs font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Note Saved to EMR
                  </span>
                ) : (
                  <span className="text-slate-400 text-[11px]">Unsigned Draft</span>
                )}
                <button
                  onClick={handleSaveNotes}
                  className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold shadow-2xs transition-colors"
                >
                  Sign & Post Note
                </button>
              </div>
            </div>

            {/* Approved Hospital Clinical Guidelines */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <BookOpen className="w-4 h-4 text-teal-600" /> Clinical Guidelines & Protocols
                </h3>
                <span className="text-[10px] font-mono bg-emerald-50 text-emerald-700 px-1.5 py-0.5 rounded border border-emerald-200 font-semibold">
                  Grounded
                </span>
              </div>
              <p className="text-xs text-slate-500">Directly searchable via the Doctor RAG Assistant</p>
              <div className="space-y-2">
                {clinicalGuidelines.slice(0, 4).map((doc) => (
                  <div
                    key={doc.id}
                    onClick={() => onOpenDoc(doc)}
                    className="p-2.5 rounded-lg border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 cursor-pointer transition-colors"
                  >
                    <strong className="text-xs text-slate-900 block leading-tight hover:text-blue-700">
                      {doc.title}
                    </strong>
                    <div className="flex items-center justify-between text-[11px] text-slate-500 mt-1">
                      <span>{doc.category}</span>
                      <span className="font-mono text-[10px] text-slate-400">{doc.id}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW: ASSIGNED PATIENTS */}
      {activeNav === 'patients' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Inpatient & Outpatient Census</h3>
              <p className="text-xs text-slate-500">Comprehensive patient roster assigned to Cardiology Primary Service</p>
            </div>
            <div className="relative w-64">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search by name, MRN..."
                value={patientSearch}
                onChange={(e) => setPatientSearch(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Patient & MRN</th>
                  <th className="p-2.5">Age/Gender</th>
                  <th className="p-2.5">Location / Bed</th>
                  <th className="p-2.5">Primary Diagnosis</th>
                  <th className="p-2.5">Allergies</th>
                  <th className="p-2.5">Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredPatients.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{p.firstName} {p.lastName}</strong>
                      <span className="font-mono text-[10px] text-slate-400">{p.mrn}</span>
                    </td>
                    <td className="p-2.5 text-slate-600">{p.age}y • {p.gender}</td>
                    <td className="p-2.5 font-medium text-slate-700">{p.currentWard || 'Ward'} - {p.currentBed || 'Bed'}</td>
                    <td className="p-2.5 text-slate-800">{p.chronicConditions?.[0] || 'Evaluation'}</td>
                    <td className="p-2.5">
                      <span className="text-rose-600 font-semibold">{p.allergies?.join(', ') || 'NKDA'}</span>
                    </td>
                    <td className="p-2.5"><StatusBadge status={p.admissionStatus} size="sm" /></td>
                    <td className="p-2.5 text-right">
                      <button
                        onClick={() => onSelectPatient ? onSelectPatient(p) : setSelectedPatient(p)}
                        className="px-2.5 py-1 bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 rounded text-[11px] font-semibold"
                      >
                        Open EMR Chart
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: LABS & DIAGNOSTICS */}
      {activeNav === 'labs' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Laboratory & Diagnostic Panic Values Console</h3>
              <p className="text-xs text-slate-500">Real-time telemetry and specimen results across assigned cardiac patients</p>
            </div>
            <span className="text-xs font-mono bg-rose-50 text-rose-700 px-2 py-0.5 rounded border border-rose-200 font-semibold">
              1 Panic Result Reported
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Patient</th>
                  <th className="p-2.5">Test Ordered</th>
                  <th className="p-2.5">Result</th>
                  <th className="p-2.5">Reference Range</th>
                  <th className="p-2.5">Flag</th>
                  <th className="p-2.5">Collected</th>
                  <th className="p-2.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {SAMPLE_LAB_TESTS.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50">
                    <td className="p-2.5 font-bold text-slate-900">{t.patientName}</td>
                    <td className="p-2.5">{t.testName}</td>
                    <td className="p-2.5 font-mono font-bold text-slate-900">{t.results?.[0] ? `${t.results[0].value} ${t.results[0].unit}` : 'Pending'}</td>
                    <td className="p-2.5 text-slate-500 font-mono text-[11px]">{t.results?.[0]?.referenceRange || 'Standard'}</td>
                    <td className="p-2.5">
                      {t.isCritical ? (
                        <span className="px-1.5 py-0.2 rounded bg-rose-50 text-rose-700 border border-rose-200 font-bold text-[10px]">
                          CRITICAL
                        </span>
                      ) : (
                        <span className="text-emerald-700 font-bold text-[10px]">NORMAL</span>
                      )}
                    </td>
                    <td className="p-2.5 text-slate-500 font-mono text-[11px]">{t.orderDate}</td>
                    <td className="p-2.5"><StatusBadge status={t.status} size="sm" /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: CLINICAL GUIDELINES */}
      {activeNav === 'guidelines' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Clinical Practice Guidelines</h3>
              <p className="text-xs text-slate-500">Board-certified clinical pathways and medication administration protocols</p>
            </div>
            <button
              onClick={onOpenRAG}
              className="px-3 py-1 bg-blue-600 text-white rounded-lg text-xs font-bold"
            >
              Ask RAG Guideline Query
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {clinicalGuidelines.map((doc) => (
              <div
                key={doc.id}
                onClick={() => onOpenDoc(doc)}
                className="p-4 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-slate-50 cursor-pointer transition-all space-y-2"
              >
                <div className="flex items-start justify-between">
                  <strong className="text-xs font-bold text-slate-900 block">{doc.title}</strong>
                  <span className="font-mono text-[10px] text-slate-400">{doc.id}</span>
                </div>
                <p className="text-xs text-slate-600 line-clamp-2">{doc.content}</p>
                <div className="flex items-center justify-between pt-1 text-[11px] text-slate-500">
                  <span>Category: {doc.category}</span>
                  <span className="text-blue-700 font-semibold flex items-center gap-0.5">
                    View Document <ArrowUpRight className="w-3 h-3" />
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* VIEW: CLINICAL WORKSTATION */}
      {activeNav === 'workspace' && (
        <DoctorWorkspace
          onOpenDoc={onOpenDoc}
          onOpenRAG={onOpenRAG}
          onSelectPatient={onSelectPatient}
        />
      )}

      {/* VIEW: LONGITUDINAL PATIENT EMR */}
      {activeNav === 'emr' && (
        <PatientEMRViewer
          patient={selectedPatient}
          onOpenDoc={onOpenDoc}
          onOpenRAG={onOpenRAG}
        />
      )}
    </div>
  );
};
