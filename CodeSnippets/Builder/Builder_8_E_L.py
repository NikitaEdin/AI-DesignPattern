# Your code here

class HouseBuilder(object):
    def __init__(self, house_type):
        self.house_type = house_type

    def build_basic_house(self):
        return BasicHouse()

    def build_luxury_house(self):
        return LuxuryHouse()

class BasicHouse(object):
    def __init__(self):
        self.walls = [Wall(), Wall()]
        self.roof = Roof()
        self.windows = [Window(), Window()]
        self.doors = [Door(), Door()]

class LuxuryHouse(object):
    def __init__(self):
        self.walls = [Wall(), Wall()]
        self.roof = Roof()
        self.windows = [Window(), Window()]
        self.doors = [Door(), Door()]
        self.luxury_features = ["hardwood floors", "marble countertops"]

class Wall(object):
    def __init__(self):
        self.height = 10
        self.width = 20

class Roof(object):
    def __init__(self):
        self.shape = "flat"
        self.size = "large"

class Window(object):
    def __init__(self):
        self.height = 15
        self.width = 25

class Door(object):
    def __init__(self):
        self.height = 20
        self.width = 30

def main():
    basic_house = HouseBuilder("basic").build_basic_house()
    luxury_house = HouseBuilder("luxury").build_luxury_house()

    print(f"Basic House: {basic_house}")
    print(f"Luxury House: {luxury_house}")

if __name__ == "__main__":
    main()