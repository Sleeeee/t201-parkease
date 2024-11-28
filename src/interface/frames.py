from tkinter import ttk, IntVar, PhotoImage, StringVar
from controllers import ParkingController, PaymentsController, PremiumCarsController, AnalyticsController
import os
from tkinter import ttk, PhotoImage

class LogoFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'logo.png')
        logo = PhotoImage(file=logo_path, width=250, height=250)
        ttk.Label(self, image=logo).pack()
        self.logo = logo

class TitleFrame(ttk.Frame):
    """Frame containing information about the current overview"""
    def __init__(self, parent, title=None):
        super().__init__(parent, style="Default.TFrame")
        self._title = ttk.Label(self, text=title, style="Default.TLabel")
        self._title.pack(pady=10)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title.config(text=title)

class BannerFrame(ttk.Frame):
    """Frame used to notify the user about actions registered, or alert about specific events"""
    def __init__(self, parent):
        super().__init__(parent, style="Default.TFrame")
        self._notification = ttk.Label(self, text="", style="Default.TLabel")
        self._notification.pack(pady=10)

    @property
    def notification(self):
        return self._notification

    @notification.setter
    def notification(self, text):
        self._notification.config(text=text)
        
class SidebarFrame(ttk.Frame):
    """Frame containing the buttons to switch the current overview"""
    def __init__(self, parent, app):
        super().__init__(parent, style="Default.TFrame")

        ttk.Button(self, text="Manage parkings", style="Default.TButton", command=lambda: app.switch_mainframe(ParkingOverviewFrame, ParkingController, "Parking Management")).pack(pady=(4,0))
        ttk.Button(self, text="Manage payments", style="Default.TButton", command=lambda: app.switch_mainframe(PaymentsOverviewFrame, PaymentsController, "Payments Management")).pack(pady=(4,0))
        ttk.Button(self, text="Manage premium car", style="Default.TButton", command=lambda: app.switch_mainframe(PremiumCarsOverviewFrame, PremiumCarsController, "Premium Cars Management")).pack(pady=(4,0))
        ttk.Button(self, text="View analytics", style="Default.TButton", command=lambda: app.switch_mainframe(AnalyticsOverviewFrame, AnalyticsController, "Analytics Visualization")).pack(pady=(4,0))

class MainFrame(ttk.Frame):
    """Parent class to the overviews"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, style="Default.TFrame")
        self.app = app
        self.controller = controller

class ParkingOverviewFrame(MainFrame):
    """Frame used to view the parking lot occupancy"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, app, controller)

        column_left = ttk.Frame(self, style="Default.TFrame")
        column_right = ttk.Frame(self, style="Default.TFrame")
        column_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        column_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10) 

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        parking_lot = self.controller.parking_lot
        self.parking_lot = ttk.Label(column_right, text=str(parking_lot), style="Default.TLabel")
        self.parking_lot.pack(pady=(1, 0))

        """Entry Form, Structure and initialisation"""
        
        floor = IntVar()
        row = IntVar()
        spot = IntVar()
        plate = StringVar()
        action = StringVar()

        ttk.Label(column_left, text="Floor", style="Default.TLabel").pack(pady=(1, 0))
        ttk.Entry(column_left, textvariable=floor).pack(pady=(1,0))
        ttk.Label(column_left, text='Row', style="Default.TLabel").pack(pady=(1,0))
        ttk.Entry(column_left, textvariable=row).pack(pady=(1,0))
        ttk.Label(column_left, text="Spot", style="Default.TLabel").pack(pady=(1,0))
        ttk.Entry(column_left, textvariable=spot).pack(pady=(1,0))
        ttk.Label(column_left, text="Registration Plate", style="Default.TLabel").pack(pady=(1,0))
        ttk.Entry(column_left, textvariable=plate).pack(pady=(1,0))
        ttk.Radiobutton(column_left, text='Enter', variable=action, value='enter').pack(pady=(3,0))
        ttk.Radiobutton(column_left, text='Exit', variable=action, value='exit',).pack(pady=(3,0))
        ttk.Button(column_left, text='Submit', command=lambda: self.submit(int(floor.get()),int(row.get()),int(spot.get()),plate.get(),action.get())).pack(pady=(3,0))

        """Creation Form, Structure and initialisation"""

        floor_create = IntVar()
        row_create = IntVar()
        spot_create = IntVar()
        action_create = StringVar()

        ttk.Label(column_left, text="Floor", style="Default.TLabel").pack(pady=(1,0))
        ttk.Entry(column_left, textvariable=floor_create).pack(pady=(1,0))
        ttk.Label(column_left, text='Row', style="Default.TLabel").pack(pady=(1,0))
        ttk.Entry(column_left, textvariable=row_create).pack(pady=(1,0))
        ttk.Label(column_left, text="Spot", style="Default.TLabel").pack(pady=(1,0))
        ttk.Entry(column_left, textvariable=spot_create).pack(pady=(1,0))
        ttk.Radiobutton(column_left, text='Create Spot', variable=action_create, value='create').pack(pady=(3,0))
        ttk.Radiobutton(column_left, text='Delete Spot', variable=action_create, value='delete',).pack(pady=(3,0))
        ttk.Button(column_left, text='Submit', command=lambda: self.submitCreate(int(floor_create.get()),int(row_create.get()),int(spot_create.get()),action_create.get())).pack(pady=(3,0))
    
    def submit(self,floor,row,spot,plate,action):
        control = ""
        if action == "enter":
            control = self.controller.new_entry(floor,row,spot,plate)
        elif action == "exit":
            control = self.controller.new_exit(floor,row,spot,plate)
        else:
            control = "[Error] Please, enter an action"
        self.app.banner_frame.notification = control
        self.parking_lot.config(text=self.controller.parking_lot)

    def submitCreate(self,floor,row,spot,action):
        if action == "create":
            control = self.controller.create_new_spot(floor,row,spot)
            self.app.banner_frame.notification = control
        elif action == "delete":
            control = self.controller.delete_spot(floor,row,spot)
            self.app.banner_frame.notification = control
            # TODO : apply color (error messages start with [Error])
        else:
            print("Please, enter an action")
        self.parking_lot.config(text=self.controller.parking_lot)

class PaymentsOverviewFrame(MainFrame):
    """Frame used to encode or review payments"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, app, controller)
        for i in self.controller.fetch_payments_data():
            ttk.Label(self, text=i, style="Default.TLabel").pack(pady=(1,0))

class PremiumCarsOverviewFrame(MainFrame):
    """Frame used to manage subscribers"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, app, controller)
        
        plate = StringVar()
        action = StringVar()

        ttk.Label(self,text="Spot", style="Default.TLabel").pack(pady=(1,0))
        ttk.Entry(self,textvariable=plate).pack(pady=(1,0))
        ttk.Radiobutton(self,text='Add premium', variable=action, value='add').pack(pady=(3,0))
        ttk.Radiobutton(self,text='Delete premium', variable=action, value='delete',).pack(pady=(3,0))
        ttk.Button(self,text='Submit', command=lambda: self.submit(int(plate.get()),action.get())).pack(pady=(3,0))
        for i in self.controller.fetch_premium_cars_data():
            ttk.Label(self, text=i, style="Default.TLabel").pack(pady=(1,0))

    def submit(self, plate, action):
        control == ""
        if action == "add":
            control = self.controller.new_premium_car()
        elif action == "del":
            control = self.controller.delete_premium_subscription
        self.app.banner_frame.notification = control


class AnalyticsOverviewFrame(MainFrame):
    """Frame used to visualize current or past data about the parking lots and generate reports"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, app, controller)
        for i in self.controller.fetch_all_usages():
            ttk.Label(self, text=i, style="Default.TLabel").pack(pady=(1,0))

