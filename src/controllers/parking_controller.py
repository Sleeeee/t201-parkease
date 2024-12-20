from .database_controller import DatabaseController
from models import ParkingLot, PremiumCar, StandardCar

class ParkingController:
    def __init__(self, root=None, update_db: bool = True):
        self.root = root
        self.update_db = update_db # Set to false when
        self.parking_lot = None
        self.fetch_parking_data() # Updates self.parking_lot with the existing spots

    def fetch_parking_data(self):
        """Retrieves all the spots stored in the database and orders them inside self.parking_lot
           Updates self.parking_lot as a ParkingLot object containing all the spots ordered by floor, row, and number"""
        db = DatabaseController()
        self.parking_lot = ParkingLot(1) # Empty ParkingLot of id 1
        if not self.update_db:
            return
        for id, spot_number, row_number, floor_number in db.fetch_all_parking_spots():
            # For every spot found in the database, create the a ParkingSpot object inside its row and floor
            self.parking_lot.add_spot({"id": id, "spot_number": spot_number, "row_number": row_number, "floor_number": floor_number})
            
            spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number] # Fetches the spot from self.parking_lot
            registration_plate, status = self.check_spot_status(id) # Verifies if a car is occupying the spot
            if status != "free":
                # Sets the occupant only if it exists
                car_class = PremiumCar if db.is_premium(registration_plate) else StandardCar
                spot.linked_car = car_class(registration_plate)
            spot.status = status

    def check_spot_status(self, spot_id: int):
        """Queries the database to verify the current status of the spot
           Returns the status : free / occupied and the registration plate of the last (or current) user"""
        db = DatabaseController()
        spot_usage = db.fetch_last_spot_usage(spot_id) # Retrieves the last time the spot was used. None if no record was found
        if spot_usage is None:
            return None, "free" # Spot is free if it was never used
        registration_plate, entry_time, exit_time = spot_usage
        status = "occupied" if (not exit_time) else "free" # If someone entered but never left, it means the spot is occupied. If the last user left, it means the spot is free
        return registration_plate, status

    def create_new_spot(self, floor_number: int, row_number: int, spot_number: int) -> str:
        db = DatabaseController()
        try:
            # If you can access the spot without error, it means it shouldn't be created
            self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
            return "[Error] This spot already exists"
        except KeyError:
            id = db.create_parking_spot(floor_number, row_number, spot_number)
            print(id)
            self.parking_lot.add_spot({"id": id, "spot_number": spot_number, "row_number": row_number, "floor_number": floor_number})
            return f"[SPOT CREATED] The parking spot at floor {floor_number} - row {row_number} - spot {spot_number} was successfully created"

    def delete_spot(self, floor_number: int, row_number: int, spot_number: int) -> str:
        db = DatabaseController()
        try:
            self.parking_lot.remove_spot({"spot_number": spot_number, "row_number": row_number, "floor_number": floor_number}) #Delete spot if it exists, raises KeyError if not 
            db.delete_parking_spot(floor_number, row_number, spot_number)
            return f"[SPOT DELETED] The parking spot at floor {floor_number} - row {row_number} - spot {spot_number} was successfully deleted"
        except KeyError as e:
            return f"[Error] This spot does not exist : {e}"

    def new_entry(self, floor_number: int, row_number: int, spot_number: int, registration_plate: str) -> str:
        """
        PRE : floor_number, row_number et spot_number sont des entiers désignant la place de parking, registration_plate est la plaque d'immatriculation du véhicule entrant
        POST : Le statut de l'emplacement est occupé, la voiture liée à l'emplacement correspond à la plaque d'immatriculation, et la base de données contient une nouvelle entrée
        RETURNS : Un str contenant un message d'erreur si l'emplacement est déjà occupé où s'il n'existe pas. Un str vide si tout se passe comme prévu
        """
        db = DatabaseController()
        try:
            spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
            if self.update_db:
                # This parameter is set to False when running unit tests
                spot.enter(registration_plate, db.is_premium(registration_plate)) # Uses ParkingSpot's method to update linked_car and status IF POSSIBLE
                db.new_entry_visitor(spot.id, registration_plate) # Creates an entry inside the database
            else:
                # If running tests
                spot.enter(registration_plate, False)
            return f"[NEW ENTRY] Car {registration_plate} was successfully parked at floor {floor_number} - row {row_number} - spot {spot_number}"
        except AssertionError:
            # Error raised by spot.enter()
            return "[Error] This spot is already occupied"
        except KeyError:
            # Error raised by trying to access a spot that isn't contained inside self.parking_lot
            return "[Error] This spot does not exist"

    def new_exit(self, floor_number: int, row_number: int, spot_number: int, registration_plate: str) -> str:
        """
        PRE : floor_number, row_number et spot_number sont des entiers désignant la place de parking, registration_plate est la plaque d'immatriculation du véhicule sortant
        POST : Le statut de l'emplacement est libre, aucune voiture n'est liée à l'emplacement, l'entrée de la base de donnée est marquée comme cloturée
        RETURNS : Un str contenant un message d'erreur si l'emplacement n'est pas occupé, si la plaque d'immatriculation ne correspond pas avec celle enregistrée dans ParkingSpot.linked_car.registration_plate, ou si l'emplacement n'existe pas. Un str vide si tout se passe comme prévu
        """
        db = DatabaseController()
        try:
            spot = self.parking_lot.floors[floor_number].rows[row_number].spots[spot_number]
            if self.update_db:
                # This parameter is set to False when running unit tests
                usage_id, time_spent = db.fetch_last_usage_time(spot.id) # Fetches the entry's id and calculates the time spent occupying the spot
                amount = spot.pay(registration_plate, time_spent) # Calculates the amount to be paid based on the car's HOURLY_RATE
                db.new_payment(usage_id, registration_plate, amount) # Stores the payment inside the database
            spot.exit(registration_plate) # Uses ParkingSpot's method to update linked_car and status IF POSSIBLE
            if self.update_db:
                db.new_exit(spot.id, registration_plate) # Sets the exit time in the database
            return f"[NEW EXIT] Car {registration_plate} was successfully parked out of floor {floor_number} - row {row_number} - spot {spot_number}"
        except (AssertionError, TypeError):
            #Error raised by spot.exit()
            return "[Error] This spot is unoccupied or the registration plates don't match"
        except KeyError:
            # Error raised by trying to access a spot that isn't contained inside self.parking_lot
            return "[Error] This spot does not exist"

    def get_available_spots(self):
        """
        Récupère toutes les places de parking disponibles (libres).
        Retourne :
            list : Une liste de toutes les places de parking actuellement libres.
        """
        db = DatabaseController()
        available_spots = []
        try:
            for spot in db.fetch_all_parking_spots():
                if self.check_spot_status(spot[0]) == "free":
                    available_spots.append(spot)
        except Exception as e:
            print(f"[Error] Unable to retrieve available spots: {e}")
        return available_spots

    def reserve_spot(self, spot_id, registration_plate):
        """
        Réserve une place de parking pour un utilisateur spécifique.
        Paramètres :
            spot_id (int) : L'identifiant unique de la place à réserver.
            registration_plate (str) : La plaque d'immatriculation du véhicule de l'utilisateur.
        """
        db = DatabaseController()
        try:
            db.new_booking(spot_id, registration_plate)
        except Exception as e:
            print(f"[Error] Unable to reserve spot {spot_id} for {registration_plate}: {e}")

    def cancel_reservation(self, spot_id, registration_plate):
        """
        Annule une réservation pour une place de parking spécifique.
        Paramètres :
            spot_id (int) : L'identifiant unique de la place réservée.
            registration_plate (str) : La plaque d'immatriculation du véhicule de l'utilisateur.
        """
        db = DatabaseController()
        try:
            db.cancel_booking(spot_id, registration_plate)
        except Exception as e:
            print(f"[Error] Unable to cancel reservation for spot {spot_id} and {registration_plate}: {e}")

    def calculate_fee(self, spot_id):
        """
        Calcule les frais de stationnement pour une place spécifique.
        Paramètres :
            spot_id (int) : L'identifiant unique de la place de parking.
        Retourne :
            nombre réel (float) : Les frais de stationnement calculés, ou 0.0 si une erreur survient.
        """
        db = DatabaseController()
        try:
            usage = db.fetch_last_usage_time(spot_id)
            if usage and usage[1] is not None:
                time_spent = usage[1]  # Durée en heures
                fee = time_spent * 5  # Exemple : 5 euros par heure
                return round(fee, 2)
        except Exception as e:
            print(f"[Error] Unable to calculate fee for spot {spot_id}: {e}")
        return 0.0

    def confirm_payment(self, spot_id, registration_plate, amount):
        """
        Enregistre le paiement pour une utilisation de place de parking.
        Paramètres :
            spot_id (int) : L'identifiant unique de la place de parking.
            registration_plate (str) : La plaque d'immatriculation du véhicule.
            amount (float) : Le montant du paiement à enregistrer.
        """
        db = DatabaseController()
        try:
            usage = db.fetch_last_spot_usage(spot_id)
            if usage:
                usage_id = usage[0]
                db.new_payment(usage_id, registration_plate, amount)
        except Exception as e:
            print(f"[Error] Unable to confirm payment for spot {spot_id} and {registration_plate}: {e}")

    def get_parked_vehicles(self):
        """
        Récupère la liste de tous les véhicules actuellement garés.
        Retourne :
            list : Une liste des véhicules garés, chaque élément contenant le numéro de la place et la plaque d'immatriculation.
        """
        db = DatabaseController()
        parked_vehicles = []
        try:
            for spot in db.fetch_all_parking_spots():
                if self.check_spot_status(spot[0]) == "occupied":
                    usage = db.fetch_last_spot_usage(spot[0])
                    if usage:
                        parked_vehicles.append((spot[1], usage[0]))  # Spot_number et plaque
        except Exception as e:
            print(f"[Error] Unable to retrieve parked vehicles: {e}")
        return parked_vehicles

    def update_parking_spot_status(self):
        """
        Met à jour l'état de toutes les places de parking en mémoire en fonction des données actuelles de la base de données.
        """
        db = DatabaseController()
        try:
            for spot in db.fetch_all_parking_spots():
                spot_id = spot[0]
                status = self.check_spot_status(spot_id)
                # Mise à jour de l'état dans self.parking_lot si nécessaire
        except Exception as e:
            print(f"[Error] Unable to update parking spot status: {e}")
