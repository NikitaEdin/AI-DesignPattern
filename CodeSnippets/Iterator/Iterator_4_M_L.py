class MyIterator:
    def __init__(self, my_list):
        self.my_list = my_list
        self.index = 0

    def __next__(self):
        if self.index < len(self.my_list):
            value = self.my_list[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

class MyCollection:
    def __init__(self, my_list):
        self.my_list = my_list

    def __iter__(self):
        return MyIterator(self.my_list)

if __name__ == "__main__":
    my_collection = MyCollection([1, 2, 3, 4, 5])
    for item in my_collection:
        print(item)