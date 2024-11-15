from .database_controller import DatabaseController

class AnalyticsController:
    def __init__(self, root):
        self.root = root

    def fetch_all_usages(self):
        db = DatabaseController()
        usages = []
        for usage_id, spot_id, registration_plate, entry_time, exit_time in db.fetch_all_usages():
            usages.append(f"#{usage_id} : Spot {spot_id} - {registration_plate} in @ {entry_time} / out @ {exit_time}")
        return usages

    def fetch_usage_statistics(self):
        """
        Calcule des statistiques sur l'utilisation du parking.
        :return: dict contenant les statistiques d'utilisation
        """
        pass

    def fetch_payment_statistics(self):
        """
        Calcule des statistiques financières.
        :return: dict contenant les statistiques financières
        """
        pass

    def fetch_subscriber_statistics(self):
        """
        Analyse les données des abonnés.
        :return: dict contenant les statistiques des abonnés
        """
        pass

    def generate_usage_report(self, start_date, end_date):
        """
        Génère un rapport détaillé sur l'utilisation du parking.
        :param start_date: date de début de la période
        :param end_date: date de fin de la période
        :return: rapport sous forme de chaîne de caractères ou de fichier
        """
        pass

    def generate_payment_report(self, start_date, end_date):
        """
        Génère un rapport détaillé sur les paiements.
        :param start_date: date de début de la période
        :param end_date: date de fin de la période
        :return: rapport sous forme de chaîne de caractères ou de fichier
        """
        pass