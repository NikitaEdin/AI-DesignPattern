class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

class AnimalShelter:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Unknown animal type")

if __name__ == "__main__":
    shelter = AnimalShelter()
    dog = shelter.create_animal("dog")
    cat = shelter.create_animal("cat")
    print(dog.speak())
    print(cat.speak())