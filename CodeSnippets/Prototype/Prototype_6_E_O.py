import copy

class Item:
    def clone(self):
        raise NotImplementedError

class Person(Item):
    def __init__(self, name, contacts):
        self.name = name
        self.contacts = contacts
    def clone(self):
        return copy.deepcopy(self)

def main():
    original = Person('Alice', {'email': 'a@example.com'})
    copy1 = original.clone()
    copy1.name = 'Bob'
    copy1.contacts['email'] = 'b@example.com'
    print(original.name, original.contacts)
    print(copy1.name, copy1.contacts)

if __name__ == '__main__':
    main()