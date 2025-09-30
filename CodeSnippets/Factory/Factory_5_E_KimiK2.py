class Cat:
    def speak(self):
        return "Meow"

class Dog:
    def speak(self):
        return "Bark"

class Bird:
    def speak(self):
        return "Tweet"

class Creator:
    @staticmethod
    def make(type_name):
        if type_name == "cat":
            return Cat()
        elif type_name == "dog":
            return Dog()
        elif type_name == "bird":
            return Bird()

if __name__ == "__main__":
    animals = ["cat", "dog", "bird"]
    for a in animals:
        creature = Creator.make(a)
        print(creature.speak())