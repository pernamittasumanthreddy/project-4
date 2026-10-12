class DoctorRosterService:
    @staticmethod
    def validate_shift_intervals(start_time, end_time, buffer_mins):
        import datetime
        fmt = "%H:%M"
        t1 = datetime.datetime.strptime(start_time, fmt)
        t2 = datetime.datetime.strptime(end_time, fmt)
        total_mins = (t2 - t1).total_seconds() / 60
        return total_mins > buffer_mins
