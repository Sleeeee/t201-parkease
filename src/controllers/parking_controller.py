from .database_controller import DatabaseController
from models import ParkingLot, Car

class ParkingController:
    def __init__(self, root):
        self.root = root
        self.parking_lot = None
        self.fetch_parking_data() # Updates self.parking_lot with the existing spots

    def fetch_parking_data(self):
        """Retrieves all the spots stored in the database and orders them inside self.parking_lot
           Updates self.parking_lot as a ParkingLot object containing all the spots ordered by floor, row, and number"""
        db = DatabaseController()
        self.parking_lot = ParkingLot(1) # Empty ParkingLot of id 1
        for id, spot_number, row_number, floor_number in db.fetch_all_parking_spots():
            # For every spot found in the database, create the a ParkingSpot object inside its row and floor
            self.parking_lot.add_spot({"id": id, "spot_number": spot_number, "row_number": row_number, "floor_number": floor_number})
            
            spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number] # Fetches the spot from self.parking_lot
            registration_plate, status = self.check_spot_status(id) # Verifies if a car is occupying the spot
            if registration_plate:
                spot.linked_car = Car(registration_plate) # Sets the occupant only if it exists
            spot.status = status

    def check_spot_status(self, spot_id: int):
        """Queries the database to verify the current status of the spot
           Returns the status : free / occupied and the registration plate of the last (or current) user"""
        db = DatabaseController()
        spot_usage = db.fetch_last_spot_usage(spot_id) # Retrieves the last time the spot was used. None if no record was found
        if spot_usage is None:
            return None, "free" # Spot is free if it was never used
        registration_plate, entry_time, exit_time = spot_usage
        status = "occupied" if exit_time is None else "free" # If someone entered but never left, it means the spot is occupied. If the last user left, it means the spot is free
        return registration_plate, status

    def create_new_spot(self, floor_number: int, row_number: int, spot_number: int):
        db = DatabaseController()
        try:
            self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
            return "[Error] This spot already exists"
        except KeyError:
            db.create_parking_spot(floor_number, row_number, spot_number)
            return ""

    def new_entry(self, floor_number: int, row_number: int, spot_number: int, registration_plate: str):
        """A user enters the specified spot
           Updates the spot within self.parking_lot : spot.status = "occupied", spot.linked_car = registration_plate
           Returns an empty string is everything worked, or a string containing the error if something failed"""
        db = DatabaseController()
        try:
            spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
            spot.enter(registration_plate) # Uses ParkingSpot's method to update linked_car and status IF POSSIBLE
            db.new_entry_visitor(spot.id, registration_plate) # Creates an entry inside the database
            return ""
        except AssertionError as e:
            # Error raised by spot.enter()
            return f"[Error] This spot is already occupied : {e}"
        except KeyError as e:
            # Error raised by trying to access a spot that isn't contained inside self.parking_lot
            return f"[Error] This spot does not exit : {e}"

    def new_exit(self, floor_number: int, row_number: int, spot_number: int, registration_plate: str):
        """A user exits the specified spot
           Updates the spot within self.parking_lot : spot.status = "free", spot.linked_car = None
           Returns an empty string is everything worked, or a string containing the error if something failed"""
        db = DatabaseController()
        try:
            spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
            usage_id, time_spent = db.fetch_last_usage_time(spot.id) # Fetches the entry's id and calculates the time spent occupying the spot
            amount = spot.pay(registration_plate, time_spent) # Calculates the amount to be paid based on the car's HOURLY_RATE
            db.new_payment(usage_id, registration_plate, amount) # Stores the payment inside the database
            spot.exit(registration_plate) # Uses ParkingSpot's method to update linked_car and status IF POSSIBLE
            db.new_exit(spot.id, registration_plate) # Sets the exit time in the database
            return ""
        except (AssertionError, TypeError) as e:
            #Error raised by spot.exit()
            return f"[Error] This spot is unoccupied or the registration plates don't match : {e}"
        except KeyError as e:
            # Error raised by trying to access a spot that isn't contained inside self.parking_lot
            return f"[Error] This spot does not exist : {e}"

