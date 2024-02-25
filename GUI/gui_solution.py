import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from cryo_sim import Cryo


# Button = ttk.Button
Button = tk.Button
# from tkmacosx import Button

class CryoGui(tk.Tk):
    def __init__(self,cryo: Cryo,*args,title="GUI Demo",refresh_rate=250,**kwargs):
        super().__init__()

        self.cryo = cryo

        self.title(title)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW",self.quit_app)

        self.initialize()

        # 4. Update temperature
        self.refresh=refresh_rate
        self.after(self.refresh,self.update)

    def initialize(self):
        """ Create gui """
        # 1. Display Temperature
        self._temperature=tk.StringVar(self,"")
        ttk.Label(self,text="Temperature: ").grid(row=0,column=0)
        ttk.Label(self,textvariable=self._temperature).grid(row=0,column=1)
        self.update_temperature()

        # 2. Setpoint Control
        self._setpoint=tk.StringVar(self,"")
        ttk.Label(self,text="Setpoint: ").grid(row=1,column=0)
        entry=ttk.Entry(self,textvariable=self._setpoint)
        entry.grid(row=1,column=1)
        entry.bind("<Return>",self.set_setpoint) # Bind "return" event
        self.update_setpoint()

        # 3. Connect/Disconnect
        self.is_connected=tk.StringVar(self,"")
        self.button=Button(self,textvariable=self.is_connected,command=self.toggle_connection)
        self.button.grid(row=2,column=0,columnspan=2,sticky="NESW")
        self.update_connection()

    def update(self):
        """Update values in gui"""
        self.update_connection()
        self.update_temperature()
        self.after(250,self.update)

    def update_temperature(self):
        self._temperature.set("%.2f C"%self.cryo.read_temperature())

    def update_setpoint(self):
        self._setpoint.set(str(self.cryo.setpoint))

    def set_setpoint(self,*args):
        if self.cryo.is_connected:
            setpoint = float(self._setpoint.get())
            self.cryo.set_setpoint(setpoint)
        else:
            messagebox.showwarning(title="Oops!",message="Cannot change setpoint when not connected")
        self.update_setpoint()

    def update_connection(self):
        if self.cryo.is_connected:
            string="Connected"
            style = {"bg":"spring green"}
        else:
            string = "Disconnected"
            style = {"bg":"tomato"}
        self.is_connected.set(string)
        self.button.configure(**style)

    def toggle_connection(self):
        if self.cryo.is_connected:
            self.cryo.close_connection()
        else:
            self.cryo.open_connection()
        self.update_connection()

    def quit_app(self):
        """Run any cleanup needed"""
        self.destroy()


if __name__=="__main__":
    cryo = Cryo()

    try:
        app = CryoGui(cryo)
        app.mainloop()
    finally:
        cryo.close_connection()