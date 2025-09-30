class DataStream:
    def __init__(self, data):
        self._data = data
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._data):
            raise StopIteration
        value = self._data[self._index]
        self._index += 1
        return value

    def __len__(self):
        return len(self._data)

    def reset(self):
        self._index = 0


class ReverseStream:
    def __init__(self, data):
        self._data = data
        self._index = len(data) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < 0:
            raise StopIteration
        value = self._data[self._index]
        self._index -= 1
        return value


class FilteredStream:
    def __init__(self, stream, predicate):
        self._stream = stream
        self._predicate = predicate
        self._next = None
        self._exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._exhausted:
            raise StopIteration
        while True:
            try:
                item = next(self._stream)
                if self._predicate(item):
                    return item
            except StopIteration:
                self._exhausted = True
                raise


class SkipStream:
    def __init__(self, stream, n):
        self._stream = stream
        self._remaining = n
        self._started = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self._started:
            self._started = True
            for _ in range(self._remaining):
                next(self._stream)
        return next(self._stream)


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    base = DataStream(data)
    print("Forward:", list(base))

    rev = ReverseStream(data)
    print("Reverse:", list(rev))

    even = FilteredStream(DataStream(data), lambda x: x % 2 == 0)
    print("Even:", list(even))

    skip = SkipStream(DataStream(data), 5)
    print("Skip first 5:", list(skip))