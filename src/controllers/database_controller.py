import os
import sqlite3

class DatabaseController:
    def __init__(self):
        self.directory = os.path.join(os.path.expanduser("~/.parkease"))
        self.path = os.path.join(self.directory, "parking_lot.db")

    def init_database(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE ParkingSpots (
                              id INTEGER PRIMARY KEY,
                              spot_number INTEGER NOT NULL,
                              row_number INTEGER NOT NULL,
                              floor_number INTEGER NOT NULL)""")
