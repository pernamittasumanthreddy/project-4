import { HospitalDocument, DocumentChunk } from '../types/rag';

export const HOSPITAL_DOCUMENTS: HospitalDocument[] = [
  {
    id: 'DOC-ADMIT-01',
    title: 'Hospital Admission Policy and Inpatient Intake Protocol',
    category: 'C. Admission Procedures',
    department: 'Hospital Administration',
    version: 'v2.4',
    effectiveDate: '2026-01-15',
    lastUpdated: '2026-08-20',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'BILLING_STAFF', 'INSURANCE_STAFF', 'DEPARTMENT_MANAGER', 'EMERGENCY_STAFF'],
    fileType: 'PDF',
    fileSize: '1.8 MB',
    sourceUri: '/documents/hospital-admission-policy-v2.pdf',
    isArchived: false,
    content: `HOSPITAL ADMISSION POLICY AND INPATIENT INTAKE PROTOCOL (SOP-ADM-2026)

Section 1: General Admission Criteria and Documentation
All patients requiring inpatient medical care must undergo formal registration through the Central Admissions Desk or Emergency Department Triage. Mandatory documentation includes: government-issued photo identification, primary and secondary health insurance cards, signed consent for treatment (Form MED-CON-01), and an attending physician admission order containing admitting diagnosis and level of care (General Floor, Telemetry, Step-Down, or Intensive Care Unit).

Section 2: Emergency vs. Elective Admission Pathways
2.1 Elective Admissions: Must be pre-scheduled at least 48 hours prior by the attending specialist. Financial pre-authorization from the patient's insurance payer must be cleared by the Insurance Coordination Desk prior to bed allocation.
2.2 Emergency Admissions: Immediate stabilization takes precedence over administrative documentation. Triage nurses initiate bedside registration while emergency physicians complete provisional admission orders within 15 minutes of bed request.

Section 3: Bed Allocation and Departmental Transfers
Bed assignment is coordinated by the Central Bed Management Bureau using the Enterprise Bed Tracking System. ICU beds are prioritized for patients requiring continuous mechanical ventilation, invasive arterial monitoring, or vasoactive infusions. Transfers between units require a formalized SBAR (Situation, Background, Assessment, Recommendation) clinical handover.`,
    sections: [
      {
        heading: 'General Admission Criteria and Documentation',
        page: 1,
        text: 'All patients requiring inpatient care must undergo formal registration with photo ID, insurance card, signed treatment consent (Form MED-CON-01), and admitting physician order.'
      },
      {
        heading: 'Emergency vs. Elective Admission Pathways',
        page: 2,
        text: 'Elective admissions require 48-hour prior scheduling and insurance pre-authorization. Emergency admissions mandate immediate stabilization; bedside registration is initiated without delaying care.'
      },
      {
        heading: 'Bed Allocation and Departmental Transfers',
        page: 3,
        text: 'Coordinated by Bed Management Bureau. ICU beds prioritized for mechanical ventilation and vasoactive infusions. SBAR handover required for all bed transfers.'
      }
    ]
  },

  {
    id: 'DOC-ED-TRAUMA-04',
    title: 'Emergency Department SOP & Triage Escalation Guidelines',
    category: 'E. Emergency Procedures',
    department: 'Emergency',
    version: 'v4.1',
    effectiveDate: '2026-02-01',
    lastUpdated: '2026-09-10',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'EMERGENCY_STAFF', 'DEPARTMENT_MANAGER'],
    fileType: 'PDF',
    fileSize: '2.4 MB',
    sourceUri: '/documents/emergency-department-sop-v4.pdf',
    isArchived: false,
    content: `EMERGENCY DEPARTMENT SOP & TRIAGE ESCALATION GUIDELINES (ED-TRAUMA-04)

Section 1: Emergency Severity Index (ESI) Triage System
All presenting emergency patients must be assessed within 5 minutes of arrival by a certified Emergency Triage Nurse using the 5-level ESI algorithm:
- ESI 1 (Resuscitation): Immediate life-saving intervention needed (cardiac arrest, severe respiratory failure, massive hemorrhage, unresponsive GCS < 8). Response time: IMMEDIATE (0 minutes).
- ESI 2 (Emergent): High-risk situation, confusional state/lethargy, severe pain/distress, or vitals in danger zone. Response time: Within 10-15 minutes.
- ESI 3 (Urgent): Patient requires 2 or more diagnostic/therapeutic resources (e.g. IV fluids + blood work + CT scan) with stable vitals. Response time: Within 30 minutes.
- ESI 4 (Less Urgent): Patient requires only 1 resource (e.g. simple x-ray or suture).
- ESI 5 (Non-urgent): Patient requires zero resources (e.g. prescription refill, mild rash).

Section 2: Code Blue Resuscitation and Rapid Response Dispatch
Upon activation of Code Blue via telephone extension 4444 or overhead alert:
1. Primary Code Team dispatches: Attending Emergency Physician, Senior Resident, ICU Charge Nurse, Respiratory Therapist, and Pharmacy Specialist.
2. Crash Cart with biphasic defibrillator must be at patient bedside in under 90 seconds.
3. High-quality CPR is initiated at 100-120 compressions/min; early rhythm analysis every 2 minutes.

Section 3: Acute STEMI and Stroke Thrombolysis Pathways
3.1 Acute STEMI: Door-to-ECG goal is ≤ 10 minutes. If STEMI is confirmed, cardiac catheterization team is activated immediately. Door-to-Balloon target time is < 90 minutes.
3.2 Acute Ischemic Stroke: Door-to-CT completion is ≤ 25 minutes. IV Alteplase/TNK window evaluated within 4.5 hours of symptom onset after intracranial hemorrhage is ruled out.

Section 4: Massive Transfusion Protocol (MTP)
In hemorrhagic shock, MTP is activated with blood bank (ext. 2210). Dispenses 1:1:1 ratio (4 units Uncrossed O-Negative PRBCs, 4 units Fresh Frozen Plasma, 1 apheresis platelet pack).`,
    sections: [
      {
        heading: 'Emergency Severity Index (ESI) Triage System',
        page: 1,
        text: '5-level algorithm: ESI 1 (Immediate 0m), ESI 2 (10-15m), ESI 3 (30m), ESI 4 (Less urgent, 1 resource), ESI 5 (Non-urgent, 0 resources).'
      },
      {
        heading: 'Code Blue Resuscitation and Rapid Response Dispatch',
        page: 2,
        text: 'Call ext 4444. Code team (ED Physician, ICU Nurse, RT, Pharmacist) arrives. Crash cart bedside within 90 seconds. CPR 100-120 bpm, rhythm check q2m.'
      },
      {
        heading: 'Acute STEMI and Stroke Thrombolysis Pathways',
        page: 3,
        text: 'Door-to-ECG < 10 mins. STEMI Door-to-Balloon < 90 mins. Acute stroke Door-to-CT < 25 mins; thrombolysis evaluated within 4.5h window.'
      },
      {
        heading: 'Massive Transfusion Protocol (MTP)',
        page: 4,
        text: 'Call blood bank ext 2210. 1:1:1 balanced ratio: 4 units O-Neg PRBCs, 4 units FFP, 1 unit apheresis platelets.'
      }
    ]
  },

  {
    id: 'DOC-DISC-02',
    title: 'Patient Discharge Policy and Continuity of Care Procedure',
    category: 'D. Discharge Procedures',
    department: 'Hospital Administration',
    version: 'v3.0',
    effectiveDate: '2026-03-01',
    lastUpdated: '2026-09-15',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'PATIENT', 'PHARMACIST', 'BILLING_STAFF'],
    fileType: 'PDF',
    fileSize: '1.2 MB',
    sourceUri: '/documents/patient-discharge-policy-v3.pdf',
    isArchived: false,
    content: `PATIENT DISCHARGE POLICY AND CONTINUITY OF CARE PROCEDURE (SOP-DIS-2026)

Section 1: Physician Discharge Authorization
Patients may only be discharged upon completion of a signed Discharge Summary by the attending physician. The summary must articulate: final diagnosis, hospital course summary, discharge medications with reconciliation, follow-up appointment timeline, wound care directions, and emergency warning signs.

Section 2: Medication Reconciliation and Pharmacy Counseling
Prior to physical discharge, the clinical pharmacist must reconcile all discharge medications against the patient's pre-admission medications to prevent therapeutic duplication or omission. Patients or designated caregivers must receive in-person or virtual counseling covering drug indication, dosing schedule, adverse effects, and dietary precautions.

Section 3: Financial Settlement and Exit Clearance
The Billing and Finance Department verifies that all inpatient service charges, room tariffs, and pharmacy dispense records are processed. The patient or payer receives an itemized billing statement. Once cleared, a Gate Pass and Discharge Packet is issued. Standard discharge window is 10:00 AM to 12:00 PM.`,
    sections: [
      {
        heading: 'Physician Discharge Authorization',
        page: 1,
        text: 'Requires signed physician discharge summary with final diagnosis, hospital course, reconciled medications, follow-up appointment, and warning signs.'
      },
      {
        heading: 'Medication Reconciliation and Pharmacy Counseling',
        page: 2,
        text: 'Pharmacist reconciles discharge meds against pre-admission meds. Mandatory counseling with patient/caregiver on dosages, side effects, and precautions.'
      },
      {
        heading: 'Financial Settlement and Exit Clearance',
        page: 3,
        text: 'Billing Department reconciles charges, issues itemized invoice, and releases Gate Pass. Standard discharge window: 10:00 AM - 12:00 PM.'
      }
    ]
  },

  {
    id: 'DOC-PHARM-01',
    title: 'Hospital Pharmacy Formulary & Dispensing SOP',
    category: 'H. Pharmacy Policies',
    department: 'Pharmacy',
    version: 'v5.0',
    effectiveDate: '2026-01-01',
    lastUpdated: '2026-08-30',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'PHARMACIST', 'DEPARTMENT_MANAGER'],
    fileType: 'PDF',
    fileSize: '3.1 MB',
    sourceUri: '/documents/pharmacy-dispensing-sop-v5.pdf',
    isArchived: false,
    content: `HOSPITAL PHARMACY FORMULARY & DISPENSING SOP (PHARM-DISP-01)

Section 1: Electronic Prescription Verification Protocol
Licensed pharmacists must verify every physician medication order in the CPOE system prior to automated or manual dispensing. Verification criteria include: patient age, body weight, calculated creatinine clearance (eGFR), known drug allergies, therapeutic duplication, drug-drug interactions, and approved indications within the Hospital Formulary.

Section 2: High-Alert and Controlled Substance Dispensing
2.1 High-Alert Medications (Insulin, Heparin, IV Potassium Chloride, Chemotherapy, Neuromuscular Blockers): Require independent double-check by two pharmacists before release. Potassium chloride concentrated ampoules are strictly banned on general floor stock.
2.2 Schedule II Narcotics (Morphine, Fentanyl, Hydromorphone, Oxycodone): Stored in biometric double-locked safes. Every dose dispensed requires two-person digital signature, patient identification, and recorded reason for use. Perpetual inventory count performed at every 8-hour shift change.

Section 3: Generic Substitution Policy
In accordance with Pharmacy and Therapeutics (P&T) Committee policy, pharmacists are authorized to dispense bioequivalent generic alternatives unless the ordering physician explicitly marks "Dispense as Written" (DAW).`,
    sections: [
      {
        heading: 'Electronic Prescription Verification Protocol',
        page: 1,
        text: 'Pharmacists verify every CPOE order checking eGFR, body weight, allergies, drug interactions, and hospital formulary compliance.'
      },
      {
        heading: 'High-Alert and Controlled Substance Dispensing',
        page: 2,
        text: 'High-alert meds require dual independent checks. Concentrated KCl banned from floor stock. Schedule II narcotics in biometric dual-lock safes with dual signatures.'
      },
      {
        heading: 'Generic Substitution Policy',
        page: 3,
        text: 'Automated bioequivalent generic dispensing unless explicitly specified as Dispense As Written (DAW) by the prescriber.'
      }
    ]
  },

  {
    id: 'DOC-MED-STORE-88',
    title: 'Medication Cold-Chain and Controlled Storage Guidelines',
    category: 'G. Medicine Information',
    department: 'Pharmacy',
    version: 'v3.2',
    effectiveDate: '2026-02-15',
    lastUpdated: '2026-07-14',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'PHARMACIST', 'NURSE', 'DOCTOR', 'DEPARTMENT_MANAGER'],
    fileType: 'PDF',
    fileSize: '1.5 MB',
    sourceUri: '/documents/medication-storage-guidelines-v3.pdf',
    isArchived: false,
    content: `MEDICATION COLD-CHAIN AND CONTROLLED STORAGE GUIDELINES (MED-STORE-88)

Section 1: Cold Chain Temperature Thresholds and Monitoring
1.1 Refrigerated Storage (2°C to 8°C / 36°F to 46°F): Required for Insulins, Monoclonal Antibodies, Vaccines, Oxytocin, Epoetin Alfa, and reconstituted antibiotics. Monitored continuously via calibrated NIST digital telemetry with automatic SMS alerts if temperature breaches ±1.5°C for > 15 minutes.
1.2 Frozen Storage (-20°C to -10°C): Required for certain viral vaccines and specialized coagulation factors.
1.3 Controlled Room Temperature (20°C to 25°C / 68°F to 77°F): Excursions permitted between 15°C and 30°C for short transit only. Relative humidity must stay below 60%.

Section 2: Handling Cold Chain Breaches
If a refrigerator fails or breaches 8°C:
1. Immediately quarantine affected products in insulated coolers with calibrated cold packs (do not freeze!).
2. Mark inventory status as "PENDING PHARMACEUTICAL QUALITY EVALUATION - DO NOT DISPENSE".
3. Contact Biomedical Engineering (ext. 3311) and log time duration in the Quality Incident Management Portal.`,
    sections: [
      {
        heading: 'Cold Chain Temperature Thresholds and Monitoring',
        page: 1,
        text: 'Refrigerated: 2°C to 8°C. Monitored 24/7 via telemetry. Controlled room temperature: 20°C to 25°C, humidity < 60%.'
      },
      {
        heading: 'Handling Cold Chain Breaches',
        page: 2,
        text: 'Immediate quarantine in insulated coolers. Mark pending quality evaluation. Alert Biomedical Engineering ext 3311 within 15 minutes.'
      }
    ]
  },

  {
    id: 'DOC-LAB-302',
    title: 'Laboratory Specimen Collection, Rejection & Critical Reporting SOP',
    category: 'I. Laboratory Guidelines',
    department: 'Pathology & Laboratory',
    version: 'v4.0',
    effectiveDate: '2026-01-20',
    lastUpdated: '2026-09-01',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'LABORATORY_STAFF', 'DOCTOR', 'NURSE', 'EMERGENCY_STAFF'],
    fileType: 'PDF',
    fileSize: '2.8 MB',
    sourceUri: '/documents/laboratory-specimen-sop-v4.pdf',
    isArchived: false,
    content: `LABORATORY SPECIMEN COLLECTION, REJECTION & CRITICAL REPORTING SOP (LAB-SPEC-302)

Section 1: Phlebotomy Order of Draw
To avoid chemical cross-contamination between additives, tubes must be drawn strictly in this sequence:
1. Blood Culture bottles (SPS / aerobic & anaerobic)
2. Coagulation tube (Light Blue, Sodium Citrate 3.2%)
3. Serum tubes with/without clot activator (Red or Gold SST)
4. Heparin tube (Green or Mint, Lithium Heparin)
5. EDTA tube (Lavender / Purple, K2-EDTA)
6. Glycolytic inhibitor (Gray, Sodium Fluoride/Potassium Oxalate)

Section 2: Specimen Rejection Criteria
Samples will be formally rejected and documented in the LIS if:
- Tube is unlabeled, mislabeled, or barcode does not match requisition.
- Grossly hemolyzed serum/plasma for Potassium, LDH, or AST testing.
- Clotted specimen in EDTA or Citrate anticoagulant tubes.
- Underfilled Citrate tube (< 90% fill line disrupts 9:1 blood-to-anticoagulant ratio).
- QNS (Quantity Not Sufficient) for ordered automated analyzer profile.

Section 3: Critical Panic Value Notification Protocol
Critical lab results representing immediate life-threatening abnormalities (e.g. Potassium < 2.5 or > 6.2 mmol/L, Troponin I > 0.04 ng/mL with upward delta, Platelets < 20,000/uL, Glucose < 45 or > 450 mg/dL):
1. Must be re-tested immediately on analyzer to verify validity.
2. Laboratory technologist must call the attending physician or unit charge nurse within 15 minutes.
3. Read-back verification of patient name, MRN, parameter, and numerical value is mandatory and logged.`,
    sections: [
      {
        heading: 'Phlebotomy Order of Draw',
        page: 1,
        text: 'Order: 1. Blood Cultures, 2. Light Blue (Citrate), 3. Red/Gold (Serum), 4. Green (Heparin), 5. Lavender (EDTA), 6. Gray (Fluoride).'
      },
      {
        heading: 'Specimen Rejection Criteria',
        page: 2,
        text: 'Mislabeled tubes, hemolyzed samples for K+/LDH, clotted EDTA/Citrate, underfilled Citrate (<90% fill), and QNS.'
      },
      {
        heading: 'Critical Panic Value Notification Protocol',
        page: 3,
        text: 'Re-test on analyzer. Mandatory telephone call to clinician within 15 minutes with read-back verification logged in LIS.'
      }
    ]
  },

  {
    id: 'DOC-RAD-12',
    title: 'Diagnostic Radiology & Contrast Media Safety Protocol',
    category: 'J. Radiology Guidelines',
    department: 'Radiology',
    version: 'v3.5',
    effectiveDate: '2026-02-10',
    lastUpdated: '2026-08-18',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'RADIOLOGY_STAFF', 'DOCTOR', 'NURSE', 'EMERGENCY_STAFF'],
    fileType: 'PDF',
    fileSize: '2.1 MB',
    sourceUri: '/documents/radiology-safety-guidelines-v3.pdf',
    isArchived: false,
    content: `DIAGNOSTIC RADIOLOGY & CONTRAST MEDIA SAFETY PROTOCOL (RAD-SAFE-12)

Section 1: Iodinated Contrast Media and Renal Function Screening
1.1 eGFR Screening: All patients receiving intravenous iodinated contrast for CT must have documented eGFR within 30 days (or 48 hours for acute inpatients).
- eGFR ≥ 45 mL/min/1.73m²: Standard contrast administration approved.
- eGFR 30 - 44 mL/min/1.73m²: High risk for Contrast-Induced Nephropathy (CIN). Requires attending radiologist approval and isotonic IV pre- and post-hydration (0.9% Normal Saline 1 mL/kg/h).
- eGFR < 30 mL/min/1.73m²: Iodinated contrast contraindicated unless emergent with informed consent and dialysis coordination.

Section 2: MRI Zone Screening and Implant Safety
The MRI suite is divided into 4 safety zones. Zone 4 (Magnet Room) requires mandatory metal detector screening and double-signature implant checklist.
Absolute Contraindications: Non-MRI-conditional cardiac pacemakers, ferromagnetic cerebral aneurysm clips, cochlear implants without removable magnets, and metallic foreign bodies in the ocular orbit.

Section 3: ALARA Principle and Radiation Dose Optimization
All ionizing imaging modalities adhere to ALARA (As Low As Reasonably Achievable). Pediatric CT protocols utilize weight-adapted kVp/mAs modulation and thyroid/gonadal bismuth shielding.`,
    sections: [
      {
        heading: 'Iodinated Contrast Media and Renal Function Screening',
        page: 1,
        text: 'eGFR required. If eGFR 30-44: IV hydration required and radiologist approval. eGFR < 30: contraindicated unless emergent life-threatening indication.'
      },
      {
        heading: 'MRI Zone Screening and Implant Safety',
        page: 2,
        text: 'Zone 4 strict magnetic screening. Absolute contraindications: non-conditional pacemakers, ferromagnetic aneurysm clips, metallic eye foreign bodies.'
      },
      {
        heading: 'ALARA Principle and Radiation Dose Optimization',
        page: 3,
        text: 'Adherence to As Low As Reasonably Achievable. Weight-based pediatric dosing and anatomical radiation shielding.'
      }
    ]
  },

  {
    id: 'DOC-INS-102',
    title: 'Insurance Pre-Authorization & Claims Submission Guidelines',
    category: 'K. Insurance Policies',
    department: 'Insurance Services',
    version: 'v4.3',
    effectiveDate: '2026-01-05',
    lastUpdated: '2026-09-12',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'INSURANCE_STAFF', 'BILLING_STAFF', 'PATIENT', 'DOCTOR'],
    fileType: 'PDF',
    fileSize: '1.9 MB',
    sourceUri: '/documents/insurance-guidelines-v4.pdf',
    isArchived: false,
    content: `INSURANCE PRE-AUTHORIZATION & CLAIMS SUBMISSION GUIDELINES (INS-PREAUTH-102)

Section 1: Pre-Authorization Requirements for Inpatient Admissions
Elective surgeries, inpatient admissions, and high-cost diagnostics (MRI, PET-CT) require pre-authorization from the contracted insurance carrier (Blue Cross, Aetna, UnitedHealthcare, Cigna, Medicare).
Mandatory submission packet:
1. Attending physician letter of medical necessity (Form INS-MED-09)
2. Pertinent diagnostic clinical reports (imaging, biopsy, lab results)
3. Itemized surgical estimate code (CPT and ICD-10-CM codes)
4. Patient insurance card copy and government ID.
Turnaround timeline: Elective requests must be submitted at least 72 business hours before admission. Emergency admissions must be notified within 24 hours of bed placement.

Section 2: Managing Claim Denials and Appeals
If a claim is denied for "Lack of Medical Necessity":
- Level 1 Appeal: Must be filed within 30 days with detailed physician clinical chart notes, vital trends, and peer-reviewed clinical guidelines.
- Peer-to-Peer Review: Attending clinician or Medical Director schedules a direct phone consultation with the insurance medical director within 5 business days.`,
    sections: [
      {
        heading: 'Pre-Authorization Requirements for Inpatient Admissions',
        page: 1,
        text: 'Requires letter of medical necessity, diagnostic reports, CPT/ICD-10 codes, and ID. Submit 72 hours before elective; 24 hours post emergency.'
      },
      {
        heading: 'Managing Claim Denials and Appeals',
        page: 2,
        text: 'File Level 1 appeal within 30 days with full clinical chart. Peer-to-peer physician conference scheduled within 5 business days.'
      }
    ]
  },

  {
    id: 'DOC-BILL-2026',
    title: 'Inpatient & Outpatient Billing, Tariffs and Refund Policy',
    category: 'L. Billing Policies',
    department: 'Billing & Finance',
    version: 'v2.8',
    effectiveDate: '2026-01-01',
    lastUpdated: '2026-08-25',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'BILLING_STAFF', 'INSURANCE_STAFF', 'PATIENT'],
    fileType: 'PDF',
    fileSize: '2.0 MB',
    sourceUri: '/documents/billing-tariffs-policy-2026.pdf',
    isArchived: false,
    content: `INPATIENT & OUTPATIENT BILLING, TARIFFS AND REFUND POLICY (BILL-TARIFF-2026)

Section 1: Daily Room Tariffs and Clinical Surcharges
- Standard Inpatient Bed: $450/day (includes nursing care, basic dietary, and bedside vitals).
- Telemetry Monitored Ward: $750/day (includes continuous cardiac rhythm monitoring).
- Intensive Care Unit (ICU): $2,200/day (includes 1:1 or 1:2 critical nursing, ventilator management).
- Isolation Room: Additional $250/day infection barrier surcharge.
Charges are calculated on a midnight census basis. Patients discharged prior to 12:00 PM will not be billed for that day.

Section 2: Patient Refund and Dispute Resolution
2.1 Overpayment Refunds: When insurance adjudication yields an overpayment of patient copays or deductibles, refunds are automatically credited to the patient within 14 business days via original payment method.
2.2 Disputed Charges: Patients may file a formal billing dispute within 60 days of invoice receipt. Disputed accounts are placed on temporary administrative hold, suspending collection workflows pending medical record review.
2.3 Financial Hardship Program: Uninsured or underinsured patients qualifying under 250% Federal Poverty Line may receive up to 60% discounted tariff upon submitting tax returns and income verification.`,
    sections: [
      {
        heading: 'Daily Room Tariffs and Clinical Surcharges',
        page: 1,
        text: 'Standard: $450/day. Telemetry: $750/day. ICU: $2,200/day. Midnight census calculation. Discharge before 12 PM waives daily room fee.'
      },
      {
        heading: 'Patient Refund and Dispute Resolution',
        page: 2,
        text: 'Refunds processed within 14 business days. Disputed charges held up to 60 days. Hardship discount up to 60% for eligible self-pay patients.'
      }
    ]
  },

  {
    id: 'DOC-IC-STERILE-04',
    title: 'Hospital Infection Prevention & Control Manual',
    category: 'Q. Infection Control',
    department: 'Internal Medicine',
    version: 'v4.5',
    effectiveDate: '2026-01-10',
    lastUpdated: '2026-09-18',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'DEPARTMENT_MANAGER', 'EMERGENCY_STAFF', 'LABORATORY_STAFF'],
    fileType: 'PDF',
    fileSize: '3.4 MB',
    sourceUri: '/documents/infection-control-manual-v4.pdf',
    isArchived: false,
    content: `HOSPITAL INFECTION PREVENTION & CONTROL MANUAL (IC-STERILE-V4)

Section 1: Hand Hygiene Compliance and 5 Moments
All hospital clinical and support staff must adhere to the WHO 5 Moments for Hand Hygiene:
1. Before touching a patient
2. Before clean/aseptic procedure
3. After body fluid exposure risk
4. After touching a patient
5. After touching patient surroundings
Alcohol-based hand rub with minimum 70% ethyl alcohol must be rubbed vigorously for at least 20 seconds. Soap and water are mandatory for Clostridioides difficile.

Section 2: Transmission-Based Isolation Precautions
- Contact Precautions (MRSA, VRE, C. diff): Gown and gloves required upon room entry. Dedicated patient equipment (stethoscope, BP cuff).
- Droplet Precautions (Influenza, Pertussis, Meningitis): Surgical mask within 6 feet, eye protection.
- Airborne Precautions (Tuberculosis, Measles, Disseminated Varicella): Negative pressure isolation room (AIIR) with minimum 12 air changes/hour; fit-tested N95 or PAPR respirator mandatory.

Section 3: Central Line and Urinary Catheter Bundle (CLABSI & CAUTI Prevention)
Full barrier drape, chlorhexidine skin antisepsis with friction, and daily review of line necessity. Foley catheters must be removed within 24 hours of indication cessation.`,
    sections: [
      {
        heading: 'Hand Hygiene Compliance and 5 Moments',
        page: 1,
        text: 'WHO 5 Moments. 70% alcohol hand rub for 20s. Soap and water mandatory for C. difficile.'
      },
      {
        heading: 'Transmission-Based Isolation Precautions',
        page: 2,
        text: 'Contact: gown/gloves. Droplet: mask/eye protection. Airborne: Negative pressure room (12 air changes/hr) and fit-tested N95.'
      },
      {
        heading: 'CLABSI & CAUTI Prevention Bundles',
        page: 3,
        text: 'Sterile barrier drape, chlorhexidine antisepsis, daily line necessity audit. Immediate catheter removal upon lack of indication.'
      }
    ]
  },

  {
    id: 'DOC-PT-RIGHTS-26',
    title: 'Patient Rights, Responsibilities and Informed Consent Policy',
    category: 'V. Consent Forms',
    department: 'Hospital Administration',
    version: 'v2.1',
    effectiveDate: '2026-01-01',
    lastUpdated: '2026-07-22',
    confidentiality: 'PUBLIC',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'PATIENT', 'DEPARTMENT_MANAGER'],
    fileType: 'PDF',
    fileSize: '1.1 MB',
    sourceUri: '/documents/patient-rights-handbook.pdf',
    isArchived: false,
    content: `PATIENT RIGHTS, RESPONSIBILITIES AND INFORMED CONSENT POLICY (PT-RIGHTS-2026)

Section 1: Inalienable Patient Rights
Every patient treated at our medical center has the right to:
1. Receive considerate, respectful, and compassionate healthcare regardless of race, gender, religion, national origin, or socioeconomic status.
2. Complete, comprehensible information regarding their diagnosis, proposed treatment, realistic prognosis, and alternative therapies.
3. Informed Consent: Voluntary consent obtained prior to any surgical operation, invasive diagnostic procedure, or blood transfusion after risks, benefits, and complications have been explained by the performing clinician.
4. Privacy and Confidentiality: Protection of all personal medical records under HIPAA and healthcare data privacy standards.
5. Pain management assessment and treatment.
6. The right to refuse treatment or request a second clinical opinion without penalty.

Section 2: Patient Responsibilities
Patients and families are responsible for:
- Providing accurate and complete details concerning past illnesses, hospitalizations, medications, allergies, and family health history.
- Following agreed treatment plans and instructions given by authorized clinical staff.
- Respecting hospital quiet hours (9:00 PM to 6:00 AM) and non-smoking campus regulations.`,
    sections: [
      {
        heading: 'Inalienable Patient Rights',
        page: 1,
        text: 'Respectful care, comprehensible diagnosis info, voluntary informed consent for surgery/transfusions, HIPAA confidentiality, pain management, right to refuse.'
      },
      {
        heading: 'Patient Responsibilities',
        page: 2,
        text: 'Provide accurate medical history, follow treatment instructions, respect hospital quiet hours (9 PM - 6 AM) and smoke-free campus.'
      }
    ]
  },

  {
    id: 'DOC-VISIT-2026',
    title: 'Hospital Visitor and Family Access Policy',
    category: 'U. Visiting Policies',
    department: 'Hospital Administration',
    version: 'v3.1',
    effectiveDate: '2026-02-01',
    lastUpdated: '2026-08-11',
    confidentiality: 'PUBLIC',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'PATIENT', 'DEPARTMENT_MANAGER'],
    fileType: 'PDF',
    fileSize: '0.9 MB',
    sourceUri: '/documents/visitor-policy-2026.pdf',
    isArchived: false,
    content: `HOSPITAL VISITOR AND FAMILY ACCESS POLICY (VISIT-POLICY-V1)

Section 1: Visiting Hours by Department
- General Inpatient Wards: Daily from 10:00 AM to 8:00 PM. Maximum 2 visitors per bedside at any time.
- Intensive Care Units (ICU & CCU): Daily from 11:00 AM to 1:00 PM and 5:00 PM to 7:00 PM. Immediate family members only; maximum 2 visitors. Children under 12 require special charge nurse dispensation.
- Neonatal ICU (NICU): 24-hour open access for tagged parents; no outside siblings or guests permitted during sterile medication rounds.
- Emergency Department: 1 designated support companion permitted at bedside during initial evaluation, provided patient condition is stable.

Section 2: Visitor Identification and Infection Screening
All visitors must check in at the Main Lobby Front Desk, display government photo ID, receive a timestamped Visitor Badge, and pass automated temperature screening. Visitors experiencing fever, respiratory symptoms, or infectious rashes are strictly prohibited from entering patient care units.`,
    sections: [
      {
        heading: 'Visiting Hours by Department',
        page: 1,
        text: 'General: 10 AM - 8 PM (max 2 visitors). ICU: 11 AM - 1 PM and 5 PM - 7 PM (max 2 family members). NICU: 24h parents. Emergency: 1 companion.'
      },
      {
        heading: 'Visitor Identification and Screening',
        page: 2,
        text: 'Check-in at front desk, valid photo ID, wearable visitor badge. Temperature check; visitors with fever/cough barred from inpatient floors.'
      }
    ]
  },

  {
    id: 'DOC-HR-LEAVE-09',
    title: 'Hospital Staff Leave, On-Call Roster & Overtime Policy',
    category: 'O. HR Policies',
    department: 'Human Resources',
    version: 'v3.4',
    effectiveDate: '2026-01-01',
    lastUpdated: '2026-09-05',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'HR_STAFF', 'DEPARTMENT_MANAGER', 'MANAGEMENT_EXECUTIVE'],
    fileType: 'PDF',
    fileSize: '1.4 MB',
    sourceUri: '/documents/staff-leave-policy-v3.pdf',
    isArchived: false,
    content: `HOSPITAL STAFF LEAVE, ON-CALL ROSTER & OVERTIME POLICY (HR-LEAVE-09)

Section 1: Annual and Medical Leave Entitlements
- Full-Time Clinical Staff (Physicians & Registered Nurses): 24 days Paid Annual Leave, 12 days Paid Sick Leave, and 5 days Continuing Medical Education (CME) Leave per calendar year.
- Planned leave requests must be submitted through the Enterprise HR Portal at least 21 days in advance to guarantee unit staffing coverage.
- Sick leave exceeding 3 consecutive calendar days requires an authorized Medical Fitness Certificate from an independent licensed physician.

Section 2: On-Call Coverage and Shift Differential Compensation
2.1 Night Shift Differential: Staff performing evening/night shifts (7:00 PM to 7:00 AM) receive a 15% hourly premium.
2.2 Mandatory On-Call: Physicians on designated on-call rosters must remain within a 30-minute travel radius of the hospital trauma center and respond to paging within 10 minutes.
2.3 Overtime Rules: Non-exempt nursing and technologist staff working beyond 40 hours per week receive 1.5x standard hourly wage.`,
    sections: [
      {
        heading: 'Annual and Medical Leave Entitlements',
        page: 1,
        text: 'Clinical staff: 24 annual days, 12 sick days, 5 CME days. Submit 21 days in advance. Sick leave > 3 days requires medical certificate.'
      },
      {
        heading: 'On-Call Coverage and Shift Differentials',
        page: 2,
        text: '15% night differential (7 PM - 7 AM). On-call physicians must be within 30-minute radius, respond within 10 mins. 1.5x overtime > 40 hours.'
      }
    ]
  },

  {
    id: 'DOC-CLIN-SEP-02',
    title: 'ICU Clinical Guideline for Sepsis Resuscitation & Antibiotic Timing',
    category: 'F. Clinical Guidelines',
    department: 'Intensive Care Unit (ICU)',
    version: 'v4.0',
    effectiveDate: '2026-02-15',
    lastUpdated: '2026-09-22',
    confidentiality: 'RESTRICTED',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'EMERGENCY_STAFF', 'PHARMACIST'],
    fileType: 'PDF',
    fileSize: '2.6 MB',
    sourceUri: '/documents/icu-sepsis-guideline-v4.pdf',
    isArchived: false,
    content: `ICU CLINICAL GUIDELINE FOR SEPSIS RESUSCITATION & ANTIBIOTIC TIMING (CLIN-ICU-SEP-02)

Section 1: Hour-1 Sepsis Bundle Initiation
Upon suspicion or confirmation of Sepsis or Septic Shock (SOFA score increase ≥ 2 or qSOFA ≥ 2):
1. Measure serum lactate immediately. Re-measure within 2-4 hours if initial lactate > 2.0 mmol/L.
2. Obtain blood cultures (two sets: aerobic and anaerobic from two distinct sites) prior to antibiotic administration, without causing unnecessary delay (> 45 minutes).
3. Administer broad-spectrum intravenous antimicrobials within 1 hour of sepsis recognition. Empiric regimen: Vancomycin (15-20 mg/kg IV q8-12h targeting trough 15-20 mcg/mL) PLUS Piperacillin-Tazobactam (4.5g IV q6h) or Cefepime (2g IV q8h).
4. Rapid administration of 30 mL/kg balanced crystalloid solution (Lactated Ringer's) for hypotension or serum lactate ≥ 4.0 mmol/L within 3 hours.

Section 2: Vasoactive Inotropic Support in Septic Shock
If mean arterial pressure (MAP) remains < 65 mmHg despite crystalloid loading:
- First-Line Vasopressor: Norepinephrine IV infusion (titrate 0.05 - 1.0 mcg/kg/min) to maintain target MAP ≥ 65 mmHg.
- Second-Line: Add Vasopressin at fixed rate 0.03 units/min if norepinephrine escalates beyond 0.25 mcg/kg/min.
- Epinephrine may be added for refractory hypotension or myocardial dysfunction.`,
    sections: [
      {
        heading: 'Hour-1 Sepsis Bundle Initiation',
        page: 1,
        text: 'Lactate measurement, 2 sets blood cultures, broad-spectrum IV antibiotics within 1 hour (Vancomycin + Pip/Tazo), 30 mL/kg crystalloids for MAP < 65 or lactate >= 4.'
      },
      {
        heading: 'Vasoactive Support in Septic Shock',
        page: 2,
        text: 'Target MAP >= 65 mmHg. First-line vasopressor: Norepinephrine. Second-line: Vasopressin 0.03 units/min. Epinephrine for refractory shock.'
      }
    ]
  },

  {
    id: 'DOC-DISASTER-01',
    title: 'Hospital Disaster Preparedness & Mass Casualty Incident (MCI) Plan',
    category: 'E. Emergency Procedures',
    department: 'Hospital Administration',
    version: 'v5.1',
    effectiveDate: '2026-03-01',
    lastUpdated: '2026-09-30',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'EMERGENCY_STAFF', 'MANAGEMENT_EXECUTIVE', 'DEPARTMENT_MANAGER'],
    fileType: 'PDF',
    fileSize: '3.0 MB',
    sourceUri: '/documents/disaster-mci-plan-2026.pdf',
    isArchived: false,
    content: `HOSPITAL DISASTER PREPAREDNESS & MASS CASUALTY INCIDENT (MCI) PLAN (DISASTER-MCI-01)

Section 1: Activation Criteria and Incident Command System (HICS)
An MCI (Code Black) is declared by the Chief Executive Officer, Chief Medical Officer, or on-duty Emergency Department Medical Director when external casualties exceed standard operational capacity.
Activation immediately triggers:
1. Hospital Incident Command Center established in Conference Room 1A.
2. Emergency Triage Staging established outside the Ambulance Bay using START triage algorithm.
3. Discharge of stable elective inpatients to free immediate floor beds.
4. Calling in the off-duty Trauma Call Roster via mass telecommunication cascade.

Section 2: START Triage Field Categorization
- Red (Immediate): Life-threatening airway, breathing, or circulatory emergency treatable with rapid intervention.
- Yellow (Delayed): Serious injury but can wait up to 2 hours without imminent threat to life.
- Green (Minor / Walking Wounded): Ambulatory casualties directed to Outpatient Clinic Auditorium.
- Black (Expectant / Deceased): Fatal injuries incompatible with life given current resource availability.`,
    sections: [
      {
        heading: 'Activation Criteria and Incident Command',
        page: 1,
        text: 'Declared by CEO/CMO/ED Director. HICS command center in Conf Room 1A. External START triage outside bay. Off-duty trauma roster called in.'
      },
      {
        heading: 'START Triage Field Categorization',
        page: 2,
        text: 'Red: Immediate life threat. Yellow: Delayed (<2h). Green: Walking wounded routed to auditorium. Black: Expectant.'
      }
    ]
  },

  {
    id: 'DOC-HIPAA-PRIV-01',
    title: 'Health Information Privacy & HIPAA/GDPR Compliance Policy',
    category: 'W. Privacy Policies',
    department: 'Hospital Administration',
    version: 'v4.0',
    effectiveDate: '2026-01-01',
    lastUpdated: '2026-08-15',
    confidentiality: 'INTERNAL',
    roleAccess: ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'PATIENT', 'BILLING_STAFF', 'INSURANCE_STAFF', 'HR_STAFF', 'MANAGEMENT_EXECUTIVE', 'DEPARTMENT_MANAGER'],
    fileType: 'PDF',
    fileSize: '2.2 MB',
    sourceUri: '/documents/hipaa-data-privacy-policy.pdf',
    isArchived: false,
    content: `HEALTH INFORMATION PRIVACY & HIPAA/GDPR COMPLIANCE POLICY (HIPAA-PRIV-01)

Section 1: Minimum Necessary Rule and Access Rights
All staff members must only access Protected Health Information (PHI) directly necessary to fulfill their assigned clinical or administrative job function. Clinical notes, diagnostic imaging, and laboratory results may only be accessed by care team clinicians directly assigned to the patient. Snooping on non-assigned patients, family members, or VIPs results in immediate termination and state board reporting.

Section 2: Security Controls for Electronic Protected Health Information (ePHI)
- Cryptographic Standards: All patient records at rest must be encrypted using AES-256; data in transit requires TLS 1.3 encryption.
- Multi-Factor Authentication: Mandatory on all workstations, mobile clinical tablets, and remote telemetry portals.
- Auto-Lockout: Workstations automatically lock screen after 3 minutes of inactivity.
- Audit Logging: Every view, export, query, and modification of patient charts is logged irrevocably with user ID, timestamp, and IP address.`,
    sections: [
      {
        heading: 'Minimum Necessary Rule and Access Rights',
        page: 1,
        text: 'Staff may only access PHI required for active job role. Chart access limited to assigned care team. Unauthorized access triggers termination.'
      },
      {
        heading: 'Security Controls for ePHI',
        page: 2,
        text: 'AES-256 rest encryption, TLS 1.3 in-transit. MFA required. 3-minute workstation auto-lockout. Irrevocable audit logging on every chart touch.'
      }
    ]
  },

  {
    id: 'DOC-PT-10023-REC',
    title: 'Clinical Summary & Inpatient Records: John Anderson (MRN-884920)',
    category: 'Patient Medical Records',
    department: 'Cardiology',
    version: 'v1.0',
    effectiveDate: '2026-10-01',
    lastUpdated: '2026-10-04',
    confidentiality: 'CONFIDENTIAL',
    roleAccess: ['DOCTOR', 'NURSE', 'PATIENT', 'EMERGENCY_STAFF', 'PHARMACIST'],
    patientId: 'PT-10023',
    fileType: 'TXT',
    fileSize: '45 KB',
    sourceUri: '/records/PT-10023-summary.txt',
    isArchived: false,
    content: `PATIENT MEDICAL RECORD SUMMARY
Patient Name: John Anderson | DOB: 1968-05-14 (Age: 58) | MRN: MRN-884920 | Hospital ID: PT-10023
Attending Physician: Dr. Marcus Vance (Cardiology) | Admitted to: Cardiac Step-Down Unit Bed 304-B
Documented Allergies: Penicillin (severe anaphylaxis), Shellfish (mild urticaria).
Chronic Conditions: Coronary Artery Disease, Hypertension, Type 2 Diabetes Mellitus.

Hospital Course & Current Clinical Notes (Updated Oct 4, 2026):
Patient presented with exertional substernal chest pressure. Coronary angiography on Oct 2 revealed 85% stenosis of Mid-LAD, successfully treated with 1 Drug-Eluting Stent (DES). Post-procedure hemodynamics stable. Troponin I down-trending from 1.45 to 0.08 ng/mL. Blood pressure 128/78 mmHg, Heart Rate 68 bpm regular, SpO2 98% on room air.

Active Prescriptions:
1. Aspirin 81 mg oral daily
2. Ticagrelor 90 mg oral twice daily (Dual Antiplatelet Therapy for 12 months)
3. Atorvastatin 80 mg oral at bedtime
4. Metoprolol Tartrate 25 mg oral twice daily
5. Metformin 500 mg oral twice daily with meals
Discharge Plan: Planned for Oct 5, 2026 with cardiac rehabilitation referral.`,
    sections: [
      {
        heading: 'Patient Demographics and Allergies',
        page: 1,
        text: 'John Anderson, 58yo male. Severe Penicillin anaphylaxis, shellfish allergy. CAD, HTN, T2DM.'
      },
      {
        heading: 'Hospital Course and Cardiac Angiography',
        page: 1,
        text: 'Mid-LAD 85% stenosis treated with drug-eluting stent. Troponin normalized to 0.08 ng/mL. Vitals stable BP 128/78.'
      },
      {
        heading: 'Active Medications and Discharge Plan',
        page: 1,
        text: 'Aspirin 81mg, Ticagrelor 90mg BID, Atorvastatin 80mg, Metoprolol 25mg BID, Metformin 500mg BID. Discharge planned Oct 5 with cardiac rehab.'
      }
    ]
  }
];

// Helper function to extract document chunks for RAG indexing
export function generateDocumentChunks(): DocumentChunk[] {
  const chunks: DocumentChunk[] = [];
  
  for (const doc of HOSPITAL_DOCUMENTS) {
    if (doc.sections && doc.sections.length > 0) {
      doc.sections.forEach((sec, idx) => {
        chunks.push({
          id: `${doc.id}-chunk-${idx + 1}`,
          documentId: doc.id,
          documentTitle: doc.title,
          category: doc.category,
          department: doc.department,
          roleAccess: doc.roleAccess,
          confidentiality: doc.confidentiality,
          patientId: doc.patientId,
          lastUpdated: doc.lastUpdated,
          version: doc.version,
          pageNumber: sec.page,
          section: sec.heading,
          content: `${doc.title} - Section: ${sec.heading}\n\n${sec.text}\n\n[Full Context]: ${doc.content.substring(0, 450)}`,
          tags: [doc.category, doc.department, sec.heading.toLowerCase(), doc.version]
        });
      });
    } else {
      // Chunk whole document
      chunks.push({
        id: `${doc.id}-chunk-1`,
        documentId: doc.id,
        documentTitle: doc.title,
        category: doc.category,
        department: doc.department,
        roleAccess: doc.roleAccess,
        confidentiality: doc.confidentiality,
        patientId: doc.patientId,
        lastUpdated: doc.lastUpdated,
        version: doc.version,
        pageNumber: 1,
        section: 'General Document Overview',
        content: doc.content,
        tags: [doc.category, doc.department, doc.version]
      });
    }
  }

  return chunks;
}
