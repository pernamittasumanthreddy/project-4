'use client';
import React, { useState } from 'react';
import { X, Activity, Calendar, FileText, CheckCircle2 } from 'lucide-react';
import { SEED_PATIENTS, SAMPLE_DOCTORS, DEPARTMENTS } from '@/lib/data/mockDatabase';

interface VitalsLoggerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave?: (vitals: any) => void;
}

export const VitalsLoggerModal: React.FC<VitalsLoggerModalProps> = ({ isOpen, onClose, onSave }) => {
  const [selectedPatientId, setSelectedPatientId] = useState(SEED_PATIENTS[0]?.id || '');
  const [sbp, setSbp] = useState('120');
  const [dbp, setDbp] = useState('80');
  const [hr, setHr] = useState('72');
  const [spo2, setSpo2] = useState('98');
  const [temp, setTemp] = useState('98.6');
  const [rr, setRr] = useState('16');
  const [pain, setPain] = useState('0');

  if (!isOpen) return null;

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSave) {
      onSave({
        patientId: selectedPatientId,
        sbp,
        dbp,
        hr,
        spo2,
        temp,
        rr,
        pain,
        timestamp: new Date().toLocaleTimeString(),
      });
    }
    alert('Vitals logged successfully to bedside telemetry flow-sheet!');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in duration-100">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-lg overflow-hidden text-slate-800">
        <div className="p-4 bg-slate-900 text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-400" />
            <h3 className="font-bold text-sm">Bedside Vitals Telemetry Logger</h3>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white rounded">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSave} className="p-5 space-y-4 text-xs">
          <div>
            <label className="font-bold text-slate-700 block mb-1">Select Patient</label>
            <select
              value={selectedPatientId}
              onChange={(e) => setSelectedPatientId(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs"
            >
              {SEED_PATIENTS.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.firstName} {p.lastName} ({p.mrn}) — {p.currentWard || 'Ward'}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-medium text-slate-600 block mb-1">Systolic BP (mmHg)</label>
              <input
                type="number"
                value={sbp}
                onChange={(e) => setSbp(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg font-mono"
                required
              />
            </div>
            <div>
              <label className="font-medium text-slate-600 block mb-1">Diastolic BP (mmHg)</label>
              <input
                type="number"
                value={dbp}
                onChange={(e) => setDbp(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg font-mono"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="font-medium text-slate-600 block mb-1">Heart Rate (bpm)</label>
              <input
                type="number"
                value={hr}
                onChange={(e) => setHr(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg font-mono"
                required
              />
            </div>
            <div>
              <label className="font-medium text-slate-600 block mb-1">SpO₂ (%)</label>
              <input
                type="number"
                value={spo2}
                onChange={(e) => setSpo2(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg font-mono"
                required
              />
            </div>
            <div>
              <label className="font-medium text-slate-600 block mb-1">Temp (°F)</label>
              <input
                type="text"
                value={temp}
                onChange={(e) => setTemp(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg font-mono"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-medium text-slate-600 block mb-1">Resp Rate (/min)</label>
              <input
                type="number"
                value={rr}
                onChange={(e) => setRr(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg font-mono"
                required
              />
            </div>
            <div>
              <label className="font-medium text-slate-600 block mb-1">Pain Scale (0 - 10)</label>
              <input
                type="number"
                min="0"
                max="10"
                value={pain}
                onChange={(e) => setPain(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg font-mono"
                required
              />
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold shadow-2xs"
            >
              Sign & Save Vitals
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

interface AppointmentSchedulerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onBook?: (appt: any) => void;
}

export const AppointmentSchedulerModal: React.FC<AppointmentSchedulerModalProps> = ({ isOpen, onClose, onBook }) => {
  const [patientId, setPatientId] = useState(SEED_PATIENTS[0]?.id || '');
  const [doctorId, setDoctorId] = useState(SAMPLE_DOCTORS[0]?.id || '');
  const [date, setDate] = useState('2026-10-05');
  const [time, setTime] = useState('09:30');
  const [type, setType] = useState('Consultation');
  const [notes, setNotes] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onBook) {
      onBook({ patientId, doctorId, date, time, type, notes });
    }
    alert('Appointment successfully booked and synced to clinic master schedule!');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in duration-100">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-lg overflow-hidden text-slate-800">
        <div className="p-4 bg-slate-900 text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Calendar className="w-5 h-5 text-blue-400" />
            <h3 className="font-bold text-sm">Schedule Clinical Appointment</h3>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white rounded">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4 text-xs">
          <div>
            <label className="font-bold text-slate-700 block mb-1">Select Patient</label>
            <select
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs"
            >
              {SEED_PATIENTS.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.firstName} {p.lastName} ({p.mrn})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="font-bold text-slate-700 block mb-1">Select Clinician / Attending</label>
            <select
              value={doctorId}
              onChange={(e) => setDoctorId(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs"
            >
              {SAMPLE_DOCTORS.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name} — {d.department} ({d.specialty})
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-medium text-slate-600 block mb-1">Appointment Date</label>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs"
                required
              />
            </div>
            <div>
              <label className="font-medium text-slate-600 block mb-1">Time Slot</label>
              <select
                value={time}
                onChange={(e) => setTime(e.target.value)}
                className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs"
              >
                <option value="08:30">08:30 AM</option>
                <option value="09:00">09:00 AM</option>
                <option value="09:30">09:30 AM</option>
                <option value="10:00">10:00 AM</option>
                <option value="10:30">10:30 AM</option>
                <option value="11:00">11:00 AM</option>
                <option value="14:00">02:00 PM</option>
                <option value="15:00">03:00 PM</option>
              </select>
            </div>
          </div>

          <div>
            <label className="font-medium text-slate-600 block mb-1">Visit Type</label>
            <select
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs"
            >
              <option value="Consultation">New Patient Consultation</option>
              <option value="Follow-up">Clinical Follow-up</option>
              <option value="Post-Op Review">Post-Op Review</option>
              <option value="Annual Physical">Comprehensive Physical Exam</option>
            </select>
          </div>

          <div>
            <label className="font-medium text-slate-600 block mb-1">Chief Complaint / Reason for Visit</label>
            <input
              type="text"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="e.g. Chest tightness on exertion, routine diabetes follow-up..."
              className="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs"
            />
          </div>

          <div className="pt-3 border-t border-slate-100 flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold shadow-2xs"
            >
              Confirm Appointment
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
