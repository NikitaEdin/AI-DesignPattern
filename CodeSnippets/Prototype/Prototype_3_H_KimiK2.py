import copy
from typing import Any

class SelfReplicator:
    __slots__ = ('_registry', '_deep')

    def __init__(self, deep: bool = True):
        self._registry: dict[str, Any] = {}
        self._deep = deep

    def register(self, key: str, instance: Any) -> None:
        if not hasattr(instance, 'clone'):
            raise TypeError("Instance must provide a clone() method")
        self._registry[key] = instance

    def spawn(self, key: str, **overrides) -> Any:
        if key not in self._registry:
            raise KeyError(f"Key '{key}' not registered")
        base = self._registry[key]
        new_obj = base.clone()
        for k, v in overrides.items():
            setattr(new_obj, k, v)
        return new_obj

class Document:
    __slots__ = ('title', 'content', 'metadata')

    def __init__(self, title: str = "", content: str = "", metadata: dict = None):
        self.title = title
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"{self.title} | {self.content[:20]}... | {self.metadata}"

class Spreadsheet:
    __slots__ = ('rows', 'cols', 'cells', 'formatting')

    def __init__(self, rows: int = 10, cols: int = 5):
        self.rows = rows
        self.cols = cols
        self.cells = [[0 for _ in range(cols)] for _ in range(rows)]
        self.formatting = {}

    def clone(self):
        new_sheet = copy.deepcopy(self)
        new_sheet.cells = [row[:] for row in self.cells]
        return new_sheet

    def set_cell(self, r, c, val):
        self.cells[r][c] = val

    def __str__(self):
        return f"Sheet {self.rows}x{self.cols} | sample cell: {self.cells[0][0]}"

if __name__ == "__main__":
    factory = SelfReplicator()

    doc = Document("Template", "Once upon a time...", {"author": "AI"})
    factory.register("report", doc)

    sheet = Spreadsheet(5, 3)
    sheet.set_cell(0, 0, 100)
    factory.register("budget", sheet)

    r1 = factory.spawn("report", title="Q1 Report")
    r2 = factory.spawn("report", content="In the beginning...")
    s1 = factory.spawn("budget", rows=8)
    s1.set_cell(1, 1, 250)

    print(r1)
    print(r2)
    print(s1)