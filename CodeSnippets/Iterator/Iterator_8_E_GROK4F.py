class NameCollection:
    def __init__(self):
        self._names = ['Alice', 'Bob', 'Charlie']

    def __iter__(self):
        return NameTraverser(self._names)

class NameTraverser:
    def __init__(self, names):
        self._names = names
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._names):
            name = self._names[self._index]
            self._index += 1
            return name
        raise StopIteration

if __name__ == "__main__":
    collection = NameCollection()
    for name in collection:
        print(name)