'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Users, UserCheck, Calendar, Award, ShieldCheck, 
  Clock, FileText, CheckCircle2, AlertCircle, Search, 
  Filter, Plus, RefreshCw, Check, X, FileBadge, Building2,
  LogOut,
} from 'lucide-react';

interface HRDashboardProps {
  onLogout?: () => void;
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

interface StaffMember {
  id: string;
  name: string;
  role: string;
  dept: string;
  shift: string;
  licenseNumber: string;
  licenseStatus: string;
  aclsStatus: string;
  attendance: string;
  lastVerified: string;
}

interface LeaveRequest {
  id: string;
  staffName: string;
  role: string;
  dept: string;
  type: string;
  dates: string;
  backfill: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
}

export const HRDashboard: React.FC<HRDashboardProps> = ({
  onLogout, 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [deptFilter, setDeptFilter] = useState('ALL');
  const [verifiedIds, setVerifiedIds] = useState<Record<string, boolean>>({});

  const [staffList, setStaffList] = useState<StaffMember[]>([
    { id: 'ST-101', name: 'Dr. Marcus Vance, MD', role: 'Attending Cardiologist', dept: 'Cardiology', shift: 'Day (07:00 - 19:00)', licenseNumber: 'MD-94021-CA', licenseStatus: 'Active (Expires Nov 2028)', aclsStatus: 'ACLS Certified', attendance: 'Present', lastVerified: '2026-09-15' },
    { id: 'ST-102', name: 'Sarah Jenkins, RN, BSN', role: 'Staff Registered Nurse', dept: 'Cardiology', shift: 'Day (07:00 - 19:00)', licenseNumber: 'RN-88102-CA', licenseStatus: 'Active (Expires Mar 2027)', aclsStatus: 'ACLS & BLS Valid', attendance: 'Present', lastVerified: '2026-08-10' },
    { id: 'ST-103', name: 'Dr. Robert Thorne, MD', role: 'Emergency Attending', dept: 'Emergency', shift: 'Night (19:00 - 07:00)', licenseNumber: 'MD-55419-CA', licenseStatus: 'Active (Expires Jul 2028)', aclsStatus: 'ATLS & ACLS Valid', attendance: 'On-Call', lastVerified: '2026-09-20' },
    { id: 'ST-104', name: 'Dr. Samuel Miller, PharmD', role: 'Clinical Pharmacist', dept: 'Pharmacy', shift: 'Day (08:00 - 17:00)', licenseNumber: 'RPH-33910-CA', licenseStatus: 'Active (Expires Jan 2029)', aclsStatus: 'BCPS Certified', attendance: 'Present', lastVerified: '2026-07-12' },
    { id: 'ST-105', name: 'David Chen, MLS (ASCP)', role: 'Medical Technologist', dept: 'Laboratory', shift: 'Day (06:00 - 15:00)', licenseNumber: 'CLS-12849-CA', licenseStatus: 'Active (Expires Oct 2027)', aclsStatus: 'ASCP Specialist', attendance: 'Present', lastVerified: '2026-06-30' },
    { id: 'ST-106', name: 'Elena Rostova, RT (R)(CT)', role: 'Senior CT/MRI Technologist', dept: 'Radiology', shift: 'Day (08:00 - 17:00)', licenseNumber: 'RT-44819-CA', licenseStatus: 'Active (Expires Apr 2028)', aclsStatus: 'ARRT Advanced', attendance: 'Present', lastVerified: '2026-09-01' },
    { id: 'ST-107', name: 'Maria Gomez, CPC', role: 'Senior Medical Biller', dept: 'Billing', shift: 'Remote (08:00 - 16:30)', licenseNumber: 'AAPC-9021', licenseStatus: 'Active (Expires Dec 2027)', aclsStatus: 'N/A', attendance: 'Present', lastVerified: '2026-05-18' },
    { id: 'ST-108', name: 'James Patel, RHIA', role: 'Utilization Review Lead', dept: 'Insurance', shift: 'Day (08:30 - 17:00)', licenseNumber: 'AHIMA-5512', licenseStatus: 'Active (Expires Aug 2028)', aclsStatus: 'N/A', attendance: 'Present', lastVerified: '2026-08-22' },
  ]);

  const [leaveRequests, setLeaveRequests] = useState<LeaveRequest[]>([
    { id: 'LR-301', staffName: 'Dr. Robert Thorne, MD', role: 'Emergency Attending', dept: 'Emergency', type: 'CME Conference', dates: 'Oct 14 - Oct 17, 2026', backfill: 'Dr. Amanda Foster, MD (Assigned)', status: 'PENDING' },
    { id: 'LR-302', staffName: 'Sarah Jenkins, RN', role: 'Staff Registered Nurse', dept: 'Cardiology', type: 'Annual Paid Leave', dates: 'Oct 20 - Oct 25, 2026', backfill: 'Nurse Mark Wilson, RN (Confirmed)', status: 'PENDING' },
    { id: 'LR-303', staffName: 'David Chen, MLS', role: 'Medical Technologist', dept: 'Laboratory', type: 'Family Medical Leave', dates: 'Nov 02 - Nov 06, 2026', backfill: 'Technologist Rachel Day (Pending)', status: 'PENDING' },
    { id: 'LR-304', staffName: 'Elena Rostova, RT', role: 'Radiology Technologist', dept: 'Radiology', type: 'Personal Leave', dates: 'Oct 10 - Oct 11, 2026', backfill: 'Locum RT Jacob Bell (Assigned)', status: 'APPROVED' },
  ]);

  const handleVerify = (id: string) => {
    setVerifiedIds(prev => ({ ...prev, [id]: true }));
  };

  const handleApproveLeave = (id: string) => {
    setLeaveRequests(prev => prev.map(req => req.id === id ? { ...req, status: 'APPROVED' } : req));
  };

  const handleRejectLeave = (id: string) => {
    setLeaveRequests(prev => prev.map(req => req.id === id ? { ...req, status: 'REJECTED' } : req));
  };

  const filteredStaff = staffList.filter(s => {
    const matchesSearch = s.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          s.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          s.licenseNumber.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDept = deptFilter === 'ALL' || s.dept.toUpperCase() === deptFilter;
    return matchesSearch && matchesDept;
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
              <Users className="w-3.5 h-3.5" /> Medical Staff Office & Credentialing
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Director of Human Capital • Eleanor Davis, SPHR</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Healthcare HR & Staff Credentialing</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Medical staff roster, board licensure audits, shift coverage allocations, and leave requests.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'roster', 'leave'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'roster' ? 'Staff Roster' : 'Leave & Shifts'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Staff Policies RAG
          </button>
        </div>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Total Hospital Staff"
          value="248 Staff"
          subtitle="Doctors, Nurses, Technologists"
          icon={Users}
          variant="purple"
        />
        <StatCard
          title="On-Duty Clinical Staff"
          value="82 Active"
          subtitle="Day shift roster filled"
          icon={UserCheck}
          variant="emerald"
        />
        <StatCard
          title="Pending Leave Requests"
          value={`${leaveRequests.filter(l => l.status === 'PENDING').length} Requests`}
          subtitle="All coverage backfills assigned"
          icon={Calendar}
          variant="amber"
        />
        <StatCard
          title="Staff License Compliance"
          value="100% Current"
          subtitle="Zero lapsed clinical credentials"
          icon={ShieldCheck}
          variant="teal"
        />
      </div>

      {/* VIEW: STAFF ROSTER & CREDENTIALS */}
      {(activeNav === 'roster' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Medical Staff Credentialing Roster</h3>
              <p className="text-xs text-slate-500">Active state licensure, departmental assignments, and Joint Commission audit compliance</p>
            </div>

            <div className="flex items-center gap-2 flex-wrap">
              <div className="relative w-48">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search staff, license..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                />
              </div>

              <select
                value={deptFilter}
                onChange={(e) => setDeptFilter(e.target.value)}
                className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700 font-medium"
              >
                <option value="ALL">All Departments</option>
                <option value="CARDIOLOGY">Cardiology</option>
                <option value="EMERGENCY">Emergency</option>
                <option value="PHARMACY">Pharmacy</option>
                <option value="LABORATORY">Laboratory</option>
                <option value="RADIOLOGY">Radiology</option>
              </select>

              <span className="text-xs font-mono bg-rose-50 text-rose-800 px-2 py-1 rounded border border-rose-200 font-bold hidden sm:inline">
                Joint Commission Ready
              </span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Staff ID & Name</th>
                  <th className="p-2.5">Department & Shift</th>
                  <th className="p-2.5">License & State Board</th>
                  <th className="p-2.5">Life Support / BLS</th>
                  <th className="p-2.5">Verification</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredStaff.map((s) => {
                  const isVerified = verifiedIds[s.id];
                  return (
                    <tr key={s.id} className="hover:bg-slate-50 transition-colors">
                      <td className="p-2.5">
                        <strong className="text-slate-900 block">{s.name}</strong>
                        <span className="text-slate-500 text-[11px]">{s.role}</span>
                      </td>
                      <td className="p-2.5">
                        <span className="font-medium text-slate-800 block">{s.dept}</span>
                        <span className="text-[10px] text-slate-500">{s.shift}</span>
                      </td>
                      <td className="p-2.5">
                        <span className="font-mono text-slate-700 block font-semibold">{s.licenseNumber}</span>
                        <span className="text-emerald-700 bg-emerald-50 px-1.5 py-0.2 rounded font-mono text-[10px] font-medium border border-emerald-100 inline-block mt-0.5">
                          {s.licenseStatus}
                        </span>
                      </td>
                      <td className="p-2.5">
                        <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-semibold text-[10px] border border-blue-100">
                          {s.aclsStatus}
                        </span>
                      </td>
                      <td className="p-2.5">
                        {isVerified ? (
                          <span className="flex items-center gap-1 text-emerald-700 text-[11px] font-bold">
                            <CheckCircle2 className="w-3.5 h-3.5" /> Re-verified Today
                          </span>
                        ) : (
                          <span className="text-slate-500 text-[11px]">
                            Verified: {s.lastVerified}
                          </span>
                        )}
                      </td>
                      <td className="p-2.5 text-right">
                        <button
                          onClick={() => handleVerify(s.id)}
                          disabled={isVerified}
                          className={`px-2.5 py-1 rounded text-[11px] font-semibold transition-all ${
                            isVerified
                              ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                              : 'bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200'
                          }`}
                        >
                          {isVerified ? 'Audit Passed' : 'Verify Board'}
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: LEAVE REQUESTS */}
      {(activeNav === 'leave' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Medical Staff Paid Leave & On-Call Coverage Schedule</h3>
              <p className="text-xs text-slate-500">Departmental coverage backfills, CME grants, and shift contingency assignments</p>
            </div>
            <span className="text-xs font-medium text-slate-600 bg-slate-100 px-2 py-1 rounded">
              Policy: Mandatory 1:1 Clinician Backfill
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Request ID</th>
                  <th className="p-2.5">Staff Member</th>
                  <th className="p-2.5">Leave Type</th>
                  <th className="p-2.5">Dates</th>
                  <th className="p-2.5">Shift Backfill Assignment</th>
                  <th className="p-2.5">Approval Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {leaveRequests.map((req) => (
                  <tr key={req.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5 font-mono text-slate-500 font-semibold">{req.id}</td>
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{req.staffName}</strong>
                      <span className="text-[11px] text-slate-500">{req.role} ({req.dept})</span>
                    </td>
                    <td className="p-2.5">
                      <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium text-[10px]">
                        {req.type}
                      </span>
                    </td>
                    <td className="p-2.5 font-medium text-slate-800">{req.dates}</td>
                    <td className="p-2.5">
                      <span className="text-blue-700 bg-blue-50 px-2 py-0.5 rounded text-[11px] font-medium border border-blue-100">
                        {req.backfill}
                      </span>
                    </td>
                    <td className="p-2.5">
                      <StatusBadge status={req.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      {req.status === 'PENDING' ? (
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => handleApproveLeave(req.id)}
                            className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[11px] font-bold shadow-2xs flex items-center gap-1"
                          >
                            <Check className="w-3 h-3" /> Approve
                          </button>
                          <button
                            onClick={() => handleRejectLeave(req.id)}
                            className="px-2 py-1 bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 rounded text-[11px] font-semibold"
                          >
                            Deny
                          </button>
                        </div>
                      ) : (
                        <span className="text-slate-400 text-[11px]">Logged</span>
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
