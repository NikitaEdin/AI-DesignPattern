class Duck:
    def quack(self):
        print("Duck quacks.")

class Turkey:
    def gobble(self):
        print("Turkey gobbles.")

class QuackingTurkey:
    def __init__(self, turkey):
        self.turkey = turkey

    def quack(self):
        self.turkey.gobble()

if __name__ == "__main__":
    turkey = Turkey()
    duck_like_turkey = QuackingTurkey(turkey)

    print("Original turkey:")
    turkey.gobble()

    print("\nAdapted turkey as duck:")
    duck_like_turkey.quack()

    print("\nReal duck:")
    mallard = Duck()
    mallard.quack()