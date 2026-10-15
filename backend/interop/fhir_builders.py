"""
FHIR R4 Observation Resource Builder for Laboratory Test Results.
Constructs valid FHIR JSON payloads with LOINC coding, valueQuantity, and interpretation flags.
"""

from typing import Dict, Any, Optional

class FHIRObservationBuilder:
    @staticmethod
    def build_observation(obs_id: str, patient_id: str, loinc_code: str,
                          display_name: str, value: float, unit: str,
                          interpretation: str = "N") -> Dict[str, Any]:
        return {
            "resourceType": "Observation",
            "id": obs_id,
            "status": "final",
            "category": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "laboratory",
                    "display": "Laboratory"
                }]
            }],
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": loinc_code,
                    "display": display_name
                }]
            },
            "subject": {"reference": f"Patient/{patient_id}"},
            "valueQuantity": {
                "value": value,
                "unit": unit,
                "system": "http://unitsofmeasure.org",
                "code": unit
            },
            "interpretation": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                    "code": interpretation
                }]
            }]
        }
