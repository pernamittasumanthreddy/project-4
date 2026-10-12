'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Pill, AlertTriangle, ShieldCheck, CheckCircle2, 
  Search, Package, ThermometerSnowflake, FileText, Lock, 
  AlertCircle, ArrowUpRight, Check, Plus, RefreshCw 
} from 'lucide-react';
import { MEDICINES_INVENTORY, SAMPLE_PRESCRIPTIONS } from '@/lib/data/mockDatabase';

interface PharmacistDashboardProps {
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const PharmacistDashboard: React.FC<PharmacistDashboardProps> = ({ 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const [inventory, setInventory] = useState(MEDICINES_INVENTORY);
  const [searchTerm, setSearchTerm] = useState('');
  const [prescriptions, setPrescriptions] = useState(SAMPLE_PRESCRIPTIONS);

  const filteredMeds = inventory.filter(m => 
    m.brandName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.genericName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const lowStockCount = inventory.filter(m => m.stockQuantity <= m.reorderLevel).length;

  const handleDispense = (rxId: string) => {
    setPrescriptions(prescriptions.map(p => 
      p.id === rxId ? { ...p, status: 'Dispensed' } : p
    ));
    alert(`Prescription ${rxId} verified & dispensed with dual-pharmacist barcode audit.`);
  };

  return (
    <div className="space-y-6 text-[#1E293B] dark:text-[#E2E8F0]">
      {/* Standard Compact Page Header (Section 3 Specification) */}
      <div className="bg-white dark:bg-[#111827] rounded-xl p-5 border border-[#DCE4EA] dark:border-[#293548] shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-[#0F8B8D] border border-teal-200 flex items-center gap-1">
              <Pill className="w-3.5 h-3.5" /> Central Inpatient Pharmacy
            </span>
            <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Pharmacist on Duty • Dr. Samuel Miller, PharmD, BCPS</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">Clinical Pharmacy Workstation</h1>
          <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5">
            Inpatient medication orders, formulary PAR management, and automated dispensing safety.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden lg:flex bg-[#F4F7FA] dark:bg-slate-800 p-1 rounded-lg border border-[#DCE4EA] dark:border-slate-700 text-xs">
              {(['dashboard', 'orders', 'formulary', 'coldchain'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all cursor-pointer ${
                    activeNav === n ? 'bg-white dark:bg-[#111827] text-[#0F8B8D] shadow-2xs' : 'text-[#64748B] dark:text-slate-300 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'Overview' : n === 'orders' ? 'Dispense Queue' : n === 'coldchain' ? 'Cold-Chain' : 'Formulary'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-[#0F8B8D] hover:bg-[#0B7476] text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" /> Formulary RAG
          </button>
        </div>
      </div>

      {/* KPI Stats Row (Section 4 Specification: 4 consistent cards) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Pending Rx Orders"
          value={`${prescriptions.filter(p => p.status !== 'Dispensed').length} Orders`}
          subtitle="CPOE verification active"
          icon={Pill}
          variant="amber"
        />
        <StatCard
          title="Low-Stock Medicines"
          value={`${lowStockCount} Items`}
          subtitle="Below PAR reorder level"
          icon={AlertTriangle}
          variant="rose"
        />
        <StatCard
          title="Total Formulary Drugs"
          value={`${inventory.length} Drugs`}
          subtitle="100% FDA Approved"
          icon={Package}
          variant="teal"
        />
        <StatCard
          title="Vaccine Cold-Chain"
          value="3.8 °C"
          subtitle="Continuous telemetry log"
          icon={ThermometerSnowflake}
          variant="emerald"
        />
      </div>

      {/* Drug Safety Alert Banner */}
      <div className="p-3.5 bg-amber-50 dark:bg-amber-950/30 rounded-xl border border-amber-200 dark:border-amber-800 flex items-center justify-between text-xs text-amber-900 dark:text-amber-200">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-700 dark:text-amber-400 shrink-0" />
          <span>
            <strong>Formulary Clinical Alert:</strong> Automated check active for Beta-Blocker + Calcium Channel Blocker cross-interactions and Vancomycin peak/trough monitoring.
          </span>
        </div>
        <span className="font-mono text-[10px] bg-amber-100 dark:bg-amber-900/60 text-amber-800 dark:text-amber-300 px-2 py-0.5 rounded font-bold">
          Live CDS Guard
        </span>
      </div>

      {/* VIEW: CPOE PRESCRIPTION DISPENSING QUEUE */}
      {(activeNav === 'dashboard' || activeNav === 'orders') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">CPOE Inpatient Prescription Verification Queue</h3>
              <p className="text-xs text-slate-500">Computerized Physician Order Entry verification and robotic dispensing cabinet sync</p>
            </div>
            <span className="text-xs font-mono bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-200 font-semibold">
              Pharmacist Sign-off Required
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Rx ID & Patient</th>
                  <th className="p-2.5">Medication & Dosage</th>
                  <th className="p-2.5">Route & Frequency</th>
                  <th className="p-2.5">Prescribing Physician</th>
                  <th className="p-2.5">Verification</th>
                  <th className="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {prescriptions.map((rx) => (
                  <tr key={rx.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-2.5">
                      <strong className="text-slate-900 block">{rx.patientName}</strong>
                      <span className="font-mono text-[10px] text-slate-400">{rx.id}</span>
                    </td>
                    <td className="p-2.5 font-bold text-slate-900 font-mono">
                      {rx.medications?.[0]?.name || 'Formulary Rx'} ({rx.medications?.[0]?.dosage || 'Standard'})
                    </td>
                    <td className="p-2.5 text-slate-700">
                      {(rx.medications?.[0] as any)?.route || 'Oral'} • {rx.medications?.[0]?.frequency || 'Daily'}
                    </td>
                    <td className="p-2.5 font-medium text-slate-800">{rx.doctorName}</td>
                    <td className="p-2.5">
                      <StatusBadge status={rx.status} size="sm" />
                    </td>
                    <td className="p-2.5 text-right">
                      {rx.status !== 'Dispensed' ? (
                        <button
                          onClick={() => handleDispense(rx.id)}
                          className="px-3 py-1 bg-amber-600 hover:bg-amber-500 text-white rounded text-[11px] font-bold shadow-2xs transition-colors"
                        >
                          Verify & Dispense
                        </button>
                      ) : (
                        <span className="text-emerald-700 text-[11px] font-semibold flex items-center justify-end gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Dispensed
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

      {/* VIEW: FORMULARY INVENTORY WITH HIGHLIGHTS */}
      {(activeNav === 'formulary' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Approved Hospital Drug Formulary & Inventory</h3>
              <p className="text-xs text-slate-500">Par levels, batch lot numbers, storage bins, and stock status indicators</p>
            </div>

            <div className="relative w-64">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search drug, generic, batch..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Brand & Generic Name</th>
                  <th className="p-2.5">Category</th>
                  <th className="p-2.5">Batch / Lot</th>
                  <th className="p-2.5">Stock Level</th>
                  <th className="p-2.5">Expiry Date</th>
                  <th className="p-2.5">Bin Location</th>
                  <th className="p-2.5">Inventory Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredMeds.map((m) => {
                  const isLow = m.stockQuantity <= m.reorderLevel;
                  const isOut = m.stockQuantity === 0;

                  return (
                    <tr key={m.id} className="hover:bg-slate-50 transition-colors">
                      <td className="p-2.5">
                        <strong className="text-slate-900 block">{m.brandName}</strong>
                        <span className="text-slate-500 text-[11px] italic">{m.genericName} ({m.strength})</span>
                      </td>
                      <td className="p-2.5 font-medium text-slate-700">{m.category}</td>
                      <td className="p-2.5 font-mono text-slate-500">{m.batchNumber}</td>
                      <td className="p-2.5 font-mono font-bold text-slate-900">
                        {m.stockQuantity} {m.dosageForm}
                      </td>
                      <td className="p-2.5 font-mono text-slate-600">{m.expiryDate}</td>
                      <td className="p-2.5 text-slate-700 font-mono text-[11px]">{m.storageRequirement}</td>
                      <td className="p-2.5">
                        {isOut ? (
                          <span className="px-2 py-0.5 rounded bg-rose-600 text-white font-bold text-[10px]">
                            OUT OF STOCK
                          </span>
                        ) : isLow ? (
                          <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-200 font-bold text-[10px]">
                            LOW STOCK
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold text-[10px]">
                            OPTIMAL
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW: COLD-CHAIN TELEMETRY */}
      {activeNav === 'coldchain' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5 text-blue-700">
                <ThermometerSnowflake className="w-4 h-4 text-blue-600" /> Biologicals & Vaccine Cold-Chain Telemetry
              </h3>
              <p className="text-xs text-slate-500">24/7 continuous sensor logging compliant with CDC Vaccine Storage & Handling</p>
            </div>
            <span className="text-xs font-mono bg-emerald-50 text-emerald-800 px-2 py-1 rounded border border-emerald-200 font-bold">
              All Chambers Within 2°C - 8°C
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <span className="text-slate-500 font-medium block">Vaccine Refrigerator Unit A</span>
              <strong className="text-2xl font-bold font-mono text-emerald-700 block">3.6 °C</strong>
              <p className="text-[11px] text-slate-600">Storage: MMR, Varicella, Influenza, Pneumococcal</p>
              <span className="text-[10px] text-slate-400 block pt-1">Calibrated Oct 01 • Sensor Probe #1</span>
            </div>

            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <span className="text-slate-500 font-medium block">Biologics & Insulin Unit B</span>
              <strong className="text-2xl font-bold font-mono text-emerald-700 block">4.1 °C</strong>
              <p className="text-[11px] text-slate-600">Storage: Lantus, Humalog, Monoclonal Antibodies</p>
              <span className="text-[10px] text-slate-400 block pt-1">Calibrated Oct 01 • Sensor Probe #2</span>
            </div>

            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
              <span className="text-slate-500 font-medium block">Ultra-Low Freezer Unit C</span>
              <strong className="text-2xl font-bold font-mono text-blue-700 block">-78.2 °C</strong>
              <p className="text-[11px] text-slate-600">Storage: Research mRNA & Specialized Tissue Cultures</p>
              <span className="text-[10px] text-slate-400 block pt-1">Calibrated Sep 15 • Liquid N2 Backup OK</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
