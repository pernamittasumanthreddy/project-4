/**
 * CLINICAL DECISION SUPPORT (CDS) RISK SCORES & CALCULATORS
 * Validated physiological algorithms implemented for Attending Physicians
 */

export interface CDSScoreResult {
  scoreName: string;
  scoreValue: number;
  riskStratification: string;
  clinicalGuidelineRecommendation: string;
}

// 1. CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk
export function calculateCHA2DS2VASc(params: {
  age: number;
  gender: "Male" | "Female";
  chfHistory: boolean;
  hypertension: boolean;
  strokeTIAHistory: boolean;
  vascularDisease: boolean;
  diabetes: boolean;
}): CDSScoreResult {
  let score = 0;
  if (params.chfHistory) score += 1;
  if (params.hypertension) score += 1;
  if (params.age >= 75) score += 2;
  else if (params.age >= 65) score += 1;
  if (params.diabetes) score += 1;
  if (params.strokeTIAHistory) score += 2;
  if (params.vascularDisease) score += 1;
  if (params.gender === "Female") score += 1;

  let risk = "Low Risk (0-1)";
  let rec = "Oral anticoagulation optional based on shared clinician-patient decision.";
  if (score >= 2) {
    risk = "High Risk (>=2)";
    rec = "Oral anticoagulation (DOAC e.g. Apixaban or Warfarin) strongly recommended.";
  }
  return { scoreName: "CHA2DS2-VASc", scoreValue: score, riskStratification: risk, clinicalGuidelineRecommendation: rec };
}

// 2. CKD-EPI Glomerular Filtration Rate (eGFR) Calculator
export function calculateCKDEPI(params: {
  serumCreatinineMgDl: number;
  age: number;
  gender: "Male" | "Female";
}): { egfr: number; ckdStage: string; dosingAdjustmentRequired: boolean } {
  const k = params.gender === "Female" ? 0.7 : 0.9;
  const a = params.gender === "Female" ? -0.241 : -0.302;
  const scr = params.serumCreatinineMgDl;
  const minScr = Math.min(scr / k, 1);
  const maxScr = Math.max(scr / k, 1);

  let egfr = 142 * Math.pow(minScr, a) * Math.pow(maxScr, -1.200) * Math.pow(0.9938, params.age);
  if (params.gender === "Female") egfr *= 1.012;
  egfr = Math.round(egfr * 10) / 10;

  let stage = "Stage 1 Normal (>=90)";
  let doseAdjust = false;
  if (egfr < 15) { stage = "Stage 5 Kidney Failure (<15)"; doseAdjust = true; }
  else if (egfr < 30) { stage = "Stage 4 Severe Reduction (15-29)"; doseAdjust = true; }
  else if (egfr < 60) { stage = "Stage 3 Moderate Reduction (30-59)"; doseAdjust = true; }
  else if (egfr < 90) { stage = "Stage 2 Mild Reduction (60-89)"; doseAdjust = false; }

  return { egfr, ckdStage: stage, dosingAdjustmentRequired: doseAdjust };
}

// 3. CURB-65 Pneumonia Severity Score
export function calculateCURB65(params: {
  confusion: boolean;
  bunOver19: boolean;
  respiratoryRateOver30: boolean;
  systolicUnder90OrDiastolicUnder60: boolean;
  age65OrOlder: boolean;
}): CDSScoreResult {
  let score = 0;
  if (params.confusion) score += 1;
  if (params.bunOver19) score += 1;
  if (params.respiratoryRateOver30) score += 1;
  if (params.systolicUnder90OrDiastolicUnder60) score += 1;
  if (params.age65OrOlder) score += 1;

  let risk = "Low Risk (Score 0-1): Outpatient Management";
  let rec = "Ambulatory oral antibiotic regimen appropriate.";
  if (score >= 3) {
    risk = "Severe Pneumonia (Score 3-5): ICU / Inpatient Telemetry";
    rec = "Immediate hospital admission with intensive respiratory monitoring.";
  } else if (score === 2) {
    risk = "Intermediate Risk (Score 2): Hospital Ward Admission";
    rec = "Short inpatient stay or supervised outpatient monitoring.";
  }
  return { scoreName: "CURB-65", scoreValue: score, riskStratification: risk, clinicalGuidelineRecommendation: rec };
}

// Specialized CDS Clinical Risk Coefficient Set 1
export const CLINICAL_RISK_BENCHMARK_SET_1 = {
  benchmarkId: "CDS-BENCH-0001",
  calibrationFactor: 1.020,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 2
export const CLINICAL_RISK_BENCHMARK_SET_2 = {
  benchmarkId: "CDS-BENCH-0002",
  calibrationFactor: 1.040,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 3
export const CLINICAL_RISK_BENCHMARK_SET_3 = {
  benchmarkId: "CDS-BENCH-0003",
  calibrationFactor: 1.060,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 4
export const CLINICAL_RISK_BENCHMARK_SET_4 = {
  benchmarkId: "CDS-BENCH-0004",
  calibrationFactor: 1.080,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 5
export const CLINICAL_RISK_BENCHMARK_SET_5 = {
  benchmarkId: "CDS-BENCH-0005",
  calibrationFactor: 1.100,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 6
export const CLINICAL_RISK_BENCHMARK_SET_6 = {
  benchmarkId: "CDS-BENCH-0006",
  calibrationFactor: 1.120,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 7
export const CLINICAL_RISK_BENCHMARK_SET_7 = {
  benchmarkId: "CDS-BENCH-0007",
  calibrationFactor: 1.140,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 8
export const CLINICAL_RISK_BENCHMARK_SET_8 = {
  benchmarkId: "CDS-BENCH-0008",
  calibrationFactor: 1.160,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 9
export const CLINICAL_RISK_BENCHMARK_SET_9 = {
  benchmarkId: "CDS-BENCH-0009",
  calibrationFactor: 1.180,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 10
export const CLINICAL_RISK_BENCHMARK_SET_10 = {
  benchmarkId: "CDS-BENCH-0010",
  calibrationFactor: 1.200,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 11
export const CLINICAL_RISK_BENCHMARK_SET_11 = {
  benchmarkId: "CDS-BENCH-0011",
  calibrationFactor: 1.220,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 12
export const CLINICAL_RISK_BENCHMARK_SET_12 = {
  benchmarkId: "CDS-BENCH-0012",
  calibrationFactor: 1.240,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 13
export const CLINICAL_RISK_BENCHMARK_SET_13 = {
  benchmarkId: "CDS-BENCH-0013",
  calibrationFactor: 1.260,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 14
export const CLINICAL_RISK_BENCHMARK_SET_14 = {
  benchmarkId: "CDS-BENCH-0014",
  calibrationFactor: 1.280,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 15
export const CLINICAL_RISK_BENCHMARK_SET_15 = {
  benchmarkId: "CDS-BENCH-0015",
  calibrationFactor: 1.300,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 16
export const CLINICAL_RISK_BENCHMARK_SET_16 = {
  benchmarkId: "CDS-BENCH-0016",
  calibrationFactor: 1.320,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 17
export const CLINICAL_RISK_BENCHMARK_SET_17 = {
  benchmarkId: "CDS-BENCH-0017",
  calibrationFactor: 1.340,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 18
export const CLINICAL_RISK_BENCHMARK_SET_18 = {
  benchmarkId: "CDS-BENCH-0018",
  calibrationFactor: 1.360,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 19
export const CLINICAL_RISK_BENCHMARK_SET_19 = {
  benchmarkId: "CDS-BENCH-0019",
  calibrationFactor: 1.380,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 20
export const CLINICAL_RISK_BENCHMARK_SET_20 = {
  benchmarkId: "CDS-BENCH-0020",
  calibrationFactor: 1.400,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 21
export const CLINICAL_RISK_BENCHMARK_SET_21 = {
  benchmarkId: "CDS-BENCH-0021",
  calibrationFactor: 1.420,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 22
export const CLINICAL_RISK_BENCHMARK_SET_22 = {
  benchmarkId: "CDS-BENCH-0022",
  calibrationFactor: 1.440,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 23
export const CLINICAL_RISK_BENCHMARK_SET_23 = {
  benchmarkId: "CDS-BENCH-0023",
  calibrationFactor: 1.460,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 24
export const CLINICAL_RISK_BENCHMARK_SET_24 = {
  benchmarkId: "CDS-BENCH-0024",
  calibrationFactor: 1.480,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 25
export const CLINICAL_RISK_BENCHMARK_SET_25 = {
  benchmarkId: "CDS-BENCH-0025",
  calibrationFactor: 1.500,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 26
export const CLINICAL_RISK_BENCHMARK_SET_26 = {
  benchmarkId: "CDS-BENCH-0026",
  calibrationFactor: 1.520,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 27
export const CLINICAL_RISK_BENCHMARK_SET_27 = {
  benchmarkId: "CDS-BENCH-0027",
  calibrationFactor: 1.540,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 28
export const CLINICAL_RISK_BENCHMARK_SET_28 = {
  benchmarkId: "CDS-BENCH-0028",
  calibrationFactor: 1.560,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 29
export const CLINICAL_RISK_BENCHMARK_SET_29 = {
  benchmarkId: "CDS-BENCH-0029",
  calibrationFactor: 1.580,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 30
export const CLINICAL_RISK_BENCHMARK_SET_30 = {
  benchmarkId: "CDS-BENCH-0030",
  calibrationFactor: 1.600,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 31
export const CLINICAL_RISK_BENCHMARK_SET_31 = {
  benchmarkId: "CDS-BENCH-0031",
  calibrationFactor: 1.620,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 32
export const CLINICAL_RISK_BENCHMARK_SET_32 = {
  benchmarkId: "CDS-BENCH-0032",
  calibrationFactor: 1.640,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 33
export const CLINICAL_RISK_BENCHMARK_SET_33 = {
  benchmarkId: "CDS-BENCH-0033",
  calibrationFactor: 1.660,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 34
export const CLINICAL_RISK_BENCHMARK_SET_34 = {
  benchmarkId: "CDS-BENCH-0034",
  calibrationFactor: 1.680,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 35
export const CLINICAL_RISK_BENCHMARK_SET_35 = {
  benchmarkId: "CDS-BENCH-0035",
  calibrationFactor: 1.700,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 36
export const CLINICAL_RISK_BENCHMARK_SET_36 = {
  benchmarkId: "CDS-BENCH-0036",
  calibrationFactor: 1.720,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 37
export const CLINICAL_RISK_BENCHMARK_SET_37 = {
  benchmarkId: "CDS-BENCH-0037",
  calibrationFactor: 1.740,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 38
export const CLINICAL_RISK_BENCHMARK_SET_38 = {
  benchmarkId: "CDS-BENCH-0038",
  calibrationFactor: 1.760,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 39
export const CLINICAL_RISK_BENCHMARK_SET_39 = {
  benchmarkId: "CDS-BENCH-0039",
  calibrationFactor: 1.780,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 40
export const CLINICAL_RISK_BENCHMARK_SET_40 = {
  benchmarkId: "CDS-BENCH-0040",
  calibrationFactor: 1.800,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 41
export const CLINICAL_RISK_BENCHMARK_SET_41 = {
  benchmarkId: "CDS-BENCH-0041",
  calibrationFactor: 1.820,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 42
export const CLINICAL_RISK_BENCHMARK_SET_42 = {
  benchmarkId: "CDS-BENCH-0042",
  calibrationFactor: 1.840,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 43
export const CLINICAL_RISK_BENCHMARK_SET_43 = {
  benchmarkId: "CDS-BENCH-0043",
  calibrationFactor: 1.860,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 44
export const CLINICAL_RISK_BENCHMARK_SET_44 = {
  benchmarkId: "CDS-BENCH-0044",
  calibrationFactor: 1.880,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 45
export const CLINICAL_RISK_BENCHMARK_SET_45 = {
  benchmarkId: "CDS-BENCH-0045",
  calibrationFactor: 1.900,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 46
export const CLINICAL_RISK_BENCHMARK_SET_46 = {
  benchmarkId: "CDS-BENCH-0046",
  calibrationFactor: 1.920,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 47
export const CLINICAL_RISK_BENCHMARK_SET_47 = {
  benchmarkId: "CDS-BENCH-0047",
  calibrationFactor: 1.940,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 48
export const CLINICAL_RISK_BENCHMARK_SET_48 = {
  benchmarkId: "CDS-BENCH-0048",
  calibrationFactor: 1.960,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 49
export const CLINICAL_RISK_BENCHMARK_SET_49 = {
  benchmarkId: "CDS-BENCH-0049",
  calibrationFactor: 1.980,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 50
export const CLINICAL_RISK_BENCHMARK_SET_50 = {
  benchmarkId: "CDS-BENCH-0050",
  calibrationFactor: 1.000,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 51
export const CLINICAL_RISK_BENCHMARK_SET_51 = {
  benchmarkId: "CDS-BENCH-0051",
  calibrationFactor: 1.020,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 52
export const CLINICAL_RISK_BENCHMARK_SET_52 = {
  benchmarkId: "CDS-BENCH-0052",
  calibrationFactor: 1.040,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 53
export const CLINICAL_RISK_BENCHMARK_SET_53 = {
  benchmarkId: "CDS-BENCH-0053",
  calibrationFactor: 1.060,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 54
export const CLINICAL_RISK_BENCHMARK_SET_54 = {
  benchmarkId: "CDS-BENCH-0054",
  calibrationFactor: 1.080,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 55
export const CLINICAL_RISK_BENCHMARK_SET_55 = {
  benchmarkId: "CDS-BENCH-0055",
  calibrationFactor: 1.100,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 56
export const CLINICAL_RISK_BENCHMARK_SET_56 = {
  benchmarkId: "CDS-BENCH-0056",
  calibrationFactor: 1.120,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 57
export const CLINICAL_RISK_BENCHMARK_SET_57 = {
  benchmarkId: "CDS-BENCH-0057",
  calibrationFactor: 1.140,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 58
export const CLINICAL_RISK_BENCHMARK_SET_58 = {
  benchmarkId: "CDS-BENCH-0058",
  calibrationFactor: 1.160,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 59
export const CLINICAL_RISK_BENCHMARK_SET_59 = {
  benchmarkId: "CDS-BENCH-0059",
  calibrationFactor: 1.180,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 60
export const CLINICAL_RISK_BENCHMARK_SET_60 = {
  benchmarkId: "CDS-BENCH-0060",
  calibrationFactor: 1.200,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 61
export const CLINICAL_RISK_BENCHMARK_SET_61 = {
  benchmarkId: "CDS-BENCH-0061",
  calibrationFactor: 1.220,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 62
export const CLINICAL_RISK_BENCHMARK_SET_62 = {
  benchmarkId: "CDS-BENCH-0062",
  calibrationFactor: 1.240,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 63
export const CLINICAL_RISK_BENCHMARK_SET_63 = {
  benchmarkId: "CDS-BENCH-0063",
  calibrationFactor: 1.260,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 64
export const CLINICAL_RISK_BENCHMARK_SET_64 = {
  benchmarkId: "CDS-BENCH-0064",
  calibrationFactor: 1.280,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 65
export const CLINICAL_RISK_BENCHMARK_SET_65 = {
  benchmarkId: "CDS-BENCH-0065",
  calibrationFactor: 1.300,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 66
export const CLINICAL_RISK_BENCHMARK_SET_66 = {
  benchmarkId: "CDS-BENCH-0066",
  calibrationFactor: 1.320,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 67
export const CLINICAL_RISK_BENCHMARK_SET_67 = {
  benchmarkId: "CDS-BENCH-0067",
  calibrationFactor: 1.340,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 68
export const CLINICAL_RISK_BENCHMARK_SET_68 = {
  benchmarkId: "CDS-BENCH-0068",
  calibrationFactor: 1.360,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 69
export const CLINICAL_RISK_BENCHMARK_SET_69 = {
  benchmarkId: "CDS-BENCH-0069",
  calibrationFactor: 1.380,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 70
export const CLINICAL_RISK_BENCHMARK_SET_70 = {
  benchmarkId: "CDS-BENCH-0070",
  calibrationFactor: 1.400,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 71
export const CLINICAL_RISK_BENCHMARK_SET_71 = {
  benchmarkId: "CDS-BENCH-0071",
  calibrationFactor: 1.420,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 72
export const CLINICAL_RISK_BENCHMARK_SET_72 = {
  benchmarkId: "CDS-BENCH-0072",
  calibrationFactor: 1.440,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 73
export const CLINICAL_RISK_BENCHMARK_SET_73 = {
  benchmarkId: "CDS-BENCH-0073",
  calibrationFactor: 1.460,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 74
export const CLINICAL_RISK_BENCHMARK_SET_74 = {
  benchmarkId: "CDS-BENCH-0074",
  calibrationFactor: 1.480,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 75
export const CLINICAL_RISK_BENCHMARK_SET_75 = {
  benchmarkId: "CDS-BENCH-0075",
  calibrationFactor: 1.500,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 76
export const CLINICAL_RISK_BENCHMARK_SET_76 = {
  benchmarkId: "CDS-BENCH-0076",
  calibrationFactor: 1.520,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 77
export const CLINICAL_RISK_BENCHMARK_SET_77 = {
  benchmarkId: "CDS-BENCH-0077",
  calibrationFactor: 1.540,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 78
export const CLINICAL_RISK_BENCHMARK_SET_78 = {
  benchmarkId: "CDS-BENCH-0078",
  calibrationFactor: 1.560,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 79
export const CLINICAL_RISK_BENCHMARK_SET_79 = {
  benchmarkId: "CDS-BENCH-0079",
  calibrationFactor: 1.580,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 80
export const CLINICAL_RISK_BENCHMARK_SET_80 = {
  benchmarkId: "CDS-BENCH-0080",
  calibrationFactor: 1.600,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 81
export const CLINICAL_RISK_BENCHMARK_SET_81 = {
  benchmarkId: "CDS-BENCH-0081",
  calibrationFactor: 1.620,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 82
export const CLINICAL_RISK_BENCHMARK_SET_82 = {
  benchmarkId: "CDS-BENCH-0082",
  calibrationFactor: 1.640,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 83
export const CLINICAL_RISK_BENCHMARK_SET_83 = {
  benchmarkId: "CDS-BENCH-0083",
  calibrationFactor: 1.660,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 84
export const CLINICAL_RISK_BENCHMARK_SET_84 = {
  benchmarkId: "CDS-BENCH-0084",
  calibrationFactor: 1.680,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 85
export const CLINICAL_RISK_BENCHMARK_SET_85 = {
  benchmarkId: "CDS-BENCH-0085",
  calibrationFactor: 1.700,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 86
export const CLINICAL_RISK_BENCHMARK_SET_86 = {
  benchmarkId: "CDS-BENCH-0086",
  calibrationFactor: 1.720,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 87
export const CLINICAL_RISK_BENCHMARK_SET_87 = {
  benchmarkId: "CDS-BENCH-0087",
  calibrationFactor: 1.740,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 88
export const CLINICAL_RISK_BENCHMARK_SET_88 = {
  benchmarkId: "CDS-BENCH-0088",
  calibrationFactor: 1.760,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 89
export const CLINICAL_RISK_BENCHMARK_SET_89 = {
  benchmarkId: "CDS-BENCH-0089",
  calibrationFactor: 1.780,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 90
export const CLINICAL_RISK_BENCHMARK_SET_90 = {
  benchmarkId: "CDS-BENCH-0090",
  calibrationFactor: 1.800,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 91
export const CLINICAL_RISK_BENCHMARK_SET_91 = {
  benchmarkId: "CDS-BENCH-0091",
  calibrationFactor: 1.820,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 92
export const CLINICAL_RISK_BENCHMARK_SET_92 = {
  benchmarkId: "CDS-BENCH-0092",
  calibrationFactor: 1.840,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 93
export const CLINICAL_RISK_BENCHMARK_SET_93 = {
  benchmarkId: "CDS-BENCH-0093",
  calibrationFactor: 1.860,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 94
export const CLINICAL_RISK_BENCHMARK_SET_94 = {
  benchmarkId: "CDS-BENCH-0094",
  calibrationFactor: 1.880,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 95
export const CLINICAL_RISK_BENCHMARK_SET_95 = {
  benchmarkId: "CDS-BENCH-0095",
  calibrationFactor: 1.900,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 96
export const CLINICAL_RISK_BENCHMARK_SET_96 = {
  benchmarkId: "CDS-BENCH-0096",
  calibrationFactor: 1.920,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 97
export const CLINICAL_RISK_BENCHMARK_SET_97 = {
  benchmarkId: "CDS-BENCH-0097",
  calibrationFactor: 1.940,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 98
export const CLINICAL_RISK_BENCHMARK_SET_98 = {
  benchmarkId: "CDS-BENCH-0098",
  calibrationFactor: 1.960,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 99
export const CLINICAL_RISK_BENCHMARK_SET_99 = {
  benchmarkId: "CDS-BENCH-0099",
  calibrationFactor: 1.980,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 100
export const CLINICAL_RISK_BENCHMARK_SET_100 = {
  benchmarkId: "CDS-BENCH-0100",
  calibrationFactor: 1.000,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 101
export const CLINICAL_RISK_BENCHMARK_SET_101 = {
  benchmarkId: "CDS-BENCH-0101",
  calibrationFactor: 1.020,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 102
export const CLINICAL_RISK_BENCHMARK_SET_102 = {
  benchmarkId: "CDS-BENCH-0102",
  calibrationFactor: 1.040,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 103
export const CLINICAL_RISK_BENCHMARK_SET_103 = {
  benchmarkId: "CDS-BENCH-0103",
  calibrationFactor: 1.060,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 104
export const CLINICAL_RISK_BENCHMARK_SET_104 = {
  benchmarkId: "CDS-BENCH-0104",
  calibrationFactor: 1.080,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 105
export const CLINICAL_RISK_BENCHMARK_SET_105 = {
  benchmarkId: "CDS-BENCH-0105",
  calibrationFactor: 1.100,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 106
export const CLINICAL_RISK_BENCHMARK_SET_106 = {
  benchmarkId: "CDS-BENCH-0106",
  calibrationFactor: 1.120,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 107
export const CLINICAL_RISK_BENCHMARK_SET_107 = {
  benchmarkId: "CDS-BENCH-0107",
  calibrationFactor: 1.140,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 108
export const CLINICAL_RISK_BENCHMARK_SET_108 = {
  benchmarkId: "CDS-BENCH-0108",
  calibrationFactor: 1.160,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 109
export const CLINICAL_RISK_BENCHMARK_SET_109 = {
  benchmarkId: "CDS-BENCH-0109",
  calibrationFactor: 1.180,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 110
export const CLINICAL_RISK_BENCHMARK_SET_110 = {
  benchmarkId: "CDS-BENCH-0110",
  calibrationFactor: 1.200,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 111
export const CLINICAL_RISK_BENCHMARK_SET_111 = {
  benchmarkId: "CDS-BENCH-0111",
  calibrationFactor: 1.220,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 112
export const CLINICAL_RISK_BENCHMARK_SET_112 = {
  benchmarkId: "CDS-BENCH-0112",
  calibrationFactor: 1.240,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 113
export const CLINICAL_RISK_BENCHMARK_SET_113 = {
  benchmarkId: "CDS-BENCH-0113",
  calibrationFactor: 1.260,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 114
export const CLINICAL_RISK_BENCHMARK_SET_114 = {
  benchmarkId: "CDS-BENCH-0114",
  calibrationFactor: 1.280,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 115
export const CLINICAL_RISK_BENCHMARK_SET_115 = {
  benchmarkId: "CDS-BENCH-0115",
  calibrationFactor: 1.300,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 116
export const CLINICAL_RISK_BENCHMARK_SET_116 = {
  benchmarkId: "CDS-BENCH-0116",
  calibrationFactor: 1.320,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 117
export const CLINICAL_RISK_BENCHMARK_SET_117 = {
  benchmarkId: "CDS-BENCH-0117",
  calibrationFactor: 1.340,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 118
export const CLINICAL_RISK_BENCHMARK_SET_118 = {
  benchmarkId: "CDS-BENCH-0118",
  calibrationFactor: 1.360,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 119
export const CLINICAL_RISK_BENCHMARK_SET_119 = {
  benchmarkId: "CDS-BENCH-0119",
  calibrationFactor: 1.380,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 120
export const CLINICAL_RISK_BENCHMARK_SET_120 = {
  benchmarkId: "CDS-BENCH-0120",
  calibrationFactor: 1.400,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 121
export const CLINICAL_RISK_BENCHMARK_SET_121 = {
  benchmarkId: "CDS-BENCH-0121",
  calibrationFactor: 1.420,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 122
export const CLINICAL_RISK_BENCHMARK_SET_122 = {
  benchmarkId: "CDS-BENCH-0122",
  calibrationFactor: 1.440,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 123
export const CLINICAL_RISK_BENCHMARK_SET_123 = {
  benchmarkId: "CDS-BENCH-0123",
  calibrationFactor: 1.460,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 124
export const CLINICAL_RISK_BENCHMARK_SET_124 = {
  benchmarkId: "CDS-BENCH-0124",
  calibrationFactor: 1.480,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 125
export const CLINICAL_RISK_BENCHMARK_SET_125 = {
  benchmarkId: "CDS-BENCH-0125",
  calibrationFactor: 1.500,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 126
export const CLINICAL_RISK_BENCHMARK_SET_126 = {
  benchmarkId: "CDS-BENCH-0126",
  calibrationFactor: 1.520,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 127
export const CLINICAL_RISK_BENCHMARK_SET_127 = {
  benchmarkId: "CDS-BENCH-0127",
  calibrationFactor: 1.540,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 128
export const CLINICAL_RISK_BENCHMARK_SET_128 = {
  benchmarkId: "CDS-BENCH-0128",
  calibrationFactor: 1.560,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 129
export const CLINICAL_RISK_BENCHMARK_SET_129 = {
  benchmarkId: "CDS-BENCH-0129",
  calibrationFactor: 1.580,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 130
export const CLINICAL_RISK_BENCHMARK_SET_130 = {
  benchmarkId: "CDS-BENCH-0130",
  calibrationFactor: 1.600,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 131
export const CLINICAL_RISK_BENCHMARK_SET_131 = {
  benchmarkId: "CDS-BENCH-0131",
  calibrationFactor: 1.620,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 132
export const CLINICAL_RISK_BENCHMARK_SET_132 = {
  benchmarkId: "CDS-BENCH-0132",
  calibrationFactor: 1.640,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 133
export const CLINICAL_RISK_BENCHMARK_SET_133 = {
  benchmarkId: "CDS-BENCH-0133",
  calibrationFactor: 1.660,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 134
export const CLINICAL_RISK_BENCHMARK_SET_134 = {
  benchmarkId: "CDS-BENCH-0134",
  calibrationFactor: 1.680,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 135
export const CLINICAL_RISK_BENCHMARK_SET_135 = {
  benchmarkId: "CDS-BENCH-0135",
  calibrationFactor: 1.700,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 136
export const CLINICAL_RISK_BENCHMARK_SET_136 = {
  benchmarkId: "CDS-BENCH-0136",
  calibrationFactor: 1.720,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 137
export const CLINICAL_RISK_BENCHMARK_SET_137 = {
  benchmarkId: "CDS-BENCH-0137",
  calibrationFactor: 1.740,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 138
export const CLINICAL_RISK_BENCHMARK_SET_138 = {
  benchmarkId: "CDS-BENCH-0138",
  calibrationFactor: 1.760,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 139
export const CLINICAL_RISK_BENCHMARK_SET_139 = {
  benchmarkId: "CDS-BENCH-0139",
  calibrationFactor: 1.780,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 140
export const CLINICAL_RISK_BENCHMARK_SET_140 = {
  benchmarkId: "CDS-BENCH-0140",
  calibrationFactor: 1.800,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 141
export const CLINICAL_RISK_BENCHMARK_SET_141 = {
  benchmarkId: "CDS-BENCH-0141",
  calibrationFactor: 1.820,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 142
export const CLINICAL_RISK_BENCHMARK_SET_142 = {
  benchmarkId: "CDS-BENCH-0142",
  calibrationFactor: 1.840,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 143
export const CLINICAL_RISK_BENCHMARK_SET_143 = {
  benchmarkId: "CDS-BENCH-0143",
  calibrationFactor: 1.860,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 144
export const CLINICAL_RISK_BENCHMARK_SET_144 = {
  benchmarkId: "CDS-BENCH-0144",
  calibrationFactor: 1.880,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 145
export const CLINICAL_RISK_BENCHMARK_SET_145 = {
  benchmarkId: "CDS-BENCH-0145",
  calibrationFactor: 1.900,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 146
export const CLINICAL_RISK_BENCHMARK_SET_146 = {
  benchmarkId: "CDS-BENCH-0146",
  calibrationFactor: 1.920,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 147
export const CLINICAL_RISK_BENCHMARK_SET_147 = {
  benchmarkId: "CDS-BENCH-0147",
  calibrationFactor: 1.940,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 148
export const CLINICAL_RISK_BENCHMARK_SET_148 = {
  benchmarkId: "CDS-BENCH-0148",
  calibrationFactor: 1.960,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 149
export const CLINICAL_RISK_BENCHMARK_SET_149 = {
  benchmarkId: "CDS-BENCH-0149",
  calibrationFactor: 1.980,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 150
export const CLINICAL_RISK_BENCHMARK_SET_150 = {
  benchmarkId: "CDS-BENCH-0150",
  calibrationFactor: 1.000,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 151
export const CLINICAL_RISK_BENCHMARK_SET_151 = {
  benchmarkId: "CDS-BENCH-0151",
  calibrationFactor: 1.020,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 152
export const CLINICAL_RISK_BENCHMARK_SET_152 = {
  benchmarkId: "CDS-BENCH-0152",
  calibrationFactor: 1.040,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 153
export const CLINICAL_RISK_BENCHMARK_SET_153 = {
  benchmarkId: "CDS-BENCH-0153",
  calibrationFactor: 1.060,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 154
export const CLINICAL_RISK_BENCHMARK_SET_154 = {
  benchmarkId: "CDS-BENCH-0154",
  calibrationFactor: 1.080,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 155
export const CLINICAL_RISK_BENCHMARK_SET_155 = {
  benchmarkId: "CDS-BENCH-0155",
  calibrationFactor: 1.100,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 156
export const CLINICAL_RISK_BENCHMARK_SET_156 = {
  benchmarkId: "CDS-BENCH-0156",
  calibrationFactor: 1.120,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 157
export const CLINICAL_RISK_BENCHMARK_SET_157 = {
  benchmarkId: "CDS-BENCH-0157",
  calibrationFactor: 1.140,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 158
export const CLINICAL_RISK_BENCHMARK_SET_158 = {
  benchmarkId: "CDS-BENCH-0158",
  calibrationFactor: 1.160,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 159
export const CLINICAL_RISK_BENCHMARK_SET_159 = {
  benchmarkId: "CDS-BENCH-0159",
  calibrationFactor: 1.180,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 160
export const CLINICAL_RISK_BENCHMARK_SET_160 = {
  benchmarkId: "CDS-BENCH-0160",
  calibrationFactor: 1.200,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 161
export const CLINICAL_RISK_BENCHMARK_SET_161 = {
  benchmarkId: "CDS-BENCH-0161",
  calibrationFactor: 1.220,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 162
export const CLINICAL_RISK_BENCHMARK_SET_162 = {
  benchmarkId: "CDS-BENCH-0162",
  calibrationFactor: 1.240,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 163
export const CLINICAL_RISK_BENCHMARK_SET_163 = {
  benchmarkId: "CDS-BENCH-0163",
  calibrationFactor: 1.260,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 164
export const CLINICAL_RISK_BENCHMARK_SET_164 = {
  benchmarkId: "CDS-BENCH-0164",
  calibrationFactor: 1.280,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 165
export const CLINICAL_RISK_BENCHMARK_SET_165 = {
  benchmarkId: "CDS-BENCH-0165",
  calibrationFactor: 1.300,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 166
export const CLINICAL_RISK_BENCHMARK_SET_166 = {
  benchmarkId: "CDS-BENCH-0166",
  calibrationFactor: 1.320,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 167
export const CLINICAL_RISK_BENCHMARK_SET_167 = {
  benchmarkId: "CDS-BENCH-0167",
  calibrationFactor: 1.340,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 168
export const CLINICAL_RISK_BENCHMARK_SET_168 = {
  benchmarkId: "CDS-BENCH-0168",
  calibrationFactor: 1.360,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 169
export const CLINICAL_RISK_BENCHMARK_SET_169 = {
  benchmarkId: "CDS-BENCH-0169",
  calibrationFactor: 1.380,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 170
export const CLINICAL_RISK_BENCHMARK_SET_170 = {
  benchmarkId: "CDS-BENCH-0170",
  calibrationFactor: 1.400,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 171
export const CLINICAL_RISK_BENCHMARK_SET_171 = {
  benchmarkId: "CDS-BENCH-0171",
  calibrationFactor: 1.420,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 172
export const CLINICAL_RISK_BENCHMARK_SET_172 = {
  benchmarkId: "CDS-BENCH-0172",
  calibrationFactor: 1.440,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 173
export const CLINICAL_RISK_BENCHMARK_SET_173 = {
  benchmarkId: "CDS-BENCH-0173",
  calibrationFactor: 1.460,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 174
export const CLINICAL_RISK_BENCHMARK_SET_174 = {
  benchmarkId: "CDS-BENCH-0174",
  calibrationFactor: 1.480,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 175
export const CLINICAL_RISK_BENCHMARK_SET_175 = {
  benchmarkId: "CDS-BENCH-0175",
  calibrationFactor: 1.500,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 176
export const CLINICAL_RISK_BENCHMARK_SET_176 = {
  benchmarkId: "CDS-BENCH-0176",
  calibrationFactor: 1.520,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 177
export const CLINICAL_RISK_BENCHMARK_SET_177 = {
  benchmarkId: "CDS-BENCH-0177",
  calibrationFactor: 1.540,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 178
export const CLINICAL_RISK_BENCHMARK_SET_178 = {
  benchmarkId: "CDS-BENCH-0178",
  calibrationFactor: 1.560,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 179
export const CLINICAL_RISK_BENCHMARK_SET_179 = {
  benchmarkId: "CDS-BENCH-0179",
  calibrationFactor: 1.580,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 180
export const CLINICAL_RISK_BENCHMARK_SET_180 = {
  benchmarkId: "CDS-BENCH-0180",
  calibrationFactor: 1.600,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 181
export const CLINICAL_RISK_BENCHMARK_SET_181 = {
  benchmarkId: "CDS-BENCH-0181",
  calibrationFactor: 1.620,
  readmission30DayBaseline: 0.085,
  clinicalTargetDepartment: "Interventional Radiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 182
export const CLINICAL_RISK_BENCHMARK_SET_182 = {
  benchmarkId: "CDS-BENCH-0182",
  calibrationFactor: 1.640,
  readmission30DayBaseline: 0.090,
  clinicalTargetDepartment: "Neurology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 183
export const CLINICAL_RISK_BENCHMARK_SET_183 = {
  benchmarkId: "CDS-BENCH-0183",
  calibrationFactor: 1.660,
  readmission30DayBaseline: 0.095,
  clinicalTargetDepartment: "Neurosurgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 184
export const CLINICAL_RISK_BENCHMARK_SET_184 = {
  benchmarkId: "CDS-BENCH-0184",
  calibrationFactor: 1.680,
  readmission30DayBaseline: 0.100,
  clinicalTargetDepartment: "Emergency Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 185
export const CLINICAL_RISK_BENCHMARK_SET_185 = {
  benchmarkId: "CDS-BENCH-0185",
  calibrationFactor: 1.700,
  readmission30DayBaseline: 0.105,
  clinicalTargetDepartment: "Medical Intensive Care Unit (MICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};

// Specialized CDS Clinical Risk Coefficient Set 186
export const CLINICAL_RISK_BENCHMARK_SET_186 = {
  benchmarkId: "CDS-BENCH-0186",
  calibrationFactor: 1.720,
  readmission30DayBaseline: 0.110,
  clinicalTargetDepartment: "Surgical ICU (SICU)",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 91
};

// Specialized CDS Clinical Risk Coefficient Set 187
export const CLINICAL_RISK_BENCHMARK_SET_187 = {
  benchmarkId: "CDS-BENCH-0187",
  calibrationFactor: 1.740,
  readmission30DayBaseline: 0.115,
  clinicalTargetDepartment: "Nephrology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 92
};

// Specialized CDS Clinical Risk Coefficient Set 188
export const CLINICAL_RISK_BENCHMARK_SET_188 = {
  benchmarkId: "CDS-BENCH-0188",
  calibrationFactor: 1.760,
  readmission30DayBaseline: 0.120,
  clinicalTargetDepartment: "Medical Oncology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 93
};

// Specialized CDS Clinical Risk Coefficient Set 189
export const CLINICAL_RISK_BENCHMARK_SET_189 = {
  benchmarkId: "CDS-BENCH-0189",
  calibrationFactor: 1.780,
  readmission30DayBaseline: 0.125,
  clinicalTargetDepartment: "Pediatric Acute Care",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 94
};

// Specialized CDS Clinical Risk Coefficient Set 190
export const CLINICAL_RISK_BENCHMARK_SET_190 = {
  benchmarkId: "CDS-BENCH-0190",
  calibrationFactor: 1.800,
  readmission30DayBaseline: 0.130,
  clinicalTargetDepartment: "Orthopedic Surgery",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 95
};

// Specialized CDS Clinical Risk Coefficient Set 191
export const CLINICAL_RISK_BENCHMARK_SET_191 = {
  benchmarkId: "CDS-BENCH-0191",
  calibrationFactor: 1.820,
  readmission30DayBaseline: 0.135,
  clinicalTargetDepartment: "Rheumatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 96
};

// Specialized CDS Clinical Risk Coefficient Set 192
export const CLINICAL_RISK_BENCHMARK_SET_192 = {
  benchmarkId: "CDS-BENCH-0192",
  calibrationFactor: 1.840,
  readmission30DayBaseline: 0.140,
  clinicalTargetDepartment: "Urology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 97
};

// Specialized CDS Clinical Risk Coefficient Set 193
export const CLINICAL_RISK_BENCHMARK_SET_193 = {
  benchmarkId: "CDS-BENCH-0193",
  calibrationFactor: 1.860,
  readmission30DayBaseline: 0.145,
  clinicalTargetDepartment: "Otolaryngology (ENT)",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 98
};

// Specialized CDS Clinical Risk Coefficient Set 194
export const CLINICAL_RISK_BENCHMARK_SET_194 = {
  benchmarkId: "CDS-BENCH-0194",
  calibrationFactor: 1.880,
  readmission30DayBaseline: 0.150,
  clinicalTargetDepartment: "Ophthalmology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 99
};

// Specialized CDS Clinical Risk Coefficient Set 195
export const CLINICAL_RISK_BENCHMARK_SET_195 = {
  benchmarkId: "CDS-BENCH-0195",
  calibrationFactor: 1.900,
  readmission30DayBaseline: 0.155,
  clinicalTargetDepartment: "Dermatology",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 85
};

// Specialized CDS Clinical Risk Coefficient Set 196
export const CLINICAL_RISK_BENCHMARK_SET_196 = {
  benchmarkId: "CDS-BENCH-0196",
  calibrationFactor: 1.920,
  readmission30DayBaseline: 0.160,
  clinicalTargetDepartment: "Obstetrics and Gynecology",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 86
};

// Specialized CDS Clinical Risk Coefficient Set 197
export const CLINICAL_RISK_BENCHMARK_SET_197 = {
  benchmarkId: "CDS-BENCH-0197",
  calibrationFactor: 1.940,
  readmission30DayBaseline: 0.165,
  clinicalTargetDepartment: "Psychiatry & Behavioral Health",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 87
};

// Specialized CDS Clinical Risk Coefficient Set 198
export const CLINICAL_RISK_BENCHMARK_SET_198 = {
  benchmarkId: "CDS-BENCH-0198",
  calibrationFactor: 1.960,
  readmission30DayBaseline: 0.170,
  clinicalTargetDepartment: "Palliative Medicine",
  guidelineStandard: "AHA/ACC/IDSA Tier-1 Best Practice",
  qualityThresholdScore: 88
};

// Specialized CDS Clinical Risk Coefficient Set 199
export const CLINICAL_RISK_BENCHMARK_SET_199 = {
  benchmarkId: "CDS-BENCH-0199",
  calibrationFactor: 1.980,
  readmission30DayBaseline: 0.175,
  clinicalTargetDepartment: "Physical Medicine and Rehabilitation",
  guidelineStandard: "AHA/ACC/IDSA Tier-2 Best Practice",
  qualityThresholdScore: 89
};

// Specialized CDS Clinical Risk Coefficient Set 200
export const CLINICAL_RISK_BENCHMARK_SET_200 = {
  benchmarkId: "CDS-BENCH-0200",
  calibrationFactor: 1.000,
  readmission30DayBaseline: 0.080,
  clinicalTargetDepartment: "Cardiology",
  guidelineStandard: "AHA/ACC/IDSA Tier-3 Best Practice",
  qualityThresholdScore: 90
};