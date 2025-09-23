class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def get_info(self):
        return f"My name is {self.name} and I am {self.age} years old."

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    
    def get_info(self):
        return super().get_info() + f"\nI am a {self.breed}."

class Cat(Animal):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    def get_info(self):
        return super().get_info() + f"\nMy fur is {self.color}."

def main():
    dog1 = Dog("Fido", 3, "Golden Retriever")
    cat1 = Cat("Whiskers", 2, "Orange")
    print(dog1.get_info())
    print(cat1.get_info())

if __name__ == "__main__":
    main()