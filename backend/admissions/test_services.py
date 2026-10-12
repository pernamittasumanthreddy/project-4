import pytest
from core.models import Tenant, HospitalBranch
from admissions.models import Ward, Room, Bed
from admissions.services import BedManagementService


@pytest.mark.django_db
def test_bed_occupancy_summary_and_cleaning_release():
    tenant = Tenant.objects.create(name="St. Mary's Hospital", slug="st-marys")
    branch = HospitalBranch.objects.create(tenant=tenant, name="North Wing", code="NW")

    ward = Ward.objects.create(tenant=tenant, branch=branch, name="Surgical Ward", ward_type="GENERAL")
    room = Room.objects.create(tenant=tenant, ward=ward, room_number="201")
    bed1 = Bed.objects.create(tenant=tenant, room=room, bed_number="S-1", status="AVAILABLE")
    bed2 = Bed.objects.create(tenant=tenant, room=room, bed_number="S-2", status="OCCUPIED")
    bed3 = Bed.objects.create(tenant=tenant, room=room, bed_number="S-3", status="CLEANING")

    summary = BedManagementService.get_ward_occupancy_summary(tenant)
    assert len(summary) == 1
    assert summary[0]["total_beds"] == 3
    assert summary[0]["available"] == 1
    assert summary[0]["occupied"] == 1
    assert summary[0]["cleaning"] == 1
    assert summary[0]["occupancy_rate_percentage"] == 33.3

    # Release cleaned bed
    res = BedManagementService.release_cleaned_bed(str(bed3.id), tenant)
    assert res["status"] == "AVAILABLE"
    bed3.refresh_from_db()
    assert bed3.status == "AVAILABLE"

