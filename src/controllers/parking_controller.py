from .database_controller import DatabaseController
from models import ParkingLot

class ParkingController:
    def __init__(self, root):
        self.root = root

    def fetch_parking_data(self):
        # Add parking and floor ids
        DatabaseController()
        return [1, 3, 4, 6, 8, 12]
