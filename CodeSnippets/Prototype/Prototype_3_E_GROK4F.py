import copy

class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def clone(self):
        return copy.copy(self)

class Sedan(Vehicle):
    def __init__(self, make, model, doors):
        super().__init__(make, model)
        self.doors = doors

    def clone(self):
        cloned = super().clone()
        cloned.doors = self.doors
        return cloned

if __name__ == "__main__":
    original = Sedan("Toyota", "Camry", 4)
    cloned = original.clone()
    cloned.make = "Honda"
    print(f"Original: {original.make} {original.model}, Doors: {original.doors}")
    print(f"Cloned: {cloned.make} {cloned.model}, Doors: {cloned.doors}")