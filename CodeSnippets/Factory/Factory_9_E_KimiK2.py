class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

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
    animal1 = c.make("dog")
    animal2 = c.make("cat")
    print(animal1.speak())
    print(animal2.speak())