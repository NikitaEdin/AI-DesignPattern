class PersonBuilder:
    def __init__(self):
        self.person = {}

    def add_name(self, name):
        self.person['name'] = name
        return self

    def add_age(self, age):
        self.person['age'] = age
        return self

    def add_gender(self, gender):
        self.person['gender'] = gender
        return self

    def build(self):
        return self.person

# Usage example
def main():
    person = PersonBuilder().add_name('Alice').add_age(30).add_gender('female').build()
    print(person)

if __name__ == '__main__':
    main()