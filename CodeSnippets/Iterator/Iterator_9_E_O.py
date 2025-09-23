class NumberCollection:
    def __init__(self, items):
        self._items = list(items)
    def make_cursor(self):
        return Cursor(self._items)

class Cursor:
    def __init__(self, items):
        self._items = items; self._i = 0
    def __iter__(self): return self
    def __next__(self):
        if self._i >= len(self._items): raise StopIteration
        v = self._items[self._i]; self._i += 1; return v

if __name__ == "__main__":
    c = NumberCollection([1, 2, 3])
    cur = c.make_cursor()
    for x in cur: print(x)
    cur2 = c.make_cursor()
    print(next(cur2), next(cur2), next(cur2))