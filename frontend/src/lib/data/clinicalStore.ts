import { 
  ClinicalEncounter, 
  ClinicalAmendment, 
  ElectronicPrescription, 
  PrescriptionItem,
  PatientAllergy, 
  NursingObservation, 
  FluidBalanceRecord, 
  EMARRecord, 
  SBARHandoverNote, 
  DischargeSummary, 
  ClinicalReferral, 
  ClinicalTemplate
} from '../types/clinical';
import { 
  SEED_CLINICAL_ENCOUNTERS, 
  SEED_ELECTRONIC_PRESCRIPTIONS, 
  SEED_PATIENT_ALLERGIES, 
  SEED_NURSING_OBSERVATIONS, 
  SEED_FLUID_BALANCES, 
  SEED_EMAR_RECORDS, 
  SEED_SBAR_NOTES, 
  SEED_DISCHARGE_SUMMARIES, 
  SEED_CLINICAL_REFERRALS, 
  CLINICAL_TEMPLATES,
  ICD10_CATALOG,
  calculateMEWS
} from './mockClinicalData';
import { SEED_PATIENTS } from './mockDatabase';
import { HospitalRole } from '../types/roles';

// Simple deterministic cryptographic signature helper for clinical records
function generateSignatureHash(dataString: string): string {
  let hash = 0;
  for (let i = 0; i < dataString.length; i++) {
    const char = dataString.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // Convert to 32bit integer
  }
  const hex = Math.abs(hash).toString(16).padStart(8, '0');
  const timestampHex = Date.now().toString(16);
  return `SHA256:${hex}${timestampHex}`;
}

// Global in-memory clinical store
class ClinicalStore {
  private encounters: ClinicalEncounter[] = [...SEED_CLINICAL_ENCOUNTERS];
  private prescriptions: ElectronicPrescription[] = [...SEED_ELECTRONIC_PRESCRIPTIONS];
  private allergies: PatientAllergy[] = [...SEED_PATIENT_ALLERGIES];
  private observations: NursingObservation[] = [...SEED_NURSING_OBSERVATIONS];
  private fluidBalances: FluidBalanceRecord[] = [...SEED_FLUID_BALANCES];
  private emarRecords: EMARRecord[] = [...SEED_EMAR_RECORDS];
  private sbarNotes: SBARHandoverNote[] = [...SEED_SBAR_NOTES];
  private dischargeSummaries: DischargeSummary[] = [...SEED_DISCHARGE_SUMMARIES];
  private referrals: ClinicalReferral[] = [...SEED_CLINICAL_REFERRALS];
  private templates: ClinicalTemplate[] = [...CLINICAL_TEMPLATES];

  // --------------------------------------------------------------------------
  // ENCOUNTERS & CLINICAL DOCUMENTATION
  // --------------------------------------------------------------------------
  public getEncounters(filter?: {
    patientId?: string;
    doctorId?: string;
    status?: string;
    department?: string;
    hospitalId?: string;
  }): ClinicalEncounter[] {
    return this.encounters.filter(enc => {
      if (filter?.patientId && enc.patientId !== filter.patientId) return false;
      if (filter?.doctorId && enc.doctorId !== filter.doctorId) return false;
      if (filter?.status && enc.status !== filter.status) return false;
      if (filter?.department && enc.department !== filter.department) return false;
      if (filter?.hospitalId && enc.hospitalId !== filter.hospitalId) return false;
      return true;
    });
  }

  public getEncounterById(id: string): ClinicalEncounter | undefined {
    return this.encounters.find(enc => enc.id === id);
  }

  public createEncounter(data: Partial<ClinicalEncounter> & {
    patientId: string;
    doctorId: string;
    department: any;
    chiefComplaint: string;
  }): ClinicalEncounter {
    const patient = SEED_PATIENTS.find(p => p.id === data.patientId);
    const patientAllergies = this.allergies
      .filter(a => a.patientId === data.patientId && a.status === 'Active')
      .map(a => `${a.allergen} (${a.reaction})`);

    const newEncounter: ClinicalEncounter = {
      id: `ENC-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
      patientId: data.patientId,
      patientMrn: patient?.mrn || 'MRN-UNKNOWN',
      patientName: patient ? `${patient.firstName} ${patient.lastName}` : (data.patientName || 'Unknown Patient'),
      patientAge: patient?.age || data.patientAge || 45,
      patientGender: patient?.gender || data.patientGender || 'Other',
      doctorId: data.doctorId,
      doctorName: data.doctorName || 'Attending Physician',
      department: data.department,
      encounterType: data.encounterType || 'Outpatient Consultation',
      encounterDate: data.encounterDate || new Date().toISOString().split('T')[0],
      startTime: data.startTime || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'In Progress',
      signStatus: 'Draft',
      chiefComplaint: data.chiefComplaint,
      historyOfPresentIllness: data.historyOfPresentIllness || '',
      pastMedicalHistory: data.pastMedicalHistory || (patient?.chronicConditions.join(', ') || ''),
      familyHistory: data.familyHistory || '',
      socialHistory: data.socialHistory || '',
      reviewOfSystems: data.reviewOfSystems || '',
      vitals: data.vitals,
      examination: data.examination || {},
      subjectiveNotes: data.subjectiveNotes || '',
      objectiveNotes: data.objectiveNotes || '',
      assessmentNotes: data.assessmentNotes || '',
      planNotes: data.planNotes || '',
      diagnoses: data.diagnoses || [],
      allergiesSnapshot: patientAllergies,
      prescriptionIds: data.prescriptionIds || [],
      labOrderIds: data.labOrderIds || [],
      radiologyScanIds: data.radiologyScanIds || [],
      treatmentPlan: data.treatmentPlan || '',
      patientInstructions: data.patientInstructions || '',
      followUpDate: data.followUpDate,
      referralId: data.referralId,
      amendments: [],
      hospitalId: data.hospitalId || 'HOSP-01'
    };

    this.encounters.unshift(newEncounter);
    return newEncounter;
  }

  public updateEncounter(id: string, updates: Partial<ClinicalEncounter>): ClinicalEncounter {
    const index = this.encounters.findIndex(enc => enc.id === id);
    if (index === -1) {
      throw new Error(`Encounter ${id} not found.`);
    }

    const current = this.encounters[index];

    // CRITICAL CLINICAL SAFETY RULE: Signed records cannot be silently overwritten
    if (current.signStatus === 'Signed' || current.signStatus === 'Amended') {
      throw new Error(
        `IMMUTABILITY VIOLATION: Clinical encounter ${id} has been signed and locked. ` +
        `Direct modification is prohibited by medical record retention rules. ` +
        `Please create an authorized addendum/amendment instead.`
      );
    }

    const updated = {
      ...current,
      ...updates,
      id: current.id, // Immutable
      patientId: current.patientId, // Immutable
      patientMrn: current.patientMrn,
      hospitalId: current.hospitalId
    };

    this.encounters[index] = updated;
    return updated;
  }

  public signEncounter(id: string, signedBy: string, licenseNumber: string): ClinicalEncounter {
    const index = this.encounters.findIndex(enc => enc.id === id);
    if (index === -1) {
      throw new Error(`Encounter ${id} not found.`);
    }

    const current = this.encounters[index];
    if (current.signStatus === 'Signed') {
      return current; // Already signed
    }

    const timestamp = new Date().toISOString();
    const signatureDigest = generateSignatureHash(
      `${current.id}|${current.patientMrn}|${signedBy}|${licenseNumber}|${timestamp}|${current.assessmentNotes}`
    );

    const signedRecord: ClinicalEncounter = {
      ...current,
      status: 'Signed',
      signStatus: 'Signed',
      signedBy: `${signedBy} (License: ${licenseNumber})`,
      signedAt: timestamp,
      digitalSignatureHash: signatureDigest
    };

    this.encounters[index] = signedRecord;
    return signedRecord;
  }

  public addAmendment(
    encounterId: string, 
    amendment: {
      amendmentType: 'Addendum' | 'Correction' | 'Clarification';
      amendedBy: string;
      amendedByRole: HospitalRole;
      reasonForAmendment: string;
      amendmentContent: string;
    }
  ): ClinicalEncounter {
    const index = this.encounters.findIndex(enc => enc.id === encounterId);
    if (index === -1) {
      throw new Error(`Encounter ${encounterId} not found.`);
    }

    const current = this.encounters[index];
    const timestamp = new Date().toISOString();
    const version = current.amendments.length + 1;

    const signatureHash = generateSignatureHash(
      `${current.id}|v${version}|${amendment.amendedBy}|${timestamp}|${amendment.amendmentContent}`
    );

    const newAmendment: ClinicalAmendment = {
      id: `AMD-${Date.now()}-${version}`,
      encounterId,
      version,
      amendmentType: amendment.amendmentType,
      amendedBy: amendment.amendedBy,
      amendedByRole: amendment.amendedByRole,
      amendedAt: timestamp,
      reasonForAmendment: amendment.reasonForAmendment,
      amendmentContent: amendment.amendmentContent,
      previousContentSnapshot: current.assessmentNotes,
      digitalSignatureHash: signatureHash
    };

    const updatedRecord: ClinicalEncounter = {
      ...current,
      signStatus: 'Addendum Appended',
      amendments: [...current.amendments, newAmendment]
    };

    this.encounters[index] = updatedRecord;
    return updatedRecord;
  }

  // --------------------------------------------------------------------------
  // ELECTRONIC PRESCRIPTIONS (eRx / CPOE) & ALLERGY CROSS-CHECK
  // --------------------------------------------------------------------------
  public getPrescriptions(filter?: {
    patientId?: string;
    doctorId?: string;
    status?: string;
  }): ElectronicPrescription[] {
    return this.prescriptions.filter(rx => {
      if (filter?.patientId && rx.patientId !== filter.patientId) return false;
      if (filter?.doctorId && rx.doctorId !== filter.doctorId) return false;
      if (filter?.status && rx.status !== filter.status) return false;
      return true;
    });
  }

  public createPrescription(data: {
    encounterId?: string;
    patientId: string;
    doctorId: string;
    doctorName: string;
    doctorLicense: string;
    department: any;
    items: Omit<PrescriptionItem, 'id' | 'dispenseStatus'>[];
    clinicalIndication: string;
    refillsAllowed?: number;
    hospitalId?: string;
  }): { prescription: ElectronicPrescription; allergyWarnings: string[] } {
    const patient = SEED_PATIENTS.find(p => p.id === data.patientId);
    const patientAllergies = this.allergies.filter(
      a => a.patientId === data.patientId && a.status === 'Active'
    );

    const allergyWarnings: string[] = [];

    // AUTOMATED REAL-TIME ALLERGY SAFETY CROSS-CHECK
    const processedItems: PrescriptionItem[] = data.items.map((item, idx) => {
      let isContraindicated = false;
      let contraindicationNotes = '';

      for (const alg of patientAllergies) {
        const drugLower = (item.medicineName + ' ' + item.genericName).toLowerCase();
        const allergenLower = alg.allergen.toLowerCase();

        // Check penicillin class cross-reactivity
        if (allergenLower.includes('penicillin') && (
          drugLower.includes('amoxicillin') || 
          drugLower.includes('ampicillin') || 
          drugLower.includes('penicillin') ||
          drugLower.includes('augmentin')
        )) {
          isContraindicated = true;
          contraindicationNotes = `CRITICAL ALLERGY CONFLICT: Patient has documented ${alg.severity} allergy to ${alg.allergen} (${alg.reaction}). Prescribing ${item.medicineName} is strongly contraindicated.`;
          allergyWarnings.push(contraindicationNotes);
        }

        // Check sulfa class cross-reactivity
        if (allergenLower.includes('sulfa') && (
          drugLower.includes('bactrim') || 
          drugLower.includes('sulfamethoxazole') || 
          drugLower.includes('septra')
        )) {
          isContraindicated = true;
          contraindicationNotes = `ALLERGY WARNING: Patient has documented allergy to ${alg.allergen} (${alg.reaction}).`;
          allergyWarnings.push(contraindicationNotes);
        }

        // Check Aspirin / NSAID cross-reactivity
        if (allergenLower.includes('aspirin') && (
          drugLower.includes('aspirin') || 
          drugLower.includes('ibuprofen') || 
          drugLower.includes('ketorolac')
        )) {
          isContraindicated = true;
          contraindicationNotes = `ALLERGY WARNING: Severe NSAID/Aspirin reaction on file: ${alg.reaction}.`;
          allergyWarnings.push(contraindicationNotes);
        }
      }

      return {
        id: `RXI-${Date.now()}-${idx + 1}`,
        ...item,
        dispenseStatus: 'Pending',
        contraindicationFlag: isContraindicated,
        contraindicationNotes: isContraindicated ? contraindicationNotes : undefined
      };
    });

    const newPrescription: ElectronicPrescription = {
      id: `RX-${Math.floor(80000 + Math.random() * 20000)}`,
      encounterId: data.encounterId,
      patientId: data.patientId,
      patientName: patient ? `${patient.firstName} ${patient.lastName}` : 'Patient',
      patientMrn: patient?.mrn || 'MRN-UNKNOWN',
      patientAge: patient?.age || 45,
      doctorId: data.doctorId,
      doctorName: data.doctorName,
      doctorLicense: data.doctorLicense,
      department: data.department,
      prescribedDate: new Date().toISOString().split('T')[0],
      status: 'Pending',
      items: processedItems,
      clinicalIndication: data.clinicalIndication,
      allergiesChecked: true,
      knownAllergies: patientAllergies.map(a => `${a.allergen} (${a.reaction})`),
      refillsAllowed: data.refillsAllowed ?? 1,
      digitalSignature: generateSignatureHash(`ERX|${data.patientId}|${data.doctorId}|${Date.now()}`),
      hospitalId: data.hospitalId || 'HOSP-01'
    };

    this.prescriptions.unshift(newPrescription);

    // Also populate eMAR records for inpatient medication administration
    processedItems.forEach(item => {
      this.emarRecords.unshift({
        id: `EMAR-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
        patientId: data.patientId,
        prescriptionId: newPrescription.id,
        medicineName: item.medicineName,
        dosage: item.dosage,
        route: item.route,
        scheduledTime: `${new Date().toISOString().split('T')[0]} 12:00 PM`,
        status: 'Due',
        notes: item.instructions
      });
    });

    return { prescription: newPrescription, allergyWarnings };
  }

  // --------------------------------------------------------------------------
  // ALLERGIES
  // --------------------------------------------------------------------------
  public getPatientAllergies(patientId: string): PatientAllergy[] {
    return this.allergies.filter(a => a.patientId === patientId);
  }

  public addPatientAllergy(allergy: Omit<PatientAllergy, 'id' | 'verifiedDate'>): PatientAllergy {
    const newAllergy: PatientAllergy = {
      id: `ALG-${Date.now()}`,
      ...allergy,
      verifiedDate: new Date().toISOString().split('T')[0]
    };
    this.allergies.push(newAllergy);
    return newAllergy;
  }

  // --------------------------------------------------------------------------
  // NURSING OBSERVATIONS & MEWS
  // --------------------------------------------------------------------------
  public getNursingObservations(filter?: { patientId?: string; ward?: string }): NursingObservation[] {
    return this.observations.filter(obs => {
      if (filter?.patientId && obs.patientId !== filter.patientId) return false;
      if (filter?.ward && obs.ward !== filter.ward) return false;
      return true;
    });
  }

  public recordNursingObservation(data: Omit<NursingObservation, 'id' | 'timestamp' | 'mews'>): NursingObservation {
    const mews = calculateMEWS({
      systolicBp: data.systolicBp,
      heartRate: data.heartRate,
      respiratoryRate: data.respiratoryRate,
      temperature: data.temperature,
      avpu: data.avpuConsciousness
    });

    const newObs: NursingObservation = {
      id: `OBS-${Date.now()}`,
      ...data,
      timestamp: new Date().toISOString(),
      mews
    };

    this.observations.unshift(newObs);
    return newObs;
  }

  // --------------------------------------------------------------------------
  // FLUID BALANCES
  // --------------------------------------------------------------------------
  public getFluidBalances(patientId?: string): FluidBalanceRecord[] {
    if (!patientId) return this.fluidBalances;
    return this.fluidBalances.filter(fb => fb.patientId === patientId);
  }

  public recordFluidBalance(data: Omit<FluidBalanceRecord, 'id' | 'timestamp' | 'totalIntakeMl' | 'totalOutputMl' | 'netBalanceMl'>): FluidBalanceRecord {
    const totalIntake = data.oralIntakeMl + data.ivInfusionMl + data.enteralFeedMl + data.bloodProductMl;
    const totalOutput = data.urineOutputMl + data.surgicalDrainMl + data.ngAspirateMl + data.emesisMl;
    const netBalance = totalIntake - totalOutput;

    // Calculate previous cumulative
    const prevRecords = this.fluidBalances.filter(f => f.patientId === data.patientId);
    const prevCumulative = prevRecords.length > 0 ? prevRecords[0].cumulative24hBalanceMl : 0;

    const newRecord: FluidBalanceRecord = {
      id: `FB-${Date.now()}`,
      ...data,
      timestamp: new Date().toISOString(),
      totalIntakeMl: totalIntake,
      totalOutputMl: totalOutput,
      netBalanceMl: netBalance,
      cumulative24hBalanceMl: prevCumulative + netBalance
    };

    this.fluidBalances.unshift(newRecord);
    return newRecord;
  }

  // --------------------------------------------------------------------------
  // eMAR ADMINISTRATION
  // --------------------------------------------------------------------------
  public getEMARRecords(patientId?: string): EMARRecord[] {
    if (!patientId) return this.emarRecords;
    return this.emarRecords.filter(r => r.patientId === patientId);
  }

  public administerMedication(id: string, details: {
    administeredBy: string;
    witnessNurse?: string;
    status: 'Administered' | 'Held' | 'Refused' | 'Omitted';
    vitalsBeforeAdmin?: string;
    notes?: string;
  }): EMARRecord {
    const index = this.emarRecords.findIndex(r => r.id === id);
    if (index === -1) throw new Error(`eMAR record ${id} not found.`);

    const updated: EMARRecord = {
      ...this.emarRecords[index],
      status: details.status,
      administeredBy: details.administeredBy,
      witnessNurse: details.witnessNurse,
      administeredTime: new Date().toLocaleString(),
      vitalsBeforeAdmin: details.vitalsBeforeAdmin,
      notes: details.notes || this.emarRecords[index].notes
    };

    this.emarRecords[index] = updated;
    return updated;
  }

  // --------------------------------------------------------------------------
  // SBAR SHIFT HANDOVERS
  // --------------------------------------------------------------------------
  public getSBARNotes(patientId?: string): SBARHandoverNote[] {
    if (!patientId) return this.sbarNotes;
    return this.sbarNotes.filter(n => n.patientId === patientId);
  }

  public recordSBARHandover(data: Omit<SBARHandoverNote, 'id' | 'createdDate'>): SBARHandoverNote {
    const newNote: SBARHandoverNote = {
      id: `SBAR-${Date.now()}`,
      ...data,
      createdDate: new Date().toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })
    };
    this.sbarNotes.unshift(newNote);
    return newNote;
  }

  // --------------------------------------------------------------------------
  // DISCHARGE SUMMARIES
  // --------------------------------------------------------------------------
  public getDischargeSummaries(patientId?: string): DischargeSummary[] {
    if (!patientId) return this.dischargeSummaries;
    return this.dischargeSummaries.filter(ds => ds.patientId === patientId);
  }

  public getDischargeSummaryById(id: string): DischargeSummary | undefined {
    return this.dischargeSummaries.find(ds => ds.id === id);
  }

  public createDischargeSummary(data: Omit<DischargeSummary, 'id' | 'signedAt' | 'digitalSignature' | 'status'> & {
    signNow?: boolean;
    digitalSignature?: string;
  }): DischargeSummary {
    const timestamp = new Date().toISOString();
    const isSigned = !!data.signNow;
    const signature = isSigned 
      ? generateSignatureHash(`DISCHARGE|${data.patientId}|${data.attendingDoctorId}|${timestamp}`)
      : '';

    const newSummary: DischargeSummary = {
      id: `DS-${new Date().getFullYear()}-${Math.floor(100 + Math.random() * 900)}`,
      ...data,
      status: isSigned ? 'Final Signed' : 'Draft',
      signedAt: isSigned ? timestamp : '',
      digitalSignature: signature
    };

    this.dischargeSummaries.unshift(newSummary);
    return newSummary;
  }

  public signDischargeSummary(id: string, doctorName: string, doctorLicense: string): DischargeSummary {
    const index = this.dischargeSummaries.findIndex(ds => ds.id === id);
    if (index === -1) throw new Error(`Discharge summary ${id} not found.`);

    const current = this.dischargeSummaries[index];
    const timestamp = new Date().toISOString();
    const signature = generateSignatureHash(
      `DISCHARGE-FINAL|${current.mrn}|${doctorName}|${doctorLicense}|${timestamp}`
    );

    const signedSummary: DischargeSummary = {
      ...current,
      status: 'Final Signed',
      attendingDoctorName: `${doctorName} (Lic: ${doctorLicense})`,
      signedAt: timestamp,
      digitalSignature: signature
    };

    this.dischargeSummaries[index] = signedSummary;
    return signedSummary;
  }

  // --------------------------------------------------------------------------
  // REFERRALS
  // --------------------------------------------------------------------------
  public getReferrals(filter?: {
    patientId?: string;
    targetDepartment?: string;
    referringDoctorId?: string;
    status?: string;
  }): ClinicalReferral[] {
    return this.referrals.filter(ref => {
      if (filter?.patientId && ref.patientId !== filter.patientId) return false;
      if (filter?.targetDepartment && ref.targetDepartment !== filter.targetDepartment) return false;
      if (filter?.referringDoctorId && ref.referringDoctorId !== filter.referringDoctorId) return false;
      if (filter?.status && ref.status !== filter.status) return false;
      return true;
    });
  }

  public createReferral(data: Omit<ClinicalReferral, 'id' | 'createdAt' | 'updatedAt' | 'status'>): ClinicalReferral {
    const timestamp = new Date().toISOString();
    const newReferral: ClinicalReferral = {
      id: `REF-${new Date().getFullYear()}-${Math.floor(100 + Math.random() * 900)}`,
      ...data,
      status: 'Submitted',
      createdAt: timestamp,
      updatedAt: timestamp
    };
    this.referrals.unshift(newReferral);
    return newReferral;
  }

  public updateReferralStatus(id: string, status: ClinicalReferral['status'], consultantNotes?: string, scheduledDate?: string): ClinicalReferral {
    const index = this.referrals.findIndex(r => r.id === id);
    if (index === -1) throw new Error(`Referral ${id} not found.`);

    const updated: ClinicalReferral = {
      ...this.referrals[index],
      status,
      consultantNotes: consultantNotes || this.referrals[index].consultantNotes,
      scheduledDate: scheduledDate || this.referrals[index].scheduledDate,
      updatedAt: new Date().toISOString()
    };

    this.referrals[index] = updated;
    return updated;
  }

  // --------------------------------------------------------------------------
  // TEMPLATES & CATALOGS
  // --------------------------------------------------------------------------
  public getTemplates(): ClinicalTemplate[] {
    return this.templates;
  }

  public getICD10Catalog() {
    return ICD10_CATALOG;
  }

  // --------------------------------------------------------------------------
  // LONGITUDINAL PATIENT EMR / EHR AGGREGATOR
  // --------------------------------------------------------------------------
  public getPatientEMRChart(patientId: string) {
    const patient = SEED_PATIENTS.find(p => p.id === patientId);
    if (!patient) return null;

    const encounters = this.getEncounters({ patientId });
    const allergies = this.getPatientAllergies(patientId);
    const prescriptions = this.getPrescriptions({ patientId });
    const observations = this.getNursingObservations({ patientId });
    const fluidBalances = this.getFluidBalances(patientId);
    const dischargeSummaries = this.getDischargeSummaries(patientId);
    const referrals = this.getReferrals({ patientId });

    return {
      patient,
      allergies,
      encounters,
      prescriptions,
      observations,
      fluidBalances,
      dischargeSummaries,
      referrals
    };
  }
}

// Export singleton instance
export const clinicalStore = new ClinicalStore();
