import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading
from cryo_sim import Cryo

class CryoGui(tk.Tk):
    def __init__(self,cryo: Cryo, *args, title="GUI Demo", **kwargs):
        super().__init__(*args,**kwargs)

        self.cryo = cryo

        self.title(title)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW",self.quit_app)

        self.initialize()

        # 4. Update temperature


    def initialize(self):
        """ Create gui """
        pass

        # 1. Display Temperature

        # 2. Setpoint Control

        # 3. Connect/Disconnect


    def update(self):
        """Update values in gui"""
        pass

    # 1b. Create functions to read temperature

    # 2b. Create functions to update setpoint

    # 3b. Create functions to Connect/Disconnect

    def quit_app(self):
        """Run any cleanup needed"""
        self.destroy()


if __name__ == "__main__":
    cryo = Cryo()
    root = CryoGui(cryo)
    root.mainloop()
