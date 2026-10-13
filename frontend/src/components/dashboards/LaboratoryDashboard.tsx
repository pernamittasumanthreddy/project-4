'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  FlaskConical, AlertTriangle, CheckCircle2, 
  Clock, Activity, Microscope, FileText, BellRing, ShieldCheck, 
  Search, Plus, Check, Flame,
  LogOut,
} from 'lucide-react';
import { SAMPLE_LAB_TESTS } from '@/lib/data/mockDatabase';

interface LaboratoryDashboardProps {
  onLogout?: () => void;
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const LaboratoryDashboard: React.FC<LaboratoryDashboardProps> = ({
  onLogout, 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [tests, setTests] = useState(SAMPLE_LAB_TESTS);
  const [filterPriority, setFilterPriority] = useState<'ALL' | 'STAT' | 'ROUTINE'>('ALL');

  const handleValidate = (testId: string) => {
    setTests(prev => prev.map(t => t.id === testId ? { ...t, status: 'Completed' } : t));
    alert(`Test ${testId} validated by Medical Technologist David Chen, MLS(ASCP)`);
  };

  const handleMarkCritical = (testId: string) => {
    setTests(prev => prev.map(t => t.id === testId ? { ...t, isCritical: true, status: 'Critical Review' } : t));
    alert(`Critical Panic Value flag placed on ${testId}. Physician telephone alert required within 15 minutes.`);
  };

  const filteredTests = tests.filter(t => {
    if (filterPriority === 'ALL') return true;
    if (filterPriority === 'STAT') return t.isCritical;
    return !t.isCritical;
  });

  return (
    <div className="space-y-6 text-[#1E293B] dark:text-[#E2E8F0]">
      {/* Standard Compact Page Header (Section 3 Specification) */}
      <div className="bg-white dark:bg-[#111827] rounded-xl p-5 border border-[#DCE4EA] dark:border-[#293548] shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
          {onLogout && (
            <button
              onClick={onLogout}
              className="px-3 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 dark:bg-rose-950/50 dark:hover:bg-rose-900/60 dark:text-rose-300 rounded-lg text-xs font-semibold border border-rose-200 dark:border-rose-800 flex items-center gap-1.5 transition-colors cursor-pointer shadow-2xs"
              title="Log Out of Workstation"
            >
              <LogOut className="w-3.5 h-3.5" /> Log Out
            </button>
          )}
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-[#0F8B8D] border border-teal-200 flex items-center gap-1">
              <Microscope className="w-3.5 h-3.5" /> CLIA & CAP Core Laboratory
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Lead Technologist • David Chen, MLS (ASCP)</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Pathology & Diagnostic Laboratory</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Specimen accessioning, automated analyzer telemetry, and critical panic value notifications.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'worklist', 'panic', 'qc'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'worklist' ? 'LIS Worklist' : n === 'panic' ? 'Panic Values' : 'Quality QC'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> LIS Protocols RAG
          </button>
        </div>
      </div>

      {/* Operational KPI Live Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <StatCard
          title="Samples Collected"
          value="142 Samples"
          subtitle="Whole blood, plasma, urine"
          icon={FlaskConical}
          variant="blue"
        />
        <StatCard
          title="Tests Pending"
          value={`${tests.filter(t => t.status !== 'Completed').length} Pending`}
          subtitle="Accessioning in progress"
          icon={Clock}
          variant="amber"
        />
        <StatCard
          title="Tests Processing"
          value="18 On Analyzer"
          subtitle="Beckman AU5800 running"
          icon={Activity}
          variant="teal"
        />
        <StatCard
          title="Completed Reports"
          value={`${tests.filter(t => t.status === 'Completed').length} Finalized`}
          subtitle="Transmitted to EMR"
          icon={CheckCircle2}
          variant="emerald"
        />
        <StatCard
          title="Critical Results"
          value={`${tests.filter(t => t.isCritical).length} Panic Values`}
          subtitle="Physician call logged"
          icon={AlertTriangle}
          variant="rose"
        />
      </div>

      {/* VIEW: LIS WORKLIST & TABLE */}
      {(activeNav === 'dashboard' || activeNav === 'worklist') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Laboratory Information System (LIS) Test Worklist</h3>
              <p className="text-xs text-slate-500">Specimen accessioning, barcode tracking, analyzer interface, and critical value reporting</p>
            </div>

            <div className="flex items-center gap-2">
              {(['ALL', 'STAT', 'ROUTINE'] as const).map(p => (
                <button
                  key={p}
                  onClick={() => setFilterPriority(p)}
                  className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                    filterPriority === p ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Accession ID</th>
                  <th className="p-2.5">Patient & MRN</th>
                  <th className="p-2.5">Test Panel</th>
                  <th className="p-2.5">Result Value</th>
                  <th className="p-2.5">Reference Range</th>
                  <th className="p-2.5">Priority</th>
                  <th className="p-2.5">Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredTests.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5 font-mono text-slate-500 font-bold">{t.id}</td>
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{t.patientName}</strong>
                      <span className="font-mono text-[10px] text-slate-400">{t.patientId}</span>
                    </td>
                    <td className="p-2.5 font-semibold text-slate-800">{t.testName}</td>
                    <td className="p-2.5 font-mono font-bold text-slate-900">
                      {t.results?.[0] ? `${t.results[0].parameter}: ${t.results[0].value} ${t.results[0].unit}` : <span className="text-slate-400 font-normal">Pending analyzer run</span>}
                    </td>
                    <td className="p-2.5 font-mono text-slate-500 text-[11px]">{t.results?.[0]?.referenceRange || 'Standard Normal'}</td>
                    <td className="p-2.5">
                      <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                        t.isCritical ? 'bg-rose-100 text-rose-800 border border-rose-200' : 'bg-slate-100 text-slate-700'
                      }`}>
                        {t.isCritical ? 'STAT' : 'ROUTINE'}
                      </span>
                    </td>
                    <td className="p-2.5">
                      <StatusBadge status={t.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        {t.status !== 'Completed' && (
                          <button
                            onClick={() => handleValidate(t.id)}
                            className="px-2.5 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-[11px] font-bold shadow-2xs"
                          >
                            Validate
                          </button>
                        )}
                        <button
                          onClick={() => handleMarkCritical(t.id)}
                          className="px-2 py-1 bg-white hover:bg-rose-50 text-rose-700 border border-rose-200 rounded text-[11px] font-semibold"
                        >
                          Mark Panic
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: PANIC VALUES LOG */}
      {activeNav === 'panic' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5 text-rose-700">
                <Flame className="w-4 h-4 text-rose-600" /> Critical Lab Panic Values Telephone Notification Log
              </h3>
              <p className="text-xs text-slate-500">Joint Commission National Patient Safety Goal (NPSG.02.03.01) Read-Back Documentation</p>
            </div>
            <span className="text-xs font-mono bg-rose-50 text-rose-800 px-2 py-0.5 rounded border border-rose-200 font-bold">
              100% Read-Back Compliance
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3.5 rounded-xl border border-rose-200 bg-rose-50/50 flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <strong className="text-slate-900 font-bold text-xs">Troponin I: 0.18 ng/mL (Reference &lt;0.04)</strong>
                  <span className="px-1.5 py-0.2 rounded bg-rose-600 text-white font-mono text-[10px] font-bold">PANIC HIGH</span>
                </div>
                <p className="text-slate-600 mt-1">
                  Patient: <strong>John Anderson (MRN-884920)</strong> • Telephoned to: <strong>Dr. Marcus Vance, MD</strong> • Read-back confirmed at 07:12 AM
                </p>
              </div>
              <span className="text-emerald-700 font-bold flex items-center gap-1 text-[11px] shrink-0">
                <CheckCircle2 className="w-3.5 h-3.5" /> Documented in EMR
              </span>
            </div>
          </div>
        </div>
      )}

      {/* VIEW: ANALYZER QUALITY CONTROL (QC) */}
      {activeNav === 'qc' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5 text-slate-800">
                <ShieldCheck className="w-4 h-4 text-emerald-600" /> Daily Analyzer Quality Control (Levey-Jennings)
              </h3>
              <p className="text-xs text-slate-500">Westgard multi-rule automated verification for CLIA 88 and CAP compliance</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded border border-emerald-200 font-bold">
              All Analyzers In-Control
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <strong className="text-slate-900 block font-bold text-xs">Beckman AU5800 Chemistry #1</strong>
              <span className="text-emerald-700 font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> 2-Level QC Passed (06:00 AM)
              </span>
              <p className="text-[11px] text-slate-500">Electrolytes, Renal, Liver, Cardiac enzymes verified.</p>
            </div>

            <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <strong className="text-slate-900 block font-bold text-xs">Sysmex XN-9000 Hematology</strong>
              <span className="text-emerald-700 font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> 3-Level QC Passed (06:15 AM)
              </span>
              <p className="text-[11px] text-slate-500">CBC, Differential, Reticulocytes calibrated within 1 SD.</p>
            </div>

            <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <strong className="text-slate-900 block font-bold text-xs">Stago STA-R Coagulation</strong>
              <span className="text-emerald-700 font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> Normal & Abnormal Controls Passed
              </span>
              <p className="text-[11px] text-slate-500">PT/INR and PTT reference standards verified.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
