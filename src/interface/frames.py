from tkinter import ttk, IntVar, PhotoImage, StringVar
from controllers import ParkingController, PaymentsController, SubscribersController, AnalyticsController

class LogoFrame(ttk.Frame):
    """Frame containing the logo"""
    def __init__(self, parent):
        super().__init__(parent, width=250, height=250, style="Default.TFrame")
        logo = PhotoImage(file="./resources/logo.png", width=250, height=250)
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
        ttk.Button(self, text="Manage subscribers", style="Default.TButton", command=lambda: app.switch_mainframe(SubscribersOverviewFrame, SubscribersController, "Subscribers Management")).pack(pady=(4,0))
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
        ttk.Label(column_right, text=str(parking_lot), style="Default.TLabel").pack(pady=(1, 0))

        """Entry Form, Structure and initialisation"""
        
        floor = IntVar()
        row = IntVar()
        spot = IntVar()
        plate = StringVar()
        action = StringVar()

        ttk.Label(column_left, text="Floor", style="Default.TLabel").pack(pady=(1, 0))
        ttk.Entry(column_left, textvariable=floor).pack()
        ttk.Label(column_left, text='Row', style="Default.TLabel").pack()
        ttk.Entry(column_left, textvariable=row).pack()
        ttk.Label(column_left, text="Spot", style="Default.TLabel").pack()
        ttk.Entry(column_left, textvariable=spot).pack()
        ttk.Label(column_left, text="Registration Plate", style="Default.TLabel").pack()
        ttk.Entry(column_left, textvariable=plate).pack()
        ttk.Radiobutton(column_left, text='Enter', variable=action, value='enter').pack()
        ttk.Radiobutton(column_left, text='Exit', variable=action, value='exit',).pack()
        ttk.Button(column_left, text='Submit', command=lambda: self.submit(int(floor.get()),int(row.get()),int(spot.get()),plate.get(),action.get())).pack()

        """Creation Form, Structure and initialisation"""

        floor_create = IntVar()
        row_create = IntVar()
        spot_create = IntVar()
        action_create = StringVar()

        ttk.Label(column_left, text="Floor", style="Default.TLabel").pack()
        ttk.Entry(column_left, textvariable=floor_create).pack()
        ttk.Label(column_left, text='Row', style="Default.TLabel").pack()
        ttk.Entry(column_left, textvariable=row_create).pack()
        ttk.Label(column_left, text="Spot", style="Default.TLabel").pack()
        ttk.Entry(column_left, textvariable=spot_create).pack()
        ttk.Radiobutton(column_left, text='Create Spot', variable=action_create, value='create').pack()
        ttk.Radiobutton(column_left, text='Delete Spot', variable=action_create, value='delete',).pack()
        ttk.Button(column_left, text='Submit', command=lambda: self.submitCreate(int(floor_create.get()),int(row_create.get()),int(spot_create.get()),action_create.get())).pack()
    
    def submit(self,floor,row,spot,plate,action):
        if action == "enter":
            control = self.controller.new_entry(floor,row,spot,plate)
            self.app.banner_frame.notification = control
        elif action == "exit":
            control = self.controller.new_exit(floor,row,spot,plate)
            self.app.banner_frame.notification = control
        else:
            print("Please, enter an action")

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

class PaymentsOverviewFrame(MainFrame):
    """Frame used to encode or review payments"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, app, controller)
        for i in self.controller.fetch_payments_data():
            ttk.Label(self, text=i, style="Default.TLabel").pack(pady=(1,0))

class SubscribersOverviewFrame(MainFrame):
    """Frame used to manage subscribers"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, app, controller)
        for i in self.controller.fetch_subscribers_data():
            ttk.Label(self, text=i, style="Default.TLabel").pack(pady=(1,0))

class AnalyticsOverviewFrame(MainFrame):
    """Frame used to visualize current or past data about the parking lots and generate reports"""
    def __init__(self, parent, app, controller):
        super().__init__(parent, app, controller)
        for i in self.controller.fetch_all_usages():
            ttk.Label(self, text=i, style="Default.TLabel").pack(pady=(1,0))

