class NameCollection:
    def __init__(self):
        self.names = []

    def add_name(self, name):
        self.names.append(name)

    def create_traversal(self):
        return NameTraversal(self.names)

class NameTraversal:
    def __init__(self, names):
        self.names = names
        self.index = 0

    def has_next(self):
        return self.index < len(self.names)

    def next_name(self):
        if self.has_next():
            name = self.names[self.index]
            self.index += 1
            return name
        return None

if __name__ == "__main__":
    collection = NameCollection()
    collection.add_name("Alice")
    collection.add_name("Bob")
    collection.add_name("Charlie")
    traversal = collection.create_traversal()
    while traversal.has_next():
        print(traversal.next_name())