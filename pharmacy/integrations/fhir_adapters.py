"""HMS FHIR R4 (Fast Healthcare Interoperability Resources) Adapter — Member 5
Provides bidirectional serialization and conversion between HMS Pharmacy models
and standard HL7 FHIR Release 4 JSON specifications:
- FHIR Medication (http://hl7.org/fhir/R4/medication.html)
- FHIR MedicationRequest (http://hl7.org/fhir/R4/medicationrequest.html)
- FHIR MedicationDispense (http://hl7.org/fhir/R4/medicationdispense.html)
- FHIR Bundle (http://hl7.org/fhir/R4/bundle.html)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch
from pharmacy.models.dispensing import DispenseRecord, DispensedItem
from clinical.models import Prescription, PrescriptionItem


class FHIRAdapter:
    """Enterprise healthcare interoperability gateway for HL7 FHIR Release 4."""

    FHIR_SYSTEM_RXNORM = "http://www.nlm.nih.gov/research/umls/rxnorm"
    FHIR_SYSTEM_ATC = "http://www.whocc.no/atc"
    FHIR_SYSTEM_SNOMED = "http://snomed.info/sct"
    FHIR_SYSTEM_HOSPITAL_SKU = "https://hospital.org/pharmacy/medicines"

    @classmethod
    def to_fhir_medication(cls, medicine: Medicine) -> Dict[str, Any]:
        """Converts an internal Medicine entity into a FHIR R4 Medication resource."""
        return {
            "resourceType": "Medication",
            "id": str(medicine.id),
            "meta": {
                "versionId": "1",
                "lastUpdated": medicine.updated_at.isoformat() if hasattr(medicine, 'updated_at') else datetime.now(timezone.utc).isoformat()
            },
            "code": {
                "coding": [
                    {
                        "system": cls.FHIR_SYSTEM_HOSPITAL_SKU,
                        "code": medicine.code,
                        "display": medicine.brand_name
                    },
                    {
                        "system": cls.FHIR_SYSTEM_ATC,
                        "code": medicine.classification,
                        "display": medicine.get_classification_display()
                    }
                ],
                "text": f"{medicine.brand_name} ({medicine.generic_name}) {medicine.strength}"
            },
            "status": "active" if medicine.is_active else "inactive",
            "form": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm",
                        "code": medicine.dosage_form,
                        "display": medicine.get_dosage_form_display()
                    }
                ],
                "text": medicine.get_dosage_form_display()
            },
            "amount": {
                "numerator": {
                    "value": 1,
                    "unit": medicine.dispensing_unit
                },
                "denominator": {
                    "value": 1,
                    "unit": medicine.unit_of_measure
                }
            }
        }

    @classmethod
    def to_fhir_medication_request(cls, prescription: Prescription) -> Dict[str, Any]:
        """Converts a clinical Prescription entity into a FHIR R4 MedicationRequest resource."""
        items_fhir = []
        for item in prescription.items.all():
            dosage_val = getattr(item, 'dosage', '') or getattr(item, 'dose', '1 unit')
            duration_val = f"{item.duration_days} days" if hasattr(item, 'duration_days') else 'as directed'
            items_fhir.append({
                "sequence": 1,
                "text": f"Take {dosage_val} {item.frequency or 'daily'} for {duration_val}",
                "additionalInstruction": [
                    {"text": item.instructions or "Take with food"}
                ],

                "timing": {
                    "code": {
                        "text": item.frequency or "daily"
                    }
                },
                "doseAndRate": [
                    {
                        "doseQuantity": {
                            "value": float(item.quantity_prescribed),
                            "unit": "doses"
                        }
                    }
                ]
            })

        return {
            "resourceType": "MedicationRequest",
            "id": str(prescription.id),
            "identifier": [
                {
                    "use": "official",
                    "system": "https://hospital.org/prescriptions",
                    "value": prescription.prescription_number
                }
            ],
            "status": "active" if prescription.status == "PENDING" else "completed",
            "intent": "order",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
                            "code": "inpatient",
                            "display": "Inpatient Pharmacy"
                        }
                    ]
                }
            ],
            "subject": {
                "reference": f"Patient/{prescription.patient.id}",
                "display": prescription.patient.full_name
            },
            "authoredOn": prescription.created_at.isoformat(),
            "requester": {
                "reference": f"Practitioner/{prescription.prescriber.id}",
                "display": prescription.prescriber.get_full_name() or prescription.prescriber.username
            },
            "dosageInstruction": items_fhir
        }

    @classmethod
    def to_fhir_medication_dispense(cls, dispense_record: DispenseRecord) -> Dict[str, Any]:
        """Converts an authorized DispenseRecord into a FHIR R4 MedicationDispense resource."""
        dispensed_items_fhir = []
        for item in dispense_record.items.all():
            batch = item.batch
            dispensed_items_fhir.append({
                "itemCodeableConcept": {
                    "text": item.prescription_item.medicine_name
                },
                "quantity": {
                    "value": float(item.quantity_dispensed),
                    "unit": "dispensing units"
                },
                "unitPrice": {
                    "value": float(item.unit_selling_price),
                    "currency": "USD"
                },
                "lotNumber": batch.batch_number,
                "expirationDate": batch.expiry_date.strftime("%Y-%m-%d")
            })

        return {
            "resourceType": "MedicationDispense",
            "id": str(dispense_record.id),
            "identifier": [
                {
                    "use": "official",
                    "system": "https://hospital.org/pharmacy/dispensations",
                    "value": dispense_record.dispense_number
                }
            ],
            "status": "completed",
            "authorizingPrescription": [
                {
                    "reference": f"MedicationRequest/{dispense_record.prescription.id}",
                    "display": dispense_record.prescription.prescription_number
                }
            ],
            "subject": {
                "reference": f"Patient/{dispense_record.prescription.patient.id}",
                "display": dispense_record.prescription.patient.full_name
            },
            "performer": [
                {
                    "actor": {
                        "reference": f"Practitioner/{dispense_record.pharmacist.id}",
                        "display": dispense_record.pharmacist.get_full_name() or dispense_record.pharmacist.username
                    }
                }
            ],
            "whenHandedOver": dispense_record.created_at.isoformat(),
            "dosageInstruction": [
                {
                    "text": "Administer strictly as instructed by prescribing physician."
                }
            ],
            "contained": dispensed_items_fhir
        }

    @classmethod
    def to_fhir_bundle(cls, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bundles multiple FHIR resources into a compliant FHIR R4 Bundle container."""
        return {
            "resourceType": "Bundle",
            "id": str(uuid.uuid4()),
            "type": "collection",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total": len(resources),
            "entry": [
                {
                    "fullUrl": f"urn:uuid:{r.get('id', uuid.uuid4())}",
                    "resource": r
                }
                for r in resources
            ]
        }
