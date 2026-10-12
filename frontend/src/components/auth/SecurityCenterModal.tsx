'use client';

import React from 'react';
import { 
  ShieldCheck, Lock, X, Server, CheckCircle2, 
  Terminal, Database, Key, ShieldAlert, Cpu, Activity 
} from 'lucide-react';

interface SecurityCenterModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SecurityCenterModal: React.FC<SecurityCenterModalProps> = ({
  isOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 dark:bg-black/75 backdrop-blur-xs transition-opacity animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
      aria-labelledby="security-center-title"
    >
      <div className="relative w-full max-w-2xl bg-white dark:bg-[#111827] border border-[#DCE4EF] dark:border-[#293548] rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-[#DCE4EF] dark:border-[#293548] bg-slate-50/50 dark:bg-[#172033]/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-semibold tracking-wider uppercase text-emerald-600 dark:text-emerald-400">
                Enterprise Infrastructure
              </span>
              <h3 id="security-center-title" className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC]">
                Security & Compliance Operations Center
              </h3>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#1D293D] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-5">
          {/* Active Directory & Identity Status Card */}
          <div className="p-4 rounded-xl border border-[#DCE4EF] dark:border-[#293548] bg-[#F5F8FC] dark:bg-[#172033]">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Server className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                <span className="text-xs font-bold text-[#0F172A] dark:text-[#F8FAFC] uppercase tracking-wider">
                  Active Directory / LDAP Sync
                </span>
              </div>
              <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-2 py-0.5 rounded-md border border-emerald-200 dark:border-emerald-800">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Synchronized (Live)
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
              <div className="p-2 rounded-lg bg-white dark:bg-[#1D293D] border border-slate-200/80 dark:border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">Domain Controller</span>
                <p className="font-mono font-semibold text-slate-800 dark:text-slate-200 text-[11px]">dc01.citycare.org</p>
              </div>
              <div className="p-2 rounded-lg bg-white dark:bg-[#1D293D] border border-slate-200/80 dark:border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">Kerberos Realm</span>
                <p className="font-mono font-semibold text-slate-800 dark:text-slate-200 text-[11px]">CITYCARE.ORG</p>
              </div>
              <div className="p-2 rounded-lg bg-white dark:bg-[#1D293D] border border-slate-200/80 dark:border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">Ticket Lifetime</span>
                <p className="font-mono font-semibold text-slate-800 dark:text-slate-200 text-[11px]">10h (Renewable 7d)</p>
              </div>
              <div className="p-2 rounded-lg bg-white dark:bg-[#1D293D] border border-slate-200/80 dark:border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">RBAC Roles</span>
                <p className="font-mono font-semibold text-emerald-600 dark:text-emerald-400 text-[11px]">15 Enforced</p>
              </div>
            </div>
          </div>

          {/* Compliance & Technical Safeguards */}
          <div className="space-y-2.5">
            <span className="text-xs font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wider">
              HIPAA / HITECH Technical Safeguards (45 CFR Part 164)
            </span>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#172033] flex items-start gap-3">
                <Lock className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-slate-800 dark:text-slate-200">Transmission Encryption</h4>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                    All workstation sessions, telemetry streams, and RAG retrieval pipelines enforce TLS 1.3 with AES-256-GCM cipher suites.
                  </p>
                </div>
              </div>

              <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#172033] flex items-start gap-3">
                <Database className="w-4 h-4 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-slate-800 dark:text-slate-200">Vector Isolation (Multi-RAG)</h4>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                    Embeddings are strictly partitioned into tenant-role namespaces. Doctors cannot query executive HR docs; patients cannot access hospital SOPs.
                  </p>
                </div>
              </div>

              <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#172033] flex items-start gap-3">
                <Terminal className="w-4 h-4 text-purple-600 dark:text-purple-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-slate-800 dark:text-slate-200">Immutable Audit Trail</h4>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                    Every EMR view, medication dispense, lab verification, and RAG query generates a SHA-256 hashed tamper-evident audit record.
                  </p>
                </div>
              </div>

              <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#172033] flex items-start gap-3">
                <Activity className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-slate-800 dark:text-slate-200">Zero Hallucination Guardrail</h4>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                    If required clinical data is not present in approved hospital documents, the assistant strictly returns a standardized non-fabrication notice.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-[#DCE4EF] dark:border-[#293548] bg-slate-50/50 dark:bg-[#172033]/50 flex items-center justify-between">
          <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400">
            Node ID: SJC-CLUSTER-04 • FedRAMP High Ready
          </span>

          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 dark:bg-slate-700 text-white hover:bg-slate-900 transition-colors"
          >
            Acknowledge & Close
          </button>
        </div>
      </div>
    </div>
  );
};
