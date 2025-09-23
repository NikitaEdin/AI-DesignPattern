class RecordSet:
    def __init__(self, items=None):
        self._items = list(items) if items is not None else []

    def add(self, item):
        self._items.append(item)

    def remove(self, item):
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError("Item not found in collection") from None

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def create_cursor(self, start=0, step=1, reverse=False):
        return Cursor(self, start=start, step=step, reverse=reverse)


class Cursor:
    def __init__(self, recordset, start=0, step=1, reverse=False):
        if not isinstance(step, int) or step == 0:
            raise ValueError("Step must be a non-zero integer")
        self._snapshot = list(recordset._items)
        if reverse:
            self._snapshot = self._snapshot[::-1]
        length = len(self._snapshot)
        if length == 0:
            self._start = 0
            self._index = 0
            self._step = step
            self._finished = True
            return
        if start < 0:
            start = length + start
        if not (0 <= start < length):
            raise IndexError("Start position out of range")
        self._start = start
        self._index = start
        self._step = step
        self._finished = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._finished or self._index >= len(self._snapshot) or self._index < 0:
            raise StopIteration
        value = self._snapshot[self._index]
        self._index += self._step
        if self._index >= len(self._snapshot) or self._index < 0:
            self._finished = True
        return value

    def reset(self):
        self._index = self._start
        self._finished = False

    def change_step(self, new_step):
        if not isinstance(new_step, int) or new_step == 0:
            raise ValueError("Step must be a non-zero integer")
        self._step = new_step


if __name__ == "__main__":
    records = RecordSet(["alpha", "beta", "gamma", "delta", "epsilon"])
    cursor = records.create_cursor()
    for item in cursor:
        print("seq:", item)

    print("--- step 2 ---")
    cursor2 = records.create_cursor(start=0, step=2)
    for item in cursor2:
        print("skip:", item)

    print("--- reverse from -1 ---")
    cursor3 = records.create_cursor(start=-1, step=1, reverse=True)
    for item in cursor3:
        print("rev:", item)

    print("--- dynamic step change ---")
    cursor4 = records.create_cursor()
    print(next(cursor4))
    cursor4.change_step(2)
    for item in cursor4:
        print("after change:", item)

    try:
        records.create_cursor(step=0)
    except ValueError as e:
        print("caught error:", e)