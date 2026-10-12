'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  ShieldCheck, FileCheck, AlertCircle, Clock, 
  Building, DollarSign, FileText, CheckCircle2, 
  Search, ArrowUpRight, Check, X, ShieldAlert 
} from 'lucide-react';
import { SAMPLE_CLAIMS } from '@/lib/data/mockDatabase';

interface InsuranceDashboardProps {
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const InsuranceDashboard: React.FC<InsuranceDashboardProps> = ({ 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [claims, setClaims] = useState(SAMPLE_CLAIMS);
  const [providerFilter, setProviderFilter] = useState('ALL');

  const handleApprove = (claimId: string) => {
    setClaims(prev => prev.map(c => c.id === claimId ? { ...c, status: 'Approved' } : c));
    alert(`Claim ${claimId} approved and scheduled for electronic remittance.`);
  };

  const handleReject = (claimId: string) => {
    setClaims(prev => prev.map(c => c.id === claimId ? { ...c, status: 'Rejected' } : c));
    alert(`Claim ${claimId} marked Rejected. Clinical appeal notice generated.`);
  };

  const filteredClaims = claims.filter(c => {
    if (providerFilter === 'ALL') return true;
    return c.provider.toLowerCase().includes(providerFilter.toLowerCase());
  });

  const pendingCount = claims.filter(c => c.status === 'Submitted' || c.status === 'Under Review').length;
  const approvedCount = claims.filter(c => c.status === 'Approved').length;
  const rejectedCount = claims.filter(c => c.status === 'Rejected').length;
  const totalValue = claims.reduce((acc, c) => acc + (c.claimedAmount || 0), 0);

  return (
    <div className="space-y-6 text-[#1E293B] dark:text-[#E2E8F0]">
      {/* Standard Compact Page Header (Section 3 Specification) */}
      <div className="bg-white dark:bg-[#111827] rounded-xl p-5 border border-[#DCE4EA] dark:border-[#293548] shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-[#0F8B8D] border border-teal-200 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" /> TPA & Commercial Payers
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">TPA Manager • Michael Chang, RHIA</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">TPA & Insurance Claims Center</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Commercial payer prior-authorizations, electronic claim adjudication, and policy compliance.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'preauth', 'payers'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'preauth' ? 'Prior-Authorizations' : 'Payer Contracts'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Payer Guidelines RAG
          </button>
        </div>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <StatCard
          title="Pending Claims"
          value={`${pendingCount} Claims`}
          subtitle="Awaiting adjudication"
          icon={Clock}
          variant="amber"
        />
        <StatCard
          title="Approved Claims"
          value={`${approvedCount} Claims`}
          subtitle="Clean payment cleared"
          icon={CheckCircle2}
          variant="emerald"
        />
        <StatCard
          title="Rejected Claims"
          value={`${rejectedCount} Claims`}
          subtitle="Appeals in progress"
          icon={AlertCircle}
          variant="rose"
        />
        <StatCard
          title="Total Claim Value"
          value={`$${(totalValue / 1000).toFixed(1)}k`}
          subtitle="Submitted to commercial TPAs"
          icon={DollarSign}
          variant="blue"
        />
        <StatCard
          title="Active Payer Contracts"
          value="14 Payers"
          subtitle="BCBS, Aetna, Cigna, Medicare"
          icon={Building}
          variant="slate"
        />
      </div>

      {/* VIEW: CLAIMS TABLE & AGING */}
      {(activeNav === 'dashboard' || activeNav === 'preauth') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Commercial & Government Insurance Claims Ledger</h3>
              <p className="text-xs text-slate-500">EDI 837 claim submissions, electronic remittance advice (835), and denial tracking</p>
            </div>

            <div className="flex items-center gap-2">
              <select
                value={providerFilter}
                onChange={(e) => setProviderFilter(e.target.value)}
                className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700"
              >
                <option value="ALL">All Payer Networks</option>
                <option value="Blue Cross">Blue Cross Shield</option>
                <option value="Aetna">Aetna Commercial</option>
                <option value="Medicare">Medicare Part A/B</option>
                <option value="Cigna">Cigna Healthcare</option>
              </select>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Claim ID</th>
                  <th className="p-2.5">Patient & Account</th>
                  <th className="p-2.5">Insurance Payer</th>
                  <th className="p-2.5">Claim Amount</th>
                  <th className="p-2.5">Submission Date</th>
                  <th className="p-2.5">Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredClaims.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5 font-mono text-slate-600 font-bold">{c.id}</td>
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{c.patientName}</strong>
                      <span className="font-mono text-[10px] text-slate-400">{c.patientId}</span>
                    </td>
                    <td className="p-2.5 font-medium text-slate-800">{c.provider}</td>
                    <td className="p-2.5 font-mono font-bold text-slate-900">
                      ${c.claimedAmount?.toLocaleString()}
                    </td>
                    <td className="p-2.5 font-mono text-slate-500">{c.submissionDate}</td>
                    <td className="p-2.5">
                      <StatusBadge status={c.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      {c.status !== 'Approved' && c.status !== 'Rejected' ? (
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => handleApprove(c.id)}
                            className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[11px] font-bold shadow-2xs"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleReject(c.id)}
                            className="px-2 py-1 bg-white hover:bg-rose-50 text-rose-700 border border-rose-200 rounded text-[11px] font-semibold"
                          >
                            Deny
                          </button>
                        </div>
                      ) : (
                        <span className="text-slate-400 text-[11px]">Adjudicated</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: PAYER CONTRACTS */}
      {activeNav === 'payers' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Contracted Commercial & Government Payers</h3>
              <p className="text-xs text-slate-500">Fee schedule multipliers, DRG carve-outs, and prior authorization SLAs</p>
            </div>
            <span className="text-xs font-mono bg-blue-50 text-blue-700 px-2 py-1 rounded border border-blue-200 font-bold">
              14 Active Payer Contracts
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
              <strong className="text-slate-900 block text-xs">Blue Cross Blue Shield (Commercial)</strong>
              <span className="text-slate-600 block">Contract Ref: PPO-2026-CA-88</span>
              <p className="text-[11px] text-slate-500">Inpatient DRG Multiplier: 114% of CMS • Pre-auth SLA: 48h</p>
              <span className="text-[10px] text-emerald-700 font-bold block pt-1">Active through Dec 2027</span>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
              <strong className="text-slate-900 block text-xs">Medicare Part A & B (CMS)</strong>
              <span className="text-slate-600 block">Contract Ref: CMS-FED-CAL-01</span>
              <p className="text-[11px] text-slate-500">Direct Fiscal Intermediary • Electronic Remittance 835</p>
              <span className="text-[10px] text-emerald-700 font-bold block pt-1">Federal Certified</span>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
              <strong className="text-slate-900 block text-xs">Aetna Commercial Choice POS</strong>
              <span className="text-slate-600 block">Contract Ref: AET-2025-HOSP-09</span>
              <p className="text-[11px] text-slate-500">Inpatient DRG Multiplier: 112% of CMS • Fast-track surgical pre-auth</p>
              <span className="text-[10px] text-emerald-700 font-bold block pt-1">Active through Oct 2027</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
