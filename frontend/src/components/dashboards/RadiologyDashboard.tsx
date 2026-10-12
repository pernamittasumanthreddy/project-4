'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Scan, ShieldCheck, Activity, Eye, FileText, 
  Clock, AlertCircle, Sparkles, CheckCircle2, 
  Search, Plus, Check, ArrowUpRight, Share2 
} from 'lucide-react';
import { SAMPLE_RADIOLOGY_SCANS } from '@/lib/data/mockDatabase';

interface RadiologyDashboardProps {
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const RadiologyDashboard: React.FC<RadiologyDashboardProps> = ({ 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [scans, setScans] = useState(SAMPLE_RADIOLOGY_SCANS);
  const [modalityFilter, setModalityFilter] = useState<'ALL' | 'CT' | 'MRI' | 'X-Ray' | 'Ultrasound'>('ALL');
  const [viewingStudy, setViewingStudy] = useState<any | null>(null);

  const handleFinalizeReport = (scanId: string) => {
    setScans(prev => prev.map(s => s.id === scanId ? { ...s, status: 'Report Verified' } : s));
    alert(`Radiologist diagnostic report for ${scanId} electronically signed and posted to PACS.`);
  };

  const filteredScans = scans.filter(s => {
    if (modalityFilter === 'ALL') return true;
    return s.modality === modalityFilter;
  });

  return (
    <div className="space-y-6 text-[#1E293B] dark:text-[#E2E8F0]">
      {/* Standard Compact Page Header (Section 3 Specification) */}
      <div className="bg-white dark:bg-[#111827] rounded-xl p-5 border border-[#DCE4EA] dark:border-[#293548] shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-[#0F8B8D] border border-teal-200 flex items-center gap-1">
              <Scan className="w-3.5 h-3.5" /> Department of Diagnostic Imaging & PACS
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Section Chief • Dr. Jonathan Blake, MD</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Diagnostic Imaging & PACS</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Cross-sectional CT/MRI modalities, DICOM telemetry, and rapid trauma reporting.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'scans', 'safety'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'scans' ? 'Modality Queue' : 'Contrast & Safety'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Contrast & Protocols RAG
          </button>
        </div>
      </div>

      {/* Operational KPI Live Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <StatCard
          title="Daily Scans"
          value="38 Studies"
          subtitle="Modality schedule"
          icon={Scan}
          variant="purple"
        />
        <StatCard
          title="Pending Reports"
          value={`${scans.filter(s => s.status !== 'Report Verified').length} Unread`}
          subtitle="Awaiting sign-off"
          icon={Clock}
          variant="amber"
        />
        <StatCard
          title="CT Scans (128-Slice)"
          value="14 Studies"
          subtitle="Trauma & Angiography"
          icon={Activity}
          variant="blue"
        />
        <StatCard
          title="MRI (3.0T High-Res)"
          value="8 Studies"
          subtitle="Neuro & Musculoskeletal"
          icon={ShieldCheck}
          variant="teal"
        />
        <StatCard
          title="Critical Findings"
          value="1 Acute Finding"
          subtitle="Aortic dissection ruled out"
          icon={AlertCircle}
          variant="rose"
        />
      </div>

      {/* DICOM Study Preview Modal */}
      {viewingStudy && (
        <div className="p-4 bg-slate-900 text-white rounded-xl border border-slate-700 shadow-xl space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div>
              <strong className="text-sm font-bold text-white block">DICOM PACS Viewer Simulation</strong>
              <span className="text-xs text-slate-400">{viewingStudy.studyType} • {viewingStudy.patientName}</span>
            </div>
            <button onClick={() => setViewingStudy(null)} className="p-1 text-slate-400 hover:text-white">✕</button>
          </div>
          <div className="bg-black rounded-lg p-6 text-center border border-slate-800 font-mono text-xs text-slate-400 min-h-36 flex flex-col items-center justify-center">
            <Scan className="w-12 h-12 text-blue-500 mb-2 animate-pulse" />
            <p className="text-white font-bold">DICOM Series: 120 Axials (Slice Thickness: 1.0mm)</p>
            <p className="text-slate-500 mt-1">Window: Lung (-600/1500) | Mediastinal (40/400) | Bone (300/1500)</p>
            <p className="text-emerald-400 text-[11px] mt-2">Zero artifact • Diagnostic Quality Verified</p>
          </div>
          <div className="flex justify-between items-center text-xs">
            <span className="text-slate-400">Radiologist: Dr. Jonathan Blake, MD</span>
            <button
              onClick={() => {
                handleFinalizeReport(viewingStudy.id);
                setViewingStudy(null);
              }}
              className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold shadow-2xs"
            >
              Sign & Finalize Report
            </button>
          </div>
        </div>
      )}

      {/* VIEW: MODALITY WORKLIST */}
      {(activeNav === 'dashboard' || activeNav === 'scans') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Radiology PACS Modality Worklist</h3>
              <p className="text-xs text-slate-500">Cross-modality queue, radiologist interpretation, and DICOM accession tracking</p>
            </div>

            <div className="flex items-center gap-1.5 flex-wrap">
              {(['ALL', 'CT', 'MRI', 'X-Ray', 'Ultrasound'] as const).map(mod => (
                <button
                  key={mod}
                  onClick={() => setModalityFilter(mod)}
                  className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
                    modalityFilter === mod ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {mod}
                </button>
              ))}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Study ID</th>
                  <th className="p-2.5">Patient & MRN</th>
                  <th className="p-2.5">Examination / Study</th>
                  <th className="p-2.5">Modality</th>
                  <th className="p-2.5">Priority</th>
                  <th className="p-2.5">Report Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredScans.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5 font-mono text-slate-500 font-bold">{s.id}</td>
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{s.patientName}</strong>
                      <span className="font-mono text-[10px] text-slate-400">{s.patientId}</span>
                    </td>
                    <td className="p-2.5 font-semibold text-slate-800">{s.anatomy} ({s.modality})</td>
                    <td className="p-2.5">
                      <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-mono font-bold text-[10px] border border-blue-200">
                        {s.modality}
                      </span>
                    </td>
                    <td className="p-2.5">
                      <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                        s.priority === 'Stat (Emergency)' ? 'bg-rose-100 text-rose-800 border border-rose-200' : 'bg-slate-100 text-slate-700'
                      }`}>
                        {s.priority}
                      </span>
                    </td>
                    <td className="p-2.5">
                      <StatusBadge status={s.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => setViewingStudy(s)}
                          className="px-2.5 py-1 bg-violet-50 hover:bg-violet-100 text-violet-700 border border-violet-200 rounded text-[11px] font-semibold flex items-center gap-1"
                        >
                          <Eye className="w-3 h-3" /> View DICOM
                        </button>
                        {s.status !== 'Report Verified' && (
                          <button
                            onClick={() => handleFinalizeReport(s.id)}
                            className="px-2.5 py-1 bg-violet-700 hover:bg-violet-600 text-white rounded text-[11px] font-bold shadow-2xs"
                          >
                            Sign Report
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: CONTRAST SAFETY & RADIATION PROTOCOLS */}
      {activeNav === 'safety' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5 text-slate-800">
                <ShieldCheck className="w-4 h-4 text-emerald-600" /> Contrast Nephropathy & Radiation Safety Protocols (ALARA)
              </h3>
              <p className="text-xs text-slate-500">ACR Manual on Contrast Media & Radiation Protection Standards</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded border border-emerald-200 font-bold">
              ACR Guidelines Verified
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <strong className="text-slate-900 block font-bold text-xs">IV Iodinated Contrast (eGFR Screening)</strong>
              <p className="text-slate-600">eGFR &gt; 30 mL/min required before routine CT with Omnipaque / Visipaque. If eGFR &lt; 30, nephrology consult and pre-hydration protocol mandated.</p>
              <span className="text-[10px] text-emerald-700 font-bold">All active patients screened: Pass</span>
            </div>

            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <strong className="text-slate-900 block font-bold text-xs">ALARA Radiation Dose Monitoring</strong>
              <p className="text-slate-600">Dose-length product (DLP) and CTDIvol tracked on all Siemens SOMATOM scanners. Pediatric adaptive low-dose kVp algorithms strictly enforced.</p>
              <span className="text-[10px] text-emerald-700 font-bold">Monthly dose benchmark: 100% compliant</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
