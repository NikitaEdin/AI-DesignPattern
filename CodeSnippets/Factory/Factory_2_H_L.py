# A simple example of a Factory design pattern in Python
class AnimalFactory:
    def __init__(self, animal_type):
        self.animal_type = animal_type
    
    def get_animal(self):
        if self.animal_type == "dog":
            return Dog()
        elif self.animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Invalid animal type")

class Dog:
    def __init__(self):
        print("A new dog has been created!")
    
    def bark(self):
        print("Woof woof!")

class Cat:
    def __init__(self):
        print("A new cat has been created!")
    
    def meow(self):
        print("Meow!")

def main():
    dog_factory = AnimalFactory("dog")
    dog = dog_factory.get_animal()
    dog.bark()

    cat_factory = AnimalFactory("cat")
    cat = cat_factory.get_animal()
    cat.meow()

if __name__ == "__main__":
    main()