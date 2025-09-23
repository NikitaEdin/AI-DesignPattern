import copy

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.accessories = []

    def clone(self):
        cloned = copy.deepcopy(self)
        return cloned

    def add_accessory(self, accessory):
        if isinstance(accessory, str) and accessory.strip():
            self.accessories.append(accessory.strip())
        else:
            raise ValueError("Accessory must be a non-empty string")

    def __str__(self):
        return f"{self.year} {self.make} {self.model} with {len(self.accessories)} accessories"

class Car(Vehicle):
    def __init__(self, make, model, year, doors):
        super().__init__(make, model, year)
        self.doors = doors

    def clone(self):
        cloned = super().clone()
        cloned.doors = self.doors  # Ensure subclass attribute is copied
        return cloned

if __name__ == "__main__":
    original = Car("Toyota", "Camry", 2020, 4)
    original.add_accessory("GPS")
    original.add_accessory("Leather seats")

    clone1 = original.clone()
    clone1.add_accessory("Sunroof")
    clone1.doors = 2

    clone2 = original.clone()
    clone2.add_accessory("Backup camera")

    print(original)  # 2020 Toyota Camry with 2 accessories
    print(clone1)    # 2020 Toyota Camry with 3 accessories (independent)
    print(clone2)    # 2020 Toyota Camry with 3 accessories (independent)