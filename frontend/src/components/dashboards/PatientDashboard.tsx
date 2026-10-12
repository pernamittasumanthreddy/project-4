'use client';
import React, { useState } from 'react';
import { StatCard } from '../shared/StatCard';
import { StatusBadge } from '../shared/StatusBadge';
import { 
  Heart, Calendar, FileText, Pill, CreditCard, 
  UserCheck, ShieldCheck, Download, AlertCircle, Clock, 
  Activity, Phone, MessageSquare, Plus, Receipt, Sparkles 
} from 'lucide-react';
import { SEED_PATIENTS, SAMPLE_LAB_TESTS, SAMPLE_PRESCRIPTIONS, SAMPLE_INVOICES, SAMPLE_CLAIMS } from '@/lib/data/mockDatabase';

interface PatientDashboardProps {
  onOpenRAG: () => void;
  onOpenDoc: (doc: any) => void;
  activeNav?: string;
  setActiveNav?: (nav: string) => void;
}

export const PatientDashboard: React.FC<PatientDashboardProps> = ({ 
  onOpenRAG, 
  onOpenDoc,
  activeNav = 'dashboard',
  setActiveNav
}) => {
  const patient = SEED_PATIENTS[0]; // John Anderson
  const labs = SAMPLE_LAB_TESTS.filter(l => l.patientId === patient.id);
  const prescriptions = SAMPLE_PRESCRIPTIONS.filter(p => p.patientId === patient.id);
  const invoice = SAMPLE_INVOICES[0];
  const claims = SAMPLE_CLAIMS.filter(c => c.patientId === patient.id);

  return (
    <div className="space-y-6 max-w-5xl mx-auto text-slate-800">
      {/* Top Patient Header Bar */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center gap-1">
              <Heart className="w-3.5 h-3.5 text-emerald-600" /> Patient Health Home
            </span>
            <span className="text-xs text-slate-500">CityCare Multi-Speciality Hospital • Central Campus</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-slate-900">Welcome, {patient.firstName} {patient.lastName}</h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Medical Record Number: <strong className="font-mono text-slate-900">{patient.mrn}</strong> • Attending Physician: <strong className="text-slate-900">{patient.assignedDoctorName}</strong>
          </p>
        </div>

        <div className="flex items-center gap-2">
          {setActiveNav && (
            <div className="hidden sm:flex bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
              {(['dashboard', 'records', 'prescriptions', 'bills'] as const).map(n => (
                <button
                  key={n}
                  onClick={() => setActiveNav(n)}
                  className={`px-2.5 py-1 rounded-md font-semibold capitalize transition-all ${
                    activeNav === n ? 'bg-white text-emerald-800 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {n === 'dashboard' ? 'My Health Home' : n === 'records' ? 'Medical Records' : n === 'prescriptions' ? 'Medications' : 'Bills & Insurance'}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={onOpenRAG}
            className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-2xs transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5" /> Ask Hospital Assistant
          </button>
        </div>
      </div>

      {/* Patient Action Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-3">
          Patient Self-Service Actions
        </span>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2 text-xs font-semibold">
          <button
            onClick={() => alert('Opening Online Appointment Booking')}
            className="p-2.5 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-800 border border-blue-200 flex flex-col items-center justify-center gap-1 transition-colors"
          >
            <Calendar className="w-4 h-4 text-blue-600" />
            <span>Book Visit</span>
          </button>
          <button
            onClick={() => alert('Downloading latest Lab & Diagnostic PDF Summary')}
            className="p-2.5 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 flex flex-col items-center justify-center gap-1 transition-colors"
          >
            <Download className="w-4 h-4 text-teal-600" />
            <span>Download Report</span>
          </button>
          <button
            onClick={() => alert('Viewing Active Digital Prescriptions with Barcodes')}
            className="p-2.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 flex flex-col items-center justify-center gap-1 transition-colors"
          >
            <Pill className="w-4 h-4 text-amber-600" />
            <span>My Prescriptions</span>
          </button>
          <button
            onClick={() => alert('Opening Secure Patient Co-Pay Gateway')}
            className="p-2.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 flex flex-col items-center justify-center gap-1 transition-colors"
          >
            <CreditCard className="w-4 h-4 text-emerald-600" />
            <span>Pay Hospital Bill</span>
          </button>
          <button
            onClick={() => alert('Dialing Hospital Main Help Line: +1 (555) 234-8800')}
            className="p-2.5 rounded-lg bg-slate-50 hover:bg-slate-100 text-slate-800 border border-slate-200 flex flex-col items-center justify-center gap-1 transition-colors"
          >
            <Phone className="w-4 h-4 text-slate-600" />
            <span>Call Clinic</span>
          </button>
          <button
            onClick={onOpenRAG}
            className="p-2.5 rounded-lg bg-purple-50 hover:bg-purple-100 text-purple-800 border border-purple-200 flex flex-col items-center justify-center gap-1 transition-colors"
          >
            <MessageSquare className="w-4 h-4 text-purple-600" />
            <span>Ask Assistant</span>
          </button>
        </div>
      </div>

      {/* KPI Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Care Location"
          value="Inpatient Unit"
          subtitle="Bed 304-B (Cardiac Step-Down)"
          icon={Heart}
          variant="emerald"
        />
        <StatCard
          title="Next Doctor Visit"
          value="Today 08:30"
          subtitle="Dr. Marcus Vance, MD"
          icon={Calendar}
          variant="blue"
        />
        <StatCard
          title="Active Medications"
          value="4 Medicines"
          subtitle="Scheduled by pharmacy"
          icon={Pill}
          variant="amber"
        />
        <StatCard
          title="Insurance Approved"
          value="80% Covered"
          subtitle="Blue Cross Blue Shield"
          icon={ShieldCheck}
          variant="purple"
        />
      </div>

      {/* Health Metrics & Upcoming Care */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Vitals Summary */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
          <h3 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100 flex items-center justify-between">
            <span>Recent Health Vitals</span>
            <span className="text-xs font-mono text-emerald-700 font-bold">Stable</span>
          </h3>
          <div className="grid grid-cols-3 gap-2.5 text-center text-xs">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span className="text-[11px] text-slate-500 block">Blood Pressure</span>
              <strong className="text-sm font-bold font-mono text-slate-900 block mt-0.5">124 / 82</strong>
              <span className="text-[10px] text-emerald-600 font-semibold">Normal</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span className="text-[11px] text-slate-500 block">Pulse Rate</span>
              <strong className="text-sm font-bold font-mono text-slate-900 block mt-0.5">72 bpm</strong>
              <span className="text-[10px] text-emerald-600 font-semibold">Resting regular</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <span className="text-[11px] text-slate-500 block">Oxygen Level</span>
              <strong className="text-sm font-bold font-mono text-slate-900 block mt-0.5">98%</strong>
              <span className="text-[10px] text-emerald-600 font-semibold">Room air</span>
            </div>
          </div>
        </div>

        {/* Emergency Contact & My Doctor */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3 text-xs">
          <h3 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100">
            Care Team & Emergency Contact
          </h3>
          <div className="space-y-2">
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Attending Physician</span>
              <strong className="text-slate-900">{patient.assignedDoctorName}</strong>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Assigned Nurse</span>
              <strong className="text-slate-900">Sarah Jenkins, BSN, RN</strong>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Emergency Contact</span>
              <strong className="text-slate-900">{patient.emergencyContact.name} ({patient.emergencyContact.relationship})</strong>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-500">Emergency Phone</span>
              <strong className="font-mono text-slate-900">{patient.emergencyContact.phone}</strong>
            </div>
          </div>
        </div>
      </div>

      {/* VIEW: MEDICATIONS */}
      {(activeNav === 'dashboard' || activeNav === 'prescriptions') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">My Daily Medications</h3>
              <p className="text-xs text-slate-500">Active prescriptions with plain-language instructions</p>
            </div>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              Verified by Pharmacy
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <strong className="text-slate-900 text-sm block">Ticagrelor (Brilinta) 90 mg</strong>
              <p className="text-slate-600">Take 1 tablet twice daily with or without food. Prevents blood clots around stent.</p>
              <span className="text-[11px] font-mono text-blue-700 block pt-1">Morning & Evening • With water</span>
            </div>
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <strong className="text-slate-900 text-sm block">Atorvastatin 40 mg</strong>
              <p className="text-slate-600">Take 1 tablet daily at bedtime. Lowers cholesterol and protects heart blood vessels.</p>
              <span className="text-[11px] font-mono text-blue-700 block pt-1">Nightly at 09:00 PM</span>
            </div>
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <strong className="text-slate-900 text-sm block">Aspirin 81 mg (Baby Aspirin)</strong>
              <p className="text-slate-600">Take 1 tablet once daily in the morning with food.</p>
              <span className="text-[11px] font-mono text-blue-700 block pt-1">Morning with breakfast</span>
            </div>
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <strong className="text-slate-900 text-sm block">Metoprolol Succinate 50 mg</strong>
              <p className="text-slate-600">Take 1 tablet once daily in the morning. Keeps heart rate steady.</p>
              <span className="text-[11px] font-mono text-blue-700 block pt-1">Morning at 08:00 AM</span>
            </div>
          </div>
        </div>
      )}

      {/* VIEW: BILLS & INSURANCE */}
      {(activeNav === 'bills' || activeNav === 'dashboard') && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4 text-xs">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hospital Account Summary & Insurance Claims</h3>
              <p className="text-xs text-slate-500">Transparent cost summary for your current hospital stay</p>
            </div>
            <button
              onClick={() => alert('Online card payment simulation: Payment successful!')}
              className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold shadow-2xs"
            >
              Pay Outstanding Co-Pay ($650.00)
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 block">Total Hospital Care Cost</span>
              <strong className="text-xl font-mono text-slate-900 block mt-1">$3,450.00</strong>
              <span className="text-[11px] text-slate-500">Room, procedures & medications</span>
            </div>
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 block">Paid by Blue Cross Shield</span>
              <strong className="text-xl font-mono text-emerald-700 block mt-1">-$2,800.00</strong>
              <span className="text-[11px] text-emerald-600 font-semibold">80% In-Network Coverage</span>
            </div>
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 block">Your Remaining Balance</span>
              <strong className="text-xl font-mono text-blue-700 block mt-1">$650.00</strong>
              <span className="text-[11px] text-slate-500">Due within 30 days of discharge</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
