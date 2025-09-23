class Dog:
    def speak(self):
        return "Woof"

class Cat:
    def speak(self):
        return "Meow"

class Creator:
    @staticmethod
    def build(pet_type):
        if pet_type == "dog":
            return Dog()
        if pet_type == "cat":
            return Cat()
        raise ValueError("Unknown pet type")

if __name__ == "__main__":
    d = Creator.build("dog")
    c = Creator.build("cat")
    print(d.speak())
    print(c.speak())