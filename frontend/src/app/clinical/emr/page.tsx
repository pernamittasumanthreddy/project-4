'use client';
import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, FileText, User } from 'lucide-react';
import { PatientEMRViewer } from '@/components/clinical/PatientEMRViewer';
import { SEED_PATIENTS } from '@/lib/data/mockDatabase';
import { Patient } from '@/lib/types/hms';

export default function PatientEMRPage() {
  const [selectedPatient, setSelectedPatient] = useState<Patient>(SEED_PATIENTS[0]);

  return (
    <div className="min-h-screen bg-slate-100 dark:bg-[#0B1120] text-slate-800 dark:text-slate-100">
      <header className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-slate-800 px-6 py-3 flex items-center justify-between sticky top-0 z-30">
        <div className="flex items-center gap-3">
          <Link
            href="/clinical"
            className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-indigo-600 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Clinical Portal
          </Link>
          <div className="h-4 w-px bg-slate-300 dark:bg-slate-700" />
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 rounded-lg">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-slate-900 dark:text-white leading-tight">
                Longitudinal Patient EMR Chart Viewer
              </h1>
              <p className="text-[11px] text-slate-500 leading-tight">Member 3 Clinical Management • Multi-Tenant SaaS</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Patient Selector */}
          <div className="flex items-center gap-1.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1">
            <User className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={selectedPatient.id}
              onChange={(e) => {
                const found = SEED_PATIENTS.find(p => p.id === e.target.value);
                if (found) setSelectedPatient(found);
              }}
              className="bg-transparent text-xs font-medium text-slate-700 dark:text-slate-200 focus:outline-none"
            >
              {SEED_PATIENTS.map(p => (
                <option key={p.id} value={p.id} className="dark:bg-slate-900">
                  {p.firstName} {p.lastName} ({p.mrn})
                </option>
              ))}
            </select>
          </div>

          <Link
            href="/clinical/doctor"
            className="text-xs font-medium text-slate-600 hover:text-indigo-600 px-2 py-1"
          >
            Doctor Workspace →
          </Link>
          <Link
            href="/clinical/nursing"
            className="text-xs font-medium text-slate-600 hover:text-indigo-600 px-2 py-1"
          >
            Nursing Station →
          </Link>
          <a
            href="http://localhost:8000/api/docs/"
            target="_blank"
            rel="noreferrer"
            className="text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 px-3 py-1.5 rounded-lg shadow-2xs"
          >
            Swagger API Docs ↗
          </a>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        <PatientEMRViewer patient={selectedPatient} />
      </main>
    </div>
  );
}
