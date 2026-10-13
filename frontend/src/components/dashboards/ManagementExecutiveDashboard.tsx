'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  TrendingUp, Award, DollarSign, Bed, Activity, 
  Building, Users, FileText, CheckCircle2, ShieldCheck, 
  Percent, ArrowUpRight, BarChart3, PieChart, Download, 
  Layers, AlertCircle, Sparkles,
  LogOut,
} from 'lucide-react';

interface ManagementExecutiveDashboardProps {
  onLogout?: () => void;
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const ManagementExecutiveDashboard: React.FC<ManagementExecutiveDashboardProps> = ({
  onLogout, 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [downloading, setDownloading] = useState(false);

  const handleExport = () => {
    setDownloading(true);
    setTimeout(() => {
      setDownloading(false);
      alert('Executive Financial Package (FY2026 Q4 Audit PDF) exported successfully.');
    }, 1200);
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
              <Award className="w-3.5 h-3.5" /> Executive Board & C-Suite Governance
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Chief Operating Officer • Victoria Hastings, MHA</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Executive Board Governance</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Quarterly operational scorecard, clinical quality benchmarks, and health network EBITDA margins.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'revenue', 'quality'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs font-bold' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Scorecard' : n === 'revenue' ? 'Revenue Analytics' : 'Quality & JCAHO'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Governance RAG
          </button>
        </div>
      </div>

      {/* Primary Financial & Quality KPIs (Section 22) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Monthly Revenue"
          value="$4.82M"
          subtitle="Net patient service revenue"
          trend={{ value: "+9.2%", isPositive: true }}
          icon={DollarSign}
          variant="emerald"
        />
        <StatCard
          title="Overall Bed Occupancy"
          value="84.6%"
          subtitle="Target: 82% - 88%"
          trend={{ value: "+1.4%", isPositive: true }}
          icon={Bed}
          variant="blue"
        />
        <StatCard
          title="Hospital Quality Score"
          value="98.5 / 100"
          subtitle="Leapfrog Grade A (Top 5%)"
          icon={Award}
          variant="teal"
        />
        <StatCard
          title="30-Day Readmission"
          value="4.1%"
          subtitle="Benchmark: < 7.5% (Exemplary)"
          trend={{ value: "-0.6%", isPositive: true }}
          icon={TrendingUp}
          variant="purple"
        />
      </div>

      {/* VIEW: EXECUTIVE SCORECARD / OVERVIEW */}
      {(activeNav === 'dashboard' || activeNav === 'revenue') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Clinical Service Line Performance Scorecard</h3>
              <p className="text-xs text-slate-500">Admissions volume, surgical case count, operating margin contribution, and patient safety rating</p>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleExport}
                disabled={downloading}
                className="px-3 py-1.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 flex items-center gap-1.5 transition-all shadow-2xs"
              >
                <Download className="w-3.5 h-3.5" />
                {downloading ? 'Exporting PDF...' : 'Export Financial Package'}
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Clinical Service Line</th>
                  <th className="p-2.5">Monthly Inpatients</th>
                  <th className="p-2.5">Bed Occupancy</th>
                  <th className="p-2.5">Surgical Procedures</th>
                  <th className="p-2.5">Net Contribution</th>
                  <th className="p-2.5">Operating Margin</th>
                  <th className="p-2.5">Quality Rating</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Cardiovascular Institute</td>
                  <td className="p-2.5 font-mono">184 Patients</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">89%</td>
                  <td className="p-2.5 font-mono">68 Cath/Interventions</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">$1,420,000</td>
                  <td className="p-2.5 font-mono text-emerald-600 font-semibold">+28.4%</td>
                  <td className="p-2.5"><span className="text-emerald-700 font-bold">★ 4.95</span></td>
                </tr>
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Trauma & Emergency Care</td>
                  <td className="p-2.5 font-mono">420 Visits</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">92%</td>
                  <td className="p-2.5 font-mono">34 Emergent OR</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">$980,000</td>
                  <td className="p-2.5 font-mono text-blue-600 font-semibold">+14.6%</td>
                  <td className="p-2.5"><span className="text-emerald-700 font-bold">★ 4.88</span></td>
                </tr>
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Neurology & Stroke Center</td>
                  <td className="p-2.5 font-mono">112 Patients</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">82%</td>
                  <td className="p-2.5 font-mono">19 Thrombectomies</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">$740,000</td>
                  <td className="p-2.5 font-mono text-emerald-600 font-semibold">+22.1%</td>
                  <td className="p-2.5"><span className="text-emerald-700 font-bold">★ 4.92</span></td>
                </tr>
                <tr className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-slate-900">Orthopedic Surgery</td>
                  <td className="p-2.5 font-mono">146 Patients</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">86%</td>
                  <td className="p-2.5 font-mono">84 Joint Replacements</td>
                  <td className="p-2.5 font-mono text-emerald-700 font-bold">$1,110,000</td>
                  <td className="p-2.5 font-mono text-emerald-600 font-semibold">+31.2%</td>
                  <td className="p-2.5"><span className="text-emerald-700 font-bold">★ 4.90</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: REVENUE ANALYTICS */}
      {activeNav === 'revenue' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <PieChart className="w-4 h-4 text-blue-600" /> Payer Mix & Reimbursement
            </h4>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Medicare (Parts A & B)</span>
                <strong className="font-mono text-slate-900">42% ($2.02M)</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Commercial (BCBS, Aetna, Cigna)</span>
                <strong className="font-mono text-slate-900">36% ($1.73M)</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Medicaid Managed Care</span>
                <strong className="font-mono text-slate-900">14% ($0.67M)</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Self-Pay & Private</span>
                <strong className="font-mono text-slate-900">8% ($0.40M)</strong>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-emerald-600" /> Revenue Cycle Performance
            </h4>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Days in Accounts Receivable (AR)</span>
                <strong className="font-mono text-emerald-700 font-bold">36.2 Days (&lt;45)</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">First-Pass Claim Clean Rate</span>
                <strong className="font-mono text-emerald-700 font-bold">96.8% (&gt;95)</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Denial Write-Off Rate</span>
                <strong className="font-mono text-emerald-700 font-bold">1.4% (&lt;2.0)</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Point of Service (POS) Collections</span>
                <strong className="font-mono text-slate-900">$214,000 / mo</strong>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-purple-600" /> Capital & Margin Health
            </h4>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Consolidated EBITDA Margin</span>
                <strong className="font-mono text-emerald-700 font-bold">+14.2%</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Operating Cash on Hand</span>
                <strong className="font-mono text-slate-900">198 Days</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Debt Service Coverage Ratio</span>
                <strong className="font-mono text-emerald-700 font-bold">3.8x (Moody&apos;s A+)</strong>
              </div>
              <div className="flex justify-between items-center p-2 rounded bg-slate-50">
                <span className="text-slate-700">Annual CapEx Reserve</span>
                <strong className="font-mono text-slate-900">$12.5M Allocated</strong>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW: QUALITY & JCAHO BENCHMARKS */}
      {(activeNav === 'quality' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">National Clinical Quality & Accreditation Readiness</h3>
              <p className="text-xs text-slate-500">The Joint Commission (TJC), CMS Star Ratings, and Leapfrog Group safety indicators</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-1 rounded border border-emerald-200 font-bold">
              Leapfrog Grade: A (Top 5%)
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-slate-500 block text-[11px]">CLABSI Infection Rate</span>
              <strong className="text-emerald-700 font-mono text-base block font-bold">0.00 / 1k</strong>
              <p className="text-[10px] text-slate-500">Benchmark: 0.82 • Zero infections in 365 days</p>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-slate-500 block text-[11px]">CAUTI Infection Rate</span>
              <strong className="text-emerald-700 font-mono text-base block font-bold">0.12 / 1k</strong>
              <p className="text-[10px] text-slate-500">Benchmark: 1.10 • Protocol compliant</p>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-slate-500 block text-[11px]">HCAHPS Patient Satisfaction</span>
              <strong className="text-blue-700 font-mono text-base block font-bold">91.4% Top Box</strong>
              <p className="text-[10px] text-slate-500">94th percentile nationally for care</p>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-slate-500 block text-[11px]">JCAHO Survey Readiness</span>
              <strong className="text-purple-700 font-mono text-base block font-bold">99.1% Ready</strong>
              <p className="text-[10px] text-slate-500">Mock audit completed • Zero findings</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
