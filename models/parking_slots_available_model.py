# app/models/parking_slots_available_model.py

class ParkingSlotAvailableModel:
    def __init__(self, parking_slot_id, slot_status, available_for_use):
        self.parking_slot_id = parking_slot_id
        self.slot_status = slot_status
        self.available_for_use = available_for_use
        
