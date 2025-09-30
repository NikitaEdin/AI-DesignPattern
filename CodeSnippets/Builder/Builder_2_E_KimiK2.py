class Coffee:
    def __init__(self):
        self.type = None
        self.milk = False
        self.sugar = 0
    def __str__(self):
        return f"{self.type} with {self.sugar} sugars{' and milk' if self.milk else ''}"

class Maker:
    def __init__(self):
        self.coffee = Coffee()
    def set_type(self, t):
        self.coffee.type = t
        return self
    def add_milk(self):
        self.coffee.milk = True
        return self
    def add_sugar(self, s):
        self.coffee.sugar = s
        return self
    def create(self):
        return self.coffee

if __name__ == "__main__":
    maker = Maker()
    drink = maker.set_type("Espresso").add_milk().add_sugar(2).create()
    print(drink)