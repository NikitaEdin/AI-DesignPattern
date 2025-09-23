class Engine:
    def __init__(self, engine_type, horsepower):
        self.engine_type = engine_type
        self.horsepower = horsepower

    def __str__(self):
        return f"{self.engine_type} ({self.horsepower} hp)"

class Vehicle:
    def __init__(self, model, color, engine=None):
        if not model or not color:
            raise ValueError("Model and color are required")
        self.model = model
        self.color = color
        self.engine = engine

    def duplicate(self):
        if self.engine is None:
            return Vehicle(self.model, self.color)
        new_engine = Engine(self.engine.engine_type, self.engine.horsepower)
        return Vehicle(self.model, self.color, new_engine)

    def __str__(self):
        engine_info = f" with {self.engine}" if self.engine else " without engine"
        return f"{self.color} {self.model}{engine_info}"

if __name__ == "__main__":
    original_engine = Engine("V6", 300)
    original_vehicle = Vehicle("Sedan", "Blue", original_engine)
    print(f"Original: {original_vehicle}")

    cloned_vehicle = original_vehicle.duplicate()
    cloned_vehicle.color = "Red"
    cloned_vehicle.engine.horsepower = 350 if cloned_vehicle.engine else 0

    print(f"Cloned: {cloned_vehicle}")
    print(f"Original after cloning: {original_vehicle}")
    print("Engines are different objects:", original_vehicle.engine is cloned_vehicle.engine)