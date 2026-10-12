'use client';

import React from 'react';
import { HospitalRole } from '@/lib/types/roles';
import { ROLE_CONFIGS } from '@/lib/data/roleConfigs';
import { DEMO_USERS } from '@/lib/data/mockDatabase';
import { 
  ShieldCheck, ShieldAlert, Lock, X, FileText, CheckCircle2, 
  AlertTriangle, Bot, Sparkles, Building, User, KeyRound, Clock
} from 'lucide-react';

interface RoleAccessScopeModalProps {
  role: HospitalRole | null;
  isOpen: boolean;
  onClose: () => void;
  onLaunch: (role: HospitalRole) => void;
}

export const RoleAccessScopeModal: React.FC<RoleAccessScopeModalProps> = ({
  role,
  isOpen,
  onClose,
  onLaunch,
}) => {
  if (!isOpen || !role) return null;

  const config = ROLE_CONFIGS[role];
  const user = DEMO_USERS[role];

  // Derive forbidden categories from standard hospital categories
  const ALL_POSSIBLE_CATEGORIES = [
    'A. Hospital Policies', 'B. Department Information', 'C. Admission Procedures',
    'D. Discharge Procedures', 'E. Emergency Procedures', 'F. Clinical Guidelines',
    'G. Medicine Information', 'H. Pharmacy Policies', 'I. Laboratory Guidelines',
    'J. Radiology Guidelines', 'K. Insurance Policies', 'L. Billing Policies',
    'M. Patient Education', 'N. Staff Policies', 'O. HR Policies', 'P. Employee Handbook',
    'Q. Infection Control', 'R. Safety Procedures', 'S. Hospital SOPs', 'T. Appointment Policies',
    'U. Visiting Policies', 'V. Consent Forms', 'W. Privacy Policies', 'X. Data Protection Policies',
    'Y. Equipment Manuals', 'Z. Hospital Announcements', 'Patient Medical Records',
    'Staff Payroll & Compensation', 'Board Contracts & Financial Reports'
  ];

  const allowedSet = new Set<string>((config?.allowedCategories || []) as string[]);
  const forbiddenCategories = ALL_POSSIBLE_CATEGORIES.filter(c => !allowedSet.has(c)).slice(0, 8);

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 dark:bg-black/75 backdrop-blur-xs transition-opacity animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
      aria-labelledby="scope-modal-title"
    >
      <div className="relative w-full max-w-2xl bg-white dark:bg-[#111827] border border-[#DCE4EF] dark:border-[#293548] rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-[#DCE4EF] dark:border-[#293548] bg-slate-50/50 dark:bg-[#172033]/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-blue-600 dark:text-blue-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[11px] font-semibold tracking-wider uppercase text-blue-600 dark:text-blue-400">
                RBAC Access Scope & Security Governance
              </span>
              <h3 id="scope-modal-title" className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC]">
                {config?.displayName} Clearance Profile
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

        {/* Scrollable Content */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Identity & Department Banner */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-4 rounded-xl border border-[#DCE4EF] dark:border-[#293548] bg-[#F5F8FC] dark:bg-[#172033]">
            <div>
              <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
                Active Directory Identity
              </div>
              <div className="text-sm font-bold text-[#0F172A] dark:text-[#F8FAFC]">
                {user?.name}
              </div>
              <div className="text-xs text-slate-500 dark:text-slate-400">
                Department: {user?.department}
              </div>
              <div className="text-xs font-mono text-blue-600 dark:text-blue-400 mt-1">
                Credential ID: {user?.employeeId}
              </div>
            </div>

            <div className="border-t sm:border-t-0 sm:border-l border-slate-200 dark:border-slate-800 pt-3 sm:pt-0 sm:pl-4">
              <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
                Security Classification
              </div>
              <div className="flex flex-wrap gap-1.5 mb-2">
                <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                  <CheckCircle2 className="w-3 h-3" />
                  PHI Scope: {config?.allowedPatientScope}
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-md bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
                  Max: {config?.allowedConfidentiality?.slice(-1)[0]}
                </span>
              </div>
              <div className="text-[11px] text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
                <Clock className="w-3 h-3" /> 15-min idle re-authentication enforced
              </div>
            </div>
          </div>

          {/* Dedicated Grounded RAG Section */}
          <div className="rounded-xl border border-blue-100 dark:border-blue-900/60 bg-blue-50/40 dark:bg-blue-950/20 p-4">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-blue-700 dark:text-blue-300">
                {config?.ragTitle}
              </span>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed mb-3">
              {config?.knowledgeScopeDescription}
            </p>
            <div className="text-[11px] font-medium text-slate-500 dark:text-slate-400 bg-white/80 dark:bg-[#111827]/80 p-2.5 rounded-lg border border-blue-200/60 dark:border-blue-800/40">
              <strong>Grounding Guardrail:</strong> Zero hallucination tolerance. All responses require exact citations from verified hospital policies or assigned patient records.
            </div>
          </div>

          {/* Authorized Document Scope */}
          <div>
            <div className="flex items-center justify-between mb-2.5">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-200 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
                Authorized Knowledge Vectors ({config?.allowedCategories?.length})
              </span>
              <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold">
                Read & Query Permitted
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {config?.allowedCategories?.map((cat) => (
                <span 
                  key={cat}
                  className="text-xs px-2.5 py-1 rounded-md bg-white dark:bg-[#172033] border border-[#DCE4EF] dark:border-[#293548] text-slate-700 dark:text-slate-300 font-medium"
                >
                  {cat}
                </span>
              ))}
            </div>
          </div>

          {/* Strictly Restricted Document Categories */}
          <div>
            <div className="flex items-center justify-between mb-2.5">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-200 flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-rose-500" />
                Strictly Isolated / Restricted Categories
              </span>
              <span className="text-[11px] text-rose-600 dark:text-rose-400 font-semibold">
                Access Denied by RBAC
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {forbiddenCategories.map((cat) => (
                <span 
                  key={cat}
                  className="text-xs px-2.5 py-1 rounded-md bg-rose-50/60 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/50 text-rose-700 dark:text-rose-400"
                >
                  ✕ {cat}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-4 border-t border-[#DCE4EF] dark:border-[#293548] bg-slate-50/50 dark:bg-[#172033]/50">
          <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
            <Lock className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>Audit trail SHA-256 logged upon entry</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#111827] text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#1D293D] transition-colors"
            >
              Close
            </button>
            <button
              type="button"
              onClick={() => {
                onClose();
                onLaunch(role);
              }}
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-colors flex items-center gap-1.5"
            >
              <span>Launch Workstation</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
