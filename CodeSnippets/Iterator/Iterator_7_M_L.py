class MyIterator:
    def __init__(self, my_list):
        self.my_list = my_list
        self.index = 0
    
    def __next__(self):
        if self.index < len(self.my_list):
            result = self.my_list[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

# Usage Example
if __name__ == "__main__":
    my_list = [1, 2, 3, 4, 5]
    iterator = MyIterator(my_list)
    for item in iterator:
        print(item)