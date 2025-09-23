class Vehicle:
    def __init__(self, model, color):
        self.model = model
        self.color = color

    def clone(self):
        return self.__class__(self.model, self.color)

class Car(Vehicle):
    def __init__(self, model, color, doors):
        super().__init__(model, color)
        self.doors = doors

    def clone(self):
        cloned = super().clone()
        cloned.doors = self.doors
        return cloned

if __name__ == "__main__":
    original = Car("Toyota", "Red", 4)
    cloned = original.clone()
    cloned.color = "Blue"
    cloned.doors = 2
    print(f"Original: {original.model}, {original.color}, {original.doors}")
    print(f"Cloned: {cloned.model}, {cloned.color}, {cloned.doors}")