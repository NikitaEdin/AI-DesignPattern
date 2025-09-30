class Numbers:
    def __init__(self):
        self.data = [10, 20, 30]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value


if __name__ == "__main__":
    collection = Numbers()
    for item in collection:
        print(item)