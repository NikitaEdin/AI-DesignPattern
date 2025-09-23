from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import RLock
from typing import Callable, Dict, Any, Optional, Type

class ProductBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def operate(self) -> str:
        ...

@dataclass
class PDFDocument(ProductBase):
    title: str
    pages: int = 1

    @property
    def name(self) -> str:
        return "PDF"

    def operate(self) -> str:
        return f"Preparing PDF '{self.title}' with {max(1, int(self.pages))} pages"

@dataclass
class WordDocument(ProductBase):
    title: str
    author: Optional[str] = None

    @property
    def name(self) -> str:
        return "Word"

    def operate(self) -> str:
        author = self.author or "Unknown"
        return f"Composing Word document '{self.title}' by {author}"

@dataclass
class SpreadsheetDocument(ProductBase):
    title: str
    rows: int = 10
    cols: int = 5

    @property
    def name(self) -> str:
        return "Spreadsheet"

    def operate(self) -> str:
        r = max(1, int(self.rows))
        c = max(1, int(self.cols))
        return f"Generating Spreadsheet '{self.title}' with {r}x{c} cells"

Builder = Callable[..., ProductBase]

class ProductMaker:
    def __init__(self) -> None:
        self._registry: Dict[str, Dict[str, Any]] = {}
        self._lock = RLock()
        self._singletons: Dict[str, ProductBase] = {}

    def register(self, key: str, builder: Builder, *, override: bool = False, singleton: bool = False) -> None:
        if not key or not callable(builder):
            raise ValueError("Invalid registration parameters")
        with self._lock:
            if key in self._registry and not override:
                raise KeyError(f"Type '{key}' already registered")
            self._registry[key] = {"builder": builder, "singleton": bool(singleton)}
            if not singleton and key in self._singletons:
                self._singletons.pop(key, None)

    def unregister(self, key: str) -> None:
        with self._lock:
            self._registry.pop(key, None)
            self._singletons.pop(key, None)

    def create(self, key: str, **kwargs) -> ProductBase:
        with self._lock:
            entry = self._registry.get(key)
            if not entry:
                raise KeyError(f"Unknown product type '{key}'")
            if entry["singleton"]:
                if key in self._singletons:
                    return self._singletons[key]
                instance = entry["builder"](**kwargs)
                if not isinstance(instance, ProductBase):
                    raise TypeError("Builder did not return a ProductBase instance")
                self._singletons[key] = instance
                return instance
            instance = entry["builder"](**kwargs)
            if not isinstance(instance, ProductBase):
                raise TypeError("Builder did not return a ProductBase instance")
            return instance

    def available_types(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {k: {"singleton": v["singleton"]} for k, v in self._registry.items()}

def _pdf_builder(**kwargs) -> ProductBase:
    title = kwargs.get("title")
    pages = kwargs.get("pages", 1)
    if not title or not isinstance(title, str):
        raise ValueError("PDF requires a non-empty title string")
    return PDFDocument(title=title, pages=int(pages))

def _word_builder(**kwargs) -> ProductBase:
    title = kwargs.get("title")
    author = kwargs.get("author")
    if not title:
        raise ValueError("Word requires a title")
    return WordDocument(title=str(title), author=(str(author) if author is not None else None))

def _sheet_builder(**kwargs) -> ProductBase:
    title = kwargs.get("title") or "Untitled"
    rows = kwargs.get("rows", 10)
    cols = kwargs.get("cols", 5)
    return SpreadsheetDocument(title=str(title), rows=int(rows), cols=int(cols))

if __name__ == "__main__":
    maker = ProductMaker()
    maker.register("pdf", _pdf_builder)
    maker.register("word", _word_builder, singleton=True)
    maker.register("sheet", _sheet_builder)

    p1 = maker.create("pdf", title="Annual Report", pages=30)
    p2 = maker.create("word", title="Meeting Notes", author="Alice")
    p3 = maker.create("sheet", title="Data", rows=20, cols=8)

    print(p1.operate())
    print(p2.operate())
    print(p3.operate())

    p2b = maker.create("word", title="Ignored Title", author="Bob")
    print("Same word instance:", p2 is p2b)

    try:
        maker.create("unknown", title="X")
    except KeyError as e:
        print("Error:", e)

    maker.register("custom_pdf", lambda **k: PDFDocument(title=k.get("title", "C"), pages=k.get("pages", 2)), override=False)
    custom = maker.create("custom_pdf", title="Custom")
    print(custom.operate())

    print("Available types:", maker.available_types())