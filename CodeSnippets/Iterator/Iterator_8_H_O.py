class ModificationError(RuntimeError):
    pass

class SequenceCollection:
    def __init__(self, initial=None):
        self._data = list(initial) if initial is not None else []
        self._mod_count = 0

    def add(self, value):
        self._data.append(value)
        self._mod_count += 1

    def insert(self, index, value):
        if index < 0:
            index = 0
        if index > len(self._data):
            index = len(self._data)
        self._data.insert(index, value)
        self._mod_count += 1

    def remove_at(self, index):
        if not (0 <= index < len(self._data)):
            raise IndexError("Index out of range")
        val = self._data.pop(index)
        self._mod_count += 1
        return val

    def get(self, index):
        return self._data[index]

    def length(self):
        return len(self._data)

    def create_cursor(self, start=None, reverse=False, step=1):
        return Cursor(self, start=start, reverse=reverse, step=step)

class Cursor:
    def __init__(self, collection, start=None, reverse=False, step=1):
        if step <= 0:
            raise ValueError("step must be positive")
        self._collection = collection
        self._expected_mod = collection._mod_count
        self._reverse = bool(reverse)
        self._step = int(step)
        length = collection.length()
        if start is None:
            self._index = length - 1 if self._reverse else 0
        else:
            if start < 0:
                start = 0
            if start >= length:
                start = length - 1 if self._reverse else length
            self._index = start
        self._length = length

    def _check_mod(self):
        if self._collection._mod_count != self._expected_mod:
            raise ModificationError("Collection was modified during traversal")

    def has_next(self):
        self._check_mod()
        if self._reverse:
            return 0 <= self._index < self._length
        return 0 <= self._index < self._length

    def next_item(self):
        self._check_mod()
        if not self.has_next():
            raise StopIteration("No more elements")
        val = self._collection.get(self._index)
        if self._reverse:
            self._index -= self._step
        else:
            self._index += self._step
        return val

    def peek(self):
        self._check_mod()
        if not self.has_next():
            raise StopIteration("No more elements")
        return self._collection.get(self._index)

    def skip(self, count):
        self._check_mod()
        if count < 0:
            raise ValueError("count must be non-negative")
        delta = self._step * count
        if self._reverse:
            self._index -= delta
        else:
            self._index += delta
        # clamp to bounds
        if self._index < 0:
            self._index = -1
        if self._index >= self._length:
            self._index = self._length

    def reset(self, start=None, reverse=None):
        self._expected_mod = self._collection._mod_count
        if reverse is not None:
            self._reverse = bool(reverse)
        length = self._collection.length()
        self._length = length
        if start is None:
            self._index = length - 1 if self._reverse else 0
        else:
            if start < 0:
                start = 0
            if start >= length:
                start = length - 1 if self._reverse else length
            self._index = start

    def clone(self):
        copy = object.__new__(Cursor)
        copy._collection = self._collection
        copy._expected_mod = self._expected_mod
        copy._reverse = self._reverse
        copy._step = self._step
        copy._index = self._index
        copy._length = self._length
        return copy

if __name__ == "__main__":
    coll = SequenceCollection(range(10))
    forward = coll.create_cursor()
    while forward.has_next():
        print("FWD", forward.next_item())

    rev = coll.create_cursor(reverse=True)
    while rev.has_next():
        print("REV", rev.next_item())

    c = coll.create_cursor(start=2, step=2)
    print("Peek:", c.peek())
    c.skip(1)
    print("After skip:", c.next_item())

    c1 = coll.create_cursor()
    c2 = c1.clone()
    print("c1 next:", c1.next_item())
    coll.add(100)
    try:
        print("c2 next after modification:", c2.next_item())
    except ModificationError as e:
        print("Detected modification:", e)