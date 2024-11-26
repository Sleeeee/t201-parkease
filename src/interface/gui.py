from tkinter import ttk
from interface.frames import LogoFrame, TitleFrame, BannerFrame, SidebarFrame, ParkingOverviewFrame
from controllers import ParkingController

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

        self.logo_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.title_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.banner_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.sidebar_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.init_grid()
        self.switch_mainframe(ParkingOverviewFrame, ParkingController, "Parking Management")

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

    def switch_mainframe(self, frame_class, frame_controller_class, title):
        """Switches the main frame between the different available views"""
        if isinstance(self.current_mainframe, frame_class):
            return
        if self.current_mainframe is not None:
            self.current_mainframe.destroy() # Frees memory for the current frame
        self.current_mainframe = frame_class(self.root, self, frame_controller_class(self)) # Sets the current frame to a new object of class *frame_class* (parent given as argument)
        self.current_mainframe.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.title_frame.title = title

