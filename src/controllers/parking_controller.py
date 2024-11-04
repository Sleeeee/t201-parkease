from .database_controller import DatabaseController
from models import ParkingLot

class ParkingController:
    def __init__(self, root):
        self.root = root
        self.parking_lot = None
        self.fetch_parking_data()

    def fetch_parking_data(self):
        db = DatabaseController()
        self.parking_lot = ParkingLot(1)
        for spot in db.fetch_all_parking_spots():
            id, spot_number, row_number, floor_number = spot[0], spot[1], spot[2], spot[3]
            self.parking_lot.add_spot({"id": id, "spot_number": spot_number, "row_number": row_number, "floor_number": floor_number})
            self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number].status = self.check_spot_status(id)

    def check_spot_status(self, spot_id):
        db = DatabaseController()
        spot_usage = db.fetch_last_spot_usage(spot_id)
        if spot_usage is None:
            return "free"
        id, entry_time, exit_time = spot_usage
        return "occupied" if exit_time is None else "free"

    def new_entry(self, floor_number, row_number, spot_number, registration_plate):
        # TODO : retrieve the spot's id using parking_lot, use db.use new_entry_visitor() then update the the spot's internal status using ParkingSpot's method
        pass

    def new_exit(self, floor_number, row_number, spot_number, registration_plate):
        # TODO : check if spot and plate match then same as new_entry
        pass
