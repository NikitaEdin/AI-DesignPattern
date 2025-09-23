class DataStore:
    def __init__(self):
        self._data = []

    def add(self, item):
        self._data.append(item)

    def remove(self, item):
        if item in self._data:
            self._data.remove(item)

    def __iter__(self):
        return Iterator(self._data)

class Iterator:
    def __init__(self, data):
        self._data = data
        self._index = 0

    def __next__(self):
        if self._index < len(self._data):
            item = self._data[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration

store = DataStore()
store.add("apple")
store.add("banana")
store.add("cherry")

for item in store:
    print(item)