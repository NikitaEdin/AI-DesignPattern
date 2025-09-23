class Engine:
    def start(self):
        return "Engine started"
    
    def stop(self):
        return "Engine stopped"

class Lights:
    def turn_on(self):
        return "Lights on"
    
    def turn_off(self):
        return "Lights off"

class Radio:
    def play(self):
        return "Radio playing"
    
    def stop(self):
        return "Radio stopped"

class CarSystem:
    def __init__(self):
        self.engine = Engine()
        self.lights = Lights()
        self.radio = Radio()
    
    def start_car(self):
        results = []
        results.append(self.engine.start())
        results.append(self.lights.turn_on())
        results.append(self.radio.play())
        return results
    
    def stop_car(self):
        results = []
        results.append(self.radio.stop())
        results.append(self.lights.turn_off())
        results.append(self.engine.stop())
        return results

if __name__ == "__main__":
    car = CarSystem()
    print(car.start_car())
    print(car.stop_car())