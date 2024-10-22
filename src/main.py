from tkinter import Tk
from interface.gui import ParkEaseApp
from controllers.parking_controller import ParkingController

if __name__ == "__main__":
    root = Tk()
    app = ParkEaseApp(root)
    root.mainloop()
