class AnimalFactory:
    def __init__(self):
        self.animals = {}

    def create_animal(self, animal_type, name, age):
        if animal_type not in self.animals:
            raise ValueError("Animal type not recognized")
        return self.animals[animal_type](name, age)

class Dog(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print("Woof!")

class Cat(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def meow(self):
        print("Meow!")

# Usage example
animal_factory = AnimalFactory()
dog = animal_factory.create_animal("Dog", "Buddy", 3)
cat = animal_factory.create_animal("Cat", "Fluffy", 2)

dog.bark()
cat.meow()