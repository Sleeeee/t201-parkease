import sqlite3
from .database_controller import DatabaseController

class PremiumCarsController:
    def __init__(self, root):
        self.root = root
        self.premium_cars = []
        self.fetch_premium_cars_data() # Retrieves the premium list on initialization

    def fetch_premium_cars_data(self):
        """
        Retrieves all the existing premium members from the database
        PRE : None
        POST : Insert all the existing premium cars in the instance variable self.premium_cars
        """
        db = DatabaseController()
        for premium_car in db.fetch_all_premium_subscriptions():
            # The db method returns a list of one-item lists
            self.premium_cars.append(premium_car[0])

    def new_premium_car(self, registration_plate: str) -> str:
        """
        Adds a car to the list of premium members
        PRE : None
        POST : Returns a string containing a message describing whether the addition was successful or not
        """
        db = DatabaseController()
        if db.is_premium(registration_plate):
            return f"[Error] {registration_plate} is already registered with premium status"
        else:
            db.add_premium_subscription(registration_plate)
            self.premium_cars.append(registration_plate)
            return f"[NEW PREMIUM]{registration_plate} was succesfully registered with premium status"

    def delete_premium_car(self, registration_plate: str) -> str:
        """
        Removes a car from the list of premium members
        PRE : None
        POST : Returns a string containing a message describing whether the deletion was successful or not
        """
        db = DatabaseController()
        if not db.is_premium(registration_plate):
            return f"[Error] {registration_plate} is not registered as premium "
        else:
            db.delete_premium_subscription(registration_plate)
            self.premium_cars.remove(registration_plate)
            return f"[DELETE PREMIUM] {registration_plate} was succesfully removed from premium list"
