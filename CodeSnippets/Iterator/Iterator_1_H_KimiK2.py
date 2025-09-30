from __future__ import annotations
import collections.abc as abc
import threading

class _Sentinel:
    def __repr__(self): return "<end>"

_END = _Sentinel()

class Page:
    def __init__(self, content):
        self.content = content

class Chapter:
    def __init__(self, pages):
        self.pages = pages
    def __len__(self): return len(self.pages)

class Book:
    def __init__(self, title, chapters):
        self.title = title
        self._chapters = chapters
    def __len__(self): return sum(len(c) for c in self._chapters)

class BookCursor:
    def __init__(self, book: Book):
        self._book = book
        self._ch_idx = 0
        self._pg_idx = 0
        self._lock = threading.Lock()
        self._mod_count = 0
    def __iter__(self): return self
    def __next__(self):
        with self._lock:
            if self._ch_idx >= len(self._book._chapters):
                raise StopIteration
            current_ch = self._book._chapters[self._ch_idx]
            if self._pg_idx >= len(current_ch.pages):
                self._ch_idx += 1
                self._pg_idx = 0
                self._mod_count += 1
                return self.__next__()
            page = current_ch.pages[self._pg_idx]
            self._pg_idx += 1
            self._mod_count += 1
            return page
    def __bool__(self):
        return self._ch_idx < len(self._book._chapters)
    def current_pos(self):
        with self._lock:
            return self._ch_idx, self._pg_idx
    def go_to_chapter(self, n):
        with self._lock:
            self._ch_idx = max(0, min(n, len(self._book._chapters)))
            self._pg_idx = 0
            self._mod_count += 1
    def __copy__(self):
        twin = BookCursor.__new__(BookCursor)
        twin.__dict__.update(self.__dict__)
        twin._lock = threading.Lock()
        return twin

class BookShelf:
    def __d(self, n):
        return self._cursor.__copy__()
    def __init__(self, cursor):
        self._cursor = cursor
        self._iter = self._cursor.__copy__()
    def __len__(self): return len(self._cursor._book)
    def __iter__(self):
        iter_copy = self._cursor.__copy__()
        return iter_copy
    def reset(self): self._cursor.go_to_chapter(0)

if __name__ == "__main__":
    pages = [Page(f"page {i + 1}") for i in range(4)]
    ch = Chapter(pages)
    book = Book("The Pattern Book", [ch] * 5)
    shelf = BookShelf(BookCursor(book))
    for p in shelf:
        print(p.content)