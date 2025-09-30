class Dog:
    def speak(self):
        return "Woof"

class Cat:
    def speak(self):
        return "Meow"

class Creator:
    types = {"dog": Dog, "cat": Cat}

    def produce(self, kind):
        return self.types[kind]()

if __name__ == "__main__":
    c = Creator()
    animal = c.produce("dog")
    print(animal.speak())