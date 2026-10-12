class BedPolicyService:
    @staticmethod
    def evaluate_reservation_timeout(reservation_hours, elapsed_hours):
        return elapsed_hours > reservation_hours
