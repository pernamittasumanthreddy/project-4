from appointments.roster_service import DoctorRosterService

def test_shift_intervals():
    valid = DoctorRosterService.validate_shift_intervals("09:00", "13:00", 30)
    assert valid is True
