class Engine:
    def start(self):
        return "Engine: started"

class Lights:
    def turn_on(self):
        return "Lights: on"

class CarController:
    def __init__(self):
        self._engine = Engine()
        self._lights = Lights()
    def prepare_trip(self):
        return f"{self._lights.turn_on()} | {self._engine.start()} | Car ready"

if __name__ == "__main__":
    controller = CarController()
    print(controller.prepare_trip())