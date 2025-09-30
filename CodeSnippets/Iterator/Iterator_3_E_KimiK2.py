class Items:
    def __init__(self):
        self.data = []
        self.index = 0
    
    def append(self, value):
        self.data.append(value)
    
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
    items = Items()
    for v in ["a", "b", "c"]:
        items.append(v)
    for v in items:
        print(v)