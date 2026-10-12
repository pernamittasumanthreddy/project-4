import { 
  ClinicalEncounter, 
  ClinicalTemplate, 
  ICD10Diagnosis, 
  PatientAllergy, 
  ElectronicPrescription, 
  NursingObservation, 
  FluidBalanceRecord, 
  EMARRecord, 
  SBARHandoverNote, 
  DischargeSummary, 
  ClinicalReferral,
  MEWSCalculation
} from '../types/clinical';

/**
 * STANDARD ICD-10 CLINICAL CODE CATALOG
 */
export const ICD10_CATALOG = [
  { code: 'I25.10', desc: 'Atherosclerotic heart disease of native coronary artery without angina pectoris', category: 'Cardiology' },
  { code: 'I21.9', desc: 'Acute myocardial infarction, unspecified (STEMI/NSTEMI)', category: 'Cardiology' },
  { code: 'I10', desc: 'Essential (primary) hypertension', category: 'Cardiology' },
  { code: 'I50.9', desc: 'Heart failure, unspecified (Congestive Heart Failure)', category: 'Cardiology' },
  { code: 'I48.91', desc: 'Unspecified atrial fibrillation', category: 'Cardiology' },
  { code: 'E11.9', desc: 'Type 2 diabetes mellitus without complications', category: 'Endocrinology' },
  { code: 'E11.65', desc: 'Type 2 diabetes mellitus with hyperglycemia', category: 'Endocrinology' },
  { code: 'E78.5', desc: 'Hyperlipidemia, unspecified', category: 'Endocrinology' },
  { code: 'J44.9', desc: 'Chronic obstructive pulmonary disease, unspecified (COPD)', category: 'Pulmonology' },
  { code: 'J18.9', desc: 'Pneumonia, unspecified organism', category: 'Pulmonology' },
  { code: 'J45.909', desc: 'Unspecified asthma, uncomplicated', category: 'Pulmonology' },
  { code: 'N18.30', desc: 'Chronic kidney disease, stage 3 unspecified', category: 'Nephrology' },
  { code: 'N39.0', desc: 'Urinary tract infection, site not specified', category: 'Infectious' },
  { code: 'A41.9', desc: 'Sepsis, unspecified organism', category: 'Infectious' },
  { code: 'K21.9', desc: 'Gastro-esophageal reflux disease without esophagitis (GERD)', category: 'Gastroenterology' },
  { code: 'G43.909', desc: 'Migraine, unspecified, not intractable', category: 'Neurology' },
  { code: 'M54.5', desc: 'Low back pain, unspecified', category: 'Orthopedics' },
  { code: 'S72.001A', desc: 'Fracture of head of right femur (Hip Fracture), initial encounter', category: 'Trauma' }
];

/**
 * COMMON ALLERGIES
 */
export const SEED_PATIENT_ALLERGIES: PatientAllergy[] = [
  {
    id: 'ALG-101',
    patientId: 'PT-10023', // John Anderson
    allergen: 'Penicillin / Amoxicillin',
    category: 'Medication',
    reaction: 'Anaphylaxis, severe diffuse urticaria, bronchospasm (2018)',
    severity: 'Life Threatening / Anaphylaxis',
    verifiedDate: '2026-01-15',
    verifiedBy: 'Dr. Marcus Vance, MD',
    status: 'Active'
  },
  {
    id: 'ALG-102',
    patientId: 'PT-10023',
    allergen: 'Iodinated Radiocontrast Media',
    category: 'Medication',
    reaction: 'Mild facial erythema and pruritus',
    severity: 'Moderate',
    verifiedDate: '2026-03-20',
    verifiedBy: 'Dr. Jonathan Blake, MD',
    status: 'Active'
  },
  {
    id: 'ALG-103',
    patientId: 'PT-10045', // Elena Rostova
    allergen: 'Sulfonamides (Bactrim/Septra)',
    category: 'Medication',
    reaction: 'Erythematous maculopapular rash on trunk',
    severity: 'Moderate',
    verifiedDate: '2025-11-10',
    verifiedBy: 'Dr. Thomas Hayes, MD',
    status: 'Active'
  },
  {
    id: 'ALG-104',
    patientId: 'PT-10089', // Marcus Brody
    allergen: 'Aspirin (NSAIDs)',
    category: 'Medication',
    reaction: 'Bronchoconstriction and periorbital edema',
    severity: 'Severe',
    verifiedDate: '2026-02-04',
    verifiedBy: 'Dr. Robert Thorne, MD',
    status: 'Active'
  },
  {
    id: 'ALG-105',
    patientId: 'PT-10045',
    allergen: 'Tree Nuts & Peanuts',
    category: 'Food',
    reaction: 'Oral tingling, lip angioedema',
    severity: 'Severe',
    verifiedDate: '2024-06-12',
    verifiedBy: 'Dr. Emily Watson, MD',
    status: 'Active'
  }
];

/**
 * CLINICAL DOCUMENTATION TEMPLATES
 */
export const CLINICAL_TEMPLATES: ClinicalTemplate[] = [
  {
    id: 'TPL-CARDIO-01',
    title: 'Cardiology Consultation & Post-PCI Evaluation',
    department: 'Cardiology',
    encounterType: 'Outpatient Consultation',
    description: 'Comprehensive coronary artery disease review, telemetry assessment, and dual antiplatelet management.',
    defaultChiefComplaint: 'Routine outpatient cardiology follow-up post percutaneous coronary intervention (PCI).',
    subjectiveTemplate: `Patient presents for scheduled cardiology follow-up. 
Denies recurrent chest tightness, exertional dyspnea, orthopnea, or paroxysmal nocturnal dyspnea.
Reports strict adherence to dual antiplatelet regimen and statin therapy.
No reported lightheadedness, syncope, or palpitations.
Exercise tolerance: ambulates comfortably 30-45 minutes without angina.`,
    objectiveTemplate: `Vitals: As charted in flow sheet.
General: Well-nourished, comfortable, in no acute cardiovascular distress.
HEENT: Normocephalic, moist mucous membranes, no carotid bruits.
Chest/Lungs: Clear to auscultation bilaterally; no wheezes, rales, or rhonchi.
Cardiovascular: Regular rate and rhythm, normal S1 and S2. No murmur, gallop (S3/S4), or pericardial friction rub. PMI non-displaced.
Extremities: Radial and dorsalis pedis pulses 2+ bilaterally. No peripheral edema. Femoral/radial sheath access site clean, well-healed without hematoma or bruit.`,
    assessmentTemplate: `1. Coronary Artery Disease (CAD), status-post drug-eluting stent (DES) placement to LAD - Stable.
2. Essential Hypertension - Well controlled on current regimen.
3. Hyperlipidemia - Target LDL < 55 mg/dL on high-intensity statin.`,
    planTemplate: `1. Continue Aspirin 81mg PO daily and Ticagrelor 90mg PO BID (complete 12-month DAPT course).
2. Continue Atorvastatin 80mg PO qHS.
3. Order fasting lipid profile, comprehensive metabolic panel, and CBC in 4 weeks.
4. Referral to Cardiac Rehabilitation 3x/week.
5. Return to clinic in 3 months or sooner for acute chest discomfort or bleeding.`,
    commonDiagnoses: [
      { code: 'I25.10', desc: 'Atherosclerotic heart disease of native coronary artery' },
      { code: 'I10', desc: 'Essential (primary) hypertension' },
      { code: 'E78.5', desc: 'Hyperlipidemia, unspecified' }
    ]
  },
  {
    id: 'TPL-OPD-SOAP-02',
    title: 'General Internal Medicine Adult SOAP Encounter',
    department: 'Internal Medicine',
    encounterType: 'Outpatient Consultation',
    description: 'Standard adult ambulatory medical evaluation covering multi-system chronic disease management.',
    defaultChiefComplaint: 'Follow-up for chronic hypertension, diabetes management, and routine medication refill.',
    subjectiveTemplate: `Patient seen for interval chronic disease follow-up. 
Home blood pressure logs demonstrate systolic 125-135, diastolic 75-84.
Home fasting blood glucoses range 110-140 mg/dL.
Denies polyuria, polydipsia, blurred vision, numbness/tingling in lower extremities.
Review of Systems (ROS): Negative for chest pain, shortness of breath, abdominal pain, or changes in bowel/bladder habits.`,
    objectiveTemplate: `Vitals: Within normal parameters.
General: Alert, oriented x 4, pleasant, well hydrated.
Cardiovascular: RRR, S1/S2 present, no murmurs.
Respiratory: Clear breath sounds throughout lung fields.
Abdomen: Soft, non-tender, non-distended, normoactive bowel sounds.
Extremities: No cyanosis or clubbing; sensation intact to monofilament exam bilateral lower extremities.`,
    assessmentTemplate: `1. Type 2 Diabetes Mellitus - Moderately controlled (A1c target < 7.0%).
2. Essential Hypertension - Controlled.
3. Routine Health Maintenance.`,
    planTemplate: `1. Continue Metformin 1000mg PO BID with meals.
2. Continue Lisinopril 20mg PO daily.
3. Order Hemoglobin A1c, Urine Microalbumin/Creatinine ratio, and eGFR.
4. Annual diabetic foot exam and ophthalmology retinal screening scheduled.
5. Follow-up visit in 3-4 months.`,
    commonDiagnoses: [
      { code: 'E11.9', desc: 'Type 2 diabetes mellitus without complications' },
      { code: 'I10', desc: 'Essential (primary) hypertension' }
    ]
  },
  {
    id: 'TPL-ED-CHEST-03',
    title: 'Emergency Resuscitation & Acute Chest Pain Triage',
    department: 'Emergency',
    encounterType: 'Emergency Intake',
    description: 'Acute coronary syndrome (ACS) protocol, EKG evaluation, troponin rule-out, and trauma stabilization.',
    defaultChiefComplaint: 'Acute onset retrosternal crushing chest pressure radiating to left arm and jaw x 45 minutes.',
    subjectiveTemplate: `Patient brought by EMS for acute severe substernal pressure (rated 8/10).
Onset while at rest 45 minutes prior to arrival. Associated with diaphoresis, mild nausea, and dyspnea.
Denies prior history of myocardial infarction. Received Aspirin 324mg chewed in transit.
Sublingual nitroglycerin administered x 1 by EMS with mild transient relief (pain 6/10).`,
    objectiveTemplate: `Vitals: BP 154/92, HR 96 bpm, RR 22/min, SpO2 96% on 2L nasal cannula, Temp 98.4°F.
General: Moderately distressed, diaphoretic, clutching sternum.
Cardiovascular: Tachycardic, S1/S2 heard, no loud murmur, no JVD.
Lungs: Minimal bibasilar crackles, no audible wheezing.
EKG: Sinus rhythm with 2mm ST-segment elevation in leads V2-V4 (STEMI criteria met).
Bedside Point-of-Care Troponin I: 0.85 ng/mL (Significantly elevated).`,
    assessmentTemplate: `1. Acute ST-Elevation Myocardial Infarction (STEMI) - Antero-septal wall involvement.
2. High-risk acute ischemic emergency.`,
    planTemplate: `1. ACTIVATE CARDIAC CATHETERIZATION LAB STAT (Code STEMI protocol).
2. Administer Heparin bolus 5,000 units IV + IV infusion protocol.
3. Administer Ticagrelor 180mg PO loading dose.
4. Continuous telemetry and defibrillator pads placed.
5. Immediate interventional cardiology consultation and transfer to Cath Lab 2.`,
    commonDiagnoses: [
      { code: 'I21.9', desc: 'Acute myocardial infarction, unspecified' },
      { code: 'I25.10', desc: 'Atherosclerotic heart disease' }
    ]
  },
  {
    id: 'TPL-INPATIENT-ROUND-04',
    title: 'Inpatient Telemetry Daily Progress & Ward Round',
    department: 'Cardiology',
    encounterType: 'Inpatient Daily Round',
    description: 'Daily SOAP progress note for hospitalized patients covering active lines, telemetry, and discharge milestones.',
    defaultChiefComplaint: 'Inpatient Post-PCI Day 2 progress evaluation.',
    subjectiveTemplate: `Overnight event review: Patient slept well without nocturnal chest tightness or respiratory distress.
Tolerating cardiac diet. Ambulated hallway with physical therapy this morning.
Voiding spontaneously, bowel movement occurred yesterday.
Pain score: 0/10 at rest.`,
    objectiveTemplate: `Telemetry strip: Normal sinus rhythm, rate 68-76 bpm, PR and QTc intervals within normal limits. No ectopy or pauses.
Vitals: BP 122/78 mmHg, HR 70 bpm, RR 16/min, SpO2 98% room air, Temp 98.6°F.
Exam: Cardiac RRR, clear lungs, soft non-tender abdomen, bilateral groin/radial sites clean and dry without hematoma. Peripheral IV patent in right forearm.`,
    assessmentTemplate: `1. Post-percutaneous coronary intervention (PCI of Mid-LAD with DES) - Excellent clinical recovery.
2. Hemodynamically stable.
3. Laboratory review: Morning Potassium 4.2 mEq/L, Creatinine 0.9 mg/dL, Troponin trending downward appropriately.`,
    planTemplate: `1. Discontinue continuous telemetry monitoring at 16:00 if stable.
2. Remove peripheral IV cannula.
3. Finalize outpatient prescription medications.
4. Prepare discharge summary for release tomorrow morning at 10:00 AM.`,
    commonDiagnoses: [
      { code: 'I25.10', desc: 'Atherosclerotic heart disease' },
      { code: 'I10', desc: 'Essential hypertension' }
    ]
  }
];

/**
 * INITIAL CLINICAL ENCOUNTERS
 */
export const SEED_CLINICAL_ENCOUNTERS: ClinicalEncounter[] = [
  {
    id: 'ENC-2026-1049',
    patientId: 'PT-10023',
    patientMrn: 'MRN-884920',
    patientName: 'John Anderson',
    patientAge: 58,
    patientGender: 'Male',
    doctorId: 'USR-DOC-03',
    doctorName: 'Dr. Marcus Vance, MD, FACC',
    department: 'Cardiology',
    encounterType: 'Inpatient Daily Round',
    encounterDate: '2026-10-04',
    startTime: '08:30 AM',
    endTime: '09:10 AM',
    status: 'Signed',
    signStatus: 'Signed',
    chiefComplaint: 'Post-percutaneous coronary intervention (DES stenting of Mid-LAD) Day 2 inpatient round.',
    historyOfPresentIllness: '58-year-old male with known CAD status-post successful DES placement to mid-LAD 48 hours ago. Patient has remained chest pain free, denies exertional shortness of breath, palpitations, or lightheadedness.',
    pastMedicalHistory: 'CAD s/p PCI, Essential Hypertension x 8 years, Hyperlipidemia, No prior stroke or CABG.',
    familyHistory: 'Father had MI at age 62; Mother alive with hypertension.',
    socialHistory: 'Former smoker (quit 2 years ago, 20 pack-year history). Occasional alcohol.',
    reviewOfSystems: 'Constitutional: No fever, chills, or night sweats. CV: Denies angina or palpitations. Resp: Denies cough or wheezing. GI: Denies nausea or vomiting. Neuro: Intact.',
    vitals: {
      systolicBp: 124,
      diastolicBp: 80,
      heartRate: 72,
      respiratoryRate: 16,
      spo2: 98,
      temperature: 98.6,
      tempUnit: 'F',
      painScore: 0,
      weightKg: 82.5,
      heightCm: 178,
      bmi: 26.0,
      gcsScore: 15,
      bloodGlucoseMgDl: 112,
      recordedAt: '2026-10-04T08:15:00Z',
      recordedBy: 'Sarah Jenkins, RN'
    },
    examination: {
      generalAppearance: 'Alert, oriented x 4, comfortably sitting in chair, in no acute distress.',
      heent: 'Normocephalic, PERRLA, moist oral mucosa, no jugular venous distention (JVD).',
      cardiovascular: 'Regular rate and rhythm, normal S1 and S2, no murmurs, rubs, or gallops heard.',
      respiratory: 'Lungs clear to auscultation bilaterally, good air entry, no wheezes or rales.',
      abdomen: 'Soft, non-distended, non-tender, normal bowel sounds present.',
      neurological: 'Alert, CN II-XII grossly intact, non-focal motor and sensory exam.',
      musculoskeletal: 'Good range of motion, peripheral pulses 2+ in all 4 extremities.',
      skinLympatics: 'Right radial arterial sheath site clean, dry, intact without hematoma, bruit, or bleeding.'
    },
    subjectiveNotes: 'Patient states he feels significantly stronger today. Ambulated around the cardiology telemetry unit without any chest tightness or dizziness. Denies nausea. Slept 7 hours undisturbed.',
    objectiveNotes: 'Vitals stable. BP 124/80, HR 72 regular, SpO2 98% room air. Telemetry confirms continuous sinus rhythm without ventricular ectopy. Access site clean. Morning Labs: K 4.1 mEq/L, BUN 16, Cr 0.92, Trop I down-trending to 0.04 ng/mL.',
    assessmentNotes: '1. Atherosclerotic coronary artery disease s/p successful mid-LAD drug-eluting stent (DES) - Clinically stable, uncomplicated post-procedure recovery.\n2. Essential Hypertension - Well controlled on beta-blocker.\n3. Hyperlipidemia - High-intensity statin therapy maintained.',
    planNotes: '1. Continue dual antiplatelet therapy: Aspirin 81mg daily and Ticagrelor 90mg BID for minimum 12 months.\n2. Continue Metoprolol Succinate 50mg daily and Atorvastatin 80mg daily.\n3. Discontinue continuous cardiac telemetry monitoring at 14:00 today.\n4. Discharge scheduled for tomorrow 10:00 AM.\n5. Follow-up clinic appointment scheduled in 4 weeks.',
    diagnoses: [
      {
        id: 'DX-101',
        code: 'I25.10',
        description: 'Atherosclerotic heart disease of native coronary artery without angina pectoris',
        type: 'Primary',
        certainty: 'Confirmed',
        diagnosedBy: 'Dr. Marcus Vance, MD',
        diagnosedAt: '2026-10-04T08:45:00Z'
      },
      {
        id: 'DX-102',
        code: 'I10',
        description: 'Essential (primary) hypertension',
        type: 'Secondary',
        certainty: 'Confirmed',
        diagnosedBy: 'Dr. Marcus Vance, MD',
        diagnosedAt: '2026-10-04T08:45:00Z'
      }
    ],
    allergiesSnapshot: ['Penicillin (Anaphylaxis)', 'Iodinated Radiocontrast Media (Mild Rash)'],
    prescriptionIds: ['RX-88401'],
    labOrderIds: ['LAB-10023-01'],
    radiologyScanIds: ['RAD-10023-01'],
    treatmentPlan: 'Maintain DAPT, high-intensity statin, cardiac rehabilitation 3x/wk, low sodium diet (<2g/day).',
    patientInstructions: 'Do not discontinue Aspirin or Ticagrelor without cardiologist consultation. Seek immediate emergency evaluation for crushing chest pain, shortness of breath, or bleeding.',
    followUpDate: '2026-11-04',
    signedBy: 'Dr. Marcus Vance, MD, FACC (License: MD-88392-CA)',
    signedAt: '2026-10-04T09:12:00Z',
    digitalSignatureHash: 'SHA256:d8a9f3b5e4c27891104eab841972b901a884efc71329',
    amendments: [
      {
        id: 'AMD-01',
        encounterId: 'ENC-2026-1049',
        version: 1,
        amendmentType: 'Addendum',
        amendedBy: 'Dr. Marcus Vance, MD',
        amendedByRole: 'DOCTOR',
        amendedAt: '2026-10-04T14:30:00Z',
        reasonForAmendment: 'Review of afternoon echocardiogram results.',
        amendmentContent: 'Addendum: Transthoracic echocardiogram reviewed. Left ventricular ejection fraction (LVEF) is 52% with mild hypokinesis of mid-anterior septum. No pericardial effusion or severe valvular disease. No medication dosage adjustments required.',
        digitalSignatureHash: 'SHA256:7f49c011e828479ba921ef0021bca981329ff0'
      }
    ],
    hospitalId: 'HOSP-01'
  },
  {
    id: 'ENC-2026-1050',
    patientId: 'PT-10045',
    patientMrn: 'MRN-449182',
    patientName: 'Elena Rostova',
    patientAge: 42,
    patientGender: 'Female',
    doctorId: 'USR-DOC-03',
    doctorName: 'Dr. Marcus Vance, MD, FACC',
    department: 'Cardiology',
    encounterType: 'Outpatient Consultation',
    encounterDate: '2026-10-04',
    startTime: '09:30 AM',
    endTime: '10:05 AM',
    status: 'In Progress',
    signStatus: 'Draft',
    chiefComplaint: 'Palpitations and occasional lightheadedness over the last 3 weeks.',
    historyOfPresentIllness: '42-year-old female presents with episodic rapid heart fluttering occurring 2-3 times weekly, typically lasting 10-20 minutes. Accompanied by mild lightheadedness, but no true syncope, chest pain, or dyspnea.',
    pastMedicalHistory: 'Mild asthma, Migraine headaches without aura.',
    reviewOfSystems: 'Denies chest pain, orthopnea, ankle swelling, or thyroid symptoms.',
    vitals: {
      systolicBp: 118,
      diastolicBp: 74,
      heartRate: 82,
      respiratoryRate: 18,
      spo2: 99,
      temperature: 98.4,
      tempUnit: 'F',
      painScore: 0,
      recordedAt: '2026-10-04T09:15:00Z',
      recordedBy: 'Nurse Jessica Gomez'
    },
    examination: {
      generalAppearance: 'Alert, pleasant, no respiratory distress.',
      cardiovascular: 'Regular rhythm at 82 bpm, S1/S2 crisp, no murmur or click heard.',
      respiratory: 'Bilateral lung fields clear to auscultation without wheeze.'
    },
    subjectiveNotes: 'Patient describes episodes as sudden "flip-flopping" in the chest, particularly after consuming coffee or during work stress. No syncope.',
    objectiveNotes: 'In-office 12-lead EKG reveals normal sinus rhythm at 80 bpm with occasional premature atrial complexes (PACs). PR interval 150ms, QRS 84ms, QTc 418ms.',
    assessmentNotes: '1. Paroxysmal palpitations, likely benign premature atrial contractions (PACs) vs paroxysmal supraventricular tachycardia (PSVT).\n2. Normal resting hemodynamic profile.',
    planNotes: '1. Order 14-day continuous ambulatory Zio patch ECG telemetry monitor.\n2. Check serum TSH, Free T4, Potassium, Magnesium, and complete blood count.\n3. Lifestyle guidance: reduce caffeine and ensure adequate hydration.\n4. Re-evaluate in clinic following Zio patch completion.',
    diagnoses: [
      {
        id: 'DX-103',
        code: 'I48.91',
        description: 'Unspecified atrial fibrillation / Paroxysmal atrial arrhythmia',
        type: 'Differential',
        certainty: 'Suspected',
        diagnosedBy: 'Dr. Marcus Vance, MD',
        diagnosedAt: '2026-10-04T09:40:00Z'
      }
    ],
    allergiesSnapshot: ['Sulfonamides (Rash)', 'Tree nuts (Angioedema)'],
    prescriptionIds: [],
    labOrderIds: [],
    radiologyScanIds: [],
    treatmentPlan: 'Diagnostic holter monitoring, lab panel, caffeine restriction.',
    patientInstructions: 'Log symptoms with exact timestamp during palpitations. Go to ER if palpitations persist > 1 hour with chest pain or syncope.',
    amendments: [],
    hospitalId: 'HOSP-01'
  }
];

/**
 * ELECTRONIC PRESCRIPTIONS
 */
export const SEED_ELECTRONIC_PRESCRIPTIONS: ElectronicPrescription[] = [
  {
    id: 'RX-88401',
    encounterId: 'ENC-2026-1049',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    patientMrn: 'MRN-884920',
    patientAge: 58,
    doctorId: 'USR-DOC-03',
    doctorName: 'Dr. Marcus Vance, MD',
    doctorLicense: 'MD-88392-CA',
    department: 'Cardiology',
    prescribedDate: '2026-10-04',
    status: 'Verified',
    items: [
      {
        id: 'RXI-01',
        medicineId: 'MED-101',
        medicineName: 'Ticagrelor (Brilinta)',
        genericName: 'Ticagrelor',
        dosage: '90 mg',
        route: 'Oral',
        frequency: 'BID (Twice Daily)',
        durationDays: 365,
        quantity: 730,
        instructions: 'Take 1 tablet by mouth twice daily with or without food. Crucial: do not miss doses.',
        indication: 'Dual antiplatelet therapy for drug-eluting stent prevention of thrombosis',
        dispenseStatus: 'Dispensed'
      },
      {
        id: 'RXI-02',
        medicineId: 'MED-102',
        medicineName: 'Aspirin Enteric Coated',
        genericName: 'Aspirin',
        dosage: '81 mg',
        route: 'Oral',
        frequency: 'QD (Once Daily)',
        durationDays: 365,
        quantity: 365,
        instructions: 'Take 1 tablet by mouth once daily in the morning with a full glass of water.',
        indication: 'Secondary prevention of atherosclerotic cardiovascular events',
        dispenseStatus: 'Dispensed'
      },
      {
        id: 'RXI-03',
        medicineId: 'MED-103',
        medicineName: 'Atorvastatin Calcium (Lipitor)',
        genericName: 'Atorvastatin',
        dosage: '80 mg',
        route: 'Oral',
        frequency: 'QD (Once Daily)',
        durationDays: 90,
        quantity: 90,
        instructions: 'Take 1 tablet by mouth at bedtime. Report any unexplained muscle pain.',
        indication: 'High-intensity lipid-lowering plaque stabilization',
        dispenseStatus: 'Pending'
      },
      {
        id: 'RXI-04',
        medicineId: 'MED-104',
        medicineName: 'Metoprolol Succinate ER (Toprol-XL)',
        genericName: 'Metoprolol Succinate',
        dosage: '50 mg',
        route: 'Oral',
        frequency: 'QD (Once Daily)',
        durationDays: 90,
        quantity: 90,
        instructions: 'Take 1 tablet once daily in the morning. Swallow whole, do not crush.',
        indication: 'Beta-blockade for myocardial oxygen demand reduction and BP control',
        dispenseStatus: 'Pending'
      }
    ],
    clinicalIndication: 'Post-PCI Acute Coronary Syndrome secondary prevention regimen',
    allergiesChecked: true,
    knownAllergies: ['Penicillin (Anaphylaxis)', 'Iodinated Radiocontrast Media'],
    refillsAllowed: 3,
    digitalSignature: 'SIG-VERIFIED:DrMarcusVance:MD-88392-CA:20261004',
    hospitalId: 'HOSP-01'
  }
];

/**
 * NURSING OBSERVATIONS & MEWS CALCULATIONS
 */
export function calculateMEWS(vitals: {
  systolicBp: number;
  heartRate: number;
  respiratoryRate: number;
  temperature: number; // in F
  avpu: 'Alert' | 'Voice' | 'Pain' | 'Unresponsive';
}): MEWSCalculation {
  let score = 0;

  // Systolic BP
  if (vitals.systolicBp <= 70) score += 3;
  else if (vitals.systolicBp <= 80) score += 2;
  else if (vitals.systolicBp <= 100) score += 1;
  else if (vitals.systolicBp >= 200) score += 2;

  // Heart Rate
  if (vitals.heartRate <= 40) score += 2;
  else if (vitals.heartRate <= 50) score += 1;
  else if (vitals.heartRate >= 130) score += 3;
  else if (vitals.heartRate >= 111) score += 2;
  else if (vitals.heartRate >= 101) score += 1;

  // Respiratory Rate
  if (vitals.respiratoryRate < 9) score += 2;
  else if (vitals.respiratoryRate >= 30) score += 3;
  else if (vitals.respiratoryRate >= 21) score += 2;
  else if (vitals.respiratoryRate >= 15) score += 1;

  // Temperature (F)
  if (vitals.temperature < 95.0) score += 2;
  else if (vitals.temperature >= 101.5) score += 2;

  // AVPU
  if (vitals.avpu === 'Voice') score += 1;
  else if (vitals.avpu === 'Pain') score += 2;
  else if (vitals.avpu === 'Unresponsive') score += 3;

  let riskCategory: MEWSCalculation['riskCategory'] = 'Low Risk (0-1)';
  let actionRequired = 'Routine 4-hourly ward vital signs monitoring.';

  if (score >= 6) {
    riskCategory = 'Critical Deterioration (>=6)';
    actionRequired = 'STAT Medical Emergency Team (MET) / Code Blue activation. Immediate physician bedside evaluation.';
  } else if (score >= 4) {
    riskCategory = 'High Alert (4-5)';
    actionRequired = 'Urgent attending physician notification. Increase monitoring frequency to every 30 minutes.';
  } else if (score >= 2) {
    riskCategory = 'Medium Risk (2-3)';
    actionRequired = 'Inform charge nurse. Increase vital signs frequency to hourly.';
  }

  return { score, riskCategory, actionRequired };
}

export const SEED_NURSING_OBSERVATIONS: NursingObservation[] = [
  {
    id: 'OBS-101',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    mrn: 'MRN-884920',
    ward: 'Cardiac Step-Down Unit 3A',
    bed: 'Bed 304-B',
    timestamp: '2026-10-04T08:00:00Z',
    nurseId: 'USR-NUR-04',
    nurseName: 'Sarah Jenkins, BSN, RN',
    systolicBp: 124,
    diastolicBp: 82,
    heartRate: 72,
    respiratoryRate: 16,
    spo2: 98,
    temperature: 98.6,
    painScore: 0,
    gcsScore: 15,
    avpuConsciousness: 'Alert',
    bloodSugarMgDl: 114,
    oxygenDevice: 'Room Air',
    mews: {
      score: 1,
      riskCategory: 'Low Risk (0-1)',
      actionRequired: 'Routine 4-hourly ward vital signs monitoring.'
    },
    nursingInterventions: 'Morning bedside assessment. Groin sheath access site evaluated - clean, soft, non-tender, no hematoma. Distal pedal pulses +2.',
    telemetryRhythm: 'Normal Sinus',
    fallRiskScore: 15,
    bradenSkinScore: 21
  },
  {
    id: 'OBS-102',
    patientId: 'PT-10045',
    patientName: 'Elena Rostova',
    mrn: 'MRN-449182',
    ward: 'Telemetry Unit 2',
    bed: 'Bed 212-A',
    timestamp: '2026-10-04T07:30:00Z',
    nurseId: 'USR-NUR-04',
    nurseName: 'Sarah Jenkins, BSN, RN',
    systolicBp: 118,
    diastolicBp: 74,
    heartRate: 82,
    respiratoryRate: 18,
    spo2: 96,
    temperature: 99.1,
    painScore: 1,
    gcsScore: 15,
    avpuConsciousness: 'Alert',
    bloodSugarMgDl: 102,
    oxygenDevice: 'Room Air',
    mews: {
      score: 1,
      riskCategory: 'Low Risk (0-1)',
      actionRequired: 'Routine 4-hourly ward vital signs monitoring.'
    },
    nursingInterventions: 'Nebulizer treatment administered. Breathing sounds clear, no audible stridor.',
    telemetryRhythm: 'Normal Sinus',
    fallRiskScore: 10,
    bradenSkinScore: 22
  },
  {
    id: 'OBS-103',
    patientId: 'PT-10089',
    patientName: 'Marcus Brody',
    mrn: 'MRN-194029',
    ward: 'Trauma Bay 1 / Emergency',
    bed: 'Bed 108',
    timestamp: '2026-10-04T09:00:00Z',
    nurseId: 'USR-NUR-04',
    nurseName: 'Sarah Jenkins, BSN, RN',
    systolicBp: 142,
    diastolicBp: 90,
    heartRate: 98,
    respiratoryRate: 22,
    spo2: 95,
    temperature: 100.4,
    painScore: 6,
    gcsScore: 14,
    avpuConsciousness: 'Alert',
    bloodSugarMgDl: 148,
    oxygenDevice: 'Nasal Cannula 2L',
    mews: {
      score: 3,
      riskCategory: 'Medium Risk (2-3)',
      actionRequired: 'Inform charge nurse. Increase vital signs frequency to hourly.'
    },
    nursingInterventions: 'Surgical wound inspection right lower leg. Ice pack applied, IV analgesia administered as ordered. Vital signs elevated due to post-trauma pain.',
    telemetryRhythm: 'Sinus Tachycardia',
    fallRiskScore: 35,
    bradenSkinScore: 18
  }
];

/**
 * FLUID BALANCE FLOWSHEETS
 */
export const SEED_FLUID_BALANCES: FluidBalanceRecord[] = [
  {
    id: 'FB-01',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    ward: 'Unit 3A Telemetry',
    bed: 'Bed 304-B',
    timestamp: '2026-10-04T12:00:00Z',
    nurseName: 'Sarah Jenkins, RN',
    oralIntakeMl: 650,
    ivInfusionMl: 500,
    enteralFeedMl: 0,
    bloodProductMl: 0,
    totalIntakeMl: 1150,
    urineOutputMl: 900,
    surgicalDrainMl: 0,
    ngAspirateMl: 0,
    emesisMl: 0,
    totalOutputMl: 900,
    netBalanceMl: 250,
    shift: 'Day',
    cumulative24hBalanceMl: 420,
    notes: 'Adequate oral intake. Clear yellow urine output exceeding 0.5 mL/kg/hr.'
  },
  {
    id: 'FB-02',
    patientId: 'PT-10089',
    patientName: 'Marcus Brody',
    ward: 'Trauma Bay 1',
    bed: 'Bed 108',
    timestamp: '2026-10-04T12:00:00Z',
    nurseName: 'Sarah Jenkins, RN',
    oralIntakeMl: 200,
    ivInfusionMl: 1000,
    enteralFeedMl: 0,
    bloodProductMl: 0,
    totalIntakeMl: 1200,
    urineOutputMl: 750,
    surgicalDrainMl: 80,
    ngAspirateMl: 0,
    emesisMl: 0,
    totalOutputMl: 830,
    netBalanceMl: 370,
    shift: 'Day',
    cumulative24hBalanceMl: 650,
    notes: '0.9% Normal Saline infusing at 100 mL/hr. Jackson-Pratt drain serosanguinous.'
  }
];

/**
 * 5-RIGHTS eMAR RECORDS
 */
export const SEED_EMAR_RECORDS: EMARRecord[] = [
  {
    id: 'EMAR-01',
    patientId: 'PT-10023',
    prescriptionId: 'RX-88401',
    medicineName: 'Ticagrelor (Brilinta)',
    dosage: '90 mg PO',
    route: 'Oral',
    scheduledTime: '2026-10-04 09:00 AM',
    administeredTime: '2026-10-04 09:05 AM',
    administeredBy: 'Sarah Jenkins, RN',
    witnessNurse: 'Lisa Morales, RN',
    status: 'Administered',
    notes: 'Patient confirmed identity via barcode wristband scan. Ingested with water without issue.',
    vitalsBeforeAdmin: 'BP 124/80, HR 72'
  },
  {
    id: 'EMAR-02',
    patientId: 'PT-10023',
    prescriptionId: 'RX-88401',
    medicineName: 'Aspirin Enteric Coated',
    dosage: '81 mg PO',
    route: 'Oral',
    scheduledTime: '2026-10-04 09:00 AM',
    administeredTime: '2026-10-04 09:05 AM',
    administeredBy: 'Sarah Jenkins, RN',
    status: 'Administered',
    notes: 'Administered concurrently with morning meal.',
    vitalsBeforeAdmin: 'BP 124/80, HR 72'
  },
  {
    id: 'EMAR-03',
    patientId: 'PT-10023',
    prescriptionId: 'RX-88401',
    medicineName: 'Atorvastatin (Lipitor)',
    dosage: '80 mg PO',
    route: 'Oral',
    scheduledTime: '2026-10-04 09:00 PM',
    status: 'Due',
    notes: 'Scheduled for evening administration.'
  }
];

/**
 * SBAR SHIFT HANDOVER NOTES
 */
export const SEED_SBAR_NOTES: SBARHandoverNote[] = [
  {
    id: 'SBAR-01',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    ward: 'Cardiac Step-Down Unit 3A',
    bed: 'Bed 304-B',
    createdDate: '2026-10-04 15:00',
    fromNurse: 'Sarah Jenkins, BSN, RN',
    toNurse: 'Michael Kelly, RN',
    shift: 'Day to Evening',
    situation: '58yo male s/p PCI to mid-LAD with DES Day 2, hemodynamically stable, prepared for anticipated morning discharge.',
    background: 'Admitted 10/02 with NSTEMI. Stented successfully. Strict DAPT adherence required. Penicillin anaphylaxis allergic.',
    assessment: 'Vitals stable all day (BP 120-128, HR 70-76 regular). Femoral/radial sites clean. Tolerating diet. Ambulated hallway x 2.',
    recommendation: 'Give evening Atorvastatin at 21:00. Discontinue telemetry per Dr. Vance order at 16:00. Ensure discharge packet and prescriptions are ready for 10:00 AM release.',
    codeStatus: 'Full Code',
    keyTasksForNextShift: [
      'Stop telemetry monitor at 16:00 if rhythm remains sinus',
      'Administer Atorvastatin 80mg at 21:00',
      'Check fasting morning blood glucose at 06:00',
      'Remind attending about morning discharge signature'
    ]
  }
];

/**
 * INPATIENT DISCHARGE SUMMARIES
 */
export const SEED_DISCHARGE_SUMMARIES: DischargeSummary[] = [
  {
    id: 'DS-2026-092',
    admissionId: 'ADM-10023',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    mrn: 'MRN-884920',
    age: 58,
    gender: 'Male',
    ward: 'Cardiac Step-Down 3A',
    bed: 'Bed 304-B',
    admissionDate: '2026-10-02',
    dischargeDate: '2026-10-05',
    admittingDiagnosis: 'Acute Non-ST Elevation Myocardial Infarction (NSTEMI) / Unstable Angina',
    dischargeDiagnosis: 'Coronary Artery Disease, status-post drug-eluting stent (DES) to mid-LAD',
    secondaryDiagnoses: [
      'Essential Hypertension',
      'Hyperlipidemia',
      'Tobacco use disorder in remission'
    ],
    hospitalCourse: `58-year-old male admitted with exertional retrosternal chest pain and elevated cardiac biomarkers (Troponin I peak 2.4 ng/mL). 
Underwent diagnostic coronary angiography on 10/02 demonstrating a 90% discrete stenosis of the mid-Left Anterior Descending (LAD) artery.
Successful percutaneous coronary intervention performed with deployment of a 3.0 x 18 mm drug-eluting stent with 0% residual stenosis and TIMI-3 flow.
Post-procedure recovery was uncomplicated in the Cardiac Care Unit and Step-Down Unit. Serial troponins decreased appropriately.
Continuous telemetry confirmed sinus rhythm without ventricular ectopy. Echocardiogram revealed preserved LVEF 52%.
Patient ambulated independently and achieved all cardiac rehabilitation phase 1 milestones.`,
    proceduresPerformed: [
      'Left Heart Catheterization and Coronary Angiography (10/02/2026)',
      'Percutaneous Coronary Intervention with Drug-Eluting Stent (DES) to Mid-LAD (10/02/2026)',
      'Transthoracic 2D Echocardiogram with Doppler (10/04/2026)'
    ],
    significantFindings: 'LVEF 52%, mid-septal mild hypokinesis, patent DES without in-stent thrombus or dissection.',
    conditionAtDischarge: 'Stable / Improved',
    dischargeMedications: [
      {
        medicineName: 'Ticagrelor (Brilinta)',
        dosage: '90 mg',
        frequency: 'Twice daily with meals',
        duration: '12 months continuous',
        specialInstructions: 'Critical: do not skip any doses. Premature stoppage increases stent thrombosis risk.'
      },
      {
        medicineName: 'Aspirin (Enteric Coated)',
        dosage: '81 mg',
        frequency: 'Once daily in the morning',
        duration: 'Lifelong',
        specialInstructions: 'Take with food and water.'
      },
      {
        medicineName: 'Atorvastatin',
        dosage: '80 mg',
        frequency: 'Once daily at bedtime',
        duration: 'Ongoing',
        specialInstructions: 'Report any sudden unexplained muscle pain or brown urine.'
      },
      {
        medicineName: 'Metoprolol Succinate ER',
        dosage: '50 mg',
        frequency: 'Once daily in the morning',
        duration: 'Ongoing',
        specialInstructions: 'Hold if pulse < 55 bpm or systolic BP < 100.'
      }
    ],
    dietInstructions: 'AHA Heart-Healthy Diet: sodium restricted to < 2,000 mg/day, low saturated fat (<7% calories), high fiber.',
    activityRestrictions: 'No lifting > 10 lbs for 7 days post-radial access. Walking encouraged up to 30 mins daily. Avoid strenuous cardiovascular strain until cleared at follow-up.',
    woundCareInstructions: 'Keep radial wrist access site clean and dry. Bandage may be removed tomorrow. Do not submerge wrist in bath or pool for 5 days.',
    warningSignsRedFlags: [
      'Recurrent severe chest tightness or crushing retrosternal pressure',
      'Shortness of breath at rest or when lying flat',
      'Sudden swelling, bleeding, or expanding lump at right wrist puncture site',
      'Dizziness, syncope (fainting), or irregular fast racing heart beats',
      'Black tarry stools or unusual bleeding gums'
    ],
    followUpAppointments: [
      {
        department: 'Cardiology',
        doctorName: 'Dr. Marcus Vance, MD, FACC',
        scheduledDate: '2026-11-04 10:00 AM',
        instructions: 'Comprehensive 4-week post-PCI clinical review and lipid panel check.'
      },
      {
        department: 'Outpatient Department',
        doctorName: 'Cardiac Rehabilitation Center',
        scheduledDate: '2026-10-14 09:00 AM',
        instructions: 'Phase 2 supervised exercise conditioning intake.'
      }
    ],
    attendingDoctorId: 'USR-DOC-03',
    attendingDoctorName: 'Dr. Marcus Vance, MD, FACC',
    signedAt: '2026-10-04T16:00:00Z',
    digitalSignature: 'SIG-VERIFIED:DrMarcusVance:CARDIOLOGY-DISCHARGE:HASH-99482',
    status: 'Final Signed',
    hospitalId: 'HOSP-01'
  }
];

/**
 * CLINICAL REFERRALS
 */
export const SEED_CLINICAL_REFERRALS: ClinicalReferral[] = [
  {
    id: 'REF-2026-081',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    mrn: 'MRN-884920',
    encounterId: 'ENC-2026-1049',
    referringDoctorId: 'USR-DOC-03',
    referringDoctorName: 'Dr. Marcus Vance, MD',
    referringDepartment: 'Cardiology',
    targetDepartment: 'Outpatient Department',
    targetDoctorName: 'Cardiac Rehabilitation Team',
    urgency: 'Routine',
    referralReason: 'Phase 2 Cardiac Rehabilitation post-DES stenting to Mid-LAD.',
    clinicalSummary: '58yo male status post successful PCI for CAD/NSTEMI. LVEF 52%. Prepared for monitored exercise titration and lifestyle education.',
    requestedInvestigations: ['Baseline 6-minute walk test', 'Supervised aerobic exercise telemetry'],
    status: 'Accepted',
    scheduledDate: '2026-10-14',
    consultantNotes: 'Referral accepted. Intake evaluation scheduled for 10/14 at 09:00 AM in Outpatient Gym Suite B.',
    createdAt: '2026-10-04T10:00:00Z',
    updatedAt: '2026-10-04T11:30:00Z',
    hospitalId: 'HOSP-01'
  },
  {
    id: 'REF-2026-082',
    patientId: 'PT-10045',
    patientName: 'Elena Rostova',
    mrn: 'MRN-449182',
    encounterId: 'ENC-2026-1050',
    referringDoctorId: 'USR-DOC-03',
    referringDoctorName: 'Dr. Marcus Vance, MD',
    referringDepartment: 'Cardiology',
    targetDepartment: 'Internal Medicine',
    targetDoctorName: 'Dr. Thomas Hayes, MD (Electrophysiology Clinic)',
    urgency: 'Urgent (<24h)',
    referralReason: 'Evaluation of symptomatic paroxysmal palpitations and recurrent lightheadedness.',
    clinicalSummary: '42yo female with episodic palpitations lasting 15-20 mins. EKG showed frequent PACs. Outpatient 14-day telemetry ordered.',
    requestedInvestigations: ['Holter review', 'Electrophysiology consult'],
    status: 'Submitted',
    createdAt: '2026-10-04T10:30:00Z',
    updatedAt: '2026-10-04T10:30:00Z',
    hospitalId: 'HOSP-01'
  }
];
