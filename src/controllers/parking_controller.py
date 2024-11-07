from .database_controller import DatabaseController
from models import ParkingLot

class ParkingController:
    def __init__(self, root):
        self.root = root
        self.parking_lot = self.fetch_parking_data()
        self.db = DatabaseController()

    def fetch_parking_data(self):
        parking_lot = ParkingLot(1)
        for spot in self.db.fetch_all_parking_spots():
            parking_lot.add_spot({
                "id": spot[0], 
                "spot_number": spot[1], 
                "row_number": spot[2], 
                "floor_number": spot[3]
            })
        return parking_lot

    def check_spot_status(self, spot_id):
        usage = self.db.fetch_last_spot_usage(spot_id) #todo
        if usage and usage[2] is None:  # exit_time is None means spot is occupied
            return "occupied"
        return "free"

    def new_entry(self, spot_id, registration_plate):
        self.db.new_entry_visitor(spot_id, registration_plate)
        # todo : update internal status 
        # Example: update the ParkingSpot status in the parking lot

    def new_exit(self, spot_id, registration_plate):
        current_usage = self.db.fetch_last_spot_usage(spot_id)
        if current_usage and current_usage[0] == registration_plate:
            self.db.new_exit(spot_id, registration_plate)
            # Update internal status 
        else:
            print("Error: Spot and plate do not match or spot is already free.")

    def get_available_spots(self):
        available_spots = []
        for spot in self.db.fetch_all_parking_spots():
            if self.check_spot_status(spot[0]) == "free":
                available_spots.append(spot)
        return available_spots

    def reserve_spot(self, spot_id, registration_plate):
        self.db.new_booking(spot_id, registration_plate)
        # Mark as reserved in the internal structure 

    def cancel_reservation(self, spot_id, registration_plate):
        # Assuming a method to remove reservation exists in DatabaseController
        self.db.cancel_booking(spot_id, registration_plate)

    def calculate_fee(self, spot_id):
        usage = self.db.fetch_last_spot_usage(spot_id)
        if usage and usage[2] is not None:  # If exit_time is not None, calculate fee
            entry_time, exit_time = usage[1], usage[2]
            duration = (exit_time - entry_time).total_seconds() / 3600  # Duration in hours
            fee = duration * 5  # Assuming a rate of 5€ per hour
            return round(fee, 2)
        return 0.0

    def confirm_payment(self, spot_id, registration_plate, amount):
        usage = self.db.fetch_last_spot_usage(spot_id)
        if usage:
            usage_id = usage[0]
            self.db.new_payment(usage_id, registration_plate, amount)

    def get_parked_vehicles(self):
        parked_vehicles = []
        for spot in self.db.fetch_all_parking_spots():
            if self.check_spot_status(spot[0]) == "occupied":
                usage = self.db.fetch_last_spot_usage(spot[0])
                if usage:
                    parked_vehicles.append((spot[1], usage[0]))  # Spot number and plate
        return parked_vehicles

    def update_parking_spot_status(self):
        for spot in self.db.fetch_all_parking_spots():
            spot_id = spot[0]
            status = self.check_spot_status(spot_id)
            # Update internal representation or display based on status
