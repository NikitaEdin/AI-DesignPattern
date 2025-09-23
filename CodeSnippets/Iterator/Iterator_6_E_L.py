class MyIterator:
    def __init__(self, my_list):
        self.my_list = my_list
        self.index = 0
    
    def next(self):
        if self.index < len(self.my_list):
            item = self.my_list[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration
    
    def __iter__(self):
        return self