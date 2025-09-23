class PersonBuilder:
    def __init__(self):
        self.person = {}

    def set_name(self, name):
        self.person["name"] = name
        return self

    def set_age(self, age):
        self.person["age"] = age
        return self

    def set_gender(self, gender):
        self.person["gender"] = gender
        return self

    def build(self):
        return Person(**self.person)

class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender