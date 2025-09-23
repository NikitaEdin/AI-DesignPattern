class Track:
    def __init__(self, title, artist, length_min):
        self.title = str(title)
        self.artist = str(artist)
        self.length_min = float(length_min)

    def __repr__(self):
        return f"{self.title} by {self.artist} ({self.length_min} min)"


class Playlist:
    def __init__(self):
        self._items = []

    def add(self, track):
        if not isinstance(track, Track):
            raise TypeError("Only Track instances can be added")
        self._items.append(track)

    def remove(self, title):
        for i, t in enumerate(self._items):
            if t.title == title:
                return self._items.pop(i)
        raise ValueError("Track not found")

    def get_cursor(self, start=0, reverse=False, predicate=None):
        return Cursor(self, start, reverse, predicate)

    def __len__(self):
        return len(self._items)

    def _get_at(self, index):
        return self._items[index]


class Cursor:
    def __init__(self, playlist, start=0, reverse=False, predicate=None):
        if not isinstance(playlist, Playlist):
            raise TypeError("Cursor requires a Playlist")
        self._playlist = playlist
        self._predicate = predicate
        self._reverse = bool(reverse)
        self.reset(start)

    def reset(self, start=0):
        if self._reverse:
            self._index = len(self._playlist) - 1 - int(start)
        else:
            self._index = int(start)

    def __iter__(self):
        return self

    def __next__(self):
        while 0 <= self._index < len(self._playlist):
            item = self._playlist._get_at(self._index)
            self._index += -1 if self._reverse else 1
            if not self._predicate or self._predicate(item):
                return item
        raise StopIteration

    def has_more(self):
        temp = Cursor(self._playlist, start=0 if not self._reverse else 0, reverse=self._reverse, predicate=self._predicate)
        temp._index = self._index
        try:
            next(temp)
            return True
        except StopIteration:
            return False


if __name__ == "__main__":
    pl = Playlist()
    pl.add(Track("Morning Sun", "A. Artist", 3.5))
    pl.add(Track("Deep Night", "B. Band", 5.2))
    pl.add(Track("Quick Beat", "C. Crew", 2.1))
    pl.add(Track("Long Journey", "D. Duo", 7.0))

    print("All tracks:")
    for t in pl.get_cursor():
        print(" -", t)

    print("\nFiltered (length > 3):")
    long_only = pl.get_cursor(predicate=lambda tr: tr.length_min > 3)
    for t in long_only:
        print(" *", t)

    print("\nManual forward traversal:")
    c = pl.get_cursor()
    try:
        while True:
            print(" >", next(c))
    except StopIteration:
        pass

    print("\nReverse traversal:")
    for t in pl.get_cursor(reverse=True):
        print(" <", t)