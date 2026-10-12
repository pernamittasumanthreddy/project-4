'use client';
import React from 'react';
import Link from 'next/link';
import { 
  Stethoscope, Activity, FileText, 
  ShieldCheck, ArrowRight, ExternalLink 
} from 'lucide-react';

export default function ClinicalPortalPage() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#0B1120] text-slate-800 dark:text-slate-100 flex flex-col">
      {/* Top Banner */}
      <header className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-slate-800 px-6 py-4 flex items-center justify-between sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600 text-white rounded-xl shadow-md">
            <Stethoscope className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-900 dark:text-white leading-tight">
              Hospital Management System — Member 3 Clinical Management
            </h1>
            <p className="text-xs text-slate-500">Multi-Tenant EMR/EHR, Doctor & Nurse Workstations, e-Prescriptions</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="text-xs font-semibold text-slate-600 hover:text-blue-600 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800"
          >
            ← Main SaaS Shell
          </Link>
          <a
            href="http://localhost:8000/api/docs/"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 px-3 py-1.5 rounded-lg shadow-sm"
          >
            Backend Swagger Docs <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 max-w-6xl mx-auto w-full p-6 md:p-8 space-y-8">
        <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-sky-700 rounded-2xl p-8 text-white shadow-lg space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/15 text-white text-xs font-semibold backdrop-blur-xs">
            <ShieldCheck className="w-3.5 h-3.5" /> Clinical Management & EMR/EHR Workstation
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight">
            Integrated Clinical & EMR/EHR Workspace
          </h2>
          <p className="text-blue-100 text-sm max-w-2xl leading-relaxed">
            Professional healthcare workflows: structured SOAP consultations, cryptographic digital signatures, immutable clinical records, automated MEWS vitals telemetry, 5-rights bedside eMAR, and master WHO ICD-10 registries.
          </p>
        </div>

        {/* Member 3 Workstation Navigation Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1: Doctor Workspace */}
          <Link
            href="/clinical/doctor"
            className="group bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 hover:shadow-xl hover:border-blue-500 transition-all flex flex-col justify-between"
          >
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Stethoscope className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors">
                  Doctor Workstation
                </h3>
                <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">
                  Full SOAP clinical documentation, live ICD-10 search (2,250 codes), e-Prescribing with allergy contraindication checking, CHA2DS2-VASc, CKD-EPI, and CURB-65 calculators, and SHA-256 digital signing.
                </p>
              </div>
            </div>
            <div className="pt-6 flex items-center gap-1.5 text-xs font-bold text-blue-600 group-hover:translate-x-1 transition-transform">
              Launch Doctor Workspace <ArrowRight className="w-4 h-4" />
            </div>
          </Link>

          {/* Card 2: Nursing Station */}
          <Link
            href="/clinical/nursing"
            className="group bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 hover:shadow-xl hover:border-teal-500 transition-all flex flex-col justify-between"
          >
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-teal-100 dark:bg-teal-900/40 text-teal-600 dark:text-teal-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Activity className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-teal-600 transition-colors">
                  Inpatient Nursing Station
                </h3>
                <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">
                  Bedside telemetry flowsheet, automated Modified Early Warning Score (MEWS) engine, fluid intake/output volume balancing, eMAR 5-rights bedside check, and SBAR shift handovers.
                </p>
              </div>
            </div>
            <div className="pt-6 flex items-center gap-1.5 text-xs font-bold text-teal-600 group-hover:translate-x-1 transition-transform">
              Launch Nursing Console <ArrowRight className="w-4 h-4" />
            </div>
          </Link>

          {/* Card 3: Patient EMR Viewer */}
          <Link
            href="/clinical/emr"
            className="group bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 hover:shadow-xl hover:border-indigo-500 transition-all flex flex-col justify-between"
          >
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 transition-colors">
                  Patient EMR Chart Viewer
                </h3>
                <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">
                  Longitudinal chart viewer with patient selector, allergy severity grading (Mild to Anaphylaxis), active medications, past consultations, and versioned addenda audit trails.
                </p>
              </div>
            </div>
            <div className="pt-6 flex items-center gap-1.5 text-xs font-bold text-indigo-600 group-hover:translate-x-1 transition-transform">
              Open Patient EMR Chart <ArrowRight className="w-4 h-4" />
            </div>
          </Link>

        </div>
      </main>
    </div>
  );
}
