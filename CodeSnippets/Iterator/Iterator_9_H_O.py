class ConcurrentModificationError(RuntimeError):
    pass

class EndOfSequenceError(StopIteration):
    pass

class SequenceContainer:
    def __init__(self, items=None):
        self._items = list(items) if items else []
        self._version = 0

    def add(self, item):
        self._items.append(item)
        self._version += 1

    def remove_at(self, index):
        if not 0 <= index < len(self._items):
            raise IndexError("index out of range")
        del self._items[index]
        self._version += 1

    def get(self, index):
        return self._items[index]

    def size(self):
        return len(self._items)

    def snapshot_version(self):
        return self._version

    def create_cursor(self, start=None, step=1, reverse=False, predicate=None):
        if step == 0:
            raise ValueError("step must be non-zero")
        if start is None:
            start = (self.size() - 1) if reverse else 0
        return Cursor(self, start, abs(step), -1 if reverse else 1, predicate)

class Cursor:
    def __init__(self, container, start, step, direction, predicate):
        self._container = container
        self._expected = container.snapshot_version()
        self._step = step
        self._dir = direction
        self._pos = start
        self._predicate = predicate

    def _check_mod(self):
        if self._expected != self._container.snapshot_version():
            raise ConcurrentModificationError("container modified during traversal")

    def has_more(self):
        self._check_mod()
        sz = self._container.size()
        i = self._pos
        while 0 <= i < sz:
            v = self._container.get(i)
            if self._predicate is None or self._predicate(v):
                return True
            i += self._dir * self._step
        return False

    def get_next(self):
        self._check_mod()
        sz = self._container.size()
        while 0 <= self._pos < sz:
            v = self._container.get(self._pos)
            self._pos += self._dir * self._step
            if self._predicate is None or self._predicate(v):
                return v
        raise EndOfSequenceError("no more elements")

    def peek(self):
        self._check_mod()
        sz = self._container.size()
        i = self._pos
        while 0 <= i < sz:
            v = self._container.get(i)
            if self._predicate is None or self._predicate(v):
                return v
            i += self._dir * self._step
        raise EndOfSequenceError("no more elements to peek")

    def reset(self, start=None):
        self._check_mod()
        if start is None:
            self._pos = (self._container.size() - 1) if self._dir < 0 else 0
        else:
            self._pos = start

    def clone(self):
        c = object.__new__(self.__class__)
        c._container = self._container
        c._expected = self._expected
        c._step = self._step
        c._dir = self._dir
        c._pos = self._pos
        c._predicate = self._predicate
        return c

    def collect_remaining(self, limit=None):
        out = []
        count = 0
        while limit is None or count < limit:
            try:
                out.append(self.get_next())
            except EndOfSequenceError:
                break
            count += 1
        return out

if __name__ == "__main__":
    data = SequenceContainer(range(1, 11))
    even_pred = lambda x: x % 2 == 0
    c1 = data.create_cursor(step=2, predicate=even_pred)
    print("Traversal c1:", end=" ")
    while c1.has_more():
        print(c1.get_next(), end=" ")
    print()

    data.add(12)
    c2 = data.create_cursor(start=0, step=1)
    print("First three from c2:", c2.collect_remaining(limit=3))

    c3 = data.create_cursor()
    print("c3 peek:", c3.peek())
    v1 = c3.get_next()
    v2 = c3.get_next()
    clone_c3 = c3.clone()
    print("c3 next after two:", v1, v2)
    print("clone continuing:", clone_c3.collect_remaining())

    c4 = data.create_cursor()
    print("mutate and detect:")
    print(c4.get_next())
    data.add(99)
    try:
        c4.get_next()
    except ConcurrentModificationError as e:
        print("Detected modification:", type(e).__name__)