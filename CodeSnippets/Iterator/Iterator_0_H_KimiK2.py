import weakref, gc

class ReverseList:
    class _Node:
        __slots__ = ('_data', '_prev', '_next')
        def __init__(self, data):
            self._data = data
            self._prev = None
            self._next = None

    class _RevCursor:
        def __init__(self, owner, node):
            self._owner_ref = weakref.ref(owner)
            self._node = node

        def __next__(self):
            if not self._owner_ref():
                raise StopIteration
            node = self._node
            if node is None:
                raise StopIteration
            self._node = node._prev
            return node._data

        def __iter__(self):
            return self

    def __init__(self, seq):
        self._head = None
        self._tail = None
        self._size = 0
        for v in seq:
            self.append(v)

    def append(self, data):
        new_node = ReverseList._Node(data)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            new_node._prev = self._tail
            self._tail._next = new_node
            self._tail = new_node
        self._size += 1
        return self

    def __iter__(self):
        return ReverseList._RevCursor(self, self._tail)

class Filtered:
    def __init__(self, source, pred):
        self._source = source
        self._pred = pred

    def __iter__(self):
        for v in self._source:
            if self._pred(v):
                yield v

if __name__ == "__main__":
    data = ReverseList([10, 20, 30, 40])
    for value in Filtered(data, lambda x: x % 20 == 0):
        print(value)