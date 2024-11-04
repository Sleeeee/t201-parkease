import os
import sqlite3

class DatabaseController:
    def __init__(self):
        self.directory = os.path.join(os.path.expanduser("~/.parkease"))
        self.path = os.path.join(self.directory, "parking_lot.db")

    def init_database(self):
        """Initializes all the relations needed to manage the parking lot
           ParkingSpots : Stores all existing spots with an id and their physical position
           ParkingUsage : History of every entry/exit. If someone is occupying the spot, entry_time is the corresponding TIMESTAMP, and exit_time is NULL
           Payments : Links payments data to the corresponding ParkingUsage"""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE ParkingSpots (
                              id INTEGER PRIMARY KEY,
                              spot_number INTEGER NOT NULL,
                              row_number INTEGER NOT NULL,
                              floor_number INTEGER NOT NULL)""")
            cursor.execute("""CREATE TABLE ParkingUsage (
                              id INTEGER PRIMARY KEY,
                              spot_id INTEGER NOT NULL,
                              registration_plate VARCHAR(10) NOT NULL,
                              entry_time TIMESTAMP,
                              exit_time TIMESTAMP,
                              FOREIGN KEY(spot_id) REFERENCES ParkingSpots(id)
                              )""")
            cursor.execute("""CREATE TABLE Payments (
                              usage_id INTEGER PRIMARY KEY,
                              registration_plate VARCHAR(10) NOT NULL,
                              amount DECIMAL(5, 2) NOT NULL,
                              FOREIGN KEY(usage_id) REFERENCES ParkingUsage(id)
                              )""")
            conn.commit()

    def fetch_all_parking_spots(self):
        """Retrieves every existing spot
           Returns : A list of lists (each spot is a 4 items long list)"""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id, spot_number, row_number, floor_number
                              FROM ParkingSpots""")
            return cursor.fetchall()

    def fetch_last_spot_usage(self, spot_id):
        """Retrieves information concerning the current spot's usage
           Returns : A list containing the registration plate, and the timestamps of last entry time. If exit_time is NULL, the spot is occupied, if not, it is free"""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT registration_plate, entry_time, exit_time
                              FROM ParkingUsage
                              WHERE spot_id = ?
                              ORDER BY entry_time DESC NULLS FIRST""", (spot_id,))
            return cursor.fetchone()

    def create_parking_spot(self, floor_number, row_number, spot_number):
        """Adds a new entry to the ParkingSpots table"""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO ParkingSpots (floor_number, row_number, spot_number)
                              VALUES (?, ?, ?)""", (floor_number, row_number, spot_number))
            conn.commit()

    def new_entry_visitor(self, spot_id, registration_plate):
        """Adds a new entry to the ParkingUsage table. The entry time is set to the current timestamp"""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO ParkingUsage (spot_id, registration_plate, entry_time)
                              VALUES (?, ?, current_timestamp)""", (spot_id, registration_plate))
            conn.commit()

    def new_entry_booking(self, spot_id, registration_plate):
        """Updates entry_time to a spot that was previously booked by the same client. entry_time is set to current_timestamp"""
        # WARNING : Not needed for MVP
        pass

    def new_exit(self, spot_id, registration_plate):
        """Updates exit_time (set to current_timestamp) to the corresponding spot."""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE ParkingUsage
                              SET exit_time = current_timestamp
                              WHERE spot_id = ? AND registration_plate = ? AND exit_time IS NULL""", (spot_id, registration_plate))
            conn.commit()

    def new_booking(self, spot_id, registration_plate):
        """Creates a new entry to the ParkingUsage. entry_time and exit_time are set to NULL"""
        # WARNING : Not needed for MVP
        pass

    def fetch_all_payments(self):
        """Retrieves all rows in the Payments table
           Returns : A list of list (each payment is a 3 items long list"""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT usage_id, registration_plate, amount
                              FROM Payments""")
            return cursor.fetchall()

    def new_payment(self, usage_id, registration_plate, amount):
        """Creates a new entry to the Payments table"""

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO Payments
                              VALUES (?, ?, ?)""", (usage_id, registration_plate, amount))
            conn.commit()
