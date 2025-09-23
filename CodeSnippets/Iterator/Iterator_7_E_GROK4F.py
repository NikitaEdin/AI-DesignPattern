class NameCollection:
    def __init__(self):
        self.names = []
    def add(self, name):
        self.names.append(name)
    def create_scanner(self):
        return NameScanner(self)

class NameScanner:
    def __init__(self, collection):
        self.collection = collection
        self.position = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.position >= len(self.collection.names):
            raise StopIteration
        name = self.collection.names[self.position]
        self.position += 1
        return name

if __name__ == "__main__":
    collection = NameCollection()
    collection.add("Alice")
    collection.add("Bob")
    scanner = collection.create_scanner()
    for name in scanner:
        print(name)