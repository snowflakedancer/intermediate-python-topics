import time
import numpy as np

TIME_CONSTANT = 5
NOISE_LEVEL = 1

class Cryo():
    def __init__(self, setpoint = 25):
        self.setpoint = setpoint
        self.temperature = 25
        self._time = time.time()
        self.is_connected = False

    def set_setpoint(self, temperature):
        if self.is_connected:
            self.setpoint = temperature
        self._time = time.time()

    def read_temperature(self):
        now = time.time()

        diff = now - self._time
        self._time = now

        self.temperature = self.setpoint - (self.setpoint-self.temperature)*np.exp( -diff/TIME_CONSTANT ) + np.random.normal(0,NOISE_LEVEL)
        return self.temperature

    def open_connection(self):
        if not self.is_connected:
            print("Opening connection...")
            time.sleep(3)
        print("Connection opened.")
        self.is_connected = True

    def close_connection(self):
        if self.is_connected:
            print("Connection closed")
        self.is_connected = False

    def __enter__(self,*args):
        self.open_connection()
        return self

    def __exit__(self,*args):
        self.close_connection()


if __name__ == "__main__":
    with Cryo() as c:
        c.set_setpoint(50)
        hist = []
        for _ in range(20):
            t = c.read_temperature()
            hist.append(t)
            time.sleep(1)

    import matplotlib.pyplot as plt
    plt.plot(hist)
    plt.show()