class StringSet:
    def __init__(self):
        self.data = []

    def add(self, item):
        self.data.append(item)

    def create_traverse(self):
        return StringSetTraverser(self.data)


class StringSetTraverser:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def has_next(self):
        return self.index < len(self.data)

    def next_item(self):
        if not self.has_next():
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value


if __name__ == "__main__":
    s = StringSet()
    s.add("alpha")
    s.add("beta")
    s.add("gamma")
    t = s.create_traverse()
    while t.has_next():
        print(t.next_item())