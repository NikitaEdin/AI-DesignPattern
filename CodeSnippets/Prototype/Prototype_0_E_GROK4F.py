class Entity:
    def clone(self):
        raise NotImplementedError("Subclasses must implement clone")

class Car(Entity):
    def __init__(self, make, color):
        self.make = make
        self.color = color

    def clone(self):
        return Car(self.make, self.color)

if __name__ == "__main__":
    original = Car("Toyota", "Red")
    cloned = original.clone()
    cloned.color = "Blue"
    print(f"Original: {original.make} {original.color}")
    print(f"Cloned: {cloned.make} {cloned.color}")