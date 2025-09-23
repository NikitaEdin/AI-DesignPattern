class NameCollection:
    def __init__(self):
        self._names = ["Alice", "Bob", "Charlie"]

    def __iter__(self):
        return NameWalker(self._names)


class NameWalker:
    def __init__(self, names):
        self._names = names
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._position < len(self._names):
            current = self._names[self._position]
            self._position += 1
            return current
        raise StopIteration


if __name__ == "__main__":
    collection = NameCollection()
    for name in collection:
        print(name)