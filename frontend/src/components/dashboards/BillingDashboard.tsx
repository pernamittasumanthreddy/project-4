'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  CreditCard, DollarSign, FileText, CheckCircle2, 
  Clock, ArrowUpRight, ShieldCheck, Download, Search, BookOpen, 
  Plus, Printer, Receipt, RefreshCcw,
  LogOut,
} from 'lucide-react';
import { SAMPLE_INVOICES } from '@/lib/data/mockDatabase';

interface BillingDashboardProps {
  onLogout?: () => void;
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const BillingDashboard: React.FC<BillingDashboardProps> = ({
  onLogout, 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [invoices, setInvoices] = useState(SAMPLE_INVOICES);
  const [searchTerm, setSearchTerm] = useState('');

  const handleRecordPayment = (invId: string) => {
    setInvoices(prev => prev.map(inv => inv.id === invId ? { ...inv, status: 'Paid', amountPaid: inv.totalAmount } : inv));
    alert(`Payment successfully posted for Invoice ${invId}. Electronic receipt dispatched.`);
  };

  const handlePrintReceipt = (invId: string) => {
    alert(`[RECEIPT PRINT SIMULATION]\nCityCare Multi-Speciality Hospital\nReceipt Ref: RCP-${invId}\nStatus: Settled in Full\nThank you for choosing CityCare.`);
  };

  const filteredInvoices = invoices.filter(inv =>
    inv.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    inv.id.toLowerCase().includes(searchTerm.toLowerCase())
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
              <CreditCard className="w-3.5 h-3.5" /> Billing & Revenue Cycle
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Revenue Cycle Lead • Claire Henderson, MBA</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Billing & Revenue Cycle</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Inpatient billing ledgers, tariff chargemaster CDM, outpatient co-pays, and electronic receipt dispatch.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'invoices', 'tariffs'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'invoices' ? 'Invoices Ledger' : 'Standard Tariffs'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Tariff Policies RAG
          </button>
        </div>
      </div>

      {/* Financial KPI Live Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <StatCard
          title="Today's Revenue"
          value="$19,635"
          subtitle="Gross patient service"
          icon={DollarSign}
          variant="emerald"
        />
        <StatCard
          title="Pending Payments"
          value="$4,120"
          subtitle="Outpatient co-pays due"
          icon={Clock}
          variant="amber"
        />
        <StatCard
          title="Outstanding Bills"
          value="$8,450"
          subtitle="Inpatient discharge bills"
          icon={FileText}
          variant="blue"
        />
        <StatCard
          title="Insurance Claims"
          value="$28,400"
          subtitle="Transmitted to TPAs"
          icon={ShieldCheck}
          variant="purple"
        />
        <StatCard
          title="Refunds Processed"
          value="$240.00"
          subtitle="Duplicate co-pay resolved"
          icon={RefreshCcw}
          variant="slate"
        />
      </div>

      {/* Department Breakdown & Payment Mix Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2.5 text-xs">
          <strong className="text-slate-900 font-bold block pb-1 border-b border-slate-100">
            Revenue by Clinical Service Line (Today)
          </strong>
          <div className="space-y-1.5">
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-600">Cardiovascular & Cath Lab</span>
              <strong className="font-mono text-slate-900">$8,240.00 (42%)</strong>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-600">Trauma & Emergency Care</span>
              <strong className="font-mono text-slate-900">$4,850.00 (25%)</strong>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-600">Orthopedic & General Surgery</span>
              <strong className="font-mono text-slate-900">$3,920.00 (20%)</strong>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-600">Diagnostic Pathology & Imaging</span>
              <strong className="font-mono text-slate-900">$2,625.00 (13%)</strong>
            </div>
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-2.5 text-xs">
          <strong className="text-slate-900 font-bold block pb-1 border-b border-slate-100">
            Payment & Settlement Methods
          </strong>
          <div className="space-y-1.5">
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-600">Electronic Insurance EDI Claims</span>
              <strong className="font-mono text-emerald-700">$14,500.00 (74%)</strong>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-600">Credit / Debit Card (Point of Service)</span>
              <strong className="font-mono text-slate-900">$3,840.00 (20%)</strong>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-600">Cash / Certified Bank Draft</span>
              <strong className="font-mono text-slate-900">$1,295.00 (6%)</strong>
            </div>
          </div>
        </div>
      </div>

      {/* VIEW: INVOICES TABLE */}
      {(activeNav === 'dashboard' || activeNav === 'invoices') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Inpatient & Outpatient Billing Invoices</h3>
              <p className="text-xs text-slate-500">Itemized room charges, procedures, pharmacy dispense, and patient responsibility</p>
            </div>

            <div className="flex items-center gap-2">
              <div className="relative w-48">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search invoice, patient..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                />
              </div>

              <button
                onClick={() => alert('Generating new inpatient invoice...')}
                className="px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white rounded-lg text-xs font-bold shadow-2xs flex items-center gap-1"
              >
                <Plus className="w-3.5 h-3.5" /> New Invoice
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Invoice ID</th>
                  <th className="p-2.5">Patient & Account</th>
                  <th className="p-2.5">Service Line</th>
                  <th className="p-2.5">Total Charges</th>
                  <th className="p-2.5">Insurance Coverage</th>
                  <th className="p-2.5">Status</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredInvoices.map((inv) => (
                  <tr key={inv.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5 font-mono text-slate-600 font-bold">{inv.id}</td>
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{inv.patientName}</strong>
                      <span className="font-mono text-[10px] text-slate-400">{inv.patientId}</span>
                    </td>
                    <td className="p-2.5 font-medium text-slate-700">Inpatient Care & Telemetry</td>
                    <td className="p-2.5 font-mono font-bold text-slate-900">${inv.totalAmount?.toLocaleString()}</td>
                    <td className="p-2.5 font-mono text-emerald-700 font-medium">
                      ${(inv.totalAmount * 0.8).toFixed(2)} (80%)
                    </td>
                    <td className="p-2.5">
                      <StatusBadge status={inv.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => handlePrintReceipt(inv.id)}
                          className="px-2 py-1 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded text-[11px] font-semibold flex items-center gap-1"
                        >
                          <Receipt className="w-3 h-3" /> Receipt
                        </button>
                        {inv.status !== 'Paid' && (
                          <button
                            onClick={() => handleRecordPayment(inv.id)}
                            className="px-2.5 py-1 bg-emerald-700 hover:bg-emerald-600 text-white rounded text-[11px] font-bold shadow-2xs"
                          >
                            Pay
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

      {/* VIEW: TARIFFS & CHARGEMASTER */}
      {activeNav === 'tariffs' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Standard Tariff Schedule (Chargemaster 2026)</h3>
              <p className="text-xs text-slate-500">Board-approved standard room rates, physician consultation fees, and procedural tariffs</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-1 rounded border border-emerald-200 font-bold">
              CMS Transparency Compliant
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-slate-500 block">ICU Bed Day (Level 3 Intensive)</span>
              <strong className="text-base text-slate-900 font-mono block">$1,850.00 / day</strong>
              <p className="text-[11px] text-slate-500">Includes continuous hemodynamics & 1:2 nursing</p>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-slate-500 block">Cardiac Step-Down Telemetry</span>
              <strong className="text-base text-slate-900 font-mono block">$850.00 / day</strong>
              <p className="text-[11px] text-slate-500">Telemetry cardiac monitoring & pulse oximetry</p>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="text-slate-500 block">General Ward Private Room</span>
              <strong className="text-base text-slate-900 font-mono block">$450.00 / day</strong>
              <p className="text-[11px] text-slate-500">Standard medical-surgical accommodation</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
