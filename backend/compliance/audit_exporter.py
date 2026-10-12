"""
HIPAA Security Rule §164.312(b) Audit Controls Exporter.
"""
from typing import List, Dict
import io
import csv

class HIPAAAuditExporter:
    @staticmethod
    def export_csv(logs: List[Dict[str, str]]) -> str:
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=["timestamp", "user_id", "patient_uhid", "action", "ip_address"])
        writer.writeheader()
        for log in logs:
            writer.writerow(log)
        return out.getvalue()
