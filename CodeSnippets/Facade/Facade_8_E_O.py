class Engine:
    def on(self): print("Engine started")
    def off(self): print("Engine stopped")

class Lights:
    def on(self): print("Lights on")
    def off(self): print("Lights off")

class CarController:
    def __init__(self):
        self._engine = Engine(); self._lights = Lights()
    def start(self):
        self._lights.on(); self._engine.on(); print("Car is ready")
    def stop(self):
        self._engine.off(); self._lights.off(); print("Car is stopped")

if __name__ == "__main__":
    controller = CarController()
    controller.start()
    controller.stop()