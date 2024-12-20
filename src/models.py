from typing import Dict

from pip._vendor.rich import status


class ParkingSpot:
    """
    A class representing a parking spot.
    The ParkingSpot constructor is only called within ParkingRow
    (eventually while creating a top-level Parking object)

    Attributes :
        - spot_number (read-only int) :
          The number of the spot inside its container ParkingRow
        - status (str) : Real-time status of the spot.
          Must be one of the following :
            - free : The spot is currently free and customers can booked
              or be placed in that spot
            - occupied : Someone is currently occuppying the spot,
              it can't be booked, noone can be placed in that spot
            - booked : Someone is meant to park in that spot.
              Only that person can be placed in that spot
        - _booking_id (read-only str | None) : The id of the current booking
          linked to the spot. None if the spot is not booked
    """

    ALLOWED_STATUSES = ["free", "occupied", "booked"] 

    def __init__(self, id: int,
                 spot_number: int,
                 status: str = "free"):
        """"""
        self._id = id
        self._spot_number = spot_number
        self.status = status # Forces usage of @status.setter
        self.linked_car = None

    @property
    def id(self):
        """"""
        return self._id

    @property
    def spot_number(self):
        """"""
        return self._spot_number

    @property
    def status(self):
        """"""
        return self._status

    @status.setter
    def status(self, status: str):
        """"""
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"""Invalid status '{status}'.
            Must be one the following : {self.ALLOWED_STATUSES}""")
        self._status = status

    def __str__(self):
        """"""
        string = f"Spot {self.spot_number} : {self.status}"
        if self.status != "free":
            # Adds the registration plate if the spot is occupied or booked
            string += f" by {self.linked_car}"
        return string

    def enter(self, registration_plate: str, is_premium: bool):
        """
        PRE : None
        POST : Change le statut du spot en "occupé" si le spot était libre et attribue une voiture avec sa plaque au spot. Si la place était boookée, change la booking_plate en None
        RAISES : AssertionError si le spot n'était pas "libre" et AssertionError si la place était bookée et que la plaque d'immatriculation enregistrée ne correspond pas à la booking_plate
        """
        if self.status == "booked":
            assert self.linked_car.registration_plate == registration_plate and is_premium
        elif self.status == "free":
            car_class = PremiumCar if is_premium else StandardCar
            self.linked_car = car_class(registration_plate)
        else:
            raise AssertionError("The spot is already occupied")
        self.status = "occupied"

    def exit(self, registration_plate: str):
        """
        PRE : None
        POST : Change le statut du spot en "libre" si le spot était occupé et désattribue la voiture désignée de ce spot
        RAISES : AssertionError si le spot n'était pas "occupé" ou si la plaque entrée dans les paramètres ne correspond pas à la plaque du véhicule sur le spot
        """
        assert (self.status == "occupied") and (self.linked_car.registration_plate == registration_plate) # Raises an error if the spot isn't occupied or if the plates don't match
        self.status = "free"
        self.linked_car = None

    def pay(self, registration_plate : str, time_spent : float):
        """Returns the amount that has to be paid by the car"""
        assert (self.status == "occupied") and (registration_plate == self.linked_car.registration_plate) # Raises an error if the spot isn't occupied or if the plates don't match
        return self.linked_car.HOURLY_RATE * time_spent

    def book(self, registration_plate : str, is_premium: bool):
        """
        Books the parking spot for the client if he is subscribed.

        PRE : None
        POST : change le statut du spot en "booké", lui attribue un identifiant de booking, tout ça si le client est premium
        RAISES : AssertionError si le client n'est pas premium et/ou que la place était occupée, TypeError si la Registration_plate n'est pas une string
        """
        assert self.status == "free" and is_premium
        self.status = "booked"
        self.linked_car = PremiumCar(registration_plate)

class ParkingRow:
    """"""
    def __init__(self, row_number: int):
        """"""
        self._row_number = row_number
        self.spots = {}

    @property
    def row_number(self):
        """"""
        return self._row_number

    def __str__(self):
        """"""
        output = [f"Row {self.row_number}"]
        for spot in sorted(self.spots):
            output.append(f"            {str(self.spots[spot])}")
        return "\n".join(output)

    def add_spot(self, spot: Dict[str, int]):
        """"""
        #spot.keys() = "id", "spot_number"
        self.spots[spot["spot_number"]] = ParkingSpot(spot["id"], spot["spot_number"])

    def remove_spot(self, spot_number : int):
        """"""
        del self.spots[spot_number]

class ParkingFloor:
    """"""
    def __init__(self, floor_number: int):
        """"""
        self._floor_number = floor_number
        self.rows = {}

    @property
    def floor_number(self):
        """"""
        return self._floor_number

    def __str__(self):
        """"""
        output = [f"Floor {self.floor_number}"]
        for row in sorted(self.rows):
            output.append(f"        {str(self.rows[row])}")
        return "\n".join(output)

    def add_spot(self, spot: Dict[str, int]):
        """"""
        #spot.keys() = "id", "spot_number", "row_number"
        id, spot_number, row_number = spot["id"], spot["spot_number"], spot["row_number"]
        if row_number not in self.rows:
            self.rows[row_number] = ParkingRow(row_number)
        self.rows[row_number].add_spot({"id": id, "spot_number": spot_number})

    def remove_spot(self, spot):
        """"""
        spot_number, row_number = spot["spot_number"], spot["row_number"]
        self.rows[row_number].remove_spot(spot_number)
        if not self.rows[row_number].spots:
            del self.rows[row_number]

class ParkingLot:
    """"""
    def __init__(self, lot_number: int):
        """
        PRE : None
        POST : l'objet ParkingLot possède un numéro d'identification
        et un dictionnaire vide contenant les étages
        (qui contiendront les rangées, qui elles contiendront les emplacements)
        RAISES : ValueError si lot_number n'est pas strictement positif
        """
        if lot_number <= 0:
            raise ValueError("lot_number must be positive")
        self._lot_number = lot_number
        self.floors = {}

    @property
    def lot_number(self):
        """"""
        return self._lot_number

    def __str__(self):
        """"""
        output = [f"Parking {self.lot_number}"]
        for floor in sorted(self.floors):
            output.append(f"    {str(self.floors[floor])}")
        return "\n".join(output)

    def add_spot(self, spot: Dict[str, int]):
        """"
        PRE : Spot est un dictionnaire dont les clés sont
              "id", "spot_number", "row_number", "floor_number",
              chacune correspondant à un entier
        POST : Si l'étage demandé n'existe pas, il est créé (à vide).
               Appelle ensuite la méthode add_spot() de l'objet ParkingFloor,
               qui va créer un ParkingRow si besoin.
               À terme, L'objet ParkingSpot est créé dans le ParkingRow correspondant
        RAISES : ValueError si l'emplacement existe déjà,
                 TypeError si spot n'est pas un dictionnaire
                 ou ne correspond pas à la description indiquée
        """
        keys = spot.keys()
        if len(keys) > 4:
            raise TypeError("There are too many keys in the spot dictionary")
        for key in ("id", "spot_number", "row_number", "floor_number"):
            if not key in keys:
                raise TypeError(f"{key} is not in spot")
            if spot[key] <= 0 and key != "floor_number":
                raise ValueError(f"{key} must be strictly positive")
        id, spot_number, row_number, floor_number = spot["id"], spot["spot_number"], spot["row_number"], spot["floor_number"] 
        if (f:= self.floors.get(floor_number)) is not None:
            if (r:= f.rows.get(row_number)) is not None:
                if r.spots.get(spot_number) is not None:
                    raise ValueError("There is already an existing spot at this position")
        if floor_number not in self.floors:
            self.floors[floor_number] = ParkingFloor(floor_number)
        self.floors[floor_number].add_spot({"id": id, 
                                            "spot_number": spot_number,
                                            "row_number": row_number})

    def remove_spot(self, spot):
        """
        PRE : Spot est un dictionnaire dont les clés sont "spot_number", "row_number", "floor_number", chacune correspondant à un entier
        POST : Supprime l'emplacement spécifié. Supprime également la rangée/l'étage si vide après l'opération
        RAISES : ValueError si l'emplacement n'existe pas / TypeError si spot n'est pas un dictionnaire ou ne correspond pas à la description indiquée
        """
        keys = spot.keys()
        if len(keys) > 3:
            raise TypeError("There are too many keys in the spot dictionary")
        for key in ("spot_number", "row_number", "floor_number"):
            if not key in keys:
                raise TypeError(f"{key} is not in spot")
        spot_number, row_number, floor_number = spot["spot_number"], spot["row_number"], spot["floor_number"]
        if (self.floors.get(floor_number) is None) or (self.floors[floor_number].rows.get(row_number) is None) or (self.floors[floor_number].rows[row_number].spots.get(spot_number) is None):
            raise ValueError("There is no existing spot at this position")
        self.floors[floor_number].remove_spot({"spot_number": spot_number, "row_number": row_number})
        if not self.floors[floor_number].rows:
            del self.floors[floor_number]

class Car:
    """"""
    def __init__(self, registration_plate):
        """"""
        self.registration_plate = registration_plate

class StandardCar(Car):
    """"""
    HOURLY_RATE = 3.00

    def __init__(self, registration_plate):
        super().__init__(registration_plate)

    def __str__(self):
        return f"{self.registration_plate} (standard)"

class PremiumCar(Car):
    """"""
    HOURLY_RATE = 2.0

    def __init__(self, registration_plate):
        super().__init__(registration_plate)

    def __str__(self):
        return f"{self.registration_plate} (premium)"

class Payment:
    """"""
    def __init__(self, usage_id, registration_plate, amount):
        """"""
        self.usage_id = usage_id
        self.registration_plate = registration_plate
        self.amount = amount

    def __str__(self):
        """"""
        return f"#{self.usage_id} - {self.registration_plate} paid {self.amount}€"

