'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Users, Calendar, Bed, UserCheck, CreditCard, 
  ShieldAlert, Activity, FileText, Building, 
  ArrowUpRight, ArrowDownRight, Clock, Plus, 
  CheckCircle2, Search, Upload, AlertCircle, Building2,
  LogOut,
} from 'lucide-react';
import { DEPARTMENTS, HOSPITAL_BEDS, INITIAL_AUDIT_LOGS } from '@/lib/data/mockDatabase';
import { HOSPITAL_DOCUMENTS } from '@/lib/data/hospitalDocuments';

interface HospitalAdminDashboardProps {
  onLogout?: () => void;
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const HospitalAdminDashboard: React.FC<HospitalAdminDashboardProps> = ({
  onLogout, 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [docSearch, setDocSearch] = useState('');
  const occupiedBeds = HOSPITAL_BEDS.filter(b => b.status === 'Occupied').length;
  const availableBeds = HOSPITAL_BEDS.filter(b => b.status === 'Available').length;

  const filteredDocs = HOSPITAL_DOCUMENTS.filter(d => 
    d.title.toLowerCase().includes(docSearch.toLowerCase()) ||
    d.category.toLowerCase().includes(docSearch.toLowerCase()) ||
    d.department.toLowerCase().includes(docSearch.toLowerCase()) ||
    d.id.toLowerCase().includes(docSearch.toLowerCase())
  );

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
              <Building2 className="w-3.5 h-3.5" /> Hospital Administration & Operations
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Chief Administrator • Dr. Arthur Pendelton</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Hospital Operations & Census</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Facility-wide bed census, admissions/discharges, and institutional clinical SOP governance.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'census', 'departments', 'documents', 'audit'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'census' ? 'Bed Census' : n}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Operations SOP RAG
          </button>
        </div>
      </div>

      {/* Operations KPI Row (Section 9) */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <StatCard
          title="Today's Appts"
          value="82 Visits"
          subtitle="Outpatient clinics"
          icon={Calendar}
          variant="indigo"
        />
        <StatCard
          title="Admissions"
          value="24 Inpatients"
          subtitle="14 via ED, 10 elective"
          icon={Users}
          variant="blue"
        />
        <StatCard
          title="Discharges"
          value="19 Cleared"
          subtitle="Medically stabilized"
          icon={CheckCircle2}
          variant="emerald"
        />
        <StatCard
          title="Bed Occupancy"
          value="78.4%"
          subtitle="328 Beds in use"
          icon={Bed}
          variant="teal"
        />
        <StatCard
          title="Staff Available"
          value="82 On Shift"
          subtitle="Rosters 100% covered"
          icon={UserCheck}
          variant="emerald"
        />
        <StatCard
          title="Approvals Pending"
          value="4 Requests"
          subtitle="Leave & equipment"
          icon={Clock}
          variant="amber"
        />
        <StatCard
          title="Emergency Cases"
          value="3 Active"
          subtitle="Trauma Bay load"
          icon={Activity}
          variant="rose"
        />
        <StatCard
          title="Hospital Alerts"
          value="Normal"
          subtitle="Zero incidents"
          icon={ShieldAlert}
          variant="purple"
        />
      </div>

      {/* VIEW: DEPARTMENT PERFORMANCE TABLE (Section 9) */}
      {(activeNav === 'dashboard' || activeNav === 'departments') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Department Performance & Workload Matrix</h3>
              <p className="text-xs text-slate-500">Live operational volume, physician coverage, outpatient throughput, and bed occupancy</p>
            </div>
            <span className="text-xs font-mono bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-200 font-semibold">
              18 Clinical Service Lines
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Department</th>
                  <th className="p-2.5">Inpatients</th>
                  <th className="p-2.5">Doctors on Duty</th>
                  <th className="p-2.5">Today&apos;s Appointments</th>
                  <th className="p-2.5">Bed Occupancy</th>
                  <th className="p-2.5">Operational Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {DEPARTMENTS.slice(0, 8).map((dept, idx) => {
                  const samplePatients = [42, 28, 38, 30, 45, 34, 50, 26][idx];
                  const sampleDocs = [8, 5, 6, 4, 7, 6, 8, 4][idx];
                  const sampleAppts = [16, 12, 22, 10, 18, 14, 15, 8][idx];
                  const occupancy = dept.bedCapacity > 0 ? Math.round((samplePatients / dept.bedCapacity) * 100) : 0;

                  return (
                    <tr key={idx} className="hover:bg-slate-50 transition-colors">
                      <td className="p-2.5">
                        <strong className="text-slate-900 block">{dept.name}</strong>
                        <span className="text-[11px] text-slate-500">{dept.head} • {dept.floor}</span>
                      </td>
                      <td className="p-2.5 font-mono font-bold text-slate-900">{samplePatients}</td>
                      <td className="p-2.5 text-slate-700 font-medium">{sampleDocs} Clinicians</td>
                      <td className="p-2.5 font-mono text-slate-800">{sampleAppts} Scheduled</td>
                      <td className="p-2.5">
                        {dept.bedCapacity > 0 ? (
                          <div className="flex items-center gap-2">
                            <span className="font-mono font-bold text-slate-900">{occupancy}%</span>
                            <div className="w-16 bg-slate-200 rounded-full h-1.5 overflow-hidden">
                              <div
                                className={`h-full rounded-full ${occupancy > 85 ? 'bg-rose-500' : 'bg-emerald-500'}`}
                                style={{ width: `${Math.min(occupancy, 100)}%` }}
                              />
                            </div>
                          </div>
                        ) : (
                          <span className="text-slate-400">Ambulatory</span>
                        )}
                      </td>
                      <td className="p-2.5">
                        <StatusBadge status={occupancy > 85 ? 'Near Capacity' : 'Optimal'} size="sm" />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: BED & WARD CENSUS */}
      {activeNav === 'census' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Ward & Bed Occupancy Census</h3>
              <p className="text-xs text-slate-500">Live telemetry and allocation tracking across intensive care, telemetry, and medical-surgical floors</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold">
                {availableBeds} Available Beds
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-800 border border-blue-200 font-bold">
                {occupiedBeds} Occupied
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-3">
            {HOSPITAL_BEDS.map((bed) => {
              const isOccupied = bed.status === 'Occupied';
              return (
                <div
                  key={bed.id}
                  className={`p-3 rounded-xl border transition-all text-xs ${
                    isOccupied ? 'bg-blue-50/50 border-blue-200' : 'bg-emerald-50/50 border-emerald-200'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <strong className="text-slate-900 font-mono">{bed.bedNumber}</strong>
                    <span className={`w-2 h-2 rounded-full ${isOccupied ? 'bg-blue-600' : 'bg-emerald-500'}`} />
                  </div>
                  <span className="text-[11px] text-slate-500 block truncate">{bed.ward}</span>
                  <span className={`text-[10px] font-bold block mt-1 ${isOccupied ? 'text-blue-700' : 'text-emerald-700'}`}>
                    {bed.status}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* VIEW: HOSPITAL DOCUMENTS REPOSITORY */}
      {activeNav === 'documents' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Knowledge Base & Approved SOP Repository</h3>
              <p className="text-xs text-slate-500">Search approved clinical guidelines, infection control protocols, and administrative policies</p>
            </div>

            <div className="relative w-64">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search documents by code, title..."
                value={docSearch}
                onChange={(e) => setDocSearch(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {filteredDocs.map((doc) => (
              <div
                key={doc.id}
                onClick={() => onOpenDoc(doc)}
                className="p-4 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-slate-50 cursor-pointer transition-all space-y-1.5"
              >
                <div className="flex items-start justify-between">
                  <strong className="text-xs font-bold text-slate-900 block">{doc.title}</strong>
                  <span className="font-mono text-[10px] text-slate-400">{doc.id}</span>
                </div>
                <p className="text-[11px] text-slate-600 line-clamp-2">{doc.content}</p>
                <div className="flex items-center justify-between pt-1 text-[10px] text-slate-500">
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

      {/* VIEW: AUDIT TRAIL */}
      {activeNav === 'audit' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Operational Events & HIPAA Activity Log</h3>
              <p className="text-xs text-slate-500">Continuous auditing of patient admissions, discharges, medication orders, and staff logins</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded border border-emerald-200 font-bold">
              Irrevocable Logging Active
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Log ID</th>
                  <th className="p-2.5">Timestamp</th>
                  <th className="p-2.5">User</th>
                  <th className="p-2.5">Role</th>
                  <th className="p-2.5">Action</th>
                  <th className="p-2.5">Resource</th>
                  <th className="p-2.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-[11px]">
                {INITIAL_AUDIT_LOGS.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50">
                    <td className="p-2.5 font-bold text-slate-700">{log.id}</td>
                    <td className="p-2.5 text-slate-500">{log.timestamp}</td>
                    <td className="p-2.5 text-slate-800">{log.userName}</td>
                    <td className="p-2.5 text-slate-600">{log.role}</td>
                    <td className="p-2.5 font-sans font-medium text-slate-900">{log.action}</td>
                    <td className="p-2.5 text-blue-700">{log.resourceType}: {log.resourceId}</td>
                    <td className="p-2.5"><span className="text-emerald-700 font-bold">SUCCESS</span></td>
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
