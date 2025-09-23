class Animal(object):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name}"
    
    def __eq__(self, other):
        return isinstance(other, Animal) and self.name == other.name
    
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def __str__(self):
        return f"{super().__str__()} is a {self.breed} dog."
    
def main():
    bob = Dog("Bob", "Golden Retriever")
    sally = Dog("Sally", "Poodle")
    
    print(bob)
    print(sally)
    print(bob == sally)