class ItemList:
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(item)
    def create_scanner(self):
        return Scanner(self.items)

class Scanner:
    def __init__(self, items):
        self.items = items
        self.index = 0
    def next(self):
        item = self.items[self.index]
        self.index += 1
        return item
    def done(self):
        return self.index >= len(self.items)

if __name__ == "__main__":
    list_ = ItemList()
    for s in ["a", "b", "c"]:
        list_.add(s)
    scanner = list_.create_scanner()
    while not scanner.done():
        print(scanner.next())