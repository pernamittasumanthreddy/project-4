'use client';
import React from 'react';
import { X, HelpCircle, Phone, Flame, Heart, AlertTriangle, Building2, ShieldCheck } from 'lucide-react';

interface HospitalHelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const HospitalHelpModal: React.FC<HospitalHelpModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in duration-100">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-lg overflow-hidden text-slate-800 text-xs">
        {/* Header */}
        <div className="p-4 bg-slate-900 text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-blue-400" />
            <h3 className="font-bold text-sm">CityCare Hospital Emergency & Clinical Directory</h3>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white rounded">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-5 space-y-4 max-h-[80vh] overflow-y-auto">
          {/* Emergency Codes */}
          <div>
            <h4 className="font-bold text-slate-900 uppercase tracking-wider text-[11px] mb-2 flex items-center gap-1.5 text-rose-700">
              <Flame className="w-4 h-4 text-rose-600" /> Emergency Codes (Dial 4444)
            </h4>
            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div className="p-2.5 rounded-lg bg-rose-50 border border-rose-200">
                <strong className="text-rose-900 block font-bold">CODE BLUE</strong>
                <span className="text-slate-600">Cardiac / Respiratory Arrest (Ext 4444)</span>
              </div>
              <div className="p-2.5 rounded-lg bg-red-50 border border-red-200">
                <strong className="text-red-900 block font-bold">CODE RED</strong>
                <span className="text-slate-600">Fire & Smoke Alarm (Ext 5555)</span>
              </div>
              <div className="p-2.5 rounded-lg bg-amber-50 border border-amber-200">
                <strong className="text-amber-900 block font-bold">TRAUMA ALPHA</strong>
                <span className="text-slate-600">Mass Casualty / Severe Trauma (Ext 2222)</span>
              </div>
              <div className="p-2.5 rounded-lg bg-purple-50 border border-purple-200">
                <strong className="text-purple-900 block font-bold">CODE PINK</strong>
                <span className="text-slate-600">Infant / Pediatric Security (Ext 8888)</span>
              </div>
            </div>
          </div>

          {/* Clinical Extensions */}
          <div>
            <h4 className="font-bold text-slate-900 uppercase tracking-wider text-[11px] mb-2 flex items-center gap-1.5 text-blue-700">
              <Phone className="w-4 h-4 text-blue-600" /> Internal Department Extensions
            </h4>
            <div className="divide-y divide-slate-100 bg-slate-50 rounded-lg p-2.5 border border-slate-200">
              <div className="flex justify-between py-1">
                <span className="text-slate-600">Central Trauma Bay</span>
                <strong className="font-mono text-slate-900">Ext. 2001</strong>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-600">Inpatient Pharmacy STAT Dispensing</span>
                <strong className="font-mono text-slate-900">Ext. 3012</strong>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-600">Core Pathology & Panic Values Lab</span>
                <strong className="font-mono text-slate-900">Ext. 4055</strong>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-600">Diagnostic CT / MRI Workstation</span>
                <strong className="font-mono text-slate-900">Ext. 5100</strong>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-600">Bedside Telemetry Nursing Station 3A</span>
                <strong className="font-mono text-slate-900">Ext. 3104</strong>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-600">Clinical IT / EMR Help Desk</span>
                <strong className="font-mono text-slate-900">Ext. 7000</strong>
              </div>
            </div>
          </div>

          {/* Campus Navigation */}
          <div>
            <h4 className="font-bold text-slate-900 uppercase tracking-wider text-[11px] mb-2 flex items-center gap-1.5 text-slate-700">
              <Building2 className="w-4 h-4 text-slate-600" /> Central Campus Directory
            </h4>
            <p className="text-slate-600 text-[11px] leading-relaxed">
              <strong>Ground Floor:</strong> Trauma Bay, Triage, Outpatient Admissions, Central Pharmacy<br />
              <strong>Floor 2:</strong> Pediatric Pavilion, Intensive Care Unit (ICU)<br />
              <strong>Floor 3:</strong> Cardiovascular Institute & Telemetry Step-Down Units 3A–3D<br />
              <strong>Floor 4:</strong> Surgical Tower & Neurology Institute<br />
              <strong>Basement L1 & L2:</strong> Diagnostic Radiology (CT/MRI/PET) & Pathology Core Labs
            </p>
          </div>
        </div>

        <div className="p-3 bg-slate-50 border-t border-slate-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold"
          >
            Close Directory
          </button>
        </div>
      </div>
    </div>
  );
};
