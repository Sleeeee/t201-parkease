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
        return parking_lot

