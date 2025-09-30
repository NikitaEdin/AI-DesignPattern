class CustomCollection:
    def __init__(self, elements=None):
        self._elements = elements or []
        self._version = 0

    def add(self, item):
        self._elements.append(item)
        self._version += 1

    def remove(self, item):
        if item in self._elements:
            self._elements.remove(item)
            self._version += 1

    def create_sequential(self):
        return SequentialAccess(self)

    def create_reverse(self):
        return ReverseAccess(self)

    def __len__(self):
        return len(self._elements)

    def get_at(self, index):
        return self._elements[index]

    def get_version(self):
        return self._version


class SequentialAccess:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0
        self._version = collection.get_version()

    def has_next(self):
        return self._index < len(self._collection)

    def next(self):
        if self._version != self._collection.get_version():
            raise RuntimeError("Collection modified during iteration")
        if not self.has_next():
            raise StopIteration
        value = self._collection.get_at(self._index)
        self._index += 1
        return value


class ReverseAccess:
    def __init__(self, collection):
        self._collection = collection
        self._index = len(collection) - 1
        self._version = collection.get_version()

    def has_next(self):
        return self._index >= 0

    def next(self):
        if self._version != self._collection.get_version():
            raise RuntimeError("Collection modified during iteration")
        if not self.has_next():
            raise StopIteration
        value = self._collection.get_at(self._index)
        self._index -= 1
        return value


if __name__ == "__main__":
    collection = CustomCollection([10, 20, 30])
    
    seq = collection.create_sequential()
    while seq.has_next():
        print(seq.next())
    
    rev = collection.create_reverse()
    while rev.has_next():
        print(rev.next())