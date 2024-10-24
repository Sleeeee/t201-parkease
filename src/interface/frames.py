from tkinter import ttk
from controllers import ParkingController, PaymentsController, SubscribersController, AnalyticsController

class LogoFrame(ttk.Frame):
    """Frame containing the logo"""
    def __init__(self, parent):
        super().__init__(parent, width=250, height=250, style="Default.TFrame")

class TitleFrame(ttk.Frame):
    """Frame containing information about the current overview"""
    def __init__(self, parent):
        super().__init__(parent, style="Default.TFrame")

class BannerFrame(ttk.Frame):
    """Frame used to notify the user about actions registered, or alert about specific events"""
    def __init__(self, parent):
        super().__init__(parent, style="Default.TFrame")
        
class SidebarFrame(ttk.Frame):
    """Frame containing the buttons to switch the current overview"""
    def __init__(self, parent, app):
        super().__init__(parent, style="Default.TFrame")

        ttk.Button(self, text="Manage parkings", style="Default.TButton", command=lambda: app.switch_mainframe(ParkingOverviewFrame, ParkingController)).pack()
        ttk.Button(self, text="Manage payments", style="Default.TButton", command=lambda: app.switch_mainframe(PaymentsOverviewFrame, PaymentsController)).pack()
        ttk.Button(self, text="Manage subscribers", style="Default.TButton", command=lambda: app.switch_mainframe(SubscribersOverviewFrame, SubscribersController)).pack()
        ttk.Button(self, text="View analytics", style="Default.TButton", command=lambda: app.switch_mainframe(AnalyticsOverviewFrame, AnalyticsController)).pack()

class MainFrame(ttk.Frame):
    """Parent class to the overviews"""
    def __init__(self, parent, controller):
        super().__init__(parent, style="Default.TFrame")
        self.controller = controller

class ParkingOverviewFrame(MainFrame):
    """Frame used to view the parking lot occupancy"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        parking_lot = self.controller.fetch_parking_data()
        ttk.Label(self, text=str(parking_lot), style="Default.TLabel").pack()

class PaymentsOverviewFrame(MainFrame):
    """Frame used to encode or review payments"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for i in self.controller.fetch_payments_data():
            ttk.Label(self, text=i, style="Default.TLabel").pack()

class SubscribersOverviewFrame(MainFrame):
    """Frame used to manage subscribers"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for i in self.controller.fetch_subscribers_data():
            ttk.Label(self, text=i, style="Default.TLabel").pack()

class AnalyticsOverviewFrame(MainFrame):
    """Frame used to visualize current or past data about the parking lots and generate reports"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for i in self.controller.fetch_analytics():
            ttk.Label(self, text=i, style="Default.TLabel").pack()

