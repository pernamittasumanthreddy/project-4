'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Users, Calendar, UserCheck, Building, Clock, 
  Search, CheckCircle2, FileText, BadgeCheck, Plus, 
  UserPlus, CreditCard, Printer, ShieldCheck, Ticket,
  LogOut,
} from 'lucide-react';
import { SEED_PATIENTS } from '@/lib/data/mockDatabase';
import { Patient } from '@/lib/types/hms';

interface ReceptionistDashboardProps {
  onLogout?: () => void;
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
  onSelectPatient?: (patient: Patient) => void;
}

export const ReceptionistDashboard: React.FC<ReceptionistDashboardProps> = ({
  onLogout, 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav,
  onSelectPatient
}) => {
  const [queue, setQueue] = useState([
    { token: 'T-101', patient: 'John Anderson', mrn: 'MRN-884920', doctor: 'Dr. Marcus Vance (Cardiology)', time: '08:30 AM', status: 'In Consultation' },
    { token: 'T-102', patient: 'Elena Rostova', mrn: 'MRN-449182', doctor: 'Dr. Marcus Vance (Cardiology)', time: '09:00 AM', status: 'Checked In / Waiting' },
    { token: 'T-103', patient: 'Sophia Martinez', mrn: 'MRN-330192', doctor: 'Dr. Emily Watson (Pediatrics)', time: '09:15 AM', status: 'Checked In / Waiting' },
    { token: 'T-104', patient: 'Marcus Brody', mrn: 'MRN-194029', doctor: 'Dr. Robert Thorne (Emergency)', time: '09:30 AM', status: 'Triaged' },
    { token: 'T-105', patient: 'David Miller', mrn: 'MRN-552019', doctor: 'Dr. James Mitchell (Orthopedics)', time: '10:00 AM', status: 'Scheduled' },
  ]);

  const [visitorBadges, setVisitorBadges] = useState([
    { id: 'VB-101', name: 'Mary Anderson', relation: 'Spouse', patient: 'John Anderson (Room 204)', issued: '08:15 AM', expires: '08:00 PM', status: 'Active' },
    { id: 'VB-102', name: 'Igor Rostov', relation: 'Brother', patient: 'Elena Rostova (Room 205)', issued: '09:00 AM', expires: '08:00 PM', status: 'Active' },
    { id: 'VB-103', name: 'Carlos Martinez', relation: 'Father', patient: 'Sophia Martinez (Room 112)', issued: '09:10 AM', expires: '08:00 PM', status: 'Active' },
  ]);

  const [isRegisterOpen, setIsRegisterOpen] = useState(false);
  const [newPtName, setNewPtName] = useState('');
  const [newPtPhone, setNewPtPhone] = useState('');
  const [newPtDept, setNewPtDept] = useState('Cardiology');

  const handleRegisterPatient = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPtName) return;
    const newToken = `T-${100 + queue.length + 1}`;
    setQueue([...queue, {
      token: newToken,
      patient: newPtName,
      mrn: `MRN-${Math.floor(100000 + Math.random() * 900000)}`,
      doctor: `Dr. Specialist (${newPtDept})`,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'Checked In / Waiting'
    }]);
    alert(`Token ${newToken} issued for ${newPtName}! Queued for ${newPtDept}.`);
    setNewPtName('');
    setNewPtPhone('');
    setIsRegisterOpen(false);
  };

  const handlePrintToken = (token: string, name: string) => {
    alert(`[PRINT TOKEN SIMULATION]\nCityCare Multi-Speciality Hospital\nToken: ${token}\nPatient: ${name}\nDate: ${new Date().toLocaleDateString()}\nPlease proceed to Waiting Lounge B.`);
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
              <BadgeCheck className="w-3.5 h-3.5" /> Patient Intake & Front Desk
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Lead Intake Coordinator • Jessica Gomez</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Patient Access & Intake</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Front desk intake queue, outpatient tokens, walk-in registration, and visitor security passes.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'appointments', 'visitors'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={() => setIsRegisterOpen(true)}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <UserPlus className="w-3.5 h-3.5" /> Register Walk-In
          </button>
        </div>
      </div>

      {/* Prominent Front-Desk Quick Actions Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-3">
          Front-Desk Rapid Actions
        </span>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
          <button
            onClick={() => setIsRegisterOpen(true)}
            className="p-3 rounded-lg bg-blue-50 hover:bg-blue-100 border border-blue-200 text-blue-900 font-bold text-xs flex flex-col items-center justify-center gap-1.5 transition-colors"
          >
            <UserPlus className="w-5 h-5 text-blue-600" />
            <span>REGISTER PATIENT</span>
          </button>
          <button
            onClick={() => alert('Opening Master Appointment Scheduler')}
            className="p-3 rounded-lg bg-teal-50 hover:bg-teal-100 border border-teal-200 text-teal-900 font-bold text-xs flex flex-col items-center justify-center gap-1.5 transition-colors"
          >
            <Calendar className="w-5 h-5 text-teal-600" />
            <span>BOOK APPOINTMENT</span>
          </button>
          <button
            onClick={() => alert('Quick Check-in: Selected Patient Marked Arrived!')}
            className="p-3 rounded-lg bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 text-emerald-900 font-bold text-xs flex flex-col items-center justify-center gap-1.5 transition-colors"
          >
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <span>EXPRESS CHECK-IN</span>
          </button>
          <button
            onClick={() => alert('Opening Patient Database Lookup')}
            className="p-3 rounded-lg bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-800 font-bold text-xs flex flex-col items-center justify-center gap-1.5 transition-colors"
          >
            <Search className="w-5 h-5 text-slate-600" />
            <span>PATIENT SEARCH</span>
          </button>
          <button
            onClick={() => alert('Opening POS Co-Pay Billing Terminal')}
            className="p-3 rounded-lg bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-900 font-bold text-xs flex flex-col items-center justify-center gap-1.5 transition-colors"
          >
            <CreditCard className="w-5 h-5 text-amber-600" />
            <span>CO-PAY BILLING</span>
          </button>
          <button
            onClick={() => handlePrintToken('T-106', 'Walk-in Intake')}
            className="p-3 rounded-lg bg-purple-50 hover:bg-purple-100 border border-purple-200 text-purple-900 font-bold text-xs flex flex-col items-center justify-center gap-1.5 transition-colors"
          >
            <Ticket className="w-5 h-5 text-purple-600" />
            <span>PRINT TOKEN</span>
          </button>
        </div>
      </div>

      {/* Registration Modal Popup */}
      {isRegisterOpen && (
        <div className="p-4 bg-white rounded-xl border border-blue-200 shadow-md space-y-3 text-xs">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <strong className="text-sm font-bold text-slate-900">New Walk-in Patient Registration</strong>
            <button onClick={() => setIsRegisterOpen(false)} className="text-slate-400 hover:text-slate-700">✕</button>
          </div>
          <form onSubmit={handleRegisterPatient} className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="text-slate-600 font-medium block mb-1">Full Name</label>
              <input
                type="text"
                value={newPtName}
                onChange={(e) => setNewPtName(e.target.value)}
                placeholder="e.g. Robert Smith"
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                required
              />
            </div>
            <div>
              <label className="text-slate-600 font-medium block mb-1">Phone Number</label>
              <input
                type="text"
                value={newPtPhone}
                onChange={(e) => setNewPtPhone(e.target.value)}
                placeholder="+1 (555) 000-0000"
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
              />
            </div>
            <div>
              <label className="text-slate-600 font-medium block mb-1">Clinic / Department</label>
              <select
                value={newPtDept}
                onChange={(e) => setNewPtDept(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
              >
                <option value="Cardiology">Cardiology</option>
                <option value="General Medicine">General Medicine</option>
                <option value="Orthopedics">Orthopedics</option>
                <option value="Pediatrics">Pediatrics</option>
              </select>
            </div>
            <div className="sm:col-span-3 flex justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsRegisterOpen(false)}
                className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold shadow-2xs"
              >
                Create Account & Print Token
              </button>
            </div>
          </form>
        </div>
      )}

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Today's Total Check-ins"
          value="42 Patients"
          subtitle="92% on-time arrival"
          icon={UserCheck}
          variant="indigo"
        />
        <StatCard
          title="Waiting Room Count"
          value="6 Waiting"
          subtitle="Target wait: < 15 mins"
          icon={Users}
          variant="amber"
        />
        <StatCard
          title="Active Visitor Badges"
          value={`${visitorBadges.length} Badges`}
          subtitle="Hours: 08:00 - 20:00"
          icon={BadgeCheck}
          variant="emerald"
        />
        <StatCard
          title="Ambulatory Clinics"
          value="12 Active"
          subtitle="All clinicians on duty"
          icon={Building}
          variant="blue"
        />
      </div>

      {/* VIEW: TODAY'S QUEUE & WAITING ROOM */}
      {(activeNav === 'dashboard' || activeNav === 'appointments') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Today&apos;s Outpatient Consultation Queue</h3>
              <p className="text-xs text-slate-500">Live token sequence, clinician assignments, and arrival verification</p>
            </div>
            <span className="text-xs font-mono bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-200 font-semibold">
              Live Token Flow
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Token</th>
                  <th className="p-2.5">Patient & MRN</th>
                  <th className="p-2.5">Assigned Clinician</th>
                  <th className="p-2.5">Appointment Time</th>
                  <th className="p-2.5">Queue Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {queue.map((item) => (
                  <tr key={item.token} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5 font-mono font-bold text-blue-700">{item.token}</td>
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{item.patient}</strong>
                      <span className="font-mono text-[10px] text-slate-400">{item.mrn}</span>
                    </td>
                    <td className="p-2.5 font-medium text-slate-800">{item.doctor}</td>
                    <td className="p-2.5 font-mono text-slate-600">{item.time}</td>
                    <td className="p-2.5">
                      <StatusBadge status={item.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => handlePrintToken(item.token, item.patient)}
                          className="px-2 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded text-[11px] font-semibold flex items-center gap-1"
                        >
                          <Printer className="w-3 h-3" /> Token
                        </button>
                        {onSelectPatient && (
                          <button
                            onClick={() => {
                              const pt = SEED_PATIENTS.find(p => p.firstName === item.patient.split(' ')[0]) || SEED_PATIENTS[0];
                              onSelectPatient(pt);
                            }}
                            className="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[11px] font-semibold"
                          >
                            Chart
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

      {/* VIEW: VISITOR BADGES */}
      {(activeNav === 'visitors' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Visitor Security Badges</h3>
              <p className="text-xs text-slate-500">Authorized bedside visitor passes with time-restricted RFID badges</p>
            </div>
            <button
              onClick={() => alert('Issuing new visitor badge...')}
              className="px-3 py-1 bg-slate-900 text-white rounded-lg text-xs font-bold"
            >
              + Issue Visitor Pass
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Badge ID</th>
                  <th className="p-2.5">Visitor Name</th>
                  <th className="p-2.5">Relationship</th>
                  <th className="p-2.5">Inpatient / Room</th>
                  <th className="p-2.5">Issued At</th>
                  <th className="p-2.5">Valid Until</th>
                  <th className="p-2.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {visitorBadges.map((vb) => (
                  <tr key={vb.id} className="hover:bg-slate-50">
                    <td className="p-2.5 font-mono text-slate-600 font-semibold">{vb.id}</td>
                    <td className="p-2.5 font-bold text-slate-900">{vb.name}</td>
                    <td className="p-2.5 text-slate-600">{vb.relation}</td>
                    <td className="p-2.5 font-medium text-slate-800">{vb.patient}</td>
                    <td className="p-2.5 font-mono text-slate-500">{vb.issued}</td>
                    <td className="p-2.5 font-mono text-slate-700 font-medium">{vb.expires}</td>
                    <td className="p-2.5">
                      <StatusBadge status={vb.status} size="sm" />
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
