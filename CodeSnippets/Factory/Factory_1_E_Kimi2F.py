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
    a = c.make("dog")
    b = c.make("cat")
    print(a.speak())
    print(b.speak())