import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading
from fake_cryo import Cyro

class App(tk.Tk):
    def __init__(self, cryo: Cyro, refresh_rate=0.25):
        super().__init__()

        self.cryo = cryo

        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW",self.quit_app)

        self.initialize()

        # 4. a bit of parallelization to update...
        self._rate = refresh_rate
        self.running=True
        self.thread1=threading.Thread(target=self.update)
        self.thread1.daemon=True
        self.thread1.start()


    def initialize(self):
        """ Create gui """

        # 1. Read Temperature
        ttk.Label(self,text="Temperature: ").grid(row=0,column=0)
        self._temperature=tk.StringVar(self,"")
        self.get_temperature()
        ttk.Label(self,textvariable=self._temperature).grid(row=0,column=1)

        # 2. Control Setpoint
        self._setpoint=tk.StringVar(self,"")
        self.get_setpoint()
        ttk.Label(self,text="Setpoint: ").grid(row=1,column=0)
        entry=ttk.Entry(self,textvariable=self._setpoint)
        entry.grid(row=1,column=1)
        entry.bind("<Return>",self.set_setpoint)  #give callback for event listener

        # 3. Connect/Disconnect
        self._is_connected=tk.StringVar(self,"")
        self.get_connection()
        connect_button=ttk.Button(self,textvariable=self._is_connected,command=self.toggle_connection)
        connect_button.grid(row=2,column=0,columnspan=2)



    def update(self):
        while self.running:
            self.get_connection()
            self.get_temperature()
            time.sleep(self._rate)


    def toggle_connection(self):
        if self.cryo.is_connected:
            self.cryo.close_connection()
        else:
            self.cryo.open_connection()
        self.get_connection()

    def get_connection(self):
        string = "Connected" if self.cryo.is_connected else "Disconnected"
        self._is_connected.set(string)

    def get_temperature(self):
        self._temperature.set("%.2f C"%self.cryo.read_temperature())

    def get_setpoint(self):
        self._setpoint.set(str(self.cryo.setpoint))

    def set_setpoint(self,*args):
        if self.cryo.is_connected:
            setpoint = float(self._setpoint.get())
            self.cryo.set_setpoint(setpoint)
        else:
            messagebox.showwarning(title="Oops!",message="Cannot change setpoint when not connected")
        self.get_setpoint()

    def quit_app(self):
        self.cryo.close_connection()
        self.running = False
        self.destroy()



if __name__=="__main__":
    cryo = Cyro()
    app = App(cryo)
    app.mainloop()
