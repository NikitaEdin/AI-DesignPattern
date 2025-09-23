class MyIterator():
    def __init__(self, my_list):
        self.my_list = my_list
        self.current = 0
    
    def hasNext(self):
        return self.current < len(self.my_list)
    
    def next(self):
        if self.hasNext():
            item = self.my_list[self.current]
            self.current += 1
            return item
        else:
            raise StopIteration()
    
    def __iter__(self):
        return self

# Usage example
if __name__ == "__main__":
    my_list = [1, 2, 3, 4, 5]
    iterator = MyIterator(my_list)
    for item in iterator:
        print(item)