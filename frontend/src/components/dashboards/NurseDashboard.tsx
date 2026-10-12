'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Heart, Activity, CheckSquare, Clock, AlertTriangle, 
  Bed, Pill, ShieldCheck, Thermometer, UserCheck, 
  Plus, CheckCircle2, FileText, ArrowRight, ShieldAlert, 
  ChevronRight, PhoneCall 
} from 'lucide-react';
import { SEED_PATIENTS } from '@/lib/data/mockDatabase';
import { Patient } from '@/lib/types/hms';
import { NursingStationConsole } from '../clinical/NursingStationConsole';

interface NurseDashboardProps {
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
  onSelectPatient?: (patient: Patient) => void;
}

export const NurseDashboard: React.FC<NurseDashboardProps> = ({ 
  onOpenRAG, 
  onOpenDoc, 
  activeNav = 'dashboard',
  setActiveNav,
  onSelectPatient
}) => {
  const [tasks, setTasks] = useState([
    { id: 'TSK-1', patient: 'John Anderson (Bed 304-B)', task: '12:00 PM Vitals & Blood Glucose Check', time: '12:00 PM', done: true },
    { id: 'TSK-2', patient: 'John Anderson (Bed 304-B)', task: 'Administer Ticagrelor 90mg PO & Atorvastatin', time: '01:00 PM', done: false },
    { id: 'TSK-3', patient: 'Elena Rostova (Bed 212-A)', task: 'Nebulizer Treatment (Albuterol) & SpO2 Titration', time: '01:30 PM', done: false },
    { id: 'TSK-4', patient: 'Elena Rostova (Bed 212-A)', task: 'Incentive Spirometry & Respiratory Assessment', time: '02:00 PM', done: false },
    { id: 'TSK-5', patient: 'Unit 3A Station', task: 'Shift Handover SBAR Documentation & Narcotic Count', time: '03:00 PM', done: false },
  ]);

  const [medsList, setMedsList] = useState([
    { id: 'M-1', patient: 'John Anderson', bed: 'Room 204 (Bed 304-B)', drug: 'Ticagrelor 90mg PO', schedule: '10:00 AM', status: 'DUE NOW', given: false },
    { id: 'M-2', patient: 'John Anderson', bed: 'Room 204 (Bed 304-B)', drug: 'Atorvastatin 40mg PO', schedule: '10:00 AM', status: 'DUE NOW', given: false },
    { id: 'M-3', patient: 'Elena Rostova', bed: 'Room 205 (Bed 212-A)', drug: 'Albuterol 2.5mg Inhalation', schedule: '11:30 AM', status: 'SCHEDULED', given: false },
    { id: 'M-4', patient: 'Marcus Brody', bed: 'Room 206 (Bed 108)', drug: 'Cefazolin 2g IVPB Infusion', schedule: '12:00 PM', status: 'SCHEDULED', given: false },
  ]);

  const [vitalsLog, setVitalsLog] = useState([
    { id: 'V-1', patient: 'John Anderson', bed: 'Bed 304-B', time: '10:00 AM', bp: '124/82', hr: 72, spo2: 98, temp: 98.6, rr: 16, status: 'Normal' },
    { id: 'V-2', patient: 'Elena Rostova', bed: 'Bed 212-A', time: '09:45 AM', bp: '118/74', hr: 82, spo2: 95, temp: 99.1, rr: 20, status: 'Monitoring' },
    { id: 'V-3', patient: 'Marcus Brody', bed: 'Bed 108', time: '09:30 AM', bp: '138/88', hr: 88, spo2: 96, temp: 98.4, rr: 18, status: 'Post-Op' },
  ]);

  const [newBp, setNewBp] = useState('120/80');
  const [newHr, setNewHr] = useState('72');
  const [newSpo2, setNewSpo2] = useState('98');
  const [newTemp, setNewTemp] = useState('98.6');
  const [newPatient, setNewPatient] = useState('John Anderson');

  const toggleTask = (id: string) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t));
  };

  const handleAdministerMed = (id: string) => {
    setMedsList(prev => prev.map(m => m.id === id ? { ...m, given: true, status: 'ADMINISTERED' } : m));
  };

  const handleLogVital = (e: React.FormEvent) => {
    e.preventDefault();
    const entry = {
      id: `V-${Date.now()}`,
      patient: newPatient,
      bed: 'Bed 304-B',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      bp: newBp,
      hr: parseInt(newHr, 10) || 72,
      spo2: parseInt(newSpo2, 10) || 98,
      temp: parseFloat(newTemp) || 98.6,
      rr: 16,
      status: 'Normal'
    };
    setVitalsLog([entry, ...vitalsLog]);
    alert(`Vital signs recorded for ${newPatient}`);
  };

  return (
    <div className="space-y-6 text-slate-800">
      {/* Standard Compact Page Header */}
      <div className="bg-white dark:bg-[#111827] rounded-xl p-5 border border-[#DCE4EA] dark:border-[#293548] shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-[#0F8B8D] border border-teal-200 flex items-center gap-1">
              <Heart className="w-3.5 h-3.5 text-[#0F8B8D]" /> Unit 3A Telemetry Step-Down
            </span>
            <span className="text-xs text-slate-500">Charge Nurse • Sarah Jenkins, BSN, RN • Ratio 1:3</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Nurse Station Console</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Bedside telemetry, 5-rights medication administration records (MAR), and shift handover.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <button
              onClick={() => setActiveNav('vitals')}
              className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-200 rounded-lg text-xs font-semibold border border-slate-200 dark:border-slate-700 transition-colors cursor-pointer"
            >
              Record Vitals
            </button>
          )}

          <button
            onClick={() => setActiveNav ? setActiveNav('tasks') : null}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <CheckSquare className="w-3.5 h-3.5" /> Shift Handover
          </button>

          <button
            onClick={onOpenRAG}
            className="px-3 py-1.5 bg-teal-50 hover:bg-teal-100 text-[#0F8B8D] dark:bg-teal-950/60 rounded-lg text-xs font-semibold border border-teal-200 dark:border-teal-800 flex items-center gap-1.5 transition-colors cursor-pointer"
            title="Open Nursing SOP & Drug RAG"
          >
            <ShieldCheck className="w-3.5 h-3.5" /> Nursing SOPs
          </button>
        </div>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Assigned Patients"
          value="3 Patients"
          subtitle="Primary telemetry load"
          icon={UserCheck}
          variant="teal"
        />
        <StatCard
          title="Vitals Due Next"
          value="10:00 AM"
          subtitle="All telemetry normal"
          icon={Activity}
          variant="blue"
        />
        <StatCard
          title="Med Administration"
          value="2 Doses Due"
          subtitle="5-Rights verification active"
          icon={Pill}
          variant="amber"
        />
        <StatCard
          title="Shift Care Tasks"
          value={`${tasks.filter(t => !t.done).length} Pending`}
          subtitle="Narcotic count verified"
          icon={CheckSquare}
          variant="emerald"
        />
      </div>

      {/* VIEW: DASHBOARD OVERVIEW */}
      {(activeNav === 'dashboard' || activeNav === 'vitals') && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Assigned Patient Bedside Telemetry Cards */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between pb-1">
              <h3 className="text-sm font-bold text-slate-900">Bedside Telemetry & Nursing Care Plan</h3>
              <span className="text-xs text-slate-500 font-mono">Telemetry Monitor Active</span>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {/* Patient 1: John Anderson */}
              <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <strong className="text-sm font-bold text-slate-900">John Anderson</strong>
                      <span className="font-mono text-xs px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">MRN-884920</span>
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                        ROOM 204 • Bed 304-B
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">
                      58y Male • CAD / Post-PCI Stent • Attending: Dr. Marcus Vance, MD
                    </p>
                  </div>
                  <StatusBadge status="Stable" size="sm" />
                </div>

                {/* Vitals Telemetry Box */}
                <div className="grid grid-cols-4 gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-200/80 text-xs text-center font-mono">
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">BP (mmHg)</span>
                    <strong className="text-slate-900 text-xs">124 / 82</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">Heart Rate</span>
                    <strong className="text-emerald-700 text-xs">72 bpm</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">SpO₂</span>
                    <strong className="text-emerald-700 text-xs">98% RA</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">Temp</span>
                    <strong className="text-slate-900 text-xs">98.6 °F</strong>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-100">
                  <span className="text-amber-700 font-semibold flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" /> Medication Due: 10:00 AM (Ticagrelor 90mg)
                  </span>

                  <div className="flex items-center gap-1.5">
                    {onSelectPatient && (
                      <button
                        onClick={() => onSelectPatient(SEED_PATIENTS[0])}
                        className="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[11px] font-semibold"
                      >
                        Open Chart
                      </button>
                    )}
                    <button
                      onClick={() => alert('Opening Vitals Entry')}
                      className="px-2.5 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded text-[11px] font-semibold"
                    >
                      Record Vitals
                    </button>
                    <button
                      onClick={() => alert('Paging Dr. Marcus Vance')}
                      className="px-2 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 rounded text-[11px] font-semibold flex items-center gap-1"
                    >
                      <PhoneCall className="w-3 h-3" /> Page MD
                    </button>
                  </div>
                </div>
              </div>

              {/* Patient 2: Elena Rostova */}
              <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <strong className="text-sm font-bold text-slate-900">Elena Rostova</strong>
                      <span className="font-mono text-xs px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">MRN-449182</span>
                      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
                        ROOM 205 • Bed 212-A
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">
                      41y Female • Asthma Exacerbation • Attending: Dr. Gregory House, MD
                    </p>
                  </div>
                  <StatusBadge status="Monitoring" size="sm" />
                </div>

                {/* Vitals Telemetry Box */}
                <div className="grid grid-cols-4 gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-200/80 text-xs text-center font-mono">
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">BP (mmHg)</span>
                    <strong className="text-slate-900 text-xs">118 / 74</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">Heart Rate</span>
                    <strong className="text-slate-900 text-xs">82 bpm</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">SpO₂</span>
                    <strong className="text-amber-700 text-xs">95% (2L NC)</strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-sans">Temp</span>
                    <strong className="text-slate-900 text-xs">99.1 °F</strong>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-100">
                  <span className="text-slate-600 font-semibold flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" /> Next Respiratory Assessment: 11:30 AM
                  </span>

                  <div className="flex items-center gap-1.5">
                    {onSelectPatient && (
                      <button
                        onClick={() => onSelectPatient(SEED_PATIENTS[1])}
                        className="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[11px] font-semibold"
                      >
                        Open Chart
                      </button>
                    )}
                    <button
                      onClick={() => alert('Opening Vitals Entry')}
                      className="px-2.5 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded text-[11px] font-semibold"
                    >
                      Record Vitals
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Col: Quick Vital Logger & SBAR Shift Tasks */}
          <div className="space-y-6">
            
            {/* Quick Bedside Vital Logger Form */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <Activity className="w-4 h-4 text-teal-600" /> Log Bedside Vitals
                </h3>
                <span className="text-[11px] font-mono text-slate-400">Flow-sheet Direct</span>
              </div>

              <form onSubmit={handleLogVital} className="space-y-3 text-xs">
                <div>
                  <label className="text-slate-600 font-medium block mb-1">Patient</label>
                  <select
                    value={newPatient}
                    onChange={(e) => setNewPatient(e.target.value)}
                    className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                  >
                    <option value="John Anderson">John Anderson (Room 204)</option>
                    <option value="Elena Rostova">Elena Rostova (Room 205)</option>
                    <option value="Marcus Brody">Marcus Brody (Room 206)</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-slate-600 font-medium block mb-1">BP (mmHg)</label>
                    <input
                      type="text"
                      value={newBp}
                      onChange={(e) => setNewBp(e.target.value)}
                      className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-mono text-xs"
                    />
                  </div>
                  <div>
                    <label className="text-slate-600 font-medium block mb-1">Pulse (bpm)</label>
                    <input
                      type="text"
                      value={newHr}
                      onChange={(e) => setNewHr(e.target.value)}
                      className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-mono text-xs"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-slate-600 font-medium block mb-1">SpO₂ (%)</label>
                    <input
                      type="text"
                      value={newSpo2}
                      onChange={(e) => setNewSpo2(e.target.value)}
                      className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-mono text-xs"
                    />
                  </div>
                  <div>
                    <label className="text-slate-600 font-medium block mb-1">Temp (°F)</label>
                    <input
                      type="text"
                      value={newTemp}
                      onChange={(e) => setNewTemp(e.target.value)}
                      className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-mono text-xs"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg font-bold shadow-2xs mt-2"
                >
                  Record to Bedside Flow-sheet
                </button>
              </form>
            </div>

            {/* SBAR Shift Handover Checklist */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <CheckSquare className="w-4 h-4 text-blue-600" /> SBAR Handover Checklist
                </h3>
                <span className="text-[11px] font-mono text-emerald-700 font-semibold">
                  {tasks.filter(t => t.done).length} / {tasks.length} Done
                </span>
              </div>

              <div className="space-y-2 text-xs">
                {tasks.map(t => (
                  <div
                    key={t.id}
                    onClick={() => toggleTask(t.id)}
                    className="p-2.5 rounded-lg border border-slate-200 bg-slate-50/50 hover:bg-slate-100 cursor-pointer flex items-center gap-2.5 transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={t.done}
                      onChange={() => {}}
                      className="rounded text-teal-600 focus:ring-teal-500 w-4 h-4"
                    />
                    <div className="min-w-0 flex-1">
                      <span className={`block font-semibold ${t.done ? 'line-through text-slate-400' : 'text-slate-900'}`}>
                        {t.task}
                      </span>
                      <span className="text-[10px] text-slate-500">{t.patient} • {t.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW: MEDICATION ADMINISTRATION (5-RIGHTS) */}
      {(activeNav === 'meds' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">5-Rights Medication Administration Station (BCMA)</h3>
              <p className="text-xs text-slate-500">Right Patient • Right Drug • Right Dose • Right Route • Right Time</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-1 rounded border border-emerald-200 font-bold">
              Barcode Verified
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Patient & Bed</th>
                  <th className="p-2.5">Medication & Dose</th>
                  <th className="p-2.5">Scheduled Time</th>
                  <th className="p-2.5">Administration Status</th>
                  <th className="p-2.5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {medsList.map((m) => (
                  <tr key={m.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{m.patient}</strong>
                      <span className="text-slate-500 text-[11px]">{m.bed}</span>
                    </td>
                    <td className="p-2.5 font-bold text-slate-800 font-mono">{m.drug}</td>
                    <td className="p-2.5 font-medium text-slate-700">{m.schedule}</td>
                    <td className="p-2.5">
                      <StatusBadge status={m.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      {!m.given ? (
                        <button
                          onClick={() => handleAdministerMed(m.id)}
                          className="px-3 py-1 bg-teal-600 hover:bg-teal-500 text-white rounded text-[11px] font-bold shadow-2xs transition-colors"
                        >
                          Verify & Give
                        </button>
                      ) : (
                        <span className="text-emerald-700 text-[11px] font-semibold flex items-center justify-end gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Given
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: NURSING STATION CONSOLE (TELEMETRY & MEWS) */}
      {activeNav === 'console' && (
        <NursingStationConsole
          onOpenDoc={onOpenDoc}
          onOpenRAG={onOpenRAG}
          onSelectPatient={onSelectPatient}
        />
      )}
    </div>
  );
};
