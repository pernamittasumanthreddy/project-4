"""
Automated Unit Tests for Interoperability (HL7 Router, FHIR Builders, DICOM Validator).
"""
import pytest
from interop.hl7_router import HL7MessageRouter
from interop.fhir_builders import FHIRObservationBuilder
from interop.fhir_diagnostic_reports import FHIRDiagnosticReportBuilder
from interop.dicom_validator import DICOMIODValidator

def test_hl7_ack_generation():
    ack = HL7MessageRouter.generate_ack("MSG1001", sending_app="TEST_LIS", ack_code="AA")
    assert "MSH|" in ack
    assert "MSA|AA|MSG1001|" in ack

def test_fhir_observation_builder():
    obs = FHIRObservationBuilder.build_observation(
        obs_id="OBS-1", patient_id="PT-1", loinc_code="2823-3",
        display_name="Potassium", value=4.5, unit="mmol/L", interpretation="N"
    )
    assert obs["resourceType"] == "Observation"
    assert obs["valueQuantity"]["value"] == 4.5
    assert obs["subject"]["reference"] == "Patient/PT-1"

def test_fhir_diagnostic_report_builder():
    rep = FHIRDiagnosticReportBuilder.build_report(
        report_id="REP-1", patient_id="PT-1", encounter_id="ENC-1",
        service_category="LIS", conclusion="Normal CBC", observation_ids=["OBS-1"]
    )
    assert rep["resourceType"] == "DiagnosticReport"
    assert rep["conclusion"] == "Normal CBC"

def test_dicom_validator_mandatory_tags():
    tags = {
        "PatientName": "Doe^John",
        "PatientID": "P123",
        "StudyInstanceUID": "1.2.3.4",
        "SeriesInstanceUID": "1.2.3.5",
        "SOPInstanceUID": "1.2.3.6",
        "Modality": "CT"
    }
    missing = DICOMIODValidator.validate_dataset(tags)
    assert len(missing) == 0

    del tags["PatientID"]
    missing = DICOMIODValidator.validate_dataset(tags)
    assert "PatientID" in missing
