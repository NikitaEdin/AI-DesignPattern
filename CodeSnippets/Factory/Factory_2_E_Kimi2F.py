class Dog:
    def speak(self):
        return "Woof"

class Cat:
    def speak(self):
        return "Meow"

class Creator:
    @staticmethod
    def make(type_):
        if type_ == "dog":
            return Dog()
        elif type_ == "cat":
            return Cat()
        raise ValueError("Unknown type")

if __name__ == "__main__":
    a = Creator.make("dog")
    b = Creator.make("cat")
    print(a.speak(), b.speak())