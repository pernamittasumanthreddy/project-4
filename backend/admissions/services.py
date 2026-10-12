from typing import List, Dict, Any
from admissions.models import Admission, Bed


class BedManagementService:
    """
    Business service orchestrating hospital bed occupancy, transfers,
    sanitization cycles, and occupancy analytics.
    """

    @classmethod
    def get_ward_occupancy_summary(cls, tenant, branch_id=None) -> List[Dict[str, Any]]:
        """
        Calculates occupancy rates, available, occupied, and cleaning counts per ward.
        """
        from admissions.models import Ward

        wards = Ward.objects.filter(tenant=tenant)
        if branch_id:
            wards = wards.filter(branch_id=branch_id)

        summary = []
        for ward in wards:
            beds = Bed.objects.filter(room__ward=ward, tenant=tenant)
            total = beds.count()
            occupied = beds.filter(status="OCCUPIED").count()
            available = beds.filter(status="AVAILABLE").count()
            cleaning = beds.filter(status="CLEANING").count()
            maintenance = beds.filter(status="MAINTENANCE").count()
            rate = round((occupied / total * 100), 1) if total > 0 else 0.0

            summary.append({
                "ward_id": str(ward.id),
                "ward_name": ward.name,
                "ward_type": ward.ward_type,
                "total_beds": total,
                "available": available,
                "occupied": occupied,
                "cleaning": cleaning,
                "maintenance": maintenance,
                "occupancy_rate_percentage": rate,
            })

        return summary

    @classmethod
    def release_cleaned_bed(cls, bed_id: str, tenant) -> Dict[str, Any]:
        """
        Marks a bed in CLEANING status back to AVAILABLE for admissions.
        """
        bed = Bed.objects.filter(id=bed_id, tenant=tenant).first()
        if not bed:
            raise ValueError("Bed not found.")

        if bed.status != "CLEANING":
            raise ValueError(f"Bed cannot be released from status: {bed.status}. Must be CLEANING.")

        bed.status = "AVAILABLE"
        bed.save()

        return {
            "bed_id": str(bed.id),
            "bed_number": bed.bed_number,
            "status": bed.status,
            "message": "Bed sanitized and released to available inventory.",
        }
