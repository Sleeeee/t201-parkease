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

    def __init__(self, id, spot_number, status="free", booking_id=None):
        self._id = id
        self._spot_number = spot_number
        self.status = status # Forces usage of @status.setter
        self._booking_id = booking_id # TODO implement book() method OR @booking.setter (easier to init everything at once) to maybe create a Booking object ? Needs to be created outside of the ParkingSpot.

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
            raise ValueError(f"Invalid status '{status}'. Must be one the following : {ALLOWED_STATUSES}")
        self._status = status

    @property
    def booking(self):
        return self._booking

    def __str__(self):
        return f"Spot {self.spot_number} : {self.status}"

    def book(self, client_id):
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

class Car:
    HOURLY_RATE = 3.00 # Price in dollars for 1 hour of parking

    def __init__(self, registration_plate, is_subscribed=False):
        self.registration_plate = registration_plate
        self.is_subscribed = is_subscribed
        if self.is_subscribed:
            self.HOURLY_RATE *= 0.8
