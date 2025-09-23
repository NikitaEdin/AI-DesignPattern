class House:
    def __init__(self):
        self.walls = None
        self.roof = None
        self.windows = None

    def __str__(self):
        return f"House: walls={self.walls}, roof={self.roof}, windows={self.windows}"

class HouseMaker:
    def __init__(self):
        self.house = House()

    def add_walls(self):
        self.house.walls = "wooden walls"

    def add_roof(self):
        self.house.roof = "tiled roof"

    def add_windows(self):
        self.house.windows = "glass windows"

    def get_house(self):
        return self.house

if __name__ == "__main__":
    maker = HouseMaker()
    maker.add_walls()
    maker.add_roof()
    maker.add_windows()
    house = maker.get_house()
    print(house)