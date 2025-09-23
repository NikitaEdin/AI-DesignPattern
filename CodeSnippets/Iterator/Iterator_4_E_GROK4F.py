class NameCollection:
    def __init__(self):
        self.names = []

    def add_name(self, name):
        self.names.append(name)

    def create_traverser(self):
        return NameTraverser(self)

class NameTraverser:
    def __init__(self, collection):
        self.collection = collection
        self.current_index = 0

    def has_next(self):
        return self.current_index < len(self.collection.names)

    def get_next(self):
        if self.has_next():
            name = self.collection.names[self.current_index]
            self.current_index += 1
            return name
        raise StopIteration

if __name__ == "__main__":
    nc = NameCollection()
    nc.add_name("Alice")
    nc.add_name("Bob")
    nc.add_name("Charlie")
    traverser = nc.create_traverser()
    while traverser.has_next():
        print(traverser.get_next())