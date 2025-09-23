class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

class AnimalCreator:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError("Unknown animal type")

if __name__ == "__main__":
    creator = AnimalCreator()
    dog = creator.create_animal("dog")
    print(dog.speak())
    cat = creator.create_animal("cat")
    print(cat.speak())