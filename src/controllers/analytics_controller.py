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
