class Engine:
    def start(self): print("Engine started")
    def stop(self): print("Engine stopped")
class Lights:
    def on(self): print("Lights on")
    def off(self): print("Lights off")
class Radio:
    def play(self): print("Radio playing")
    def stop(self): print("Radio stopped")
class CarController:
    def __init__(self):
        self.engine = Engine(); self.lights = Lights(); self.radio = Radio()
    def start_trip(self):
        self.engine.start(); self.lights.on(); self.radio.play()
    def end_trip(self):
        self.radio.stop(); self.lights.off(); self.engine.stop()
if __name__ == "__main__":
    controller = CarController(); controller.start_trip(); controller.end_trip()