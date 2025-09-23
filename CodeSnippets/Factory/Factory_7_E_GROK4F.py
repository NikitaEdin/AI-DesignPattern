class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

class AnimalProvider:
    def get_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        return None

if __name__ == "__main__":
    provider = AnimalProvider()
    dog = provider.get_animal("dog")
    print(dog.speak())
    cat = provider.get_animal("cat")
    print(cat.speak())