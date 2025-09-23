class PersonBuilder:
    def __init__(self):
        self.name = None
        self.age = None
        self.gender = None

    def set_name(self, name):
        self.name = name
        return self

    def set_age(self, age):
        self.age = age
        return self

    def set_gender(self, gender):
        self.gender = gender
        return self

    def build(self):
        return Person(self.name, self.age, self.gender)

class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender