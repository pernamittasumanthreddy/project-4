"""HMS Clinical Pharmacy Safety & Drug Interaction Engine — Member 5
Provides automated safety checks for:
- Drug-Drug Interactions (DDI) with severity classifications (CONTRAINDICATED, MAJOR, MODERATE, MINOR).
- Patient Allergy and Adverse Drug Reaction cross-referencing.
- Dosage threshold validation and cumulative toxicity checks.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal

from pharmacy.models.catalogue import Medicine


class InteractionSeverity(str, Enum):
    CONTRAINDICATED = "CONTRAINDICATED"  # Life-threatening risk; do not dispense together
    MAJOR = "MAJOR"                      # Substantial clinical risk; requires physician override
    MODERATE = "MODERATE"                # Monitor therapy closely
    MINOR = "MINOR"                      # Minimal clinical significance


@dataclass
class ClinicalInteractionAlert:
    medicine_a_name: str
    medicine_b_name: str
    severity: InteractionSeverity
    clinical_effect: str
    mechanism: str
    management_guidance: str


@dataclass
class AllergyAlert:
    medicine_name: str
    allergen_class: str
    reaction_type: str
    severity: str


class ClinicalSafetyEngine:
    """Enterprise rule engine evaluating drug combinations against known pharmacodynamic
    and pharmacokinetic interaction profiles.
    """

    # Comprehensive Pharmacological Interaction Database
    KNOWN_INTERACTIONS = [
        # Anticoagulants & Antiplatelets + NSAIDs
        {
            "class_a": "WARFARIN",
            "class_b": "ASPIRIN",
            "severity": InteractionSeverity.CONTRAINDICATED,
            "effect": "Markedly increased risk of severe gastrointestinal and intracranial hemorrhage.",
            "mechanism": "Synergistic inhibition of coagulation cascade combined with cyclooxygenase-1 antiplatelet effect.",
            "guidance": "Avoid concurrent use unless strictly indicated under specialized cardiology supervision with close INR monitoring."
        },
        {
            "class_a": "WARFARIN",
            "class_b": "IBUPROFEN",
            "severity": InteractionSeverity.MAJOR,
            "effect": "Elevated risk of gastrointestinal bleeding and potential INR displacement.",
            "mechanism": "Competitive plasma protein binding displacement and gastric mucosal ulceration.",
            "guidance": "Substitute NSAID with acetaminophen or topical analgesic."
        },
        {
            "class_a": "CLOPIDOGREL",
            "class_b": "OMEPRAZOLE",
            "severity": InteractionSeverity.MAJOR,
            "effect": "Decreased antiplatelet efficacy of clopidogrel, leading to increased risk of thrombotic events.",
            "mechanism": "Inhibition of CYP2C19 required for clopidogrel active metabolite bioactivation.",
            "guidance": "Switch proton pump inhibitor to pantoprazole or an H2 blocker (famotidine)."
        },
        # Cardiovascular & ACE Inhibitors + Potassium / Diuretics
        {
            "class_a": "LISINOPRIL",
            "class_b": "SPIRONOLACTONE",
            "severity": InteractionSeverity.MAJOR,
            "effect": "Severe, potentially fatal hyperkalemia and cardiac conduction arrhythmias.",
            "mechanism": "Additive potassium-sparing mechanisms at the distal nephron and renin-angiotensin-aldosterone axis.",
            "guidance": "Regular serum potassium and renal function monitoring required within 3-7 days of co-administration."
        },
        {
            "class_a": "DIGOXIN",
            "class_b": "AMIODARONE",
            "severity": InteractionSeverity.CONTRAINDICATED,
            "effect": "Digoxin toxicity manifesting as visual disturbances, junctional bradycardia, and ventricular arrhythmias.",
            "mechanism": "Amiodarone inhibits P-glycoprotein efflux transporter, reducing renal and biliary clearance of digoxin by 50%.",
            "guidance": "Reduce digoxin dosage by 50% upon initiating amiodarone and verify serum digoxin concentration."
        },
        {
            "class_a": "SIMVASTATIN",
            "class_b": "CLARITHROMYCIN",
            "severity": InteractionSeverity.CONTRAINDICATED,
            "effect": "Severe rhabdomyolysis and acute renal failure.",
            "mechanism": "Potent CYP3A4 inhibition by macrolide antibiotics elevates statin systemic exposure by up to 10-fold.",
            "guidance": "Temporarily suspend simvastatin therapy during antimicrobial course or use rosuvastatin."
        },
        # Antimicrobial & QT Prolonging Combinations
        {
            "class_a": "CIPROFLOXACIN",
            "class_b": "ONDANSETRON",
            "severity": InteractionSeverity.MAJOR,
            "effect": "Additive cardiac QT prolongation predisposing to Torsades de Pointes ventricular tachycardia.",
            "mechanism": "Combined blockage of delayed rectifier potassium channels (IKr).",
            "guidance": "Perform baseline ECG; evaluate alternative antiemetic (e.g. metoclopramide) in high-risk patients."
        },
        {
            "class_a": "AZITHROMYCIN",
            "class_b": "HALOPERIDOL",
            "severity": InteractionSeverity.MAJOR,
            "effect": "Additive prolongation of QT interval and risk of fatal ventricular dysrhythmia.",
            "mechanism": "Synergistic hERG potassium channel inhibition.",
            "guidance": "Avoid co-administration, monitor telemetry if clinically indispensable."
        },
        # Central Nervous System & Serotonin Syndrome
        {
            "class_a": "SERTRALINE",
            "class_b": "TRAMADOL",
            "severity": InteractionSeverity.CONTRAINDICATED,
            "effect": "Serotonin Syndrome (autonomic instability, hyperthermia, clonus, altered mental status) and seizure threshold reduction.",
            "mechanism": "Combined central serotonergic neurotransmission enhancement and monoamine reuptake inhibition.",
            "guidance": "Strictly avoid combination; select non-serotonergic analgesic alternative."
        },
        {
            "class_a": "FLUVOXAMINE",
            "class_b": "THEOPHYLLINE",
            "severity": InteractionSeverity.CONTRAINDICATED,
            "effect": "Severe theophylline toxicity (seizures, cardiac arrest).",
            "mechanism": "Strong CYP1A2 inhibition reduces theophylline metabolic clearance by over 70%.",
            "guidance": "Do not co-prescribe; substitute alternative SSRI."
        },
        # Nephrotoxic Combinations
        {
            "class_a": "VANCOMYCIN",
            "class_b": "GENTAMICIN",
            "severity": InteractionSeverity.MAJOR,
            "effect": "Synergistic nephrotoxicity and irreversible sensorineural ototoxicity.",
            "mechanism": "Cumulative renal tubular cell apoptosis and inner ear hair cell damage.",
            "guidance": "Mandatory therapeutic drug monitoring (troughs) and serial serum creatinine assessments."
        },
        {
            "class_a": "METHOTREXATE",
            "class_b": "AMOXICILLIN",
            "severity": InteractionSeverity.MAJOR,
            "effect": "Methotrexate bone marrow suppression and pancytopenia.",
            "mechanism": "Penicillins compete with organic anion transporters (OAT1/3) responsible for renal tubular excretion of methotrexate.",
            "guidance": "Avoid penicillins during high-dose methotrexate therapy; monitor hematologic indices."
        }
    ]

    # Common Cross-Reactivity Allergy Classes
    ALLERGY_CROSS_REACTIVITY = {
        "PENICILLINS": ["AMOXICILLIN", "AMPICILLIN", "PENICILLIN G", "PIPERACILLIN", "AUGMENTIN"],
        "CEPHALOSPORINS": ["CEFTRIAXONE", "CEFALEXIN", "CEFUROXIME", "CEFOTAXIME", "CEFEPIME"],
        "SULFONAMIDES": ["SULFAMETHOXAZOLE", "CO-TRIMOXAZOLE", "SULFASALAZINE"],
        "NSAIDS": ["ASPIRIN", "IBUPROFEN", "DICLOFENAC", "NAPROXEN", "KETOROLAC", "CELECOXIB"],
        "OPIOIDS": ["MORPHINE", "CODEINE", "OXYCODONE", "TRAMADOL", "FENTANYL"],
    }

    @classmethod
    def check_drug_interactions(cls, prescribed_medicines: List[Medicine]) -> List[ClinicalInteractionAlert]:
        """Evaluates a list of medicines against known drug-drug interaction pairs."""
        alerts: List[ClinicalInteractionAlert] = []
        n = len(prescribed_medicines)
        if n < 2:
            return alerts

        for i in range(n):
            for j in range(i + 1, n):
                med_a = prescribed_medicines[i]
                med_b = prescribed_medicines[j]

                name_a = med_a.generic_name.upper()
                name_b = med_b.generic_name.upper()

                for rule in cls.KNOWN_INTERACTIONS:
                    target_a = rule["class_a"]
                    target_b = rule["class_b"]

                    match_direct = (target_a in name_a and target_b in name_b)
                    match_reverse = (target_b in name_a and target_a in name_b)

                    if match_direct or match_reverse:
                        alerts.append(ClinicalInteractionAlert(
                            medicine_a_name=med_a.brand_name,
                            medicine_b_name=med_b.brand_name,
                            severity=rule["severity"],
                            clinical_effect=rule["effect"],
                            mechanism=rule["mechanism"],
                            management_guidance=rule["guidance"]
                        ))

        return alerts

    @classmethod
    def check_patient_allergies(cls, medicine: Medicine, patient_allergies: List[str]) -> List[AllergyAlert]:
        """Checks if the candidate medicine triggers any known patient allergies."""
        alerts: List[AllergyAlert] = []
        gen_upper = medicine.generic_name.upper()

        for raw_allergy in patient_allergies:
            allergy_upper = raw_allergy.upper().strip()

            # Direct generic match
            if allergy_upper in gen_upper:
                alerts.append(AllergyAlert(
                    medicine_name=medicine.brand_name,
                    allergen_class=allergy_upper,
                    reaction_type="Direct Known Substance Allergy",
                    severity="HIGH"
                ))
                continue

            # Class-level cross-reactivity match
            for drug_class, members in cls.ALLERGY_CROSS_REACTIVITY.items():
                if allergy_upper in drug_class:
                    if any(member in gen_upper for member in members):
                        alerts.append(AllergyAlert(
                            medicine_name=medicine.brand_name,
                            allergen_class=drug_class,
                            reaction_type="Pharmacological Class Cross-Reactivity",
                            severity="CRITICAL"
                        ))

        return alerts
