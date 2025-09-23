class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def clone(self):
        return Vehicle(self.make, self.model)

    def display(self):
        return f"{self.make} {self.model}"

if __name__ == "__main__":
    original = Vehicle("Toyota", "Camry")
    cloned = original.clone()
    print(original.display())
    print(cloned.display())
    cloned.model = "Corolla"
    print(original.display())
    print(cloned.display())