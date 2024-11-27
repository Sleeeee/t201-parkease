import sqlite3
from .database_controller import DatabaseController

class PremiumCarsController:
    def __init__(self, root):
        self.root = root

    def fetch_premium_cars_data(self):
        db = DatabaseController()
        #TODO : fetch data from database
        return ["Hank is subscribed", "Darius is subscribed", "Marilyn is subscribed"]

    def new_premium_car(self, registration_plate: str) -> str:
        """
        Adds a car to the list of premium members
        PRE : None
        POST : Returns a string containing an message describing whether the addition was successful or not
        """
        # TODO : check if the registration_plate matches an existing premium subscription and add it to the table if not
        db = DatabaseController()

    def delete_premium_car(self, registration_plate: str) -> str:
        """
        Removes a car from the list of premium members
        PRE : None
        POST : Returns a string containing an message describing whether the deletion was successful or not
        """
        # TODO : check if the registration_plate matches an existing premium subscription and remove it from the table if so
        db = DatabaseController()
