class NameCollection:
    def __init__(self):
        self.names = ["Alice", "Bob", "Charlie"]

    def create_traverser(self):
        return NameTraverser(self)

class NameTraverser:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.collection.names):
            name = self.collection.names[self.index]
            self.index += 1
            return name
        raise StopIteration

if __name__ == "__main__":
    collection = NameCollection()
    traverser = collection.create_traverser()
    for name in traverser:
        print(name)