class Animal():
    def __init__(self, species):
        self.species = species
    
    def clone(self):
        return Animal(self.species)
    
    def __str__(self):
        return f"{self.species}"
    
class Dog(Animal):
    def __init__(self, species, breed):
        super().__init__(species)
        self.breed = breed
    
    def clone(self):
        return Dog(self.species, self.breed)
    
    def __str__(self):
        return f"{super().__str__()}, {self.breed}"

if __name__ == "__main__":
    dog = Dog("dog", "Golden Retriever")
    print(dog)
    cloned_dog = dog.clone()
    print(cloned_dog)