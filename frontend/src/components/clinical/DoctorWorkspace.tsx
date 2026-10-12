'use client';
import React, { useState, useEffect } from 'react';
import { 
  Stethoscope, FileText, CheckCircle2, AlertTriangle, 
  Pill, Plus, Search, ShieldCheck, Clock, User, 
  Calendar, ChevronRight, Bookmark, ArrowUpRight, 
  Send, RefreshCw, X, ShieldAlert, Award, Printer,
  FileCheck, Lock, Activity, Eye, Heart, Check
} from 'lucide-react';
import { 
  ClinicalEncounter, 
  ElectronicPrescription, 
  DischargeSummary, 
  ClinicalReferral,
  ICD10Diagnosis,
  ClinicalTemplate
} from '@/lib/types/clinical';
import { Patient } from '@/lib/types/hms';
import { SEED_PATIENTS } from '@/lib/data/mockDatabase';
import { clinicalStore } from '@/lib/data/clinicalStore';
import { StatusBadge } from '../shared/StatusBadge';

interface DoctorWorkspaceProps {
  onOpenDoc?: (doc: any) => void;
  onOpenRAG?: () => void;
  onSelectPatient?: (patient: Patient) => void;
}

export const DoctorWorkspace: React.FC<DoctorWorkspaceProps> = ({
  onOpenDoc,
  onOpenRAG,
  onSelectPatient
}) => {
  // Clinical state
  const [encounters, setEncounters] = useState<ClinicalEncounter[]>([]);
  const [selectedEncounter, setSelectedEncounter] = useState<ClinicalEncounter | null>(null);
  const [templates, setTemplates] = useState<ClinicalTemplate[]>([]);
  const [queueFilter, setQueueFilter] = useState<'all' | 'waiting' | 'in_progress' | 'signed'>('all');
  const [patientSearch, setPatientSearch] = useState('');

  // Active Encounter Form State
  const [activeTab, setActiveTab] = useState<'soap' | 'prescriptions' | 'diagnoses' | 'amendments' | 'referral' | 'discharge'>('soap');
  const [chiefComplaint, setChiefComplaint] = useState('');
  const [hpi, setHpi] = useState('');
  const [subjectiveNotes, setSubjectiveNotes] = useState('');
  const [objectiveNotes, setObjectiveNotes] = useState('');
  const [assessmentNotes, setAssessmentNotes] = useState('');
  const [planNotes, setPlanNotes] = useState('');
  const [treatmentPlan, setTreatmentPlan] = useState('');
  const [patientInstructions, setPatientInstructions] = useState('');
  const [selectedDiagnoses, setSelectedDiagnoses] = useState<ICD10Diagnosis[]>([]);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);

  // New Prescription State
  const [prescriptions, setPrescriptions] = useState<ElectronicPrescription[]>([]);
  const [newMedName, setNewMedName] = useState('Ticagrelor (Brilinta)');
  const [newGenericName, setNewGenericName] = useState('Ticagrelor');
  const [newDosage, setNewDosage] = useState('90 mg');
  const [newRoute, setNewRoute] = useState<'Oral' | 'IVPB Infusion' | 'Subcutaneous' | 'Inhalation'>('Oral');
  const [newFrequency, setNewFrequency] = useState<'BID (Twice Daily)' | 'QD (Once Daily)' | 'TID (Three times daily)' | 'PRN (As Needed)'>('BID (Twice Daily)');
  const [newDurationDays, setNewDurationDays] = useState(30);
  const [newInstructions, setNewInstructions] = useState('Take 1 tablet by mouth twice daily with meals.');
  const [allergyAlerts, setAllergyAlerts] = useState<string[]>([]);

  // Add Amendment State
  const [showAmendmentModal, setShowAmendmentModal] = useState(false);
  const [amendmentType, setAmendmentType] = useState<'Addendum' | 'Correction' | 'Clarification'>('Addendum');
  const [amendmentReason, setAmendmentReason] = useState('');
  const [amendmentText, setAmendmentText] = useState('');

  // Referral State
  const [targetDepartment, setTargetDepartment] = useState('Internal Medicine');
  const [referralUrgency, setReferralUrgency] = useState<'Routine' | 'Urgent (<24h)' | 'Emergency / Stat'>('Routine');
  const [referralReason, setReferralReason] = useState('');
  const [referrals, setReferrals] = useState<ClinicalReferral[]>([]);

  // Discharge Summary State
  const [dischargeSummaries, setDischargeSummaries] = useState<DischargeSummary[]>([]);
  const [showDischargeModal, setShowDischargeModal] = useState(false);
  const [dischargeHospitalCourse, setDischargeHospitalCourse] = useState('');
  const [dischargeDiagnosis, setDischargeDiagnosis] = useState('');
  const [dischargeCondition, setDischargeCondition] = useState<'Stable / Improved' | 'Good' | 'Fair' | 'Against Medical Advice (AMA)'>('Stable / Improved');

  // Load Initial Data
  const reloadData = () => {
    const allEnc = clinicalStore.getEncounters();
    setEncounters(allEnc);
    setTemplates(clinicalStore.getTemplates());
    setPrescriptions(clinicalStore.getPrescriptions());
    setReferrals(clinicalStore.getReferrals());
    setDischargeSummaries(clinicalStore.getDischargeSummaries());

    if (!selectedEncounter && allEnc.length > 0) {
      loadEncounter(allEnc[0]);
    }
  };

  useEffect(() => {
    reloadData();
  }, []);

  const loadEncounter = (enc: ClinicalEncounter) => {
    setSelectedEncounter(enc);
    setChiefComplaint(enc.chiefComplaint || '');
    setHpi(enc.historyOfPresentIllness || '');
    setSubjectiveNotes(enc.subjectiveNotes || '');
    setObjectiveNotes(enc.objectiveNotes || '');
    setAssessmentNotes(enc.assessmentNotes || '');
    setPlanNotes(enc.planNotes || '');
    setTreatmentPlan(enc.treatmentPlan || '');
    setPatientInstructions(enc.patientInstructions || '');
    setSelectedDiagnoses(enc.diagnoses || []);
    setAllergyAlerts([]);
  };

  // Template Quick Insert
  const applyTemplate = (tpl: ClinicalTemplate) => {
    setChiefComplaint(tpl.defaultChiefComplaint);
    setSubjectiveNotes(tpl.subjectiveTemplate);
    setObjectiveNotes(tpl.objectiveTemplate);
    setAssessmentNotes(tpl.assessmentTemplate);
    setPlanNotes(tpl.planTemplate);

    const initialDiag: ICD10Diagnosis[] = tpl.commonDiagnoses.map((d, i) => ({
      id: `DX-TPL-${Date.now()}-${i}`,
      code: d.code,
      description: d.desc,
      type: i === 0 ? 'Primary' : 'Secondary',
      certainty: 'Confirmed',
      diagnosedBy: 'Dr. Marcus Vance, MD',
      diagnosedAt: new Date().toISOString()
    }));
    setSelectedDiagnoses(initialDiag);

    setSaveStatus(`Applied template: ${tpl.title}`);
    setTimeout(() => setSaveStatus(null), 3000);
  };

  // Save Draft Encounter
  const handleSaveDraft = () => {
    if (!selectedEncounter) return;

    try {
      const updated = clinicalStore.updateEncounter(selectedEncounter.id, {
        chiefComplaint,
        historyOfPresentIllness: hpi,
        subjectiveNotes,
        objectiveNotes,
        assessmentNotes,
        planNotes,
        treatmentPlan,
        patientInstructions,
        diagnoses: selectedDiagnoses
      });

      setSelectedEncounter(updated);
      setEncounters(clinicalStore.getEncounters());
      setSaveStatus('Draft progress note saved.');
      setTimeout(() => setSaveStatus(null), 2500);
    } catch (err: any) {
      alert(`Save error: ${err.message}`);
    }
  };

  // Sign Encounter Digitally (Locks record)
  const handleSignEncounter = () => {
    if (!selectedEncounter) return;

    if (window.confirm('Are you sure you want to sign this clinical encounter? Once signed, this record is permanently locked against direct editing in compliance with medical record regulations.')) {
      try {
        const signed = clinicalStore.signEncounter(
          selectedEncounter.id,
          'Dr. Marcus Vance, MD, FACC',
          'MD-88392-CA'
        );
        setSelectedEncounter(signed);
        setEncounters(clinicalStore.getEncounters());
        setSaveStatus('Record signed & locked with cryptographic digest.');
        setTimeout(() => setSaveStatus(null), 3000);
      } catch (err: any) {
        alert(err.message);
      }
    }
  };

  // Append Versioned Amendment / Addendum
  const handleAddAmendment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedEncounter || !amendmentText.trim() || !amendmentReason.trim()) return;

    try {
      const updated = clinicalStore.addAmendment(selectedEncounter.id, {
        amendmentType,
        amendedBy: 'Dr. Marcus Vance, MD, FACC',
        amendedByRole: 'DOCTOR',
        reasonForAmendment: amendmentReason,
        amendmentContent: amendmentText
      });

      setSelectedEncounter(updated);
      setEncounters(clinicalStore.getEncounters());
      setShowAmendmentModal(false);
      setAmendmentText('');
      setAmendmentReason('');
      setSaveStatus('Official Addendum successfully appended.');
      setTimeout(() => setSaveStatus(null), 3000);
    } catch (err: any) {
      alert(err.message);
    }
  };

  // Create Electronic Prescription with Real-time Allergy Cross-Check
  const handleAddPrescription = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedEncounter) return;

    const { prescription, allergyWarnings } = clinicalStore.createPrescription({
      encounterId: selectedEncounter.id,
      patientId: selectedEncounter.patientId,
      doctorId: 'USR-DOC-03',
      doctorName: 'Dr. Marcus Vance, MD',
      doctorLicense: 'MD-88392-CA',
      department: selectedEncounter.department,
      items: [
        {
          medicineId: `MED-${Date.now()}`,
          medicineName: newMedName,
          genericName: newGenericName,
          dosage: newDosage,
          route: newRoute,
          frequency: newFrequency,
          durationDays: newDurationDays,
          quantity: newDurationDays * (newFrequency.includes('BID') ? 2 : 1),
          instructions: newInstructions,
          indication: selectedEncounter.chiefComplaint
        }
      ],
      clinicalIndication: selectedEncounter.assessmentNotes || selectedEncounter.chiefComplaint
    });

    setPrescriptions(clinicalStore.getPrescriptions());
    if (allergyWarnings.length > 0) {
      setAllergyAlerts(allergyWarnings);
    } else {
      setAllergyAlerts([]);
      setSaveStatus(`e-Prescription issued for ${newMedName}`);
      setTimeout(() => setSaveStatus(null), 3000);
    }
  };

  // Submit Referral
  const handleCreateReferral = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedEncounter || !referralReason.trim()) return;

    const newRef = clinicalStore.createReferral({
      patientId: selectedEncounter.patientId,
      patientName: selectedEncounter.patientName,
      mrn: selectedEncounter.patientMrn,
      encounterId: selectedEncounter.id,
      referringDoctorId: 'USR-DOC-03',
      referringDoctorName: 'Dr. Marcus Vance, MD',
      referringDepartment: selectedEncounter.department,
      targetDepartment: targetDepartment as any,
      urgency: referralUrgency,
      referralReason,
      clinicalSummary: selectedEncounter.assessmentNotes || selectedEncounter.chiefComplaint,
      requestedInvestigations: ['Standard baseline consultation', 'Diagnostic records review'],
      hospitalId: 'HOSP-01'
    });

    setReferrals(clinicalStore.getReferrals());
    setReferralReason('');
    setSaveStatus(`Referral submitted to ${targetDepartment}`);
    setTimeout(() => setSaveStatus(null), 3000);
  };

  // Submit Discharge Summary
  const handleCreateDischargeSummary = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedEncounter) return;

    const summary = clinicalStore.createDischargeSummary({
      admissionId: `ADM-${selectedEncounter.patientId}`,
      patientId: selectedEncounter.patientId,
      patientName: selectedEncounter.patientName,
      mrn: selectedEncounter.patientMrn,
      age: selectedEncounter.patientAge,
      gender: selectedEncounter.patientGender,
      ward: 'Cardiac Step-Down 3A',
      bed: 'Bed 304-B',
      admissionDate: selectedEncounter.encounterDate,
      dischargeDate: new Date().toISOString().split('T')[0],
      admittingDiagnosis: selectedEncounter.chiefComplaint,
      dischargeDiagnosis: dischargeDiagnosis || selectedEncounter.diagnoses[0]?.description || 'CAD s/p PCI',
      secondaryDiagnoses: selectedEncounter.diagnoses.slice(1).map(d => d.description),
      hospitalCourse: dischargeHospitalCourse || selectedEncounter.subjectiveNotes + '\n' + selectedEncounter.objectiveNotes,
      proceduresPerformed: ['Percutaneous Coronary Intervention with Drug-Eluting Stent (DES)'],
      significantFindings: 'LVEF 52%, patent coronary stent, stable telemetry.',
      conditionAtDischarge: dischargeCondition,
      dischargeMedications: [
        {
          medicineName: 'Ticagrelor 90mg PO',
          dosage: '90 mg',
          frequency: 'Twice daily',
          duration: '12 months',
          specialInstructions: 'Do not discontinue prematurely.'
        },
        {
          medicineName: 'Aspirin 81mg PO',
          dosage: '81 mg',
          frequency: 'Once daily',
          duration: 'Lifelong',
          specialInstructions: 'Take with morning food.'
        }
      ],
      dietInstructions: 'Cardiac low-sodium diet (< 2000mg/day).',
      activityRestrictions: 'No lifting > 10 lbs for 7 days. Walking encouraged.',
      warningSignsRedFlags: [
        'Acute chest pressure or radiating left arm pain',
        'Severe shortness of breath',
        'Bleeding at catheter puncture site'
      ],
      followUpAppointments: [
        {
          department: 'Cardiology',
          doctorName: 'Dr. Marcus Vance, MD',
          scheduledDate: '2026-11-04 10:00 AM',
          instructions: '4-week post-PCI clinical check.'
        }
      ],
      attendingDoctorId: 'USR-DOC-03',
      attendingDoctorName: 'Dr. Marcus Vance, MD, FACC',
      hospitalId: 'HOSP-01',
      signNow: true
    });

    setDischargeSummaries(clinicalStore.getDischargeSummaries());
    setShowDischargeModal(false);
    setSaveStatus('Inpatient Discharge Summary signed and finalized.');
    setTimeout(() => setSaveStatus(null), 3000);
  };

  const filteredEncounters = encounters.filter(enc => {
    const matchSearch = enc.patientName.toLowerCase().includes(patientSearch.toLowerCase()) ||
      enc.patientMrn.toLowerCase().includes(patientSearch.toLowerCase());
    if (!matchSearch) return false;

    if (queueFilter === 'waiting') return enc.status === 'Waiting';
    if (queueFilter === 'in_progress') return enc.status === 'In Progress';
    if (queueFilter === 'signed') return enc.signStatus === 'Signed' || enc.signStatus === 'Addendum Appended';
    return true;
  });

  const patientObj = selectedEncounter ? SEED_PATIENTS.find(p => p.id === selectedEncounter.patientId) : null;
  const currentPatientPrescriptions = selectedEncounter ? prescriptions.filter(p => p.patientId === selectedEncounter.patientId) : [];
  const currentPatientReferrals = selectedEncounter ? referrals.filter(r => r.patientId === selectedEncounter.patientId) : [];
  const currentPatientDischarge = selectedEncounter ? dischargeSummaries.filter(d => d.patientId === selectedEncounter.patientId) : [];

  return (
    <div className="space-y-6">
      {/* Clinician Top Header */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 flex items-center gap-1">
              <Stethoscope className="w-3.5 h-3.5" /> Doctor Workspace & CPOE Console
            </span>
            <span className="text-xs text-slate-500">Member 3 Clinical Management • Multi-Tenant EMR</span>
          </div>
          <h1 className="text-xl font-bold mt-1 text-slate-900">Dr. Marcus Vance, MD, FACC</h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Active Clinical Consultations • Encounters • ICD-10 Coding • e-Prescriptions • Digital Records
          </p>
        </div>

        {saveStatus && (
          <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span className="font-medium">{saveStatus}</span>
          </div>
        )}
      </div>

      {/* Main Grid: Left Queue & Right Clinical Workstation */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Patient Consultation Queue (4 Cols) */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-white rounded-xl border border-slate-200 shadow-2xs p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Clock className="w-4 h-4 text-blue-600" /> Clinical Queue ({filteredEncounters.length})
              </h2>
              <span className="text-xs text-slate-500">Today</span>
            </div>

            {/* Filter Pills */}
            <div className="flex gap-1.5 mb-3 text-xs">
              {(['all', 'in_progress', 'signed', 'waiting'] as const).map(tab => (
                <button
                  key={tab}
                  onClick={() => setQueueFilter(tab)}
                  className={`px-2.5 py-1 rounded-md font-medium capitalize transition-all ${
                    queueFilter === tab
                      ? 'bg-blue-600 text-white shadow-2xs'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {tab.replace('_', ' ')}
                </button>
              ))}
            </div>

            {/* Search Input */}
            <div className="relative mb-3">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                value={patientSearch}
                onChange={e => setPatientSearch(e.target.value)}
                placeholder="Search patient name or MRN..."
                className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Encounter Cards List */}
            <div className="space-y-2 max-h-[620px] overflow-y-auto pr-1">
              {filteredEncounters.map(enc => {
                const isSelected = selectedEncounter?.id === enc.id;
                const isSigned = enc.signStatus === 'Signed' || enc.signStatus === 'Addendum Appended';

                return (
                  <div
                    key={enc.id}
                    onClick={() => loadEncounter(enc)}
                    className={`p-3 rounded-lg border cursor-pointer transition-all ${
                      isSelected
                        ? 'bg-blue-50/70 border-blue-400 ring-1 ring-blue-400'
                        : 'bg-white hover:bg-slate-50 border-slate-200'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-xs text-slate-900">{enc.patientName}</span>
                          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-100 text-slate-600">
                            {enc.patientMrn}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-1">{enc.chiefComplaint}</p>
                      </div>

                      {isSigned ? (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 flex items-center gap-0.5">
                          <Lock className="w-3 h-3" /> Signed
                        </span>
                      ) : (
                        <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-amber-100 text-amber-800">
                          Draft
                        </span>
                      )}
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-slate-500 mt-2 pt-2 border-t border-slate-100">
                      <span>{enc.encounterType}</span>
                      <span className="font-mono">{enc.startTime}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Clinical Template Quick-Apply Picker */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-2xs p-4">
            <h3 className="text-xs font-bold text-slate-900 mb-2 flex items-center gap-1.5">
              <Bookmark className="w-3.5 h-3.5 text-blue-600" /> Clinical Templates Library
            </h3>
            <p className="text-[11px] text-slate-500 mb-3">
              One-click standard structured medical documentation formats:
            </p>

            <div className="space-y-1.5">
              {templates.map(tpl => (
                <button
                  key={tpl.id}
                  onClick={() => applyTemplate(tpl)}
                  className="w-full text-left p-2 rounded-lg border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 transition-all text-xs flex items-center justify-between group"
                >
                  <div>
                    <div className="font-semibold text-slate-800 group-hover:text-blue-700">{tpl.title}</div>
                    <div className="text-[10px] text-slate-500">{tpl.department} • {tpl.encounterType}</div>
                  </div>
                  <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Comprehensive Encounter & Clinical Documentation Workspace (8 Cols) */}
        <div className="lg:col-span-8 space-y-4">
          {selectedEncounter ? (
            <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
              
              {/* Encounter Header Bar */}
              <div className="bg-slate-900 text-white p-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs px-2 py-0.5 rounded bg-blue-900/60 text-blue-300 border border-blue-700">
                        {selectedEncounter.id}
                      </span>
                      <h2 className="text-base font-bold text-white">
                        {selectedEncounter.patientName} ({selectedEncounter.patientAge}y, {selectedEncounter.patientGender})
                      </h2>
                      <span className="text-xs text-slate-400 font-mono">{selectedEncounter.patientMrn}</span>
                    </div>
                    <div className="text-xs text-slate-300 mt-1 flex items-center gap-4">
                      <span>Department: <strong>{selectedEncounter.department}</strong></span>
                      <span>Type: <strong>{selectedEncounter.encounterType}</strong></span>
                      <span>Date: <strong>{selectedEncounter.encounterDate}</strong></span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {selectedEncounter.signStatus === 'Draft' ? (
                      <>
                        <button
                          onClick={handleSaveDraft}
                          className="px-3 py-1.5 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-white rounded-lg border border-slate-700 transition-all"
                        >
                          Save Draft
                        </button>
                        <button
                          onClick={handleSignEncounter}
                          className="px-3 py-1.5 text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white rounded-lg shadow-2xs flex items-center gap-1.5 transition-all"
                        >
                          <Lock className="w-3.5 h-3.5" /> Sign & Lock Record
                        </button>
                      </>
                    ) : (
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-1 text-xs font-bold rounded-lg bg-emerald-900/80 text-emerald-200 border border-emerald-700 flex items-center gap-1">
                          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                          Signed by {selectedEncounter.signedBy?.split('(')[0]}
                        </span>
                        <button
                          onClick={() => setShowAmendmentModal(true)}
                          className="px-3 py-1.5 text-xs font-semibold bg-amber-600 hover:bg-amber-500 text-white rounded-lg shadow-2xs flex items-center gap-1 transition-all"
                        >
                          <Plus className="w-3.5 h-3.5" /> Append Addendum
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {/* Patient Allergy Warning Banner */}
                {selectedEncounter.allergiesSnapshot && selectedEncounter.allergiesSnapshot.length > 0 && (
                  <div className="mt-3 bg-red-950/80 border border-red-800/80 rounded-lg p-2.5 text-xs text-red-200 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                      <div>
                        <strong>Documented Patient Allergies:</strong>{' '}
                        {selectedEncounter.allergiesSnapshot.join(' • ')}
                      </div>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-red-900 text-red-100 font-bold">
                      Safety Protocol Active
                    </span>
                  </div>
                )}
              </div>

              {/* Navigation Tabs */}
              <div className="flex border-b border-slate-200 px-4 bg-slate-50 gap-2 overflow-x-auto text-xs">
                {[
                  { id: 'soap', label: 'SOAP Progress Note', icon: FileText },
                  { id: 'diagnoses', label: `Diagnoses (${selectedDiagnoses.length})`, icon: Activity },
                  { id: 'prescriptions', label: `e-Prescriptions (${currentPatientPrescriptions.length})`, icon: Pill },
                  { id: 'amendments', label: `Addenda History (${selectedEncounter.amendments.length})`, icon: ShieldCheck },
                  { id: 'referral', label: `Specialist Referrals (${currentPatientReferrals.length})`, icon: Send },
                  { id: 'discharge', label: `Discharge Summary (${currentPatientDischarge.length})`, icon: FileCheck },
                ].map(tab => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={`py-3 px-3 font-semibold border-b-2 flex items-center gap-1.5 whitespace-nowrap transition-all ${
                        activeTab === tab.id
                          ? 'border-blue-600 text-blue-700 bg-white'
                          : 'border-transparent text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      {tab.label}
                    </button>
                  );
                })}
              </div>

              {/* Tab 1: SOAP Clinical Documentation */}
              {activeTab === 'soap' && (
                <div className="p-5 space-y-4 text-xs">
                  {/* Chief Complaint & HPI */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block font-bold text-slate-700 mb-1">Chief Complaint</label>
                      <input
                        type="text"
                        disabled={selectedEncounter.signStatus !== 'Draft'}
                        value={chiefComplaint}
                        onChange={e => setChiefComplaint(e.target.value)}
                        placeholder="Primary reason for visit..."
                        className="w-full p-2.5 rounded-lg border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
                      />
                    </div>
                    <div>
                      <label className="block font-bold text-slate-700 mb-1">History of Present Illness (HPI)</label>
                      <input
                        type="text"
                        disabled={selectedEncounter.signStatus !== 'Draft'}
                        value={hpi}
                        onChange={e => setHpi(e.target.value)}
                        placeholder="Onset, duration, severity, characteristics..."
                        className="w-full p-2.5 rounded-lg border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
                      />
                    </div>
                  </div>

                  {/* Vitals Summary Card */}
                  {selectedEncounter.vitals && (
                    <div className="bg-blue-50/50 rounded-lg p-3 border border-blue-200 flex flex-wrap items-center justify-between gap-4 text-xs">
                      <div className="flex items-center gap-1.5 font-bold text-blue-900">
                        <Heart className="w-4 h-4 text-red-500" /> Triage Vitals:
                      </div>
                      <div>BP: <strong className="text-slate-900">{selectedEncounter.vitals.systolicBp}/{selectedEncounter.vitals.diastolicBp} mmHg</strong></div>
                      <div>HR: <strong className="text-slate-900">{selectedEncounter.vitals.heartRate} bpm</strong></div>
                      <div>RR: <strong className="text-slate-900">{selectedEncounter.vitals.respiratoryRate}/min</strong></div>
                      <div>SpO2: <strong className="text-slate-900">{selectedEncounter.vitals.spo2}%</strong></div>
                      <div>Temp: <strong className="text-slate-900">{selectedEncounter.vitals.temperature}°F</strong></div>
                      <div>Pain: <strong className="text-slate-900">{selectedEncounter.vitals.painScore}/10</strong></div>
                    </div>
                  )}

                  {/* SOAP Note Fields */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block font-bold text-slate-800 mb-1">Subjective (S)</label>
                      <textarea
                        rows={4}
                        disabled={selectedEncounter.signStatus !== 'Draft'}
                        value={subjectiveNotes}
                        onChange={e => setSubjectiveNotes(e.target.value)}
                        placeholder="Patient symptoms, pain description, interval history..."
                        className="w-full p-2.5 rounded-lg border border-slate-300 font-sans focus:outline-hidden focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
                      />
                    </div>
                    <div>
                      <label className="block font-bold text-slate-800 mb-1">Objective (O)</label>
                      <textarea
                        rows={4}
                        disabled={selectedEncounter.signStatus !== 'Draft'}
                        value={objectiveNotes}
                        onChange={e => setObjectiveNotes(e.target.value)}
                        placeholder="Physical exam findings, heart sounds, lungs, wound inspection..."
                        className="w-full p-2.5 rounded-lg border border-slate-300 font-sans focus:outline-hidden focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block font-bold text-slate-800 mb-1">Assessment (A)</label>
                      <textarea
                        rows={4}
                        disabled={selectedEncounter.signStatus !== 'Draft'}
                        value={assessmentNotes}
                        onChange={e => setAssessmentNotes(e.target.value)}
                        placeholder="Clinical judgment, differential diagnoses, progression..."
                        className="w-full p-2.5 rounded-lg border border-slate-300 font-sans focus:outline-hidden focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
                      />
                    </div>
                    <div>
                      <label className="block font-bold text-slate-800 mb-1">Plan (P)</label>
                      <textarea
                        rows={4}
                        disabled={selectedEncounter.signStatus !== 'Draft'}
                        value={planNotes}
                        onChange={e => setPlanNotes(e.target.value)}
                        placeholder="Diagnostic workup, therapy titration, patient counseling..."
                        className="w-full p-2.5 rounded-lg border border-slate-300 font-sans focus:outline-hidden focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
                      />
                    </div>
                  </div>

                  {/* Cryptographic Signature Stamp */}
                  {selectedEncounter.digitalSignatureHash && (
                    <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-[11px] text-slate-600 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Lock className="w-4 h-4 text-emerald-600" />
                        <div>
                          <div>Cryptographically Verified Electronic Signature:</div>
                          <span className="font-mono text-slate-800 font-bold">{selectedEncounter.digitalSignatureHash}</span>
                        </div>
                      </div>
                      <span className="text-[10px] text-slate-500 font-mono">{selectedEncounter.signedAt}</span>
                    </div>
                  )}
                </div>
              )}

              {/* Tab 2: Codified ICD-10 Diagnoses */}
              {activeTab === 'diagnoses' && (
                <div className="p-5 space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold text-slate-900 text-sm">Active Codified ICD-10 Diagnoses</h3>
                    <span className="text-slate-500">{selectedDiagnoses.length} Diagnoses assigned</span>
                  </div>

                  <div className="space-y-2">
                    {selectedDiagnoses.map(dx => (
                      <div key={dx.id} className="p-3 rounded-lg border border-slate-200 bg-white flex items-center justify-between">
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-0.5 rounded font-mono font-bold bg-blue-100 text-blue-800 text-xs">
                              {dx.code}
                            </span>
                            <span className="font-semibold text-slate-900 text-xs">{dx.description}</span>
                          </div>
                          <div className="text-[11px] text-slate-500 mt-1 flex items-center gap-3">
                            <span>Type: <strong className="text-slate-700">{dx.type}</strong></span>
                            <span>Certainty: <strong className="text-slate-700">{dx.certainty}</strong></span>
                            <span>Diagnosed by: {dx.diagnosedBy}</span>
                          </div>
                        </div>
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700">
                          {dx.type}
                        </span>
                      </div>
                    ))}
                  </div>

                  {/* Add Diagnosis Quick Selector */}
                  <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
                    <h4 className="font-bold text-slate-800 mb-2">Add Common ICD-10 Code to Encounter:</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {[
                        { code: 'I25.10', desc: 'Atherosclerotic heart disease of native coronary artery' },
                        { code: 'I10', desc: 'Essential (primary) hypertension' },
                        { code: 'E11.9', desc: 'Type 2 diabetes mellitus without complications' },
                        { code: 'I48.91', desc: 'Unspecified atrial fibrillation' },
                      ].map(item => (
                        <button
                          key={item.code}
                          disabled={selectedEncounter.signStatus !== 'Draft'}
                          onClick={() => {
                            const newDiag: ICD10Diagnosis = {
                              id: `DX-${Date.now()}`,
                              code: item.code,
                              description: item.desc,
                              type: selectedDiagnoses.length === 0 ? 'Primary' : 'Secondary',
                              certainty: 'Confirmed',
                              diagnosedBy: 'Dr. Marcus Vance, MD',
                              diagnosedAt: new Date().toISOString()
                            };
                            setSelectedDiagnoses([...selectedDiagnoses, newDiag]);
                          }}
                          className="text-left p-2 rounded border border-slate-300 hover:border-blue-500 hover:bg-white transition-all text-xs flex items-center justify-between disabled:opacity-50"
                        >
                          <div>
                            <span className="font-mono font-bold text-blue-700 mr-1.5">{item.code}</span>
                            <span className="text-slate-700">{item.desc}</span>
                          </div>
                          <Plus className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Tab 3: e-Prescriptions & Allergy Cross-Check */}
              {activeTab === 'prescriptions' && (
                <div className="p-5 space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900 text-sm">CPOE Electronic Prescriptions (e-Prescribing)</h3>
                      <p className="text-slate-500 text-[11px]">Real-time contraindication and allergy cross-checking enabled</p>
                    </div>
                  </div>

                  {/* Allergy Conflict Warning Banner */}
                  {allergyAlerts.length > 0 && (
                    <div className="bg-red-50 border-2 border-red-500 rounded-lg p-3 text-red-900 space-y-1">
                      <div className="flex items-center gap-2 font-bold text-red-700">
                        <ShieldAlert className="w-5 h-5 text-red-600" />
                        ALLERGY CONTRAINDICATION DETECTED:
                      </div>
                      {allergyAlerts.map((w, idx) => (
                        <p key={idx} className="text-xs font-semibold pl-7">{w}</p>
                      ))}
                    </div>
                  )}

                  {/* Prescribed Items Table */}
                  <div className="space-y-2">
                    {currentPatientPrescriptions.map(rx => (
                      <div key={rx.id} className="p-3 rounded-lg border border-slate-200 bg-white">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <span className="font-mono font-bold text-blue-700">{rx.id}</span>
                            <span className="text-slate-600">Prescribed: {rx.prescribedDate}</span>
                          </div>
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                            {rx.status}
                          </span>
                        </div>

                        <div className="divide-y divide-slate-100">
                          {rx.items.map(it => (
                            <div key={it.id} className="py-2 flex items-start justify-between">
                              <div>
                                <div className="font-bold text-slate-900 flex items-center gap-2">
                                  {it.medicineName}
                                  <span className="font-mono text-slate-500 font-normal">({it.genericName})</span>
                                  {it.contraindicationFlag && (
                                    <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-red-100 text-red-800">
                                      Contraindicated
                                    </span>
                                  )}
                                </div>
                                <div className="text-slate-600 text-[11px] mt-0.5">
                                  Dosage: <strong>{it.dosage}</strong> • Route: <strong>{it.route}</strong> • Frequency: <strong>{it.frequency}</strong> • Duration: {it.durationDays} days
                                </div>
                                <div className="text-slate-500 text-[11px] italic mt-0.5">
                                  Instructions: &ldquo;{it.instructions}&rdquo;
                                </div>
                              </div>
                              <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700">
                                {it.dispenseStatus}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Prescription Builder Form */}
                  <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                    <h4 className="font-bold text-slate-900 mb-3 flex items-center gap-1.5">
                      <Plus className="w-4 h-4 text-blue-600" /> Prescribe New Medication
                    </h4>

                    <form onSubmit={handleAddPrescription} className="space-y-3">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Medication Name</label>
                          <input
                            type="text"
                            value={newMedName}
                            onChange={e => setNewMedName(e.target.value)}
                            className="w-full p-2 rounded border border-slate-300 text-xs focus:ring-2 focus:ring-blue-500"
                            placeholder="e.g. Ticagrelor, Amoxicillin, Atorvastatin..."
                          />
                        </div>
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Generic Name</label>
                          <input
                            type="text"
                            value={newGenericName}
                            onChange={e => setNewGenericName(e.target.value)}
                            className="w-full p-2 rounded border border-slate-300 text-xs focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Dosage</label>
                          <input
                            type="text"
                            value={newDosage}
                            onChange={e => setNewDosage(e.target.value)}
                            className="w-full p-2 rounded border border-slate-300 text-xs"
                          />
                        </div>
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Route</label>
                          <select
                            value={newRoute}
                            onChange={e => setNewRoute(e.target.value as any)}
                            className="w-full p-2 rounded border border-slate-300 text-xs"
                          >
                            <option value="Oral">Oral</option>
                            <option value="IVPB Infusion">IVPB Infusion</option>
                            <option value="Subcutaneous">Subcutaneous</option>
                            <option value="Inhalation">Inhalation</option>
                          </select>
                        </div>
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Frequency</label>
                          <select
                            value={newFrequency}
                            onChange={e => setNewFrequency(e.target.value as any)}
                            className="w-full p-2 rounded border border-slate-300 text-xs"
                          >
                            <option value="BID (Twice Daily)">BID (Twice Daily)</option>
                            <option value="QD (Once Daily)">QD (Once Daily)</option>
                            <option value="TID (Three times daily)">TID (Three times daily)</option>
                            <option value="PRN (As Needed)">PRN (As Needed)</option>
                          </select>
                        </div>
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Duration (Days)</label>
                          <input
                            type="number"
                            value={newDurationDays}
                            onChange={e => setNewDurationDays(Number(e.target.value))}
                            className="w-full p-2 rounded border border-slate-300 text-xs"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block font-semibold text-slate-700 mb-1">Administration Instructions</label>
                        <input
                          type="text"
                          value={newInstructions}
                          onChange={e => setNewInstructions(e.target.value)}
                          className="w-full p-2 rounded border border-slate-300 text-xs"
                        />
                      </div>

                      <div className="flex justify-end gap-2 pt-2">
                        <button
                          type="button"
                          onClick={() => {
                            // Test safety alert by attempting to prescribe penicillin
                            setNewMedName('Amoxicillin Clavulanate (Augmentin)');
                            setNewGenericName('Amoxicillin');
                            setNewDosage('875 mg');
                            setNewInstructions('Take 1 tab PO q12h');
                          }}
                          className="px-2.5 py-1.5 text-[11px] font-semibold text-amber-700 bg-amber-50 hover:bg-amber-100 rounded border border-amber-300"
                        >
                          Test Allergy Trigger (Amoxicillin)
                        </button>
                        <button
                          type="submit"
                          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold shadow-2xs"
                        >
                          Verify & Sign e-Prescription
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              )}

              {/* Tab 4: Versioned Amendments & Addenda History */}
              {activeTab === 'amendments' && (
                <div className="p-5 space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900 text-sm">Official Record Amendment & Addenda Trail</h3>
                      <p className="text-slate-500 text-[11px]">Strict HIPAA compliance: signed records are never overwritten silently</p>
                    </div>

                    <button
                      onClick={() => setShowAmendmentModal(true)}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold flex items-center gap-1"
                    >
                      <Plus className="w-3.5 h-3.5" /> Append Addendum
                    </button>
                  </div>

                  {selectedEncounter.amendments.length === 0 ? (
                    <div className="text-center py-8 text-slate-400 bg-slate-50 rounded-lg border border-dashed border-slate-200">
                      No amendments or addenda appended to this encounter.
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {selectedEncounter.amendments.map(amd => (
                        <div key={amd.id} className="p-4 rounded-lg border border-amber-200 bg-amber-50/40 space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-amber-900 bg-amber-200/80 px-2 py-0.5 rounded text-xs">
                                Version {amd.version} ({amd.amendmentType})
                              </span>
                              <span className="font-semibold text-slate-900">{amd.amendedBy}</span>
                            </div>
                            <span className="text-slate-500 font-mono text-[11px]">{amd.amendedAt}</span>
                          </div>

                          <div className="text-slate-700">
                            <strong>Reason:</strong> {amd.reasonForAmendment}
                          </div>

                          <div className="p-3 bg-white rounded border border-amber-200 text-slate-900 whitespace-pre-wrap font-sans">
                            {amd.amendmentContent}
                          </div>

                          <div className="text-[10px] font-mono text-slate-500 pt-1 flex items-center justify-between border-t border-amber-200/60">
                            <span>Digital Signature: <strong>{amd.digitalSignatureHash}</strong></span>
                            <span>Audit Stamp: Verified</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Tab 5: Specialist Referrals */}
              {activeTab === 'referral' && (
                <div className="p-5 space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold text-slate-900 text-sm">Inter-Departmental Clinical Referrals</h3>
                    <span className="text-slate-500">{currentPatientReferrals.length} on file</span>
                  </div>

                  {/* List of Referrals */}
                  <div className="space-y-2">
                    {currentPatientReferrals.map(ref => (
                      <div key={ref.id} className="p-3 rounded-lg border border-slate-200 bg-white space-y-1">
                        <div className="flex items-center justify-between">
                          <div className="font-bold text-slate-900">
                            To: {ref.targetDepartment} {ref.targetDoctorName ? `(${ref.targetDoctorName})` : ''}
                          </div>
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">
                            {ref.status}
                          </span>
                        </div>
                        <div className="text-slate-700">Reason: {ref.referralReason}</div>
                        <div className="text-slate-500 text-[11px]">Summary: {ref.clinicalSummary}</div>
                        {ref.consultantNotes && (
                          <div className="p-2 bg-blue-50 rounded text-blue-900 text-[11px] mt-1">
                            Consultant Response: {ref.consultantNotes}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  {/* Create Referral Form */}
                  <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                    <h4 className="font-bold text-slate-900 mb-3 flex items-center gap-1.5">
                      <Send className="w-4 h-4 text-blue-600" /> Create Specialist Referral
                    </h4>

                    <form onSubmit={handleCreateReferral} className="space-y-3">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Target Department</label>
                          <select
                            value={targetDepartment}
                            onChange={e => setTargetDepartment(e.target.value)}
                            className="w-full p-2 rounded border border-slate-300 text-xs"
                          >
                            <option value="Cardiology">Cardiology</option>
                            <option value="Neurology">Neurology</option>
                            <option value="Internal Medicine">Internal Medicine</option>
                            <option value="Orthopedics">Orthopedics</option>
                            <option value="Outpatient Department">Outpatient / Cardiac Rehab</option>
                            <option value="General Surgery">General Surgery</option>
                          </select>
                        </div>
                        <div>
                          <label className="block font-semibold text-slate-700 mb-1">Urgency</label>
                          <select
                            value={referralUrgency}
                            onChange={e => setReferralUrgency(e.target.value as any)}
                            className="w-full p-2 rounded border border-slate-300 text-xs"
                          >
                            <option value="Routine">Routine</option>
                            <option value="Urgent (<24h)">Urgent (&lt;24h)</option>
                            <option value="Emergency / Stat">Emergency / Stat</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="block font-semibold text-slate-700 mb-1">Clinical Reason for Referral</label>
                        <input
                          type="text"
                          value={referralReason}
                          onChange={e => setReferralReason(e.target.value)}
                          placeholder="e.g. Phase 2 Cardiac Rehabilitation post-stent placement..."
                          className="w-full p-2 rounded border border-slate-300 text-xs"
                        />
                      </div>

                      <div className="flex justify-end">
                        <button
                          type="submit"
                          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold shadow-2xs"
                        >
                          Submit Referral
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              )}

              {/* Tab 6: Discharge Summary */}
              {activeTab === 'discharge' && (
                <div className="p-5 space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900 text-sm">Inpatient Discharge Summary</h3>
                      <p className="text-slate-500 text-[11px]">Comprehensive release documentation, hospital course, and discharge prescriptions</p>
                    </div>

                    <button
                      onClick={() => setShowDischargeModal(true)}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold flex items-center gap-1"
                    >
                      <Plus className="w-3.5 h-3.5" /> Generate Discharge Summary
                    </button>
                  </div>

                  {currentPatientDischarge.length === 0 ? (
                    <div className="text-center py-8 text-slate-400 bg-slate-50 rounded-lg border border-dashed border-slate-200">
                      No discharge summary created yet for this patient admission.
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {currentPatientDischarge.map(ds => (
                        <div key={ds.id} className="p-5 rounded-xl border border-slate-300 bg-white space-y-3">
                          <div className="flex items-start justify-between border-b pb-3 border-slate-200">
                            <div>
                              <div className="flex items-center gap-2">
                                <span className="font-mono text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 font-bold">
                                  {ds.id}
                                </span>
                                <h4 className="font-bold text-sm text-slate-900">Inpatient Hospital Discharge Summary</h4>
                              </div>
                              <p className="text-slate-500 text-[11px] mt-0.5">
                                Admitted: <strong>{ds.admissionDate}</strong> • Discharged: <strong>{ds.dischargeDate}</strong> • Ward: <strong>{ds.ward} ({ds.bed})</strong>
                              </p>
                            </div>

                            <span className="px-2.5 py-1 rounded text-xs font-bold bg-emerald-100 text-emerald-800 flex items-center gap-1">
                              <ShieldCheck className="w-3.5 h-3.5" /> {ds.status}
                            </span>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <span className="font-bold text-slate-800">Admitting Diagnosis:</span>
                              <p className="text-slate-700 mt-0.5">{ds.admittingDiagnosis}</p>
                            </div>
                            <div>
                              <span className="font-bold text-slate-800">Discharge Diagnosis:</span>
                              <p className="text-slate-700 mt-0.5">{ds.dischargeDiagnosis}</p>
                            </div>
                          </div>

                          <div>
                            <span className="font-bold text-slate-800">Hospital Course Summary:</span>
                            <div className="p-3 bg-slate-50 rounded border border-slate-200 text-slate-800 whitespace-pre-wrap mt-1">
                              {ds.hospitalCourse}
                            </div>
                          </div>

                          <div>
                            <span className="font-bold text-slate-800">Discharge Medications:</span>
                            <div className="mt-1 divide-y divide-slate-100 border border-slate-200 rounded-lg overflow-hidden">
                              {ds.dischargeMedications.map((m, idx) => (
                                <div key={idx} className="p-2.5 bg-white text-slate-800 flex items-center justify-between">
                                  <div>
                                    <strong className="text-blue-900">{m.medicineName}</strong> ({m.dosage}) - {m.frequency}
                                    <div className="text-slate-500 text-[11px] italic">{m.specialInstructions}</div>
                                  </div>
                                  <span className="text-slate-600 font-mono text-[11px]">{m.duration}</span>
                                </div>
                              ))}
                            </div>
                          </div>

                          <div className="p-3 bg-amber-50 rounded-lg border border-amber-200 text-amber-900">
                            <strong>Warning Signs (Seek Emergency Care If):</strong>
                            <ul className="list-disc pl-5 mt-1 space-y-0.5">
                              {ds.warningSignsRedFlags.map((w, idx) => (
                                <li key={idx}>{w}</li>
                              ))}
                            </ul>
                          </div>

                          <div className="flex items-center justify-between pt-2 border-t border-slate-200 text-slate-500 text-[11px]">
                            <span>Signed by: <strong>{ds.attendingDoctorName}</strong></span>
                            <span className="font-mono">Digest: {ds.digitalSignature}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-500">
              Select an encounter from the queue to start clinical documentation.
            </div>
          )}
        </div>
      </div>

      {/* Append Amendment Modal */}
      {showAmendmentModal && selectedEncounter && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in">
          <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-lg p-5 space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                <Plus className="w-4 h-4 text-blue-600" /> Append Official Clinical Addendum
              </h3>
              <button onClick={() => setShowAmendmentModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-600">
              In accordance with medical record retention regulations, the signed encounter is permanent. Your note will be appended as an official versioned addendum with an irrevocable timestamp.
            </p>

            <form onSubmit={handleAddAmendment} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Addendum Type</label>
                <select
                  value={amendmentType}
                  onChange={e => setAmendmentType(e.target.value as any)}
                  className="w-full p-2 rounded border border-slate-300"
                >
                  <option value="Addendum">Addendum (Supplemental clinical information)</option>
                  <option value="Clarification">Clarification (Explaining existing clinical data)</option>
                  <option value="Correction">Correction (Documenting factual clarification)</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Clinical Justification / Reason</label>
                <input
                  type="text"
                  required
                  value={amendmentReason}
                  onChange={e => setAmendmentReason(e.target.value)}
                  placeholder="e.g. Echo report finalized; lab value review..."
                  className="w-full p-2 rounded border border-slate-300"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Addendum Clinical Text</label>
                <textarea
                  rows={4}
                  required
                  value={amendmentText}
                  onChange={e => setAmendmentText(e.target.value)}
                  placeholder="Enter addendum text..."
                  className="w-full p-2 rounded border border-slate-300"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t">
                <button
                  type="button"
                  onClick={() => setShowAmendmentModal(false)}
                  className="px-3 py-1.5 rounded border border-slate-300 text-slate-700 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded bg-blue-600 hover:bg-blue-500 text-white font-semibold shadow-2xs"
                >
                  Sign & Append Addendum
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Discharge Summary Modal */}
      {showDischargeModal && selectedEncounter && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in">
          <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-2xl p-6 space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <FileCheck className="w-5 h-5 text-blue-600" /> Finalize Inpatient Discharge Summary
              </h3>
              <button onClick={() => setShowDischargeModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateDischargeSummary} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Final Discharge Diagnosis</label>
                  <input
                    type="text"
                    required
                    value={dischargeDiagnosis}
                    onChange={e => setDischargeDiagnosis(e.target.value)}
                    placeholder="e.g. Coronary Artery Disease s/p DES to mid-LAD"
                    className="w-full p-2.5 rounded border border-slate-300"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Condition at Discharge</label>
                  <select
                    value={dischargeCondition}
                    onChange={e => setDischargeCondition(e.target.value as any)}
                    className="w-full p-2.5 rounded border border-slate-300"
                  >
                    <option value="Stable / Improved">Stable / Improved</option>
                    <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                    <option value="Against Medical Advice (AMA)">Against Medical Advice (AMA)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Hospital Course & Clinical Summary</label>
                <textarea
                  rows={5}
                  required
                  value={dischargeHospitalCourse}
                  onChange={e => setDischargeHospitalCourse(e.target.value)}
                  placeholder="Summarize admission events, catheterization, stent details, response to therapy, and ambulation..."
                  className="w-full p-2.5 rounded border border-slate-300 font-sans"
                />
              </div>

              <div className="p-3 bg-blue-50 rounded border border-blue-200 text-blue-900">
                <strong>Standard Post-Discharge Meds & Red Flags:</strong> Will automatically include dual antiplatelet therapy (Aspirin + Ticagrelor), statin, and emergency return instructions.
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button
                  type="button"
                  onClick={() => setShowDischargeModal(false)}
                  className="px-4 py-2 rounded border border-slate-300 text-slate-700 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded bg-blue-600 hover:bg-blue-500 text-white font-bold shadow-2xs"
                >
                  Sign & Finalize Discharge Summary
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
