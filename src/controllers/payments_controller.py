class PaymentsController:
    def __init__(self, root):
        self.root = root

    def fetch_payments_data(self):
        # TODO : Use the database call to retrieve real data and display it as text
        return ["James paid 24 dollars", "Caitlyn paid 12 dollars"]
