class EndOfSequenceError(Exception):
    pass

class SequenceContainer:
    def __init__(self, source=None):
        self._data = list(source) if source is not None else []

    def add(self, element):
        self._data.append(element)

    def count(self):
        return len(self._data)

    def get_at(self, index):
        if index < 0 or index >= len(self._data):
            raise IndexError("Index out of range")
        return self._data[index]

    def create_cursor(self, direction='forward', predicate=None):
        if predicate is not None and not callable(predicate):
            raise TypeError("predicate must be callable or None")
        return Cursor(self, direction, predicate)

class Cursor:
    def __init__(self, container, direction='forward', predicate=None):
        if direction not in ('forward', 'backward'):
            raise ValueError("direction must be 'forward' or 'backward'")
        self._container = container
        self._predicate = predicate
        self._direction = direction
        self.reset()

    def reset(self):
        self._index = 0 if self._direction == 'forward' else (self._container.count() - 1)
        self._exhausted = False

    def has_more(self):
        if self._exhausted:
            return False
        idx = self._index
        cnt = self._container.count()
        step = 1 if self._direction == 'forward' else -1
        while 0 <= idx < cnt:
            item = self._container.get_at(idx)
            if self._predicate is None or self._predicate(item):
                return True
            idx += step
        self._exhausted = True
        return False

    def next_item(self):
        if not self.has_more():
            raise EndOfSequenceError("No more elements")
        while 0 <= self._index < self._container.count():
            current = self._container.get_at(self._index)
            self._index += 1 if self._direction == 'forward' else -1
            if self._predicate is None or self._predicate(current):
                return current
        raise EndOfSequenceError("No more elements")

if __name__ == '__main__':
    c = SequenceContainer(range(1, 11))
    forward_even = c.create_cursor(direction='forward', predicate=lambda x: x % 2 == 0)
    print("Forward even numbers:")
    while forward_even.has_more():
        print(forward_even.next_item(), end=' ')
    print("\nReverse all numbers:")
    reverse_all = c.create_cursor(direction='backward')
    while reverse_all.has_more():
        print(reverse_all.next_item(), end=' ')
    print()