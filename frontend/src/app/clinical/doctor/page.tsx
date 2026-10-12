'use client';
import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Stethoscope } from 'lucide-react';
import { DoctorWorkspace } from '@/components/clinical/DoctorWorkspace';

export default function DoctorWorkspacePage() {
  return (
    <div className="min-h-screen bg-slate-100 dark:bg-[#0B1120] text-slate-800 dark:text-slate-100">
      <header className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-slate-800 px-6 py-3 flex items-center justify-between sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <Link
            href="/clinical"
            className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-blue-600 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Clinical Portal
          </Link>
          <div className="h-4 w-px bg-slate-300 dark:bg-slate-700" />
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 rounded-lg">
              <Stethoscope className="w-4 h-4" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-slate-900 dark:text-white leading-tight">
                Doctor Workstation (EMR / SOAP / e-Prescriptions)
              </h1>
              <p className="text-[11px] text-slate-500 leading-tight">Member 3 Clinical Management • Multi-Tenant SaaS</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link
            href="/clinical/nursing"
            className="text-xs font-medium text-slate-600 hover:text-blue-600 px-2.5 py-1"
          >
            Nursing Station →
          </Link>
          <Link
            href="/clinical/emr"
            className="text-xs font-medium text-slate-600 hover:text-blue-600 px-2.5 py-1"
          >
            Patient EMR →
          </Link>
          <a
            href="http://localhost:8000/api/docs/"
            target="_blank"
            rel="noreferrer"
            className="text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 px-3 py-1.5 rounded-lg shadow-2xs"
          >
            Swagger API Docs ↗
          </a>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        <DoctorWorkspace />
      </main>
    </div>
  );
}
