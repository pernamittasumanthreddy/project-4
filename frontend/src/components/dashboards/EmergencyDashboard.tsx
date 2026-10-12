'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  ShieldAlert, Activity, Heart, Clock, AlertTriangle, 
  Bed, UserCheck, Flame, FileText, PhoneCall, CheckCircle2, 
  Ambulance, Stethoscope, ChevronRight 
} from 'lucide-react';
import { SAMPLE_EMERGENCY_CASES, SEED_PATIENTS } from '@/lib/data/mockDatabase';
import { Patient } from '@/lib/types/hms';

interface EmergencyDashboardProps {
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
  onSelectPatient?: (patient: Patient) => void;
}

export const EmergencyDashboard: React.FC<EmergencyDashboardProps> = ({ 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav,
  onSelectPatient
}) => {
  const [cases, setCases] = useState(SAMPLE_EMERGENCY_CASES);
  const [triageFilter, setTriageFilter] = useState<'ALL' | 'ESI-1' | 'ESI-2' | 'ESI-3' | 'ESI-4' | 'ESI-5'>('ALL');

  const filteredCases = cases.filter(c => {
    if (triageFilter === 'ALL') return true;
    return c.triageLevel.startsWith(triageFilter);
  });

  return (
    <div className="space-y-6 text-slate-800">
      {/* Top Operational Urgent Banner */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 flex items-center gap-1">
              <AlertTriangle className="w-3.5 h-3.5 text-rose-600" /> EMERGENCY DEPARTMENT — Central Trauma Command
            </span>
            <span className="text-xs text-slate-500">Level 1 Trauma Center • Ground Floor Trauma Bay</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-slate-900">Dr. Robert Thorne, MD, FACEP (ED Director)</h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Active ED Load: <strong className="text-rose-700">3 Critical Patients</strong> • 2 Incoming Ambulances • 4 Resuscitation Beds Available • Active view: <span className="font-semibold text-rose-700 capitalize">{activeNav}</span>
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
              {(['dashboard', 'queue', 'codeblue'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all ${
                    activeNav === n ? 'bg-white text-rose-700 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'queue' ? 'ESI Queue' : 'Code Blue'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={() => alert('Code Blue overhead broadcast initiated on Extension 4444! Crash Cart 1 & Trauma Bay Activated.')}
            className="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors"
          >
            <PhoneCall className="w-3.5 h-3.5" /> Code Blue (Ext 4444)
          </button>

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors"
          >
            <FileText className="w-3.5 h-3.5" /> Trauma SOP RAG
          </button>
        </div>
      </div>

      {/* Operational KPI Live Stats */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
        <StatCard
          title="Critical Patients"
          value="3 Critical"
          subtitle="ESI-1 Resus Bay"
          icon={AlertTriangle}
          variant="rose"
        />
        <StatCard
          title="Incoming Ambulances"
          value="2 Inbound"
          subtitle="ETA: 4 & 9 mins"
          icon={Ambulance}
          variant="amber"
        />
        <StatCard
          title="Available Beds"
          value="4 / 16 Beds"
          subtitle="Trauma Bay capacity"
          icon={Bed}
          variant="blue"
        />
        <StatCard
          title="Doctors On Duty"
          value="4 ED MDs"
          subtitle="Attending + Residents"
          icon={Stethoscope}
          variant="teal"
        />
        <StatCard
          title="Nurses On Shift"
          value="8 RNs"
          subtitle="Triage & Bedside"
          icon={Heart}
          variant="emerald"
        />
        <StatCard
          title="Trauma Rooms"
          value="2 Ready"
          subtitle="Bays 1 & 3 Cleared"
          icon={Activity}
          variant="slate"
        />
      </div>

      {/* VIEW: ESI QUEUE & DASHBOARD */}
      {(activeNav === 'dashboard' || activeNav === 'queue') && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Emergency Severity Index (ESI) Patient Queue</h3>
              <p className="text-xs text-slate-500">Live triage priority: RED (ESI-1/2 Resus & Emergent) • AMBER (ESI-3 Urgent) • GREEN (ESI-4/5 Stable)</p>
            </div>

            <div className="flex items-center gap-1.5 flex-wrap">
              {(['ALL', 'ESI-1', 'ESI-2', 'ESI-3', 'ESI-4', 'ESI-5'] as const).map(lvl => (
                <button
                  key={lvl}
                  onClick={() => setTriageFilter(lvl)}
                  className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                    triageFilter === lvl
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {lvl}
                </button>
              ))}
            </div>
          </div>

          {/* Emergency Patient Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredCases.map((ec) => {
              const isEsi1or2 = ec.triageLevel.startsWith('ESI-1') || ec.triageLevel.startsWith('ESI-2');
              const isEsi3 = ec.triageLevel.startsWith('ESI-3');
              
              return (
                <div 
                  key={ec.id} 
                  className={`p-4 rounded-xl border transition-all ${
                    isEsi1or2 
                      ? 'bg-rose-50/50 border-rose-200 hover:border-rose-300' 
                      : isEsi3 
                      ? 'bg-amber-50/40 border-amber-200 hover:border-amber-300' 
                      : 'bg-white border-slate-200 hover:border-slate-300'
                  } shadow-2xs flex flex-col justify-between`}
                >
                  <div>
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <strong className="text-sm font-bold text-slate-900">{ec.patientName}</strong>
                          <span className="text-xs text-slate-500">{ec.age}y</span>
                        </div>
                        <span className="text-[11px] text-slate-500 block mt-0.5">
                          Arrival: <strong className="font-mono text-slate-700">{ec.arrivalTime}</strong> • Bay: <strong className="text-slate-800">{ec.assignedBay || 'Triage'}</strong>
                        </span>
                      </div>

                      <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                        isEsi1or2 ? 'bg-rose-600 text-white' :
                        isEsi3 ? 'bg-amber-500 text-white' :
                        'bg-emerald-600 text-white'
                      }`}>
                        {ec.triageLevel}
                      </span>
                    </div>

                    <div className="mt-3 p-2.5 rounded-lg bg-white border border-slate-200/80 text-xs space-y-1">
                      <div className="flex justify-between">
                        <span className="text-slate-500">Chief Complaint:</span>
                        <strong className="text-slate-900">{ec.chiefComplaint}</strong>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Bedside Vitals:</span>
                        <span className="font-mono font-medium text-slate-800">BP 90/60 • HR 118 • SpO₂ 94%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-500">Attending:</span>
                        <span className="font-medium text-slate-700">{ec.assignedDoctor || 'Dr. Robert Thorne'}</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-3 pt-2.5 border-t border-slate-200/80 flex items-center justify-between text-xs">
                    <StatusBadge status={ec.status} size="sm" />
                    <button
                      onClick={() => {
                        const pt = SEED_PATIENTS.find(p => p.firstName === ec.patientName.split(' ')[0]) || SEED_PATIENTS[0];
                        if (onSelectPatient) onSelectPatient(pt);
                      }}
                      className="px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[11px] font-semibold"
                    >
                      Open Trauma EMR
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* VIEW: CODE BLUE PROTOCOL */}
      {activeNav === 'codeblue' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5 text-rose-700">
                <Heart className="w-4 h-4 text-rose-600" /> ACLS Cardiac Arrest & Code Blue Protocol
              </h3>
              <p className="text-xs text-slate-500">American Heart Association (AHA) 2026 Resuscitation Algorithm</p>
            </div>
            <span className="text-xs font-mono bg-rose-50 text-rose-700 px-2 py-1 rounded border border-rose-200 font-bold">
              Immediate Life Support
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-4 rounded-xl border border-rose-200 bg-rose-50/50 space-y-2">
              <strong className="text-rose-900 block font-bold text-xs">Phase 1: Immediate Recognition</strong>
              <ul className="list-disc pl-4 space-y-1 text-slate-700 text-[11px]">
                <li>Confirm unresponsiveness & absent pulse (&lt; 10 sec)</li>
                <li>Activate Code Blue broadcast (Ext 4444)</li>
                <li>Initiate high-quality CPR (100–120/min, 2 inches depth)</li>
                <li>Attach defibrillator pads (Anterior-lateral)</li>
              </ul>
            </div>

            <div className="p-4 rounded-xl border border-amber-200 bg-amber-50/50 space-y-2">
              <strong className="text-amber-900 block font-bold text-xs">Phase 2: Rhythm Analysis</strong>
              <ul className="list-disc pl-4 space-y-1 text-slate-700 text-[11px]">
                <li><strong>Shockable:</strong> VF / Pulseless VT → Defibrillate 200J Biphasic</li>
                <li><strong>Non-Shockable:</strong> PEA / Asystole → Resume CPR immediately</li>
                <li>Establish IV/IO vascular access</li>
                <li>Epinephrine 1mg IV/IO q3–5 minutes</li>
              </ul>
            </div>

            <div className="p-4 rounded-xl border border-blue-200 bg-blue-50/50 space-y-2">
              <strong className="text-blue-900 block font-bold text-xs">Phase 3: Advanced Airway & H&apos;s/T&apos;s</strong>
              <ul className="list-disc pl-4 space-y-1 text-slate-700 text-[11px]">
                <li>Endotracheal intubation with waveform capnography</li>
                <li>Evaluate reversible causes (Hypovolemia, Hypoxia, Hydrogen ion, Tension pneumo)</li>
                <li>Amiodarone 300mg IV push for refractory VF/pVT</li>
                <li>Post-cardiac arrest targeted temperature management</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
