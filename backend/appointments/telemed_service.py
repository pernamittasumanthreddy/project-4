import uuid

class TelemedicineSlotAllocator:
    @staticmethod
    def allocate_secure_room(appointment):
        room_token = str(uuid.uuid4())
        appointment.telemedicine_room_id = room_token
        appointment.save()
        return {"room_token": room_token, "join_url": f"/teleconsult/{room_token}"}
