class SlotAssignmentModel:
    def __init__(self, slot_id, time_occupied_data):
        self.slot_id = slot_id
        self.time_occupied_data = time_occupied_data

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "time_occupied_data": self.time_occupied_data
        }
