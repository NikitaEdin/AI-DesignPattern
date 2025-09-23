```python
class PersonBuilder:
    def __init__(self):
        self.person = {}

    def add_name(self, name):
        self.person["name"] = name
        return self

    def add_age(self, age):
        self.person["age"] = age
        return self

    def build(self):
        return Person(**self.person)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Usage example
builder = PersonBuilder()
builder.add_name("Alice").add_age(30).build()
  ```