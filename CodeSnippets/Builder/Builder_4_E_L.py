class CarBuilder:
    def __init__(self):
        self.car = {}
    
    def add_engine(self, engine):
        self.car["engine"] = engine
        return self
    
    def add_transmission(self, transmission):
        self.car["transmission"] = transmission
        return self
    
    def add_brakes(self, brakes):
        self.car["brakes"] = brakes
        return self
    
    def add_suspension(self, suspension):
        self.car["suspension"] = suspension
        return self
    
    def get_car(self):
        return self.car
    
# Main
if __name__ == "__main__":
    car = CarBuilder()\
            .add_engine("V6")\
            .add_transmission("Manual")\
            .add_brakes("ABS")\
            .add_suspension("MacPherson Strut")\
            .get_car()
    print(car)