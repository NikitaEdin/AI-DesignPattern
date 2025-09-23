class SequenceContainer:
    def __init__(self, items=None):
        self._data = list(items) if items is not None else []
        self._mod_count = 0

    def add(self, item):
        self._data.append(item)
        self._mod_count += 1

    def remove_at(self, index):
        if index < 0 or index >= len(self._data):
            raise IndexError("Index out of range")
        val = self._data.pop(index)
        self._mod_count += 1
        return val

    def size(self):
        return len(self._data)

    def get(self, index):
        return self._data[index]

    def create_cursor(self, direction=1, snapshot=False):
        return Navigator(self, direction, snapshot)


class Navigator:
    def __init__(self, container, direction=1, snapshot=False):
        if direction not in (1, -1):
            raise ValueError("direction must be 1 or -1")
        self._container = container
        self._direction = direction
        self._use_snapshot = bool(snapshot)
        self._snapshot = list(container._data) if snapshot else None
        self._data = self._snapshot if snapshot else container._data
        self._index = 0 if direction == 1 else len(self._data) - 1
        self._last = None
        self._expected = container._mod_count

    def _check_mod(self):
        if not self._use_snapshot and self._expected != self._container._mod_count:
            raise RuntimeError("Concurrent modification detected")

    def has_more(self):
        self._check_mod()
        return (self._index < len(self._data)) if self._direction == 1 else (self._index >= 0)

    def peek(self):
        if not self.has_more():
            raise StopIteration
        return self._data[self._index]

    def advance(self):
        if not self.has_more():
            raise StopIteration
        self._check_mod()
        val = self._data[self._index]
        self._last = self._index
        if self._direction == 1:
            self._index += 1
        else:
            self._index -= 1
        return val

    def current(self):
        if self._last is None:
            raise RuntimeError("No current element")
        return self._data[self._last]

    def remove_current(self):
        self._check_mod()
        if self._last is None:
            raise RuntimeError("No element to remove")
        saved = self._last
        if self._use_snapshot:
            removed = self._snapshot.pop(saved)
            # adjust index relative to snapshot before clearing last
            if self._direction == 1:
                if saved < self._index:
                    self._index -= 1
            else:
                if saved <= self._index:
                    self._index += 1
            self._data = self._snapshot
            self._last = None
            return removed
        else:
            removed = self._container.remove_at(saved)
            # container mod_count updated; sync expected and view
            self._expected = self._container._mod_count
            self._data = self._container._data
            if self._direction == 1:
                if saved < self._index:
                    self._index -= 1
            else:
                if saved <= self._index:
                    self._index += 1
            self._last = None
            return removed

    def reset(self):
        self._check_mod()
        self._data = self._snapshot if self._use_snapshot else self._container._data
        self._index = 0 if self._direction == 1 else len(self._data) - 1
        self._last = None
        self._expected = self._container._mod_count

    def move_to(self, pos):
        self._check_mod()
        if pos < 0 or pos >= len(self._data):
            raise IndexError("Position out of bounds")
        self._index = pos
        self._last = None

    def set_direction(self, direction):
        if direction not in (1, -1):
            raise ValueError("direction must be 1 or -1")
        self._direction = direction

    def remaining_list(self):
        self._check_mod()
        if self._direction == 1:
            start = self._index
            return list(self._data[start:]) if start < len(self._data) else []
        else:
            end = self._index
            return list(reversed(self._data[: end + 1])) if end >= 0 else []


if __name__ == "__main__":
    c = SequenceContainer([1, 2, 3, 4, 5])
    cur = c.create_cursor(direction=1, snapshot=False)
    print(cur.has_more(), cur.peek())
    print(cur.advance())
    print(cur.advance())
    print("current before remove:", cur.current())
    removed = cur.remove_current()
    print("removed:", removed)
    print("remaining (cursor):", cur.remaining_list())
    try:
        c.add(99)  # external modification should break live cursor on next check
        print("external add done")
        print(cur.peek())  # triggers concurrent modification detection
    except RuntimeError as e:
        print("caught:", e)

    snap = c.create_cursor(direction=-1, snapshot=True)
    print("snapshot reverse has_more:", snap.has_more())
    print("snapshot advance:", snap.advance())
    print("snapshot remove:", snap.remove_current())
    print("container after snapshot removal (unchanged):", [c.get(i) for i in range(c.size())])
    print("snapshot remaining:", snap.remaining_list())