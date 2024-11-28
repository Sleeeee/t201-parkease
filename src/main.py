import os
from tkinter import Tk
from interface.gui import ParkEaseApp
from controllers import DatabaseController

def main():
    db_controller = DatabaseController()
    if not os.path.exists(db_controller.path):
        os.makedirs(db_controller.directory, exist_ok=True) # Ensure the directory exists
        db_controller.init_database()

    root = Tk()
    app = ParkEaseApp(root)
    root.mainloop()
