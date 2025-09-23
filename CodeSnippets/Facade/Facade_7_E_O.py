class FuelPump:
    def on(self): print("Fuel pump: on")
    def off(self): print("Fuel pump: off")

class Ignition:
    def engage(self): print("Ignition: engaged")
    def disengage(self): print("Ignition: disengaged")

class Stereo:
    def play(self): print("Stereo: playing")
    def stop(self): print("Stereo: stopped")

class CarController:
    def __init__(self):
        self.pump = FuelPump()
        self.ignition = Ignition()
        self.stereo = Stereo()

    def start(self):
        self.pump.on()
        self.ignition.engage()
        self.stereo.play()
        print("Car started")

    def stop(self):
        self.stereo.stop()
        self.ignition.disengage()
        self.pump.off()
        print("Car stopped")

def main():
    controller = CarController()
    controller.start()
    controller.stop()

if __name__ == "__main__":
    main()