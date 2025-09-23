class EndOfSequenceError(Exception):
    pass

class ConcurrentModificationError(RuntimeError):
    pass

class SequenceContainer:
    def __init__(self, items=None):
        self._items = list(items or [])
        self._mod_count = 0

    def add(self, item):
        self._items.append(item)
        self._mod_count += 1

    def insert(self, index, item):
        self._items.insert(index, item)
        self._mod_count += 1

    def remove_at(self, index):
        value = self._items.pop(index)
        self._mod_count += 1
        return value

    def size(self):
        return len(self._items)

    def get(self, index):
        return self._items[index]

    def create_cursor(self, match=None, start=None, forward=True):
        if start is None:
            start = 0 if forward else max(0, len(self._items) - 1)
        return TraversalHandle(self, match, start, forward, self._mod_count)

class TraversalHandle:
    def __init__(self, container, match, index, forward, expected_mod):
        self._container = container
        self._match = match if match is not None else (lambda x: True)
        self._index = index
        self._forward = bool(forward)
        self._expected_mod = expected_mod
        self._last_returned = None

    def _check_mod(self):
        if self._expected_mod != self._container._mod_count:
            raise ConcurrentModificationError("collection modified during traversal")

    def _in_bounds(self, idx):
        return 0 <= idx < self._container.size()

    def has_more(self):
        self._check_mod()
        idx = self._index
        if self._forward:
            while self._in_bounds(idx):
                if self._match(self._container.get(idx)):
                    return True
                idx += 1
            return False
        else:
            while self._in_bounds(idx):
                if self._match(self._container.get(idx)):
                    return True
                idx -= 1
            return False

    def next(self):
        self._check_mod()
        n = self._container.size()
        while self._in_bounds(self._index):
            val = self._container.get(self._index)
            if self._match(val):
                self._last_returned = self._index
                out = val
                self._index = self._index + 1 if self._forward else self._index - 1
                return out
            self._index = self._index + 1 if self._forward else self._index - 1
        raise EndOfSequenceError("no more elements")

    def prev(self):
        self._check_mod()
        step = -1 if self._forward else 1
        idx = self._index + step
        while self._in_bounds(idx):
            val = self._container.get(idx)
            if self._match(val):
                self._last_returned = idx
                self._index = idx
                return val
            idx += step
        raise EndOfSequenceError("no previous matching element")

    def peek(self):
        self._check_mod()
        idx = self._index
        if self._forward:
            while self._in_bounds(idx):
                val = self._container.get(idx)
                if self._match(val):
                    return val
                idx += 1
        else:
            while self._in_bounds(idx):
                val = self._container.get(idx)
                if self._match(val):
                    return val
                idx -= 1
        raise EndOfSequenceError("nothing to peek")

    def reset(self, start=None, forward=None):
        if forward is not None:
            self._forward = bool(forward)
        if start is None:
            self._index = 0 if self._forward else max(0, self._container.size() - 1)
        else:
            self._index = start
        self._last_returned = None
        self._check_mod()

    def skip(self, count):
        if count == 0:
            return
        if count > 0:
            for _ in range(count):
                self.next()
        else:
            for _ in range(-count):
                self.prev()

    def delete(self):
        self._check_mod()
        if self._last_returned is None:
            raise RuntimeError("no element to delete")
        idx = self._last_returned
        self._container.remove_at(idx)
        self._expected_mod = self._container._mod_count
        if self._forward:
            if idx < self._index:
                self._index -= 1
        else:
            if idx > self._index:
                self._index += 1
        self._last_returned = None

    def clone(self):
        copy = TraversalHandle(self._container, self._match, self._index, self._forward, self._expected_mod)
        copy._last_returned = self._last_returned
        return copy

if __name__ == "__main__":
    c = SequenceContainer([1, 2, 3, 4, 5, 6, 7])
    c.add(9)
    handle = c.create_cursor(match=lambda x: x % 2 == 1)  # odd numbers
    collected = []
    while handle.has_more():
        val = handle.next()
        collected.append(val)
        if val == 3:
            handle.delete()
    print("collected after deletion:", collected)
    h2 = handle.clone()
    try:
        print("peek next on clone:", h2.peek())
    except EndOfSequenceError:
        print("clone has nothing to peek")
    h2.reset(forward=False)
    back_list = []
    while True:
        try:
            back_list.append(h2.prev())
        except EndOfSequenceError:
            break
    print("reverse traversal (matching):", back_list)
    # demonstrate concurrent modification detection
    h3 = c.create_cursor()
    c.add(99)
    try:
        h3.next()
    except ConcurrentModificationError as e:
        print("concurrent modification detected:", e)