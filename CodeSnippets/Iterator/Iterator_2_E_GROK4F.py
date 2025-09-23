class NameList:
    def __init__(self):
        self.names = ['Alice', 'Bob', 'Charlie']

    def __iter__(self):
        return NameWalker(self.names)

class NameWalker:
    def __init__(self, names):
        self.names = names
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.names):
            name = self.names[self.index]
            self.index += 1
            return name
        raise StopIteration

if __name__ == "__main__":
    names = NameList()
    for name in names:
        print(name)