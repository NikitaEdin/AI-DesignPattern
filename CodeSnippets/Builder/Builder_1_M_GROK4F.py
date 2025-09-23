class House:
    def __init__(self):
        self.foundation = None
        self.walls = None
        self.roof = None
        self.windows = None

    def __str__(self):
        return f"House with {self.foundation} foundation, {self.walls} walls, {self.roof} roof, and {self.windows} windows."

class HouseConstructor:
    def __init__(self):
        self.reset()

    def reset(self):
        self.house = House()

    def set_foundation(self, material):
        self.house.foundation = material
        return self

    def set_walls(self, material):
        self.house.walls = material
        return self

    def set_roof(self, material):
        self.house.roof = material
        return self

    def set_windows(self, count):
        if count < 0:
            raise ValueError("Window count must be non-negative")
        self.house.windows = f"{count} windows"
        return self

    def get_house(self):
        if not all([self.house.foundation, self.house.walls, self.house.roof]):
            raise ValueError("Essential house parts are missing")
        return self.house

class HouseArchitect:
    def __init__(self, constructor):
        self.constructor = constructor

    def construct_standard_house(self):
        self.constructor.set_foundation("concrete").set_walls("brick").set_roof("shingles").set_windows(6)

    def construct_modern_house(self):
        self.constructor.set_foundation("reinforced concrete").set_walls("glass").set_roof("metal").set_windows(10)

if __name__ == "__main__":
    constructor = HouseConstructor()
    architect = HouseArchitect(constructor)
    architect.construct_standard_house()
    house = constructor.get_house()
    print(house)