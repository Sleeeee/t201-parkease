class ParkingSpot:
    """
    A class representing a parking spot. The ParkingSpot constructor is only called within ParkingRow (eventually while creating a top-level Parking object)

    Attributes :
        - spot_number (read-only int) : The number of the spot inside its container ParkingRow
        - status (str) : Real-time status of the spot. Must be one of the following :
            - free : The spot is currently free and customers can book or be placed in that spot
            - occupied : Someone is currently occuppying the spot, it can't be booked, noone can be placed in that spot
            - booked : Someone is meant to park in that spot. Only that person can be placed in that spot
        - _booking_id (read-only str | None) : The id of the current booking linked to the spot. None if the spot is not booked
    """

    ALLOWED_STATUSES = ["free", "occupied", "booked"] 

    def __init__(self, id: int, spot_number: int, status: str = "free", booking_id: int = None):
        self._id = id
        self._spot_number = spot_number
        self.status = status # Forces usage of @status.setter
        self.linked_car = None

    @property
    def id(self):
        return self._id

    @property
    def spot_number(self):
        return self._spot_number

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one the following : {self.ALLOWED_STATUSES}")
        self._status = status

    def __str__(self):
        string = f"Spot {self.spot_number} : {self.status}"
        if self.status != "free":
            string += f" by {self.linked_car.registration_plate}" # Adds the registration plate if the spot is occupied or booked
        return string

    def enter(self, registration_plate: str):
        """Updates status = "occupied" and linked_car = Car(registration_plate)"""
        assert self.status == "free" # Raises an error if someone is occupying the spot
        self.status = "occupied"
        self.linked_car = Car(registration_plate)

    def exit(self, registration_plate: str):
        """Updates status = "free" and linked_car = None """
        assert (self.status == "occupied") and (self.linked_car.registration_plate == registration_plate) # Raises an error if the spot isn't occupied or if the plates don't match
        self.status = "free"
        self.linked_car = None

    def pay(self, registration_plate : int, time_spent : float):
        """Returns the amount that has to be paid by the car"""
        assert (self.status == "occupied") and (registration_plate == self.linked_car.registration_plate) # Raises an error if the spot isn't occupied or if the plates don't match
        return self.linked_car.HOURLY_RATE * time_spent

    def book(self, client_id):
        # WARNING : Not needed for MVP
        """
        Books the parking spot for the client if he is subscribed.

        Updates :
            - self.status : Set to "booked"
            - _booking : The id created for the booking
        """
        self.status = "booked"
        #self._booking_id = booking_id
        pass

class ParkingRow:
    def __init__(self, row_number):
        self._row_number = row_number
        self.spots = {}

    @property
    def row_number(self):
        return self._row_number

    def __str__(self):
        output = [f"Row {self.row_number}"]
        for spot in sorted(self.spots):
            output.append(f"            {str(self.spots[spot])}")
        return "\n".join(output)

    def add_spot(self, spot):
        #spot.keys() = "id", "spot_number"
        self.spots[spot["spot_number"]] = ParkingSpot(spot["id"], spot["spot_number"])

    def remove_spot(self, spot):
        pass

class ParkingFloor:
    def __init__(self, floor_number):
        self._floor_number = floor_number
        self.rows = {}

    @property
    def floor_number(self):
        return self._floor_number

    def __str__(self):
        output = [f"Floor {self.floor_number}"]
        for row in sorted(self.rows):
            output.append(f"        {str(self.rows[row])}")
        return "\n".join(output)

    def add_spot(self, spot):
        #spot.keys() = "id", "spot_number", "row_number"
        id, spot_number, row_number = spot["id"], spot["spot_number"], spot["row_number"]
        if row_number not in self.rows:
            self.rows[row_number] = ParkingRow(row_number)
        self.rows[row_number].add_spot({"id": id, "spot_number": spot_number})

    def remove_spot(self, spot):
        pass

class ParkingLot:
    def __init__(self, lot_number):
        self._lot_number = lot_number
        self.floors = {}

    @property
    def lot_number(self):
        return self._lot_number

    def __str__(self):
        output = [f"Parking {self.lot_number}"]
        for floor in sorted(self.floors):
            output.append(f"    {str(self.floors[floor])}")
        return "\n".join(output)

    def add_spot(self, spot):
        #spot.keys() = "id", "spot_number", "row_number", "floor_number"
        id, spot_number, row_number, floor_number = spot["id"], spot["spot_number"], spot["row_number"], spot["floor_number"] 
        if floor_number not in self.floors:
            self.floors[floor_number] = ParkingFloor(floor_number)
        self.floors[floor_number].add_spot({"id": id, "spot_number": spot_number, "row_number": row_number})

    def remove_spot(spot):
        pass

class Car:
    def __init__(self, registration_plate):
        self.registration_plate = registration_plate

class StandardCar(Car):
    HOURLY_RATE = 3.00
    def __init__(self, registration_plate):
        super().__init__(self, registration_plate)

class PremiumCar(Car):
    HOURLY_RATE = 2.00
    def __init__(self, registration_plate):
        super().__init__(self, registration_plate)

class Payment:
    def __init__(self, usage_id, registration_plate, amount):
        self.usage_id = usage_id
        self.registration_plate = registration_plate
        self.amount = amount

    def __str__(self):
        return f"#{self.usage_id} - {self.registration_plate} paid {self.amount}€"

