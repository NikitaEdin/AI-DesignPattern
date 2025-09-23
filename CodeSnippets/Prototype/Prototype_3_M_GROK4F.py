class Engine:
    def __init__(self, engine_type, horsepower):
        if not isinstance(horsepower, int) or horsepower <= 0:
            raise ValueError("Horsepower must be a positive integer")
        self.engine_type = engine_type
        self.horsepower = horsepower

    def __str__(self):
        return f"{self.engine_type} engine ({self.horsepower} hp)"

class Vehicle:
    def __init__(self, make, model, year, engine):
        if not make or not model or not isinstance(year, int) or year < 1886:
            raise ValueError("Invalid vehicle details")
        self.make = make
        self.model = model
        self.year = year
        self.engine = engine

    def clone(self):
        new_engine = Engine(self.engine.engine_type, self.engine.horsepower)
        return Vehicle(self.make, self.model, self.year, new_engine)

    def display(self):
        print(f"{self.year} {self.make} {self.model} with {self.engine}")

if __name__ == "__main__":
    try:
        base_engine = Engine("V6", 300)
        original_vehicle = Vehicle("Ford", "Mustang", 2023, base_engine)
        original_vehicle.display()

        cloned_vehicle = original_vehicle.clone()
        cloned_vehicle.make = "Chevrolet"
        cloned_vehicle.model = "Camaro"
        cloned_vehicle.engine.horsepower = 350

        print("\nAfter modifications:")
        original_vehicle.display()
        cloned_vehicle.display()
    except ValueError as e:
        print(f"Error: {e}")