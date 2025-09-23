class Playlist:
    def __init__(self, name):
        self.name = name
        self._tracks = []
    def add_track(self, track):
        if not isinstance(track, str):
            raise TypeError("track must be a string")
        self._tracks.append(track)
    def open_cursor(self, predicate=None, reverse=False):
        if predicate is not None and not callable(predicate):
            raise ValueError("predicate must be callable or None")
        return TrackCursor(self._tracks, predicate, bool(reverse))
class TrackCursor:
    def __init__(self, tracks, predicate, reverse):
        self._tracks = list(tracks)
        self._predicate = predicate
        self._reverse = reverse
        self.reset()
    def reset(self):
        self._position = len(self._tracks)-1 if self._reverse else 0
        self._ended = False
        self._advance_to_valid()
    def _advance_to_valid(self):
        while 0 <= self._position < len(self._tracks):
            cur = self._tracks[self._position]
            if self._predicate is None or self._predicate(cur):
                return
            self._position += -1 if self._reverse else 1
        self._ended = True
    def has_more(self):
        return not self._ended
    def next_item(self):
        if self._ended:
            raise IndexError("No more items")
        cur = self._tracks[self._position]
        self._position += -1 if self._reverse else 1
        self._advance_to_valid()
        return cur
if __name__ == "__main__":
    pl = Playlist("Favorites")
    for t in ["Song A", "Song B", "Reminder", "Song C"]:
        pl.add_track(t)
    print("Filtered (contain 'Song'):")
    c2 = pl.open_cursor(predicate=lambda s: "Song" in s)
    while c2.has_more():
        print("-", c2.next_item())
    print("\nReverse order:")
    c3 = pl.open_cursor(reverse=True)
    while c3.has_more():
        print("-", c3.next_item())