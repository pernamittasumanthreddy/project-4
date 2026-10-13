'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Building2, Users, Bed, Activity, ShieldCheck, 
  Clock, FileText, CheckCircle2, ChevronRight, AlertTriangle, 
  Wrench, Check, Plus, RefreshCw, Sparkles,
  LogOut,
} from 'lucide-react';

interface DepartmentManagerDashboardProps {
  onLogout?: () => void;
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

interface StaffingUnit {
  id: string;
  unit: string;
  census: number;
  capacity: number;
  nursesOnDuty: number;
  targetRatio: string;
  actualRatio: string;
  acuityLevel: 'High' | 'Moderate' | 'Stable';
  status: 'OPTIMAL' | 'NEAR_THRESHOLD' | 'STAFFING_DEFICIT';
}

interface BioMedDevice {
  id: string;
  name: string;
  serial: string;
  location: string;
  lastQC: string;
  nextPM: string;
  status: 'OPERATIONAL' | 'NEEDS_QC' | 'MAINTENANCE_REQUIRED';
}

export const DepartmentManagerDashboard: React.FC<DepartmentManagerDashboardProps> = ({
  onLogout, 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [units, setUnits] = useState<StaffingUnit[]>([
    { id: 'U-3A', unit: 'Acute Inpatient Unit 3A', census: 14, capacity: 16, nursesOnDuty: 4, targetRatio: '1:4', actualRatio: '1:3.5', acuityLevel: 'High', status: 'OPTIMAL' },
    { id: 'U-3B', unit: 'Step-Down Telemetry 3B', census: 20, capacity: 22, nursesOnDuty: 5, targetRatio: '1:4', actualRatio: '1:4.0', acuityLevel: 'Moderate', status: 'OPTIMAL' },
    { id: 'U-3C', unit: 'General Medical Floor 3C', census: 18, capacity: 20, nursesOnDuty: 3, targetRatio: '1:5', actualRatio: '1:6.0', acuityLevel: 'Moderate', status: 'STAFFING_DEFICIT' },
    { id: 'U-3D', unit: 'Rapid Observation Unit 3D', census: 8, capacity: 10, nursesOnDuty: 2, targetRatio: '1:4', actualRatio: '1:4.0', acuityLevel: 'Stable', status: 'OPTIMAL' },
  ]);

  const [equipmentList, setEquipmentList] = useState<BioMedDevice[]>([
    { id: 'EQ-801', name: 'Zoll R-Series Crash Cart Defibrillator', serial: 'ZL-90241-DEF', location: 'Unit 3A Hallway Station', lastQC: 'Today 06:30 (Shift Start)', nextPM: 'Nov 2026', status: 'OPERATIONAL' },
    { id: 'EQ-802', name: 'Telemetry Cardiac Transmitters (24 Units)', serial: 'PHIL-TX-BATCH-03', location: 'Telemetry Central Desk', lastQC: 'Yesterday 18:00', nextPM: 'Dec 2026', status: 'OPERATIONAL' },
    { id: 'EQ-803', name: 'GE Healthcare Mechanical Ventilator Carescape', serial: 'GE-VENT-4410', location: 'Bed 302 Isolation Room', lastQC: 'Oct 02, 2026', nextPM: 'Jan 2027', status: 'OPERATIONAL' },
    { id: 'EQ-804', name: 'Alaris Smart IV Infusion Pump Bank (32 Modules)', serial: 'BD-ALAR-8015-BANK', location: 'Medication Clean Room', lastQC: 'Oct 01, 2026', nextPM: 'Oct 15, 2026', status: 'NEEDS_QC' },
    { id: 'EQ-805', name: 'Portable Suction Unit Laerdal Compact', serial: 'LAER-SUC-190', location: 'Unit 3C Emergency Bay', lastQC: 'Sep 28, 2026', nextPM: 'Nov 2026', status: 'OPERATIONAL' },
    { id: 'EQ-806', name: 'Sonosite Portable Vascular Ultrasound', serial: 'FUJI-SONO-204', location: 'Physician Workstation', lastQC: 'Sep 15, 2026', nextPM: 'Immediate', status: 'MAINTENANCE_REQUIRED' },
  ]);

  const handleDeployFloatNurse = (unitId: string) => {
    setUnits(prev => prev.map(u => {
      if (u.id === unitId) {
        const newNurses = u.nursesOnDuty + 1;
        const newRatio = `1:${(u.census / newNurses).toFixed(1)}`;
        return { ...u, nursesOnDuty: newNurses, actualRatio: newRatio, status: 'OPTIMAL' };
      }
      return u;
    }));
  };

  const handleVerifyQC = (eqId: string) => {
    setEquipmentList(prev => prev.map(eq => {
      if (eq.id === eqId) {
        return { ...eq, lastQC: 'Today (Verified by Chief)', status: 'OPERATIONAL' };
      }
      return eq;
    }));
  };

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
              <Building2 className="w-3.5 h-3.5" /> Department Operations & Staffing
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Department Chief • Dr. Gregory House, MD</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Department Operations & Staffing</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Nurse-to-patient acuity ratios, unit census tracking, and biomedical equipment maintenance protocols.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'staffing', 'equipment'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs font-bold' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'staffing' ? 'Staff Ratios' : 'Equipment QC'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Department SOP RAG
          </button>
        </div>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Department Bed Census"
          value="60 / 68"
          subtitle="88.2% Occupancy Rate"
          icon={Bed}
          variant="blue"
        />
        <StatCard
          title="Clinical Staff on Shift"
          value="19 Staff"
          subtitle="4 MDs, 14 RNs, 1 Lead Tech"
          icon={Users}
          variant="teal"
        />
        <StatCard
          title="Mean Length of Stay"
          value="3.4 Days"
          subtitle="Benchmark: < 4.0 Days"
          icon={Clock}
          variant="emerald"
        />
        <StatCard
          title="Quality Compliance"
          value="99.2%"
          subtitle="Zero CAUTI / CLABSI incidents"
          icon={ShieldCheck}
          variant="purple"
        />
      </div>

      {/* VIEW: STAFFING RATIOS & NURSE-TO-PATIENT BALANCE */}
      {(activeNav === 'staffing' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Shift Staffing Ratios & Nurse-to-Patient Safety Monitor</h3>
              <p className="text-xs text-slate-500">Title 22 & ANA Safe Staffing Standard compliance with real-time acuity tracking</p>
            </div>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
              Safe Patient Ratios Enforced
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {units.map((unit) => {
              const isDeficit = unit.status === 'STAFFING_DEFICIT';
              return (
                <div 
                  key={unit.id} 
                  className={`p-4 rounded-xl border transition-all ${
                    isDeficit 
                      ? 'bg-rose-50/50 border-rose-200' 
                      : 'bg-slate-50 border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-1.5">
                        <strong className="text-slate-900 text-sm">{unit.unit}</strong>
                        <span className="text-[10px] font-mono text-slate-400 font-bold">{unit.id}</span>
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">
                        {unit.census} Patients admitted ({unit.capacity} capacity) • Acuity: <strong className="text-slate-700">{unit.acuityLevel}</strong>
                      </p>
                    </div>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      isDeficit ? 'bg-rose-100 text-rose-800 border border-rose-200' : 'bg-emerald-100 text-emerald-800'
                    }`}>
                      {unit.status.replace('_', ' ')}
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-slate-200/60 text-xs">
                    <div>
                      <span className="text-[11px] text-slate-400 block">Nurses on Duty</span>
                      <strong className="text-slate-800 font-bold">{unit.nursesOnDuty} RNs</strong>
                    </div>
                    <div>
                      <span className="text-[11px] text-slate-400 block">Target Mandate</span>
                      <strong className="text-slate-800 font-mono">{unit.targetRatio}</strong>
                    </div>
                    <div>
                      <span className="text-[11px] text-slate-400 block">Actual Ratio</span>
                      <strong className={`font-mono font-bold ${isDeficit ? 'text-rose-600' : 'text-emerald-700'}`}>
                        {unit.actualRatio}
                      </strong>
                    </div>
                  </div>

                  {isDeficit && (
                    <div className="mt-3 pt-2 flex items-center justify-between">
                      <span className="text-[11px] text-rose-700 font-medium flex items-center gap-1">
                        <AlertTriangle className="w-3.5 h-3.5" /> High workload alert
                      </span>
                      <button
                        onClick={() => handleDeployFloatNurse(unit.id)}
                        className="px-3 py-1 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-bold shadow-2xs transition-all flex items-center gap-1"
                      >
                        <Plus className="w-3.5 h-3.5" /> Deploy Float RN
                      </button>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* VIEW: BIOMEDICAL EQUIPMENT */}
      {(activeNav === 'equipment' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Biomedical Equipment & Life-Support Readiness Console</h3>
              <p className="text-xs text-slate-500">Preventive maintenance logs, calibration certifications, and shift crash-cart readiness</p>
            </div>
            <span className="text-xs font-mono bg-slate-100 text-slate-700 px-2 py-1 rounded">
              FDA 21 CFR Part 820 & Joint Commission EC
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Device Name & Serial</th>
                  <th className="p-2.5">Location / Bed</th>
                  <th className="p-2.5">Last Daily QC Check</th>
                  <th className="p-2.5">Next PM Calibration</th>
                  <th className="p-2.5">Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {equipmentList.map((eq) => (
                  <tr key={eq.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{eq.name}</strong>
                      <span className="font-mono text-slate-400 text-[10px]">{eq.serial}</span>
                    </td>
                    <td className="p-2.5 font-medium text-slate-700">{eq.location}</td>
                    <td className="p-2.5 text-slate-600">{eq.lastQC}</td>
                    <td className="p-2.5 font-mono text-slate-700">{eq.nextPM}</td>
                    <td className="p-2.5">
                      <StatusBadge status={eq.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      {eq.status !== 'OPERATIONAL' ? (
                        <button
                          onClick={() => handleVerifyQC(eq.id)}
                          className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[11px] font-bold shadow-2xs flex items-center gap-1 ml-auto"
                        >
                          <Check className="w-3 h-3" /> Sign-Off
                        </button>
                      ) : (
                        <span className="text-emerald-700 text-[11px] font-semibold flex items-center justify-end gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Ready
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
    </div>
  );
};
