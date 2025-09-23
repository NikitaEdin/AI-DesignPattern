class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Creator:
    @staticmethod
    def create(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("unknown animal")

if __name__ == "__main__":
    dog = Creator.create("dog")
    cat = Creator.create("cat")
    print(dog.speak())
    print(cat.speak())