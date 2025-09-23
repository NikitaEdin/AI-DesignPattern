class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalShelter:
    def adopt_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Unknown animal type")

if __name__ == "__main__":
    shelter = AnimalShelter()
    dog = shelter.adopt_animal("dog")
    cat = shelter.adopt_animal("cat")
    print(dog.speak())
    print(cat.speak())