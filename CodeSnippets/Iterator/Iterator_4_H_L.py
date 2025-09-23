class MyIterator:
    def __init__(self, my_list):
        self.my_list = my_list
        self.index = 0
    
    def hasNext(self):
        return self.index < len(self.my_list)
    
    def next(self):
        if not self.hasNext():
            raise StopIteration()
        item = self.my_list[self.index]
        self.index += 1
        return item

class MyList:
    def __init__(self, my_list):
        self.my_list = my_list
    
    def getIterator(self):
        return MyIterator(self.my_list)

# Usage example
my_list = [1, 2, 3]
it = MyList(my_list).getIterator()
while it.hasNext():
    print(it.next())