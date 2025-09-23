class Vehicle:
    def clone(self):
        raise NotImplementedError("Clone method must be implemented")

class Car(Vehicle):
    def __init__(self, model="Unknown", year=2020):
        self.model = model
        self.year = year

    def clone(self):
        cloned = Car()
        cloned.model = self.model
        cloned.year = self.year
        return cloned

    def __str__(self):
        return f"{self.model} {self.year}"

if __name__ == "__main__":
    original = Car("Honda", 2019)
    cloned = original.clone()
    print(original)
    print(cloned)
    print(id(original) != id(cloned))