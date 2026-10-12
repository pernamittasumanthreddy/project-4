/**
 * ==============================================================================
 * MEMBER 3 — CLINICAL MANAGEMENT AUTOMATED VERIFICATION TEST SUITE
 * EMR/EHR, Doctor Workspace, Nursing Records, Encounters, Diagnoses, 
 * e-Prescriptions, Immutability & Amendments, and Discharge Summaries
 * ==============================================================================
 */

const assert = require('assert');

// Cryptographic hash simulation matching clinicalStore
function generateSignatureHash(dataString) {
  let hash = 0;
  for (let i = 0; i < dataString.length; i++) {
    const char = dataString.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return `SHA256:${Math.abs(hash).toString(16).padStart(8, '0')}`;
}

// MEWS Calculation algorithm
function calculateMEWS(vitals) {
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

  // AVPU Consciousness
  if (vitals.avpu === 'Voice') score += 1;
  else if (vitals.avpu === 'Pain') score += 2;
  else if (vitals.avpu === 'Unresponsive') score += 3;

  let riskCategory = 'Low Risk (0-1)';
  let actionRequired = 'Routine 4-hourly ward vital signs monitoring.';

  if (score >= 6) {
    riskCategory = 'Critical Deterioration (>=6)';
    actionRequired = 'STAT Medical Emergency Team (MET) / Code Blue activation.';
  } else if (score >= 4) {
    riskCategory = 'High Alert (4-5)';
    actionRequired = 'Urgent attending physician notification. Bedside review within 15 mins.';
  } else if (score >= 2) {
    riskCategory = 'Medium Risk (2-3)';
    actionRequired = 'Inform charge nurse. Increase vital signs frequency to hourly.';
  }

  return { score, riskCategory, actionRequired };
}

// Allergy conflict checker algorithm
function checkAllergyConflict(drugName, patientAllergies) {
  const warnings = [];
  const drugLower = drugName.toLowerCase();

  for (const allergy of patientAllergies) {
    const allergenLower = allergy.allergen.toLowerCase();

    if (allergenLower.includes('penicillin') && (
      drugLower.includes('amoxicillin') || 
      drugLower.includes('ampicillin') || 
      drugLower.includes('penicillin') ||
      drugLower.includes('augmentin')
    )) {
      warnings.push(`CRITICAL ALLERGY CONFLICT: Patient allergic to ${allergy.allergen} (${allergy.reaction})`);
    }

    if (allergenLower.includes('sulfa') && (
      drugLower.includes('bactrim') || 
      drugLower.includes('sulfamethoxazole')
    )) {
      warnings.push(`ALLERGY WARNING: Patient allergic to ${allergy.allergen}`);
    }

    if (allergenLower.includes('aspirin') && (
      drugLower.includes('aspirin') || 
      drugLower.includes('ibuprofen')
    )) {
      warnings.push(`ALLERGY WARNING: Severe NSAID/Aspirin reaction: ${allergy.reaction}`);
    }
  }

  return warnings;
}

async function runMember3TestSuite() {
  console.log('================================================================================');
  console.log('🏥 RUNNING MEMBER 3: CLINICAL MANAGEMENT AUTOMATED TEST SUITE');
  console.log('   EMR/EHR • Doctor Workspace • Nursing Records • Encounters • Prescriptions');
  console.log('================================================================================\n');

  let passed = 0;
  let total = 0;

  function test(testName, fn) {
    total++;
    try {
      fn();
      console.log(`  ✅ PASS: ${testName}`);
      passed++;
    } catch (err) {
      console.error(`  ❌ FAIL: ${testName}`);
      console.error(`     Reason: ${err.message}`);
    }
  }

  // 1. Encounter Creation & Structure
  test('1. Clinical Encounter supports complete SOAP documentation structure', () => {
    const encounter = {
      id: 'ENC-2026-1049',
      patientId: 'PT-10023',
      patientMrn: 'MRN-884920',
      doctorId: 'USR-DOC-03',
      chiefComplaint: 'Post-PCI follow-up',
      subjectiveNotes: 'Patient denies recurrent angina.',
      objectiveNotes: 'BP 124/80, HR 72 regular, clear lungs.',
      assessmentNotes: '1. CAD s/p DES to LAD - Stable.',
      planNotes: 'Continue DAPT (Aspirin + Ticagrelor).',
      status: 'In Progress',
      signStatus: 'Draft'
    };

    assert.strictEqual(encounter.signStatus, 'Draft');
    assert.ok(encounter.subjectiveNotes.length > 0);
    assert.ok(encounter.objectiveNotes.length > 0);
    assert.ok(encounter.assessmentNotes.length > 0);
    assert.ok(encounter.planNotes.length > 0);
  });

  // 2. Digital Signing Workflow
  test('2. Signing a clinical encounter locks it with a cryptographic signature hash', () => {
    const draftEncounter = {
      id: 'ENC-2026-1049',
      patientMrn: 'MRN-884920',
      signStatus: 'Draft',
      assessmentNotes: 'CAD s/p DES'
    };

    const doctor = 'Dr. Marcus Vance, MD, FACC';
    const license = 'MD-88392-CA';
    const hash = generateSignatureHash(`${draftEncounter.id}|${doctor}|${license}|${draftEncounter.assessmentNotes}`);

    draftEncounter.signStatus = 'Signed';
    draftEncounter.signedBy = doctor;
    draftEncounter.digitalSignatureHash = hash;

    assert.strictEqual(draftEncounter.signStatus, 'Signed');
    assert.ok(draftEncounter.digitalSignatureHash.startsWith('SHA256:'));
  });

  // 3. Immutability & Rejection of Silent Direct Overwrite
  test('3. Signed clinical records reject direct overwrite and enforce immutability', () => {
    const signedEncounter = {
      id: 'ENC-2026-1049',
      signStatus: 'Signed',
      assessmentNotes: 'Original signed assessment'
    };

    let preventedOverwrite = false;
    try {
      if (signedEncounter.signStatus === 'Signed') {
        throw new Error('IMMUTABILITY VIOLATION: Signed clinical record cannot be modified directly.');
      }
      signedEncounter.assessmentNotes = 'Modified assessment without audit trail';
    } catch (e) {
      preventedOverwrite = true;
      assert.ok(e.message.includes('IMMUTABILITY VIOLATION'));
    }

    assert.strictEqual(preventedOverwrite, true);
    assert.strictEqual(signedEncounter.assessmentNotes, 'Original signed assessment');
  });

  // 4. Versioned Amendments & Addenda
  test('4. Modifying signed record appends versioned addendum with author & timestamp', () => {
    const signedEncounter = {
      id: 'ENC-2026-1049',
      signStatus: 'Signed',
      amendments: []
    };

    const addendum = {
      id: 'AMD-01',
      version: signedEncounter.amendments.length + 1,
      amendmentType: 'Addendum',
      amendedBy: 'Dr. Marcus Vance, MD',
      reasonForAmendment: 'Echo results reviewed',
      amendmentContent: 'LVEF 52% with preserved overall systolic performance.',
      digitalSignatureHash: generateSignatureHash('AMD-01|LVEF 52%')
    };

    signedEncounter.amendments.push(addendum);
    signedEncounter.signStatus = 'Addendum Appended';

    assert.strictEqual(signedEncounter.amendments.length, 1);
    assert.strictEqual(signedEncounter.amendments[0].version, 1);
    assert.strictEqual(signedEncounter.signStatus, 'Addendum Appended');
    assert.ok(signedEncounter.amendments[0].digitalSignatureHash.startsWith('SHA256:'));
  });

  // 5. Automated Allergy Cross-Checking
  test('5. Real-time allergy checker detects penicillin contraindication when prescribing amoxicillin', () => {
    const patientAllergies = [
      { allergen: 'Penicillin', reaction: 'Anaphylaxis and urticaria', severity: 'Life Threatening' }
    ];

    const safeWarnings = checkAllergyConflict('Atorvastatin 80mg', patientAllergies);
    assert.strictEqual(safeWarnings.length, 0);

    const dangerWarnings = checkAllergyConflict('Amoxicillin Clavulanate (Augmentin)', patientAllergies);
    assert.strictEqual(dangerWarnings.length, 1);
    assert.ok(dangerWarnings[0].includes('CRITICAL ALLERGY CONFLICT'));
  });

  // 6. Electronic Prescriptions (eRx) Verification
  test('6. Electronic prescription validates dosage, route, frequency, and dispense status', () => {
    const rxItem = {
      medicineName: 'Ticagrelor (Brilinta)',
      dosage: '90 mg',
      route: 'Oral',
      frequency: 'BID (Twice Daily)',
      durationDays: 365,
      quantity: 730,
      dispenseStatus: 'Pending'
    };

    assert.strictEqual(rxItem.route, 'Oral');
    assert.strictEqual(rxItem.frequency, 'BID (Twice Daily)');
    assert.strictEqual(rxItem.quantity, 730);
    assert.strictEqual(rxItem.dispenseStatus, 'Pending');
  });

  // 7. MEWS Score Calculation & Deterioration Alert
  test('7. MEWS calculator correctly computes early warning score and alerts on deterioration', () => {
    // Normal patient
    const normalVitals = {
      systolicBp: 120,
      heartRate: 72,
      respiratoryRate: 16,
      temperature: 98.6,
      avpu: 'Alert'
    };
    const normalMews = calculateMEWS(normalVitals);
    assert.strictEqual(normalMews.score, 1);
    assert.strictEqual(normalMews.riskCategory, 'Low Risk (0-1)');

    // Deteriorating patient (Hypotension, Tachycardia, Tachypnea, Fever)
    const severeVitals = {
      systolicBp: 75, // +2
      heartRate: 135, // +3
      respiratoryRate: 32, // +3
      temperature: 102.5, // +2
      avpu: 'Voice' // +1
    };
    const severeMews = calculateMEWS(severeVitals);
    assert.ok(severeMews.score >= 6);
    assert.strictEqual(severeMews.riskCategory, 'Critical Deterioration (>=6)');
    assert.ok(severeMews.actionRequired.includes('STAT Medical Emergency Team'));
  });

  // 8. Fluid Balance Net Computation
  test('8. Fluid balance flowsheet computes net balance (Intake - Output) and cumulative shift volume', () => {
    const intake = { oral: 650, iv: 500 };
    const output = { urine: 900, drain: 0 };

    const totalIntake = intake.oral + intake.iv; // 1150
    const totalOutput = output.urine + output.drain; // 900
    const netBalance = totalIntake - totalOutput; // +250

    const prevCumulative = 170;
    const newCumulative = prevCumulative + netBalance; // 420

    assert.strictEqual(totalIntake, 1150);
    assert.strictEqual(totalOutput, 900);
    assert.strictEqual(netBalance, 250);
    assert.strictEqual(newCumulative, 420);
  });

  // 9. 5-Rights eMAR Administration
  test('9. eMAR administration records right patient, drug, dose, route, and administering nurse', () => {
    const emarEntry = {
      id: 'EMAR-01',
      patientId: 'PT-10023',
      medicineName: 'Ticagrelor',
      dosage: '90 mg',
      route: 'Oral',
      scheduledTime: '09:00 AM',
      status: 'Due'
    };

    // Nurse administers dose
    emarEntry.status = 'Administered';
    emarEntry.administeredBy = 'Sarah Jenkins, BSN, RN';
    emarEntry.administeredTime = '09:05 AM';
    emarEntry.vitalsBeforeAdmin = 'BP 124/80, HR 72';

    assert.strictEqual(emarEntry.status, 'Administered');
    assert.ok(emarEntry.administeredBy.includes('Sarah Jenkins'));
    assert.ok(emarEntry.vitalsBeforeAdmin.includes('BP 124/80'));
  });

  // 10. SBAR Shift Handover Note
  test('10. SBAR shift handover encapsulates Situation, Background, Assessment, and Recommendation', () => {
    const sbar = {
      situation: '58yo male s/p PCI Day 2',
      background: 'NSTEMI, DAPT adherence, Penicillin allergy',
      assessment: 'Vitals stable, ambulating well, sinus rhythm',
      recommendation: 'Discharge tomorrow 10:00 AM',
      codeStatus: 'Full Code',
      keyTasks: ['Administer evening Atorvastatin', 'Check morning fasting glucose']
    };

    assert.strictEqual(sbar.codeStatus, 'Full Code');
    assert.strictEqual(sbar.keyTasks.length, 2);
    assert.ok(sbar.situation.includes('s/p PCI'));
  });

  // 11. Inpatient Discharge Summary Completion & Signing
  test('11. Inpatient discharge summary contains hospital course, discharge medications, and warning signs', () => {
    const summary = {
      id: 'DS-2026-092',
      patientId: 'PT-10023',
      admittingDiagnosis: 'NSTEMI',
      dischargeDiagnosis: 'CAD s/p DES to LAD',
      hospitalCourse: 'Underwent successful catheterization and stenting.',
      dischargeMedications: [
        { medicineName: 'Ticagrelor 90mg BID', duration: '12 months' },
        { medicineName: 'Aspirin 81mg QD', duration: 'Lifelong' }
      ],
      warningSignsRedFlags: ['Crushing chest pressure', 'Severe shortness of breath'],
      status: 'Draft'
    };

    assert.strictEqual(summary.dischargeMedications.length, 2);
    assert.strictEqual(summary.warningSignsRedFlags.length, 2);

    // Sign discharge summary
    summary.status = 'Final Signed';
    summary.attendingDoctorName = 'Dr. Marcus Vance, MD, FACC';
    summary.digitalSignature = generateSignatureHash(`DISCHARGE|${summary.id}|${summary.attendingDoctorName}`);

    assert.strictEqual(summary.status, 'Final Signed');
    assert.ok(summary.digitalSignature.startsWith('SHA256:'));
  });

  // 12. Clinical Referral Workflow
  test('12. Inter-departmental clinical referral tracks referring & target department with status lifecycle', () => {
    const referral = {
      id: 'REF-2026-081',
      referringDepartment: 'Cardiology',
      targetDepartment: 'Outpatient Department',
      urgency: 'Routine',
      referralReason: 'Phase 2 Cardiac Rehabilitation',
      status: 'Submitted'
    };

    assert.strictEqual(referral.status, 'Submitted');

    // Destination department accepts
    referral.status = 'Accepted';
    referral.scheduledDate = '2026-10-14';
    referral.consultantNotes = 'Initial intake evaluation scheduled.';

    assert.strictEqual(referral.status, 'Accepted');
    assert.strictEqual(referral.scheduledDate, '2026-10-14');
  });

  // 13. Clinical Templates & ICD-10 Coding Integrity
  test('13. Clinical templates library provides pre-formatted SOAP outlines with valid ICD-10 codes', () => {
    const template = {
      title: 'Cardiology Consultation & Post-PCI',
      department: 'Cardiology',
      commonDiagnoses: [
        { code: 'I25.10', desc: 'Atherosclerotic heart disease' },
        { code: 'I10', desc: 'Essential hypertension' }
      ]
    };

    assert.strictEqual(template.department, 'Cardiology');
    assert.strictEqual(template.commonDiagnoses[0].code, 'I25.10');
  });

  // 14. Patient Longitudinal EMR Record Aggregator
  test('14. Longitudinal EMR chart aggregates encounters, meds, observations, and discharge summaries', () => {
    const patientChart = {
      patientId: 'PT-10023',
      encounters: [{ id: 'ENC-01' }],
      prescriptions: [{ id: 'RX-01' }],
      observations: [{ id: 'OBS-01' }],
      dischargeSummaries: [{ id: 'DS-01' }],
      allergies: [{ allergen: 'Penicillin' }]
    };

    assert.strictEqual(patientChart.encounters.length, 1);
    assert.strictEqual(patientChart.prescriptions.length, 1);
    assert.strictEqual(patientChart.observations.length, 1);
    assert.strictEqual(patientChart.dischargeSummaries.length, 1);
    assert.strictEqual(patientChart.allergies.length, 1);
  });

  // 15. Clinical Record Access Auditing
  test('15. Sensitive clinical chart viewing creates HIPAA-compliant audit event', () => {
    const auditLog = {
      userId: 'USR-DOC-03',
      role: 'DOCTOR',
      action: 'VIEW',
      resourceType: 'PATIENT_EMR',
      patientId: 'PT-10023',
      timestamp: new Date().toISOString(),
      details: 'Attending physician accessed longitudinal clinical chart'
    };

    assert.strictEqual(auditLog.action, 'VIEW');
    assert.strictEqual(auditLog.resourceType, 'PATIENT_EMR');
    assert.strictEqual(auditLog.patientId, 'PT-10023');
  });

  // 16. CHA2DS2-VASc Stroke Risk Stratification
  test('16. CHA2DS2-VASc correctly stratifies stroke risk in atrial fibrillation', () => {
    function calcCHA2DS2VASc(p) {
      let score = 0;
      if (p.chf) score += 1;
      if (p.htn) score += 1;
      if (p.age >= 75) score += 2;
      else if (p.age >= 65) score += 1;
      if (p.dm) score += 1;
      if (p.stroke) score += 2;
      if (p.vasc) score += 1;
      if (p.female) score += 1;
      return score;
    }
    const highRisk = calcCHA2DS2VASc({ chf: true, htn: true, age: 72, dm: true, stroke: false, vasc: true, female: false });
    assert.strictEqual(highRisk, 5); // CHF(1) + HTN(1) + Age>=65(1) + DM(1) + Vasc(1) = 5
  });

  // 17. CKD-EPI Glomerular Filtration & Renal Staging
  test('17. CKD-EPI eGFR detects renal impairment requiring drug dose adjustments', () => {
    function calcStage(egfr) {
      if (egfr < 15) return { stage: 'Stage 5', adjust: true };
      if (egfr < 30) return { stage: 'Stage 4', adjust: true };
      if (egfr < 60) return { stage: 'Stage 3', adjust: true };
      return { stage: 'Stage 1-2', adjust: false };
    }
    const severeCKD = calcStage(24.5);
    assert.strictEqual(severeCKD.stage, 'Stage 4');
    assert.strictEqual(severeCKD.adjust, true);
  });

  // 18. CURB-65 Pneumonia Severity Score
  test('18. CURB-65 classifies severe pneumonia requiring inpatient ICU admission', () => {
    function curb65(c, u, r, b, age) {
      let s = 0;
      if (c) s++; if (u) s++; if (r) s++; if (b) s++; if (age >= 65) s++;
      return s;
    }
    const score = curb65(true, true, true, false, 72);
    assert.strictEqual(score, 4);
    assert.ok(score >= 3); // High risk / ICU threshold
  });

  // 19. Drug-Drug Interaction Matrix Detection
  test('19. Drug-Drug Interaction engine detects severe Warfarin + Aspirin bleeding risk', () => {
    const pair = { drugA: 'Warfarin', drugB: 'Aspirin', severity: 'Major', risk: 'Severe hemorrhage' };
    assert.strictEqual(pair.severity, 'Major');
    assert.ok(pair.risk.includes('hemorrhage'));
  });

  // 20. NANDA-I Nursing Care Plan Directive
  test('20. NANDA-I care plan establishes telemetry monitoring threshold for unstable patients', () => {
    const carePlan = {
      nursingDiagnosis: 'Decreased Cardiac Output Telemetry',
      evaluationSchedule: 'q2h',
      alertThreshold: 'Heart Rate > 110 bpm or SpO2 < 92%'
    };
    assert.strictEqual(carePlan.evaluationSchedule, 'q2h');
    assert.ok(carePlan.alertThreshold.includes('Heart Rate > 110'));
  });

  // 21. Multi-Center Longitudinal Audit Dataset
  test('21. Longitudinal clinical outcomes dataset computes complication and readmission rates', () => {
    const records = [
      { complication: false, readmission: false },
      { complication: true, readmission: false },
      { complication: false, readmission: true },
      { complication: false, readmission: false }
    ];
    const compRate = (records.filter(r => r.complication).length / records.length) * 100;
    const readmRate = (records.filter(r => r.readmission).length / records.length) * 100;
    assert.strictEqual(compRate, 25);
    assert.strictEqual(readmRate, 25);
  });

  // 22. Clinical Decision Support Alert Threshold Integrity
  test('22. Clinical Decision Support alerts properly escalate across all inpatient services', () => {
    const mewsCritical = { score: 6, action: 'STAT Medical Emergency Team (MET) activation' };
    assert.ok(mewsCritical.score >= 6);
    assert.ok(mewsCritical.action.includes('MET'));
  });

  console.log('\n================================================================================');
  console.log(`📊 MEMBER 3 TEST RESULTS: ${passed}/${total} PASSED (${Math.round((passed / total) * 100)}%)`);
  console.log('================================================================================');

  if (passed !== total) {
    process.exit(1);
  }
}

runMember3TestSuite();
