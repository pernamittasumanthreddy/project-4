'use client';
import React, { useState, useEffect } from 'react';
import { 
  Heart, Activity, CheckSquare, Clock, AlertTriangle, 
  Bed, Pill, ShieldCheck, Thermometer, UserCheck, 
  Plus, CheckCircle2, FileText, ArrowRight, ShieldAlert, 
  ChevronRight, PhoneCall, Droplets, RefreshCw, AlertCircle,
  Eye, Check
} from 'lucide-react';
import { 
  NursingObservation, 
  FluidBalanceRecord, 
  EMARRecord, 
  SBARHandoverNote 
} from '@/lib/types/clinical';
import { Patient } from '@/lib/types/hms';
import { SEED_PATIENTS } from '@/lib/data/mockDatabase';
import { clinicalStore } from '@/lib/data/clinicalStore';
import { StatusBadge } from '../shared/StatusBadge';

interface NursingStationConsoleProps {
  onOpenDoc?: (doc: any) => void;
  onOpenRAG?: () => void;
  onSelectPatient?: (patient: Patient) => void;
}

export const NursingStationConsole: React.FC<NursingStationConsoleProps> = ({
  onOpenDoc,
  onOpenRAG,
  onSelectPatient
}) => {
  // Navigation tabs
  const [activeTab, setActiveTab] = useState<'vitals' | 'fluid' | 'emar' | 'sbar'>('vitals');
  const [selectedPatientId, setSelectedPatientId] = useState<string>('PT-10023');

  // Observations State
  const [observations, setObservations] = useState<NursingObservation[]>([]);
  const [newSystolic, setNewSystolic] = useState('124');
  const [newDiastolic, setNewDiastolic] = useState('80');
  const [newHeartRate, setNewHeartRate] = useState('72');
  const [newRespRate, setNewRespRate] = useState('16');
  const [newSpo2, setNewSpo2] = useState('98');
  const [newTemp, setNewTemp] = useState('98.6');
  const [newPain, setNewPain] = useState('0');
  const [newAvpu, setNewAvpu] = useState<'Alert' | 'Voice' | 'Pain' | 'Unresponsive'>('Alert');
  const [newInterventions, setNewInterventions] = useState('Routine morning vital assessment. Patient resting comfortably.');
  const [mewsAlertBanner, setMewsAlertBanner] = useState<string | null>(null);

  // Fluid Balance State
  const [fluidBalances, setFluidBalances] = useState<FluidBalanceRecord[]>([]);
  const [oralIntake, setOralIntake] = useState('350');
  const [ivInfusion, setIvInfusion] = useState('500');
  const [urineOutput, setUrineOutput] = useState('450');
  const [surgicalDrain, setSurgicalDrain] = useState('0');
  const [fluidNotes, setFluidNotes] = useState('IV 0.9% Normal Saline at 75 mL/hr. Good spontaneous voiding.');

  // eMAR State
  const [emarRecords, setEmarRecords] = useState<EMARRecord[]>([]);
  const [administeringModalId, setAdministeringModalId] = useState<string | null>(null);
  const [witnessNurseName, setWitnessNurseName] = useState('Lisa Morales, RN');

  // SBAR State
  const [sbarNotes, setSbarNotes] = useState<SBARHandoverNote[]>([]);
  const [sbarSituation, setSbarSituation] = useState('');
  const [sbarBackground, setSbarBackground] = useState('');
  const [sbarAssessment, setSbarAssessment] = useState('');
  const [sbarRecommendation, setSbarRecommendation] = useState('');
  const [sbarCodeStatus, setSbarCodeStatus] = useState<'Full Code' | 'DNR / DNI'>('Full Code');

  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  const reloadData = () => {
    setObservations(clinicalStore.getNursingObservations());
    setFluidBalances(clinicalStore.getFluidBalances());
    setEmarRecords(clinicalStore.getEMARRecords());
    setSbarNotes(clinicalStore.getSBARNotes());
  };

  useEffect(() => {
    reloadData();
  }, []);

  const activePatient = SEED_PATIENTS.find(p => p.id === selectedPatientId) || SEED_PATIENTS[0];
  const patientObservations = observations.filter(o => o.patientId === selectedPatientId);
  const patientFluids = fluidBalances.filter(f => f.patientId === selectedPatientId);
  const patientEmar = emarRecords.filter(e => e.patientId === selectedPatientId);
  const patientSbar = sbarNotes.filter(s => s.patientId === selectedPatientId);

  // Record Vital Signs and Automated MEWS
  const handleRecordVitals = (e: React.FormEvent) => {
    e.preventDefault();

    const created = clinicalStore.recordNursingObservation({
      patientId: selectedPatientId,
      patientName: `${activePatient.firstName} ${activePatient.lastName}`,
      mrn: activePatient.mrn,
      ward: activePatient.currentWard || 'Cardiac Step-Down Unit 3A',
      bed: activePatient.currentBed || 'Bed 304-B',
      nurseId: 'USR-NUR-04',
      nurseName: 'Sarah Jenkins, BSN, RN',
      systolicBp: parseInt(newSystolic, 10) || 120,
      diastolicBp: parseInt(newDiastolic, 10) || 80,
      heartRate: parseInt(newHeartRate, 10) || 72,
      respiratoryRate: parseInt(newRespRate, 10) || 16,
      spo2: parseInt(newSpo2, 10) || 98,
      temperature: parseFloat(newTemp) || 98.6,
      painScore: parseInt(newPain, 10) || 0,
      gcsScore: 15,
      avpuConsciousness: newAvpu,
      bloodSugarMgDl: 110,
      oxygenDevice: 'Room Air',
      nursingInterventions: newInterventions,
      telemetryRhythm: 'Normal Sinus',
      fallRiskScore: 15,
      bradenSkinScore: 21
    });

    reloadData();
    if (created.mews.score >= 4) {
      setMewsAlertBanner(`CRITICAL MEWS ALERT (${created.mews.score}): ${created.mews.actionRequired}`);
    } else {
      setMewsAlertBanner(null);
      showToast(`Vitals recorded. MEWS Score: ${created.mews.score} (${created.mews.riskCategory})`);
    }
  };

  // Record Fluid Balance
  const handleRecordFluid = (e: React.FormEvent) => {
    e.preventDefault();

    const created = clinicalStore.recordFluidBalance({
      patientId: selectedPatientId,
      patientName: `${activePatient.firstName} ${activePatient.lastName}`,
      ward: activePatient.currentWard || 'Unit 3A',
      bed: activePatient.currentBed || 'Bed 304-B',
      nurseName: 'Sarah Jenkins, RN',
      oralIntakeMl: parseInt(oralIntake, 10) || 0,
      ivInfusionMl: parseInt(ivInfusion, 10) || 0,
      enteralFeedMl: 0,
      bloodProductMl: 0,
      urineOutputMl: parseInt(urineOutput, 10) || 0,
      surgicalDrainMl: parseInt(surgicalDrain, 10) || 0,
      ngAspirateMl: 0,
      emesisMl: 0,
      shift: 'Day',
      cumulative24hBalanceMl: 0,
      notes: fluidNotes
    });

    reloadData();
    showToast(`Fluid shift balance logged. Net: ${created.netBalanceMl > 0 ? '+' : ''}${created.netBalanceMl} mL`);
  };

  // eMAR 5-Rights Administration
  const handleAdministerMedication = (id: string, status: 'Administered' | 'Held' | 'Refused') => {
    try {
      clinicalStore.administerMedication(id, {
        administeredBy: 'Sarah Jenkins, BSN, RN',
        witnessNurse: witnessNurseName,
        status,
        vitalsBeforeAdmin: `BP ${newSystolic}/${newDiastolic}, HR ${newHeartRate}, SpO2 ${newSpo2}%`,
        notes: status === 'Administered' ? 'Verified 5-rights & scanned patient wristband barcode.' : `Medication ${status}.`
      });
      reloadData();
      showToast(`Medication ${status} with 5-Rights compliance.`);
    } catch (err: any) {
      alert(err.message);
    }
  };

  // Record SBAR Handover
  const handleRecordSBAR = (e: React.FormEvent) => {
    e.preventDefault();
    if (!sbarSituation.trim() || !sbarRecommendation.trim()) return;

    clinicalStore.recordSBARHandover({
      patientId: selectedPatientId,
      patientName: `${activePatient.firstName} ${activePatient.lastName}`,
      ward: activePatient.currentWard || 'Unit 3A',
      bed: activePatient.currentBed || 'Bed 304-B',
      fromNurse: 'Sarah Jenkins, BSN, RN',
      toNurse: 'Michael Kelly, RN',
      shift: 'Day to Evening',
      situation: sbarSituation,
      background: sbarBackground,
      assessment: sbarAssessment,
      recommendation: sbarRecommendation,
      codeStatus: sbarCodeStatus,
      keyTasksForNextShift: [
        'Check evening blood glucose',
        'Verify evening Atorvastatin administration',
        'Observe radial catheter puncture site'
      ]
    });

    reloadData();
    setSbarSituation('');
    setSbarRecommendation('');
    showToast('SBAR shift handover note saved.');
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-teal-50 text-teal-700 border border-teal-200 flex items-center gap-1">
              <Heart className="w-3.5 h-3.5 text-teal-600" /> Nurse Station Telemetry & Bedside Console
            </span>
            <span className="text-xs text-slate-500">Unit 3A Telemetry Step-Down • Floor 3</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-slate-900">Sarah Jenkins, BSN, RN (Charge Nurse)</h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Shift: <strong className="text-slate-900">Day (07:00 - 19:00)</strong> • Staffing Ratio: <strong className="text-emerald-700">1:3 (Compliant)</strong>
          </p>
        </div>

        {toastMessage && (
          <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span className="font-medium">{toastMessage}</span>
          </div>
        )}
      </div>

      {/* Critical MEWS Alert Banner */}
      {mewsAlertBanner && (
        <div className="bg-red-50 border-2 border-red-500 rounded-xl p-4 text-red-900 flex items-start gap-3 animate-bounce">
          <ShieldAlert className="w-6 h-6 text-red-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <div className="font-bold text-sm text-red-700">EARLY WARNING CLINICAL DETERIORATION ALERT</div>
            <p className="text-xs mt-0.5 font-medium">{mewsAlertBanner}</p>
          </div>
          <button 
            onClick={() => setMewsAlertBanner(null)}
            className="text-xs font-bold px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Acknowledge
          </button>
        </div>
      )}

      {/* Patient Bedside Census Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {SEED_PATIENTS.slice(0, 3).map(p => {
          const isSelected = selectedPatientId === p.id;
          const patientObs = observations.find(o => o.patientId === p.id);
          const mews = patientObs?.mews;

          return (
            <div
              key={p.id}
              onClick={() => setSelectedPatientId(p.id)}
              className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                isSelected
                  ? 'bg-teal-50/70 border-teal-500 ring-2 ring-teal-500 shadow-2xs'
                  : 'bg-white hover:bg-slate-50 border-slate-200'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-mono text-xs font-bold text-teal-900 bg-teal-100/80 px-2 py-0.5 rounded">
                  {p.currentBed || 'Bed 304-B'}
                </span>
                {mews && (
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    mews.score >= 4 
                      ? 'bg-red-100 text-red-800' 
                      : mews.score >= 2 
                      ? 'bg-amber-100 text-amber-800' 
                      : 'bg-emerald-100 text-emerald-800'
                  }`}>
                    MEWS: {mews.score}
                  </span>
                )}
              </div>

              <div className="font-bold text-xs text-slate-900">{p.firstName} {p.lastName}</div>
              <div className="text-[11px] text-slate-500">{p.mrn} • {p.age}y {p.gender}</div>

              <div className="text-[11px] text-slate-600 mt-2 pt-2 border-t border-slate-100 flex items-center justify-between">
                <span>Rhythm: <strong>{patientObs?.telemetryRhythm || 'Sinus'}</strong></span>
                <span className="text-teal-700 font-semibold">{patientObs?.oxygenDevice || 'Room Air'}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Console Box */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
        
        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-200 bg-slate-50 px-4 gap-2 text-xs overflow-x-auto">
          {[
            { id: 'vitals', label: `Bedside Vitals & MEWS (${patientObservations.length})`, icon: Activity },
            { id: 'fluid', label: `24h Fluid Balance Flowsheet (${patientFluids.length})`, icon: Droplets },
            { id: 'emar', label: `5-Rights eMAR Medication Rounds (${patientEmar.length})`, icon: Pill },
            { id: 'sbar', label: `SBAR Shift Handover Notes (${patientSbar.length})`, icon: FileText },
          ].map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-3 px-3 font-semibold border-b-2 flex items-center gap-1.5 whitespace-nowrap transition-all ${
                  activeTab === tab.id
                    ? 'border-teal-600 text-teal-700 bg-white'
                    : 'border-transparent text-slate-600 hover:text-slate-900'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Tab 1: Bedside Vitals Flowsheet & MEWS */}
        {activeTab === 'vitals' && (
          <div className="p-5 space-y-5 text-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  Continuous Telemetry Flowsheet — {activePatient.firstName} {activePatient.lastName} ({activePatient.mrn})
                </h3>
                <p className="text-slate-500 text-[11px]">
                  Automated Modified Early Warning Score (MEWS) calculated on every entry.
                </p>
              </div>
            </div>

            {/* Vitals History Table */}
            <div className="overflow-x-auto border border-slate-200 rounded-lg">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
                  <tr>
                    <th className="p-2.5">Time</th>
                    <th className="p-2.5">BP (mmHg)</th>
                    <th className="p-2.5">HR (bpm)</th>
                    <th className="p-2.5">RR (/min)</th>
                    <th className="p-2.5">SpO2 (%)</th>
                    <th className="p-2.5">Temp (°F)</th>
                    <th className="p-2.5">Pain</th>
                    <th className="p-2.5">AVPU</th>
                    <th className="p-2.5">MEWS Score</th>
                    <th className="p-2.5">Nurse</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {patientObservations.map(obs => (
                    <tr key={obs.id} className="hover:bg-slate-50/60">
                      <td className="p-2.5 font-mono text-slate-500">{new Date(obs.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
                      <td className="p-2.5 font-semibold text-slate-900">{obs.systolicBp}/{obs.diastolicBp}</td>
                      <td className="p-2.5 font-semibold text-slate-900">{obs.heartRate}</td>
                      <td className="p-2.5 text-slate-700">{obs.respiratoryRate}</td>
                      <td className="p-2.5 font-semibold text-teal-700">{obs.spo2}%</td>
                      <td className="p-2.5 text-slate-700">{obs.temperature}</td>
                      <td className="p-2.5 text-slate-700">{obs.painScore}/10</td>
                      <td className="p-2.5 text-slate-700">{obs.avpuConsciousness}</td>
                      <td className="p-2.5">
                        <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                          obs.mews.score >= 4
                            ? 'bg-red-100 text-red-800'
                            : obs.mews.score >= 2
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-emerald-100 text-emerald-800'
                        }`}>
                          {obs.mews.score} ({obs.mews.riskCategory.split(' ')[0]})
                        </span>
                      </td>
                      <td className="p-2.5 text-slate-600">{obs.nurseName.split(',')[0]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Log Vitals Entry Form */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
              <h4 className="font-bold text-slate-900 mb-3 flex items-center gap-1.5">
                <Plus className="w-4 h-4 text-teal-600" /> Record Bedside Vital Signs
              </h4>

              <form onSubmit={handleRecordVitals} className="space-y-3">
                <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3">
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Systolic BP</label>
                    <input
                      type="number"
                      value={newSystolic}
                      onChange={e => setNewSystolic(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs text-center font-bold"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Diastolic BP</label>
                    <input
                      type="number"
                      value={newDiastolic}
                      onChange={e => setNewDiastolic(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs text-center font-bold"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Heart Rate</label>
                    <input
                      type="number"
                      value={newHeartRate}
                      onChange={e => setNewHeartRate(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs text-center font-bold"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Resp Rate</label>
                    <input
                      type="number"
                      value={newRespRate}
                      onChange={e => setNewRespRate(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs text-center"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">SpO2 (%)</label>
                    <input
                      type="number"
                      value={newSpo2}
                      onChange={e => setNewSpo2(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs text-center font-bold text-teal-700"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Temp (°F)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={newTemp}
                      onChange={e => setNewTemp(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs text-center"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Pain (0-10)</label>
                    <input
                      type="number"
                      min="0"
                      max="10"
                      value={newPain}
                      onChange={e => setNewPain(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs text-center"
                    />
                  </div>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Nursing Interventions & Observations</label>
                  <input
                    type="text"
                    value={newInterventions}
                    onChange={e => setNewInterventions(e.target.value)}
                    className="w-full p-2 rounded border border-slate-300 text-xs"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => {
                      // Trigger high MEWS alert test values
                      setNewSystolic('70');
                      setNewHeartRate('135');
                      setNewRespRate('32');
                      setNewTemp('102.5');
                    }}
                    className="px-2.5 py-1.5 text-[11px] font-semibold text-amber-700 bg-amber-50 hover:bg-amber-100 rounded border border-amber-300"
                  >
                    Simulate Deterioration Alert (High MEWS)
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg font-semibold shadow-2xs"
                  >
                    Save Vitals & Compute MEWS
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Tab 2: 24h Fluid Balance Flowsheet */}
        {activeTab === 'fluid' && (
          <div className="p-5 space-y-5 text-xs">
            <div>
              <h3 className="font-bold text-slate-900 text-sm">
                Strict Fluid Intake & Output (I/O) Reconciliation
              </h3>
              <p className="text-slate-500 text-[11px]">
                Tracks IV infusions, oral liquids, urinary output, and surgical drains to prevent volume overload.
              </p>
            </div>

            {/* Fluid History Table */}
            <div className="overflow-x-auto border border-slate-200 rounded-lg">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
                  <tr>
                    <th className="p-2.5">Timestamp</th>
                    <th className="p-2.5">Shift</th>
                    <th className="p-2.5">Oral (mL)</th>
                    <th className="p-2.5">IV Infusion (mL)</th>
                    <th className="p-2.5">Total Intake</th>
                    <th className="p-2.5">Urine (mL)</th>
                    <th className="p-2.5">Drain (mL)</th>
                    <th className="p-2.5">Total Output</th>
                    <th className="p-2.5">Shift Net</th>
                    <th className="p-2.5">24h Cumulative</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {patientFluids.map(fb => (
                    <tr key={fb.id} className="hover:bg-slate-50/60">
                      <td className="p-2.5 font-mono text-slate-500">{new Date(fb.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
                      <td className="p-2.5 font-semibold text-slate-800">{fb.shift}</td>
                      <td className="p-2.5 text-slate-700">{fb.oralIntakeMl}</td>
                      <td className="p-2.5 text-slate-700">{fb.ivInfusionMl}</td>
                      <td className="p-2.5 font-bold text-blue-700">{fb.totalIntakeMl} mL</td>
                      <td className="p-2.5 text-slate-700">{fb.urineOutputMl}</td>
                      <td className="p-2.5 text-slate-700">{fb.surgicalDrainMl}</td>
                      <td className="p-2.5 font-bold text-amber-700">{fb.totalOutputMl} mL</td>
                      <td className="p-2.5 font-bold">
                        <span className={`px-2 py-0.5 rounded text-[10px] ${
                          fb.netBalanceMl >= 0 ? 'bg-blue-100 text-blue-800' : 'bg-amber-100 text-amber-800'
                        }`}>
                          {fb.netBalanceMl > 0 ? '+' : ''}{fb.netBalanceMl} mL
                        </span>
                      </td>
                      <td className="p-2.5 font-mono font-bold text-slate-900">
                        {fb.cumulative24hBalanceMl > 0 ? '+' : ''}{fb.cumulative24hBalanceMl} mL
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Log Fluid Entry Form */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
              <h4 className="font-bold text-slate-900 mb-3 flex items-center gap-1.5">
                <Droplets className="w-4 h-4 text-teal-600" /> Log Intake & Output Entry
              </h4>

              <form onSubmit={handleRecordFluid} className="space-y-3">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Oral Intake (mL)</label>
                    <input
                      type="number"
                      value={oralIntake}
                      onChange={e => setOralIntake(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs font-bold"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">IV Infusion (mL)</label>
                    <input
                      type="number"
                      value={ivInfusion}
                      onChange={e => setIvInfusion(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs font-bold"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Urine Output (mL)</label>
                    <input
                      type="number"
                      value={urineOutput}
                      onChange={e => setUrineOutput(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs font-bold text-amber-700"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Surgical Drain (mL)</label>
                    <input
                      type="number"
                      value={surgicalDrain}
                      onChange={e => setSurgicalDrain(e.target.value)}
                      className="w-full p-2 rounded border border-slate-300 text-xs font-bold text-amber-700"
                    />
                  </div>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Fluid Balance Notes</label>
                  <input
                    type="text"
                    value={fluidNotes}
                    onChange={e => setFluidNotes(e.target.value)}
                    className="w-full p-2 rounded border border-slate-300 text-xs"
                  />
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    type="submit"
                    className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg font-semibold shadow-2xs"
                  >
                    Log Fluid Reconciliation
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Tab 3: 5-Rights eMAR Administration */}
        {activeTab === 'emar' && (
          <div className="p-5 space-y-5 text-xs">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  Electronic Medication Administration Record (eMAR)
                </h3>
                <p className="text-slate-500 text-[11px]">
                  Enforces 5 Rights: Right Patient • Right Drug • Right Dose • Right Route • Right Time
                </p>
              </div>

              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 font-mono text-[10px]">
                  Wristband Barcode Scan: VERIFIED
                </span>
              </div>
            </div>

            <div className="space-y-3">
              {patientEmar.map(med => (
                <div key={med.id} className="p-4 rounded-xl border border-slate-200 bg-white flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="font-bold text-slate-900 text-sm">{med.medicineName}</h4>
                      <span className="font-bold text-xs text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                        {med.dosage}
                      </span>
                      <span className="text-slate-500 font-medium">({med.route})</span>
                    </div>

                    <div className="text-slate-600 mt-1">
                      Scheduled: <strong>{med.scheduledTime}</strong>
                      {med.administeredTime && (
                        <span> • Administered: <strong>{med.administeredTime}</strong> by {med.administeredBy}</span>
                      )}
                    </div>

                    {med.vitalsBeforeAdmin && (
                      <div className="text-[11px] text-teal-800 bg-teal-50/70 p-1.5 rounded mt-1.5 inline-block">
                        Pre-Administration Vitals: <strong>{med.vitalsBeforeAdmin}</strong>
                      </div>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    {med.status === 'Due' ? (
                      <>
                        <button
                          onClick={() => handleAdministerMedication(med.id, 'Held')}
                          className="px-3 py-1.5 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 font-semibold"
                        >
                          Hold Dose
                        </button>
                        <button
                          onClick={() => handleAdministerMedication(med.id, 'Administered')}
                          className="px-4 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-bold shadow-2xs flex items-center gap-1.5"
                        >
                          <Check className="w-3.5 h-3.5" /> 5-Rights Administer
                        </button>
                      </>
                    ) : (
                      <span className={`px-3 py-1 rounded-lg text-xs font-bold flex items-center gap-1 ${
                        med.status === 'Administered'
                          ? 'bg-emerald-100 text-emerald-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        <CheckCircle2 className="w-3.5 h-3.5" /> {med.status}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 4: SBAR Shift Handover Notes */}
        {activeTab === 'sbar' && (
          <div className="p-5 space-y-5 text-xs">
            <div>
              <h3 className="font-bold text-slate-900 text-sm">
                SBAR Shift Handover Documentation
              </h3>
              <p className="text-slate-500 text-[11px]">
                Structured clinical communication: Situation • Background • Assessment • Recommendation
              </p>
            </div>

            {/* Past Handover Cards */}
            <div className="space-y-3">
              {patientSbar.map(sbar => (
                <div key={sbar.id} className="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-2">
                  <div className="flex items-center justify-between border-b pb-2 border-slate-200">
                    <span className="font-bold text-slate-900">
                      Shift: {sbar.shift} ({sbar.fromNurse} → {sbar.toNurse})
                    </span>
                    <span className="font-mono text-slate-500 text-[11px]">{sbar.createdDate}</span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-800">
                    <div>
                      <strong className="text-teal-900 block">Situation (S):</strong>
                      <p className="text-slate-700 mt-0.5">{sbar.situation}</p>
                    </div>
                    <div>
                      <strong className="text-teal-900 block">Background (B):</strong>
                      <p className="text-slate-700 mt-0.5">{sbar.background}</p>
                    </div>
                    <div>
                      <strong className="text-teal-900 block">Assessment (A):</strong>
                      <p className="text-slate-700 mt-0.5">{sbar.assessment}</p>
                    </div>
                    <div>
                      <strong className="text-teal-900 block">Recommendation (R):</strong>
                      <p className="text-slate-700 mt-0.5">{sbar.recommendation}</p>
                    </div>
                  </div>

                  {sbar.keyTasksForNextShift && (
                    <div className="pt-2 border-t border-slate-200/80">
                      <strong className="text-slate-800">Key Tasks for Next Shift:</strong>
                      <ul className="list-disc pl-5 mt-1 space-y-0.5 text-slate-600">
                        {sbar.keyTasksForNextShift.map((task, idx) => (
                          <li key={idx}>{task}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Create SBAR Handover Form */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
              <h4 className="font-bold text-slate-900 mb-3 flex items-center gap-1.5">
                <Plus className="w-4 h-4 text-teal-600" /> New Shift Handover Note (SBAR)
              </h4>

              <form onSubmit={handleRecordSBAR} className="space-y-3">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Situation (S)</label>
                    <input
                      type="text"
                      required
                      value={sbarSituation}
                      onChange={e => setSbarSituation(e.target.value)}
                      placeholder="Current status, admitting diagnosis, recent procedure..."
                      className="w-full p-2 rounded border border-slate-300 text-xs"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Background (B)</label>
                    <input
                      type="text"
                      value={sbarBackground}
                      onChange={e => setSbarBackground(e.target.value)}
                      placeholder="Medical history, allergies, code status..."
                      className="w-full p-2 rounded border border-slate-300 text-xs"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Assessment (A)</label>
                    <input
                      type="text"
                      value={sbarAssessment}
                      onChange={e => setSbarAssessment(e.target.value)}
                      placeholder="Vitals stability, line patency, ambulation..."
                      className="w-full p-2 rounded border border-slate-300 text-xs"
                    />
                  </div>
                  <div>
                    <label className="block font-semibold text-slate-700 mb-1">Recommendation (R)</label>
                    <input
                      type="text"
                      required
                      value={sbarRecommendation}
                      onChange={e => setSbarRecommendation(e.target.value)}
                      placeholder="Pending labs, medication timings, discharge plan..."
                      className="w-full p-2 rounded border border-slate-300 text-xs"
                    />
                  </div>
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    type="submit"
                    className="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg font-semibold shadow-2xs"
                  >
                    Save SBAR Shift Handover
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
