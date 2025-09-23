import copy

class Prototype(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def clone(self):
        return copy.deepcopy(self)
    
    def print_details(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")

# Usage example
person1 = Prototype("John Doe", 30)
person2 = person1.clone()
person2.name = "Jane Doe"
person2.print_details()