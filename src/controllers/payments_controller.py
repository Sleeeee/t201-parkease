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

