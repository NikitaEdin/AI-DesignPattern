class NumberGroup:
    def __init__(self):
        self.data = [1, 2, 3, 4, 5]
    
    def __iter__(self):
        return GroupWalker(self.data)


class GroupWalker:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value


if __name__ == "__main__":
    group = NumberGroup()
    for num in group:
        print(num)