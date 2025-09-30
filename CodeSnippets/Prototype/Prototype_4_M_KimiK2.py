import copy

class Vehicle:
    def __init__(self, make, model, color):
        self.make = make
        self.model = model
        self.color = color
        self._options = []

    def add_option(self, option):
        self._options.append(option)

    def clone(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return f"{self.color} {self.make} {self.model} with {self._options}"

class Registry:
    def __init__(self):
        self._templates = {}

    def register(self, name, vehicle):
        self._templates[name] = vehicle

    def get(self, name):
        if name not in self._templates:
            raise ValueError(f"Template '{name}' not found")
        return self._templates[name].clone()

if __name__ == "__main__":
    registry = Registry()

    base_sedan = Vehicle("Tesla", "Model 3", "Red")
    base_sedan.add_option("Autopilot")
    registry.register("base_sedan", base_sedan)

    base_suv = Vehicle("Tesla", "Model Y", "Blue")
    base_suv.add_option("Tow Hitch")
    registry.register("base_suv", base_suv)

    order1 = registry.get("base_sedan")
    order1.color = "White"
    order1.add_option("Full Self-Driving")

    order2 = registry.get("base_suv")
    order2.color = "Black"
    order2.add_option("Third Row")

    print(order1)
    print(order2)