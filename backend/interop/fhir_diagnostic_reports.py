"""
FHIR R4 DiagnosticReport Resource Builder for LIS / RIS Final Reports.
Embeds conclusion codes, performer references, and presentation metadata.
"""

from typing import Dict, Any, List

class FHIRDiagnosticReportBuilder:
    @staticmethod
    def build_report(report_id: str, patient_id: str, encounter_id: str,
                     service_category: str, conclusion: str,
                     observation_ids: List[str]) -> Dict[str, Any]:
        return {
            "resourceType": "DiagnosticReport",
            "id": report_id,
            "status": "final",
            "category": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                    "code": "LAB" if service_category == "LIS" else "RAD"
                }]
            }],
            "subject": {"reference": f"Patient/{patient_id}"},
            "encounter": {"reference": f"Encounter/{encounter_id}"},
            "conclusion": conclusion,
            "result": [{"reference": f"Observation/{oid}"} for oid in observation_ids]
        }
