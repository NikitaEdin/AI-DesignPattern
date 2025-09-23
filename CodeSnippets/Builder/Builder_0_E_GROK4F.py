class House:
    def __init__(self):
        self.walls = 0
        self.doors = 0
        self.windows = 0
        self.roof = False

class HouseConstructor:
    def __init__(self):
        self.house = House()

    def set_walls(self, num):
        self.house.walls = num
        return self

    def set_doors(self, num):
        self.house.doors = num
        return self

    def set_windows(self, num):
        self.house.windows = num
        return self

    def set_roof(self):
        self.house.roof = True
        return self

    def get_result(self):
        return self.house

if __name__ == "__main__":
    hc = HouseConstructor()
    result = hc.set_walls(4).set_doors(1).set_windows(2).set_roof().get_result()
    print(f"Built house: {result.walls} walls, {result.doors} doors, {result.windows} windows, roof: {result.roof}")