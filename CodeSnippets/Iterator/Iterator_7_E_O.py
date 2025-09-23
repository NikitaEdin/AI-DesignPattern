class SimpleCollection:
    def __init__(self, items):
        self._items = list(items)
    def create_cursor(self):
        return Cursor(self._items)
class Cursor:
    def __init__(self, items):
        self._items = items
        self._index = 0
    def has_more(self):
        return self._index < len(self._items)
    def next_item(self):
        if not self.has_more(): raise IndexError('No more items')
        val = self._items[self._index]
        self._index += 1
        return val
if __name__ == '__main__':
    col = SimpleCollection([1, 2, 3, 4])
    first = col.create_cursor()
    second = col.create_cursor()
    while first.has_more():
        print('first', first.next_item())
    while second.has_more():
        print('second', second.next_item())