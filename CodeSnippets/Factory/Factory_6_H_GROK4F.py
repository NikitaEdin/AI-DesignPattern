from abc import ABC, abstractmethod
from typing import Dict, Type, Any

class Animal(ABC):
    @abstractmethod
    def make_sound(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class Dog(Animal):
    def __init__(self, breed: str = "Unknown"):
        self.breed = breed

    def make_sound(self) -> str:
        return "Woof!"

    def __str__(self) -> str:
        return f"Dog ({self.breed})"

class Cat(Animal):
    def __init__(self, color: str = "Tabby"):
        self.color = color

    def make_sound(self) -> str:
        return "Meow!"

    def __str__(self) -> str:
        return f"Cat ({self.color})"

class Bird(Animal):
    def __init__(self, species: str = "Sparrow"):
        self.species = species

    def make_sound(self) -> str:
        return "Tweet!"

    def __str__(self) -> str:
        return f"Bird ({self.species})"

class Shelter:
    def __init__(self):
        self._registry: Dict[str, Type[Animal]] = {
            "dog": Dog,
            "cat": Cat,
            "bird": Bird
        }
        self._default_params: Dict[str, Dict[str, Any]] = {
            "dog": {"breed": "Labrador"},
            "cat": {"color": "Black"},
            "bird": {"species": "Eagle"}
        }

    def register_type(self, key: str, cls: Type[Animal], default_params: Dict[str, Any] = None):
        if not issubclass(cls, Animal):
            raise ValueError("Registered class must subclass Animal")
        self._registry[key.lower()] = cls
        if default_params:
            self._default_params[key.lower()] = default_params

    def create_pet(self, pet_type: str, **kwargs) -> Animal:
        key = pet_type.lower()
        if key not in self._registry:
            raise ValueError(f"Unknown pet type: {pet_type}. Available: {list(self._registry.keys())}")
        
        cls = self._registry[key]
        params = self._default_params.get(key, {})
        params.update(kwargs)
        try:
            return cls(**params)
        except TypeError as e:
            raise ValueError(f"Invalid parameters for {pet_type}: {e}")

    def list_available_types(self) -> list:
        return list(self._registry.keys())

if __name__ == "__main__":
    shelter = Shelter()
    
    # Basic creation
    dog = shelter.create_pet("dog")
    cat = shelter.create_pet("cat", color="White")
    bird = shelter.create_pet("bird")
    
    print(f"{dog}: {dog.make_sound()}")
    print(f"{cat}: {cat.make_sound()}")
    print(f"{bird}: {bird.make_sound()}")
    
    # Dynamic registration
    class Fish(Animal):
        def __init__(self, species: str = "Goldfish"):
            self.species = species
        
        def make_sound(self) -> str:
            return "Blub!"
        
        def __str__(self) -> str:
            return f"Fish ({self.species})"
    
    shelter.register_type("fish", Fish, {"species": "Tuna"})
    fish = shelter.create_pet("fish")
    print(f"{fish}: {fish.make_sound()}")
    
    # Edge case: invalid type
    try:
        shelter.create_pet("lion")
    except ValueError as e:
        print(f"Error: {e}")
    
    # List types
    print("Available types:", shelter.list_available_types())