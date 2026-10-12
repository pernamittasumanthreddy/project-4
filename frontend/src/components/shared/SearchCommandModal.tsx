'use client';
import React, { useState, useEffect, useRef } from 'react';
import { 
  Search, X, User, Stethoscope, Calendar, FileText, 
  FlaskConical, Scan, ArrowRight, ShieldCheck, Sparkles 
} from 'lucide-react';
import { SEED_PATIENTS, SAMPLE_DOCTORS, SAMPLE_APPOINTMENTS, DEPARTMENTS } from '@/lib/data/mockDatabase';
import { HOSPITAL_DOCUMENTS } from '@/lib/data/hospitalDocuments';
import { Patient } from '@/lib/types/hms';
import { HospitalDocument } from '@/lib/types/rag';

interface SearchCommandModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectPatient: (patient: Patient) => void;
  onSelectDocument: (doc: HospitalDocument) => void;
}

export const SearchCommandModal: React.FC<SearchCommandModalProps> = ({
  isOpen,
  onClose,
  onSelectPatient,
  onSelectDocument,
}) => {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  // Handle Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!isOpen) return null;

  const q = query.toLowerCase().trim();

  // Search Results
  const matchedPatients = SEED_PATIENTS.filter(p => 
    !q || 
    p.firstName.toLowerCase().includes(q) || 
    p.lastName.toLowerCase().includes(q) || 
    p.mrn.toLowerCase().includes(q) || 
    p.assignedDoctorName.toLowerCase().includes(q)
  ).slice(0, 4);

  const matchedDoctors = SAMPLE_DOCTORS.filter(d => 
    !q || 
    d.name.toLowerCase().includes(q) || 
    d.department.toLowerCase().includes(q) || 
    d.specialty.toLowerCase().includes(q)
  ).slice(0, 3);

  const matchedAppointments = SAMPLE_APPOINTMENTS.filter(a => 
    !q || 
    a.patientName.toLowerCase().includes(q) || 
    a.doctorName.toLowerCase().includes(q) || 
    a.department.toLowerCase().includes(q)
  ).slice(0, 3);

  const matchedDocs = HOSPITAL_DOCUMENTS.filter(doc => 
    !q || 
    doc.title.toLowerCase().includes(q) || 
    doc.category.toLowerCase().includes(q) || 
    doc.department.toLowerCase().includes(q)
  ).slice(0, 4);

  const totalResults = matchedPatients.length + matchedDoctors.length + matchedAppointments.length + matchedDocs.length;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in duration-100">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden text-slate-800 flex flex-col max-h-[80vh]">
        
        {/* Search Input Bar */}
        <div className="p-4 border-b border-slate-200 flex items-center gap-3 bg-slate-50">
          <Search className="w-5 h-5 text-slate-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search patients by name or MRN, doctors, documents, appointments..."
            className="w-full bg-transparent border-none text-sm text-slate-900 placeholder:text-slate-400 focus:outline-hidden"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="p-1 text-slate-400 hover:text-slate-600 rounded"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          <kbd className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-mono bg-white border border-slate-200 rounded text-slate-500 shadow-2xs">
            ESC to close
          </kbd>
        </div>

        {/* Results List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs divide-y divide-slate-100">
          
          {totalResults === 0 && (
            <div className="text-center py-8 text-slate-400">
              <Search className="w-8 h-8 mx-auto mb-2 opacity-40" />
              <p className="font-semibold text-slate-600">No matching hospital records found</p>
              <p className="text-[11px] mt-0.5">Try searching for &quot;Anderson&quot;, &quot;Cardiology&quot;, &quot;MRN-884920&quot;, or &quot;Infection&quot;</p>
            </div>
          )}

          {/* Group: Patients */}
          {matchedPatients.length > 0 && (
            <div className="pt-2">
              <div className="px-2 pb-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <User className="w-3.5 h-3.5 text-blue-600" />
                <span>Patients ({matchedPatients.length})</span>
              </div>
              <div className="space-y-1">
                {matchedPatients.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => {
                      onSelectPatient(p);
                      onClose();
                    }}
                    className="w-full text-left p-2.5 rounded-lg hover:bg-blue-50/70 border border-transparent hover:border-blue-100 transition-all flex items-center justify-between group"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <strong className="text-slate-900 group-hover:text-blue-700 text-xs">
                          {p.firstName} {p.lastName}
                        </strong>
                        <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                          {p.mrn}
                        </span>
                        <span className="text-[11px] text-slate-500">{p.age}y • {p.gender}</span>
                      </div>
                      <p className="text-[11px] text-slate-500 mt-0.5">
                        Ward: {p.currentWard || 'Outpatient'} • Attending: {p.assignedDoctorName}
                      </p>
                    </div>
                    <span className="text-[11px] font-semibold text-blue-600 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      Open EMR <ArrowRight className="w-3 h-3" />
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Group: Doctors */}
          {matchedDoctors.length > 0 && (
            <div className="pt-3">
              <div className="px-2 pb-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Stethoscope className="w-3.5 h-3.5 text-teal-600" />
                <span>Doctors & Attending Clinicians ({matchedDoctors.length})</span>
              </div>
              <div className="space-y-1">
                {matchedDoctors.map((doc) => (
                  <div
                    key={doc.id}
                    className="p-2.5 rounded-lg hover:bg-slate-50 border border-transparent flex items-center justify-between"
                  >
                    <div>
                      <strong className="text-slate-900 text-xs block">{doc.name}</strong>
                      <span className="text-[11px] text-slate-500">{doc.department} • {doc.specialty}</span>
                    </div>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-100">
                      {doc.onDuty ? 'On Duty' : 'Consulting'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Group: Documents & Policies */}
          {matchedDocs.length > 0 && (
            <div className="pt-3">
              <div className="px-2 pb-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-purple-600" />
                <span>Hospital Policies & SOPs ({matchedDocs.length})</span>
              </div>
              <div className="space-y-1">
                {matchedDocs.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => {
                      onSelectDocument(d);
                      onClose();
                    }}
                    className="w-full text-left p-2.5 rounded-lg hover:bg-purple-50/70 border border-transparent hover:border-purple-100 transition-all flex items-center justify-between group"
                  >
                    <div>
                      <strong className="text-slate-900 group-hover:text-purple-700 text-xs block">
                        {d.title}
                      </strong>
                      <span className="text-[11px] text-slate-500">
                        {d.category} • Dept: {d.department} • ID: {d.id}
                      </span>
                    </div>
                    <span className="text-[11px] font-semibold text-purple-600 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      View SOP <ArrowRight className="w-3 h-3" />
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Group: Appointments */}
          {matchedAppointments.length > 0 && (
            <div className="pt-3">
              <div className="px-2 pb-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-amber-600" />
                <span>Today&apos;s Appointments ({matchedAppointments.length})</span>
              </div>
              <div className="space-y-1">
                {matchedAppointments.map((a) => (
                  <div
                    key={a.id}
                    className="p-2.5 rounded-lg hover:bg-slate-50 border border-transparent flex items-center justify-between"
                  >
                    <div>
                      <strong className="text-slate-900 text-xs block">{a.patientName} with {a.doctorName}</strong>
                      <span className="text-[11px] text-slate-500">{a.department} • {a.date} at {a.time}</span>
                    </div>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-100">
                      {a.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* Footer shortcuts */}
        <div className="p-3 bg-slate-50 border-t border-slate-200 text-[11px] text-slate-500 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <span>Press <kbd className="font-mono bg-white border border-slate-200 px-1 py-0.5 rounded text-slate-600 font-bold">↵</kbd> to select</span>
            <span>Use <kbd className="font-mono bg-white border border-slate-200 px-1 py-0.5 rounded text-slate-600 font-bold">ESC</kbd> to dismiss</span>
          </div>
          <span className="font-semibold text-slate-700">CityCare Global Index</span>
        </div>
      </div>
    </div>
  );
};
