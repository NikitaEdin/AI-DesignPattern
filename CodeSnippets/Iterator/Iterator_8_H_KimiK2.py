from __future__ import annotations
from typing import Any, List, Optional, Protocol, Tuple
import weakref

class _Book:
    __slots__ = ('_title', '_author', '_year')
    
    def __init__(self, title: str, author: str, year: int):
        self._title = title
        self._author = author
        self._year = year
    
    @property
    def title(self) -> str: return self._title
    @property
    def author(self) -> str: return self._author
    @property
    def year(self) -> int: return self._year
    
    def __repr__(self) -> str:
        return f"_Book('{self._title}', '{self._author}', {self._year})"

class _Traversal(Protocol):
    def __next__(self) -> _Book: ...
    def __iter__(self) -> _Traversal: ...

class _ForwardTraversal:
    __slots__ = ('_catalog_ref', '_index')
    
    def __init__(self, catalog: 'LibraryCatalog'):
        self._catalog_ref = weakref.ref(catalog)
        self._index = 0
    
    def __iter__(self) -> _ForwardTraversal:
        return self
    
    def __next__(self) -> _Book:
        catalog = self._catalog_ref()
        if catalog is None or self._index >= len(catalog._shelf):
            raise StopIteration
        book = catalog._shelf[self._index]
        self._index += 1
        return book

class _ReverseTraversal:
    __slots__ = ('_catalog_ref', '_index')
    
    def __init__(self, catalog: 'LibraryCatalog'):
        self._catalog_ref = weakref.ref(catalog)
        self._index = len(catalog._shelf) - 1
    
    def __iter__(self) -> _ReverseTraversal:
        return self
    
    def __next__(self) -> _Book:
        catalog = self._catalog_ref()
        if catalog is None or self._index < 0:
            raise StopIteration
        book = catalog._shelf[self._index]
        self._index -= 1
        return book

class _FilteredTraversal:
    __slots__ = ('_catalog_ref', '_predicate', '_index')
    
    def __init__(self, catalog: 'LibraryCatalog', predicate):
        self._catalog_ref = weakref.ref(catalog)
        self._predicate = predicate
        self._index = 0
    
    def __iter__(self) -> _FilteredTraversal:
        return self
    
    def __next__(self) -> _Book:
        catalog = self._catalog_ref()
        if catalog is None:
            raise StopIteration
        
        while self._index < len(catalog._shelf):
            book = catalog._shelf[self._index]
            self._index += 1
            if self._predicate(book):
                return book
        raise StopIteration

class LibraryCatalog:
    __slots__ = ('_shelf',)
    
    def __init__(self):
        self._shelf: List[_Book] = []
    
    def add(self, book: _Book) -> None:
        self._shelf.append(book)
    
    def __iter__(self) -> _ForwardTraversal:
        return _ForwardTraversal(self)
    
    def reverse(self) -> _ReverseTraversal:
        return _ReverseTraversal(self)
    
    def where(self, predicate) -> _FilteredTraversal:
        return _FilteredTraversal(self, predicate)
    
    def __len__(self) -> int:
        return len(self._shelf)

if __name__ == "__main__":
    catalog = LibraryCatalog()
    catalog.add(_Book("1984", "Orwell", 1949))
    catalog.add(_Book("Dune", "Herbert", 1965))
    catalog.add(_Book("Foundation", "Asimov", 1951))
    
    print("Forward:")
    for book in catalog:
        print(book)
    
    print("\nReverse:")
    for book in catalog.reverse():
        print(book)
    
    print("\nFiltered (year > 1950):")
    for book in catalog.where(lambda b: b.year > 1950):
        print(book)