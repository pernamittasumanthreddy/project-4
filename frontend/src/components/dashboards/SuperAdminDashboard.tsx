'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  ShieldCheck, Server, Key, AlertOctagon, Users, 
  Building2, Database, Lock, Eye, RefreshCw, Settings, 
  Activity, DollarSign, Calendar, Bed, Flame, AlertCircle, 
  CheckCircle2, FileText, ArrowUpRight, Clock 
} from 'lucide-react';
import { INITIAL_AUDIT_LOGS } from '@/lib/data/mockDatabase';

interface SuperAdminDashboardProps {
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ 
  activeNav = 'dashboard',
  setActiveNav 
}) => {
  return (
    <div className="space-y-6 text-[#1E293B] dark:text-[#E2E8F0]">
      {/* Standard Compact Page Header (Section 3 Specification) */}
      <div className="bg-white dark:bg-[#111827] rounded-xl p-5 border border-[#DCE4EA] dark:border-[#293548] shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-[#0F8B8D] border border-teal-200 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" /> Cluster Super Admin Governance
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Cluster CTO • Alexander Sterling</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Cluster Super Admin Governance</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Multi-tenant hospital network infrastructure, cryptographic audit logs, and global RBAC security.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'tenants', 'rbac', 'audit', 'settings'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'tenants' ? 'Tenants' : n === 'rbac' ? 'RBAC Matrix' : n === 'audit' ? 'Audit Stream' : 'Settings'}
                </button>
              ))}
            </div>
          )}

          <div className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 rounded-lg text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Cluster Healthy (4 Nodes)</span>
          </div>
        </div>
      </div>

      {/* Hospital-Wide KPI Cards (Section 8) */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <StatCard
          title="Total Patients"
          value="1,420"
          subtitle="Hospital system total"
          icon={Users}
          variant="blue"
        />
        <StatCard
          title="Active Doctors"
          value="184 MDs"
          subtitle="All specialties"
          icon={Activity}
          variant="teal"
        />
        <StatCard
          title="Appointments"
          value="82 Today"
          subtitle="Outpatient pavilion"
          icon={Calendar}
          variant="indigo"
        />
        <StatCard
          title="Available Beds"
          value="48 Beds"
          subtitle="System census: 78%"
          icon={Bed}
          variant="emerald"
        />
        <StatCard
          title="Emergency Cases"
          value="3 Active"
          subtitle="Trauma Bay load"
          icon={Flame}
          variant="rose"
        />
        <StatCard
          title="Daily Revenue"
          value="$19.6k"
          subtitle="Patient billing"
          icon={DollarSign}
          variant="emerald"
        />
        <StatCard
          title="Pending Bills"
          value="$4.1k"
          subtitle="Awaiting co-pay"
          icon={Clock}
          variant="amber"
        />
        <StatCard
          title="System Alerts"
          value="0 Fatal"
          subtitle="Zero breaches"
          icon={ShieldCheck}
          variant="purple"
        />
      </div>

      {/* Operational Live Status Panel */}
      <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-3">
        <div className="flex items-center justify-between pb-2 border-b border-slate-100">
          <strong className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
            <Activity className="w-4 h-4 text-blue-600" /> LIVE HOSPITAL SYSTEM OPERATIONAL STATUS
          </strong>
          <span className="text-[11px] font-mono text-slate-400">Real-time Telemetry Engine</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span className="text-slate-500 block">Emergency Status</span>
            <strong className="text-base text-rose-700 font-mono block mt-0.5">3 Active Cases</strong>
            <span className="text-[10px] text-rose-600 font-semibold">Trauma Bay Level 1 Active</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span className="text-slate-500 block">ICU Bed Occupancy</span>
            <strong className="text-base text-amber-700 font-mono block mt-0.5">82% Occupied</strong>
            <span className="text-[10px] text-amber-600 font-semibold">23 / 28 Critical Beds</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span className="text-slate-500 block">General Ward Occupancy</span>
            <strong className="text-base text-blue-700 font-mono block mt-0.5">71% Occupied</strong>
            <span className="text-[10px] text-blue-600 font-semibold">142 / 200 Beds In Use</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span className="text-slate-500 block">Total Beds Available</span>
            <strong className="text-base text-emerald-700 font-mono block mt-0.5">48 Beds Open</strong>
            <span className="text-[10px] text-emerald-600 font-semibold">Direct admission capacity</span>
          </div>
        </div>
      </div>

      {/* VIEW: TENANTS DIRECTORY */}
      {(activeNav === 'dashboard' || activeNav === 'tenants') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Multi-Hospital Tenant Isolation Directory</h3>
              <p className="text-xs text-slate-500">Logical schema isolation and tenant boundary enforcement</p>
            </div>
            <span className="text-xs font-mono bg-purple-50 text-purple-700 px-2 py-0.5 rounded border border-purple-200 font-bold">
              PostgreSQL Row-Level Security Enforced
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5 text-xs">
            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <div className="flex items-center justify-between">
                <strong className="text-slate-900 font-bold">CityCare Main (HOSP-01)</strong>
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
              </div>
              <p className="text-[11px] text-slate-600">Central Campus • 450 Beds • Primary Academic Medical Center</p>
              <div className="pt-2 border-t border-slate-200 text-[10px] text-slate-500 flex justify-between">
                <span>Active Users: 840</span>
                <span className="text-emerald-700 font-bold">Primary Node</span>
              </div>
            </div>

            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <div className="flex items-center justify-between">
                <strong className="text-slate-900 font-bold">CityCare North (HOSP-02)</strong>
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
              </div>
              <p className="text-[11px] text-slate-600">Suburban Ambulatory Pavilion & Surgical Specialty Center</p>
              <div className="pt-2 border-t border-slate-200 text-[10px] text-slate-500 flex justify-between">
                <span>Active Users: 280</span>
                <span className="text-emerald-700 font-bold">Replicated</span>
              </div>
            </div>

            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <div className="flex items-center justify-between">
                <strong className="text-slate-900 font-bold">CityCare Children&apos;s (HOSP-03)</strong>
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
              </div>
              <p className="text-[11px] text-slate-600">Pediatric Specialty Hospital & Neonatal Intensive Care Unit</p>
              <div className="pt-2 border-t border-slate-200 text-[10px] text-slate-500 flex justify-between">
                <span>Active Users: 195</span>
                <span className="text-emerald-700 font-bold">Replicated</span>
              </div>
            </div>

            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <div className="flex items-center justify-between">
                <strong className="text-slate-900 font-bold">CityCare Oncology (HOSP-04)</strong>
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
              </div>
              <p className="text-[11px] text-slate-600">Comprehensive Cancer Institute & Infusion Center</p>
              <div className="pt-2 border-t border-slate-200 text-[10px] text-slate-500 flex justify-between">
                <span>Active Users: 105</span>
                <span className="text-emerald-700 font-bold">Replicated</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW: RBAC MATRIX */}
      {activeNav === 'rbac' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Role-Based Access Control (RBAC) Privilege Matrix</h3>
              <p className="text-xs text-slate-500">Fine-grained resource access permissions across all 15 clinical & administrative roles</p>
            </div>
            <span className="text-xs font-mono bg-purple-50 text-purple-700 px-2 py-0.5 rounded border border-purple-200 font-bold">
              15 Roles Isolated
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Hospital Role</th>
                  <th className="p-2.5">Patient Records</th>
                  <th className="p-2.5">Medications / Rx</th>
                  <th className="p-2.5">Billing & Claims</th>
                  <th className="p-2.5">Clinical Guidelines</th>
                  <th className="p-2.5">RAG Scope</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Doctor</td>
                  <td className="p-2.5"><StatusBadge status="Read / Write" size="sm" variant="success" /></td>
                  <td className="p-2.5"><StatusBadge status="Prescribe" size="sm" variant="success" /></td>
                  <td className="p-2.5"><StatusBadge status="No Access" size="sm" variant="neutral" /></td>
                  <td className="p-2.5"><StatusBadge status="Full Access" size="sm" variant="success" /></td>
                  <td className="p-2.5 text-blue-700 font-medium">Clinical Protocols & EMR</td>
                </tr>
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Nurse</td>
                  <td className="p-2.5"><StatusBadge status="Vitals / Notes" size="sm" variant="success" /></td>
                  <td className="p-2.5"><StatusBadge status="Administer" size="sm" variant="success" /></td>
                  <td className="p-2.5"><StatusBadge status="No Access" size="sm" variant="neutral" /></td>
                  <td className="p-2.5"><StatusBadge status="Nursing SOPs" size="sm" variant="success" /></td>
                  <td className="p-2.5 text-blue-700 font-medium">Nursing SOPs & Meds</td>
                </tr>
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Pharmacist</td>
                  <td className="p-2.5"><StatusBadge status="Med History" size="sm" variant="info" /></td>
                  <td className="p-2.5"><StatusBadge status="Dispense / Audit" size="sm" variant="success" /></td>
                  <td className="p-2.5"><StatusBadge status="No Access" size="sm" variant="neutral" /></td>
                  <td className="p-2.5"><StatusBadge status="Drug Formulary" size="sm" variant="success" /></td>
                  <td className="p-2.5 text-blue-700 font-medium">Formulary & Cold-Chain</td>
                </tr>
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Patient</td>
                  <td className="p-2.5"><StatusBadge status="Own Chart Only" size="sm" variant="info" /></td>
                  <td className="p-2.5"><StatusBadge status="View Only" size="sm" variant="neutral" /></td>
                  <td className="p-2.5"><StatusBadge status="View & Pay" size="sm" variant="info" /></td>
                  <td className="p-2.5"><StatusBadge status="Patient Education" size="sm" variant="info" /></td>
                  <td className="p-2.5 text-blue-700 font-medium">Patient Education & Records</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: AUDIT STREAM */}
      {(activeNav === 'audit' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Global HIPAA Audit Trail Stream</h3>
              <p className="text-xs text-slate-500">Cryptographically verifiable immutable audit log for HIPAA 45 CFR § 164.312</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded border border-emerald-200 font-bold">
              SHA-256 Hash Chain Intact
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
                  <th className="p-2.5">Action Performed</th>
                  <th className="p-2.5">Resource</th>
                  <th className="p-2.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-[11px]">
                {INITIAL_AUDIT_LOGS.slice(0, 6).map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50">
                    <td className="p-2.5 font-bold text-slate-700">{log.id}</td>
                    <td className="p-2.5 text-slate-500">{log.timestamp}</td>
                    <td className="p-2.5 text-slate-800">{log.userName}</td>
                    <td className="p-2.5 text-slate-600">{log.role}</td>
                    <td className="p-2.5 font-sans font-medium text-slate-900">{log.action}</td>
                    <td className="p-2.5 text-blue-700">{log.resourceType}: {log.resourceId}</td>
                    <td className="p-2.5">
                      <span className="text-emerald-700 font-bold">SUCCESS</span>
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
