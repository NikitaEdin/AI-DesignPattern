class AnimalFactory:
    def __init__(self):
        self.animals = {}
    
    def create_animal(self, animal_type, name, age, species):
        if animal_type not in self.animals:
            raise ValueError("Invalid animal type")
        
        return self.animals[animal_type](name, age, species)
    
    def register_animal(self, animal_type, class_object):
        self.animals[animal_type] = class_object
    
class Dog(AnimalFactory):
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species
    
    def bark(self):
        print("Woof!")
    
class Cat(AnimalFactory):
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species
    
    def meow(self):
        print("Meow!")
    
animal_factory = AnimalFactory()
animal_factory.register_animal("dog", Dog)
animal_factory.register_animal("cat", Cat)

# Usage example
dog = animal_factory.create_animal("dog", "Fido", 3, "Canis lupus familiaris")
dog.bark()
cat = animal_factory.create_animal("cat", "Whiskers", 2, "Felis catus")
cat.meow()