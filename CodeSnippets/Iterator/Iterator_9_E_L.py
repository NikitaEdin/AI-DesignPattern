# A simple example of an Iterator class in Python
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