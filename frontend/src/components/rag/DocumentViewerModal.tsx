'use client';
import React from 'react';
import { HospitalDocument } from '@/lib/types/rag';
import { X, FileText, Calendar, Building, ShieldCheck, Download, Layers } from 'lucide-react';

interface DocumentViewerModalProps {
  document: HospitalDocument | null;
  onClose: () => void;
}

export const DocumentViewerModal: React.FC<DocumentViewerModalProps> = ({ document, onClose }) => {
  if (!document) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/70 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-100 text-blue-700 rounded-lg">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                  {document.id}
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-medium">
                  {document.version}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded font-semibold ${
                  document.confidentiality === 'CONFIDENTIAL' || document.confidentiality === 'RESTRICTED'
                    ? 'bg-rose-100 text-rose-700'
                    : 'bg-emerald-100 text-emerald-800'
                }`}>
                  {document.confidentiality}
                </span>
              </div>
              <h2 className="text-base font-bold text-slate-900 mt-1">{document.title}</h2>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Metadata Strip */}
        <div className="px-6 py-3 bg-slate-100/60 border-b border-slate-200 text-xs text-slate-600 flex flex-wrap gap-5">
          <div className="flex items-center gap-1.5">
            <Building className="w-3.5 h-3.5 text-slate-400" />
            <span><strong>Department:</strong> {document.department}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-slate-400" />
            <span><strong>Category:</strong> {document.category}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <span><strong>Effective:</strong> {document.effectiveDate}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
            <span><strong>Verified Hospital SOP</strong></span>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {document.sections && document.sections.length > 0 ? (
            document.sections.map((sec, idx) => (
              <div key={idx} className="bg-slate-50 border border-slate-200/80 rounded-xl p-5">
                <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-200">
                  <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    <span className="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs">
                      {idx + 1}
                    </span>
                    {sec.heading}
                  </h4>
                  <span className="text-xs text-slate-400">Page {sec.page}</span>
                </div>
                <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">{sec.text}</p>
              </div>
            ))
          ) : (
            <div className="bg-slate-50 p-6 rounded-xl border border-slate-200">
              <pre className="text-xs font-mono text-slate-700 whitespace-pre-wrap leading-relaxed">{document.content}</pre>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-xs text-slate-500">
          <span>St. Jude Metropolitan Medical Center • Enterprise Document Bureau</span>
          <div className="flex gap-2">
            <button
              onClick={() => alert(`Downloaded copy of ${document.title}`)}
              className="px-3 py-1.5 border border-slate-300 rounded-lg text-slate-700 hover:bg-white flex items-center gap-1.5 transition-colors font-medium"
            >
              <Download className="w-3.5 h-3.5" /> Export PDF
            </button>
            <button
              onClick={onClose}
              className="px-4 py-1.5 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors font-medium"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
