"""Unit tests for HIPAA audit exporter."""
import pytest
from compliance.audit_exporter import HIPAAAuditExporter

def test_audit_export():
    sample = [{"timestamp": "2026-10-12T10:00:00Z", "user_id": "DR1", "patient_uhid": "UHID-1", "action": "VIEW", "ip_address": "127.0.0.1"}]
    csv_str = HIPAAAuditExporter.export_csv(sample)
    assert "timestamp,user_id,patient_uhid,action,ip_address" in csv_str
    assert "UHID-1" in csv_str
