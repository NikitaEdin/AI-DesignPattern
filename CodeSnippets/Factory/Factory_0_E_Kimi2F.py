class Dog:
    def speak(self):
        return "Woof"

class Cat:
    def speak(self):
        return "Meow"

class Creator:
    def make(self, kind):
        if kind == "dog":
            return Dog()
        elif kind == "cat":
            return Cat()
        else:
            raise ValueError("Unknown kind")

if __name__ == "__main__":
    c = Creator()
    a1 = c.make("dog")
    a2 = c.make("cat")
    print(a1.speak())
    print(a2.speak())