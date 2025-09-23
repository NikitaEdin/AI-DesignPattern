class Inventory:
    def __init__(self, items):
        self._items = items
        self._index = 0
    
    def next(self):
        if self._index >= len(self._items):
            return None
        item = self._items[self._index]
        self._index += 1
        return item
    
    def has_next(self):
        return self._index < len(self._items)