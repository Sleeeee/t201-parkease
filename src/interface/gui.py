from tkinter import *
from tkinter import ttk

class ParkEaseApp:
    """
    A class that represents the window available to the user. It contains frames and can replace them to display different views
    """
    def __init__(self, root):
        self.root = root
        self.root.title = "ParkEase - Simple parking management"

        self.logo_frame = LogoFrame(self.root)
        self.title_frame = TitleFrame(self.root)
        self.sidebar_frame = SidebarFrame(self.root)
        self.current_frame = None

    def switch_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy() # Frees memory for the current frame
        # TODO check for values and raise ValueErrors
        self.current_frame = frame_class(self.root) # Sets the current frame to a new object of class *frame_class* (parent given as argument)

class LogoFrame(ttk.Frame):
    """Frame containing the logo"""
    def __init__(self, parent):
        super().__init__(parent)

class TitleFrame(ttk.Frame):
    """Frame containing information about the current overview"""
    def __init__(self, parent):
        super().__init__(parent)

class BannerFrame(ttk.Frame):
    """Frame used to notify the user about actions registered, or alert about specific events"""
    def __init__(self, parent):
        super().__init__(parent)

class SidebarFrame(ttk.Frame):
    """Frame containing the buttons to switch the current overview"""
    def __init__(self, parent):
        super().__init__(parent)

class MainFrame(ttk.Frame):
    """Parent class to the overviews"""
    def __init__(self, parent):
        super().__init__(parent)

class ParkingOverviewFrame(MainFrame):
    """Frame used to view the parking lot occupancy"""
    def __init__(self, parent):
        super().__init__(parent) 

class PaymentsOverviewFrame(MainFrame):
    """Frame used to encode or review payments"""
    def __init__(self, parent):
        super().__init__(parent) 

class SubscribersOverviewFame(MainFrame):
    """Frame used to manage subscribers"""
    def __init__(self, parent):
        super().__init__(parent)

class AnalyticsOverviewFrame(MainFrame):
    """Frame used to visualize current or past data about the parking lots and generate reports"""
    def __init__(self, parent):
        super().__init__(parent)

if __name__ == "__main__":
    root = Tk()
    app = ParkEaseApp(root)
    root.mainloop()
