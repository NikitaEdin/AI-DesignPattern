class SimpleNumbers:
    def __init__(self, items):
        self._items = items

    def __iter__(self):
        return Numbers(self._items)


class Numbers:
    def __init__(self, items):
        self._items = items
        self._index = 0

    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        val = self._items[self._index]
        self._index += 1
        return val


if __name__ == "__main__":
    nums = SimpleNumbers([1, 2, 3])
    for n in nums:
        print(n)