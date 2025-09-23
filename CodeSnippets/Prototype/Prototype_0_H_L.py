class Animal(object):
    """
    Base class for all animals.
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def move(self):
        print("I'm moving")
    
class Dog(Animal):
    """
    A dog is an animal that can bark and wag its tail.
    """
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    
    def bark(self):
        print("Woof!")
    
    def wag_tail(self):
        print("I'm wagging my tail!")

# Usage example
if __name__ == "__main__":
    dog = Dog("Max", 3, "Golden Retriever")
    dog.bark()
    dog.wag_tail()
    dog2 = dog.clone()
    dog2.name = "Buddy"
    dog2.breed = "Labrador"
    dog2.age = 4
    print(dog)
    print(dog2)

# Output:
I'm moving
Woof!
I'm wagging my tail!
Dog(name='Buddy', age=4, breed='Labrador')
Dog(name='Max', age=3, breed='Golden Retriever')