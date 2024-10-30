from .database_controller import DatabaseController
from models import ParkingLot

class ParkingController:
    def __init__(self, root):
        self.root = root
        self.parking_lot = None
        self.fetch_parking_data()

    def fetch_parking_data(self):
        parking_lot = ParkingLot(1)
        db = DatabaseController()
        for spot in db.fetch_all_parking_spots():
            parking_lot.add_spot({"id": spot[0], "spot_number": spot[1], "row_number": spot[2], "floor_number": spot[3]})
            # TODO : verify status and update it (maybe need to modify add_spot() or update it manually)
        return parking_lot

    def check_spot_status(self, spot_id):
        # TODO : call to db to check if last usage entry/exit_time is NULL
        pass

    def new_entry(self, floor_number, row_number, spot_number, registration_plate):
        # TODO : retrieve the spot's id using parking_lot, use db.use new_entry_visitor() then update the the spot's internal status using ParkingSpot's method
        pass

    def new_exit(self, floor_number, row_number, spot_number, registration_plate):
        # TODO : check if spot and plate match then same as new_entry
        pass
