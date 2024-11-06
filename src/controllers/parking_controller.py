from .database_controller import DatabaseController
from models import ParkingLot, Car

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
            
            spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
            registration_plate, status = self.check_spot_status(id)
            spot.linked_car = Car(registration_plate)
            spot.status = status

    def check_spot_status(self, spot_id):
        db = DatabaseController()
        spot_usage = db.fetch_last_spot_usage(spot_id)
        if spot_usage is None:
            return None, "free"
        registration_plate, entry_time, exit_time = spot_usage
        status = "occupied" if exit_time is None else "free"
        return registration_plate, status

    def new_entry(self, floor_number, row_number, spot_number, registration_plate):
        db = DatabaseController()
        spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
        
        try:
            spot.enter(registration_plate)
            db.new_entry_visitor(spot.id, registration_plate)
            return ""
        except AssertionError as e:
            return f"[Error] This spot is already occupied : {e}"

    def new_exit(self, floor_number, row_number, spot_number, registration_plate):
        db = DatabaseController()
        spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
        
        try:
            usage_id, time_spent = db.fetch_last_usage_time(spot.id)
            amount = spot.pay(time_spent)
            db.new_payment(usage_id, registration_plate, amount)
            spot.exit(registration_plate)
            db.new_exit(spot.id, registration_plate)
            return ""
        except AssertionError as e:
            return f"[Error] This spot is unoccupied or the registration plates don't match : {e}"

