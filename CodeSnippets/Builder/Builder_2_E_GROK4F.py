class House:
    def __init__(self):
        self.num_doors = 0
        self.num_windows = 0
        self.has_garden = False

    def __str__(self):
        return f"House: {self.num_doors} doors, {self.num_windows} windows, garden: {self.has_garden}"

class HouseCreator:
    def __init__(self):
        self.house = House()

    def add_doors(self, num):
        self.house.num_doors = num
        return self

    def add_windows(self, num):
        self.house.num_windows = num
        return self

    def include_garden(self, has):
        self.house.has_garden = has
        return self

    def build(self):
        return self.house

if __name__ == "__main__":
    creator = HouseCreator()
    house = creator.add_doors(4).add_windows(6).include_garden(True).build()
    print(house)