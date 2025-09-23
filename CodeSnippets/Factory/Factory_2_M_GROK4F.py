from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

    def prepare(self):
        self.name = "Unknown Animal"

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

    def prepare(self):
        self.name = "Buddy"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

    def prepare(self):
        self.name = "Whiskers"

class AnimalShelter(ABC):
    def create_animal(self):
        try:
            animal = self._make_animal()
            if hasattr(animal, 'prepare'):
                animal.prepare()
            return animal
        except AttributeError as e:
            raise ValueError("Animal creation failed: missing required methods") from e
        except Exception as e:
            raise ValueError(f"Unexpected error during animal creation: {e}") from e

    @abstractmethod
    def _make_animal(self):
        pass

class DogShelter(AnimalShelter):
    def _make_animal(self):
        return Dog()

class CatShelter(AnimalShelter):
    def _make_animal(self):
        return Cat()

if __name__ == "__main__":
    dog_shelter = DogShelter()
    cat_shelter = CatShelter()
    
    dog = dog_shelter.create_animal()
    cat = cat_shelter.create_animal()
    
    print(f"{dog.name} says: {dog.make_sound()}")
    print(f"{cat.name} says: {cat.make_sound()}")