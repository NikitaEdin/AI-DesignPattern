class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def clone(self):
        return Vehicle(self.make, self.model)

if __name__ == "__main__":
    original = Vehicle("Toyota", "Camry")
    cloned = original.clone()
    print(f"Original: {original.make} {original.model}, ID: {id(original)}")
    print(f"Cloned: {cloned.make} {cloned.model}, ID: {id(cloned)}")