class SubscribersController:
    def __init__(self, root):
        self.root = root

    def fetch_subscribers_data(self):
        return ["Hank is subscribed", "Darius is subscribed", "Marilyn is subscribed"]
