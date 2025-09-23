class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class AnimalCreator:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            return None

if __name__ == "__main__":
    creator = AnimalCreator()
    
    dog = creator.create_animal("dog")
    cat = creator.create_animal("cat")
    
    print(dog.speak())
    print(cat.speak())