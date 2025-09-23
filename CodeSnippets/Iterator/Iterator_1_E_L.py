class MyIterator:
    def __init__(self, my_list):
        self.my_list = my_list
        self.index = 0
    
    def has_next(self):
        return self.index < len(self.my_list)
    
    def next(self):
        if not self.has_next():
            raise StopIteration
        item = self.my_list[self.index]
        self.index += 1
        return item

class MyContainer:
    def __init__(self, my_list):
        self.my_list = my_list
    
    def __iter__(self):
        return MyIterator(self.my_list)

if __name__ == '__main__':
    container = MyContainer([1, 2, 3, 4, 5])
    for item in container:
        print(item)