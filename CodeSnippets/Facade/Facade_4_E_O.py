class Engine:
    def start(self):
        return "Engine: started"

class Lights:
    def on(self):
        return "Lights: on"

class Radio:
    def play(self):
        return "Radio: playing"

class CarController:
    def __init__(self):
        self.engine = Engine()
        self.lights = Lights()
        self.radio = Radio()

    def prepare_trip(self):
        parts = [
            self.lights.on(),
            self.engine.start(),
            self.radio.play()
        ]
        return " | ".join(parts)

if __name__ == "__main__":
    controller = CarController()
    print(controller.prepare_trip())