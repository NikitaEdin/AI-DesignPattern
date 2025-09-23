class Duck:
    def quack(self):
        pass

class WildDuck(Duck):
    def quack(self):
        print("Quack")

class Turkey:
    def gobble(self):
        print("Gobble gobble")

class TurkeyDuck(Duck):
    def __init__(self, turkey):
        self.turkey = turkey

    def quack(self):
        self.turkey.gobble()

if __name__ == "__main__":
    wild_duck = WildDuck()
    wild_duck.quack()

    turkey = Turkey()
    turkey_duck = TurkeyDuck(turkey)
    turkey_duck.quack()