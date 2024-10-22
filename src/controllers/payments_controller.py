class PaymentsController:
    def __init__(self, root):
        self.root = root

    def fetch_payments_data(self):
        return ["James paid 24 dollars", "Caitlyn paid 12 dollars"]
