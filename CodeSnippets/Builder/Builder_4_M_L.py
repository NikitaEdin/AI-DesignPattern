class CarBuilder:
    def __init__(self, brand):
        self.brand = brand
        self.parts = []
        
    def add_engine(self, engine):
        self.parts.append(engine)
        return self
    
    def add_transmission(self, transmission):
        self.parts.append(transmission)
        return self
    
    def add_wheels(self, wheels):
        self.parts.append(wheels)
        return self
    
    def build(self):
        return Car(self.brand, self.parts)

class Car:
    def __init__(self, brand, parts):
        self.brand = brand
        self.parts = parts
    
    def get_description(self):
        return f"A {self.brand} car with {len(self.parts)} parts."
    
def main():
    builder = CarBuilder("Toyota")
    builder.add_engine("2.0L engine").add_transmission("Manual transmission").add_wheels("4-door sedan")
    toyota = builder.build()
    
    print(toyota.get_description())