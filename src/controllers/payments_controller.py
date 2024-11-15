from .database_controller import DatabaseController
from models import Payment

class PaymentsController:
    def __init__(self, root):
        self.root = root

    def fetch_payments_data(self):
        db = DatabaseController()
        payments = []
        for payment in db.fetch_all_payments():
            usage_id, registration_plate, amount = payment
            payments.append(Payment(usage_id, registration_plate, amount))
        return payments

    def calculate_total_revenue(self):
        """
        Calcule le revenu total généré par les paiements.
        :return: float représentant le revenu total
        """
        pass

    def calculate_average_payment(self):
        """
        Calcule le montant moyen des paiements.
        :return: float représentant le montant moyen des paiements
        """
        pass

    def fetch_payments_by_date(self, start_date, end_date):
        """
        Récupère les paiements effectués entre deux dates spécifiques.
        :param start_date: date de début de la période
        :param end_date: date de fin de la période
        :return: list de paiements effectués dans la période spécifiée
        """
        pass

    def generate_payment_summary(self):
        """
        Génère un résumé des paiements.
        :return: dict contenant le résumé des paiements
        """
        pass

    def fetch_payments_by_registration_plate(self, registration_plate):
        """
        Récupère les paiements associés à un véhicule spécifique.
        :param registration_plate: plaque d'immatriculation du véhicule
        :return: list de paiements associés à la plaque d'immatriculation spécifiée
        """
        pass