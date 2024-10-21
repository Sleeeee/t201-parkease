from tkinter import ttk

class ParkEaseApp:
    """
    A class that represents the window available to the user. It contains frames and can replace them to display different views
    """
    def __init__(self, root):
        self.root = root
        self.root.title("ParkEase - Simple parking management")
        self.root.configure(background="white")

        self.create_default_style()

        self.logo_frame = LogoFrame(self.root)
        self.title_frame = TitleFrame(self.root)
        self.banner_frame = BannerFrame(self.root)
        self.sidebar_frame = SidebarFrame(self.root, self)
        self.current_mainframe = None
    
        self.init_grid()
        self.switch_mainframe(ParkingOverviewFrame)

    def init_grid(self):
        """Initializes the grid layout"""
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

    def create_default_style(self):
        """Creates the style for the child frames to use"""
        style = ttk.Style()
        style.configure("Default.TFrame", margin=5, padding=5, borderwidth=1, relief="solid", background="white")
        style.configure("Default.TButton", background="white", borderwidth=1)
        style.configure("Default.TLabel", background="white")

    def switch_mainframe(self, frame_class):
        """Switches the main frame between the different available views"""
        if isinstance(self.current_mainframe, frame_class):
            return
        if self.current_mainframe is not None:
            self.current_mainframe.destroy() # Frees memory for the current frame
        # TODO check for values and raise ValueErrors
        self.current_mainframe = frame_class(self.root) # Sets the current frame to a new object of class *frame_class* (parent given as argument)

class LogoFrame(ttk.Frame):
    """Frame containing the logo"""
    def __init__(self, parent):
        super().__init__(parent, width=250, height=250, style="Default.TFrame")
        self.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

class TitleFrame(ttk.Frame):
    """Frame containing information about the current overview"""
    def __init__(self, parent):
        super().__init__(parent, style="Default.TFrame")
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

class BannerFrame(ttk.Frame):
    """Frame used to notify the user about actions registered, or alert about specific events"""
    def __init__(self, parent):
        super().__init__(parent, style="Default.TFrame")
        self.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

class SidebarFrame(ttk.Frame):
    """Frame containing the buttons to switch the current overview"""
    def __init__(self, parent, app):
        super().__init__(parent, style="Default.TFrame")
        self.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Button(self, text="Manage parkings", style="Default.TButton", command=lambda: app.switch_mainframe(ParkingOverviewFrame)).pack()
        ttk.Button(self, text="Manage payments", style="Default.TButton", command=lambda: app.switch_mainframe(PaymentsOverviewFrame)).pack()
        ttk.Button(self, text="Manage subscribers", style="Default.TButton", command=lambda: app.switch_mainframe(SubscribersOverviewFrame)).pack()
        ttk.Button(self, text="View analytics", style="Default.TButton", command=lambda: app.switch_mainframe(AnalyticsOverviewFrame)).pack()

class MainFrame(ttk.Frame):
    """Parent class to the overviews"""
    def __init__(self, parent):
        super().__init__(parent, style="Default.TFrame")
        self.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

class ParkingOverviewFrame(MainFrame):
    """Frame used to view the parking lot occupancy"""
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="I love parkings !", style="Default.TLabel").pack()

class PaymentsOverviewFrame(MainFrame):
    """Frame used to encode or review payments"""
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="I love payments !", style="Default.TLabel").pack()

class SubscribersOverviewFrame(MainFrame):
    """Frame used to manage subscribers"""
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="I love subscribers !", style="Default.TLabel").pack()

class AnalyticsOverviewFrame(MainFrame):
    """Frame used to visualize current or past data about the parking lots and generate reports"""
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="I love analytics !", style="Default.TLabel").pack()

