class Duck:
    def quack(self):
        pass

    def fly(self):
        pass

class Turkey:
    def gobble(self):
        print("Gobble gobble")

    def fly(self):
        print("Flapping wings")

class TurkeyToDuck:
    def __init__(self, turkey):
        self.turkey = turkey

    def quack(self):
        self.turkey.gobble()

    def fly(self):
        self.turkey.fly()

if __name__ == "__main__":
    turkey = Turkey()
    duck = TurkeyToDuck(turkey)
    duck.quack()
    duck.fly()