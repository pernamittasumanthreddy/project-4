"""
FHIR R4 CapabilityStatement and Resource Endpoint Registry.
"""
from typing import Dict, List

FHIR_ENDPOINTS: Dict[str, str] = {
    "Patient": "/api/fhir/r4/Patient",
    "Observation": "/api/fhir/r4/Observation",
    "DiagnosticReport": "/api/fhir/r4/DiagnosticReport",
    "ServiceRequest": "/api/fhir/r4/ServiceRequest",
    "ImagingStudy": "/api/fhir/r4/ImagingStudy"
}

def get_fhir_url(resource_name: str) -> str:
    return FHIR_ENDPOINTS.get(resource_name, "/api/fhir/r4")
