class Duck:
    def quack(self):
        pass

    def fly(self):
        pass

class WildDuck(Duck):
    def quack(self):
        print("Quack!")

    def fly(self):
        print("Flying high!")

class Turkey:
    def gobble(self):
        print("Gobble gobble!")

    def fly(self):
        print("Flapping wings short distance!")

class TurkeyToDuck(Duck):
    def __init__(self, turkey):
        self.turkey = turkey

    def quack(self):
        try:
            self.turkey.gobble()
        except AttributeError:
            print("Turkey cannot gobble properly.")

    def fly(self):
        try:
            self.turkey.fly()
        except AttributeError:
            print("Turkey flight limited.")

if __name__ == "__main__":
    wild_duck = WildDuck()
    turkey = Turkey()
    turkey_wrapper = TurkeyToDuck(turkey)

    print("Wild Duck:")
    wild_duck.quack()
    wild_duck.fly()

    print("\nTurkey as Duck:")
    turkey_wrapper.quack()
    turkey_wrapper.fly()