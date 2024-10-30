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
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT id, spot_number, row_number, floor_number
                              FROM ParkingSpots""")
            return cursor.fetchall()

    def fetch_last_spot_usage(self, spot_id):
        # TODO : retrieve entry/exit times to verify status
        pass

    def create_parking_spot(self, floor_number, row_number, spot_number):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO ParkingSpots (floor_number, row_number, spot_number)
                              VALUES (?, ?, ?)""", (floor_number, row_number, spot_number))
            conn.commit()

    def new_entry_visitor(self, spot_id, registration_plate):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO ParkingUsage (spot_id, registration_plate, entry_time)
                              VALUES (?, ?, current_timestamp)""", (spot_id, registration_plate))
            conn.commit()

    def new_entry_booking(self, spot_id, registration_plate):
        # WARNING : Not needed for MVP
        pass

    def new_exit(self, spot_id, registration_plate):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE ParkingUsage
                              SET exit_time = current_timestamp
                              WHERE spot_id = ? AND registration_plate = ? AND exit_time IS NULL""", (spot_id, registration_plate))
            conn.commit()

    def new_booking(self, spot_id, registration_plate):
        # WARNING : Not needed for MVP
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("")
            conn.commit()

    def fetch_all_payments(self):
        # TODO : fetch payments
        pass
