class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def copy(self):
        return Person(self.name, self.age)

    def display(self):
        return f"{self.name}, {self.age} years old"

if __name__ == "__main__":
    original = Person("Alice", 30)
    cloned = original.copy()
    cloned.age = 31
    print(original.display())
    print(cloned.display())