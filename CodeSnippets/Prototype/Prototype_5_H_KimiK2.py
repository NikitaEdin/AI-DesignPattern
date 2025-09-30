import copy
import uuid
from typing import Any, Dict

class Registry:
    _templates: Dict[str, 'Product'] = {}

    @classmethod
    def add(cls, key: str, product: 'Product') -> None:
        cls._templates[key] = product

    @classmethod
    def get(cls, key: str) -> 'Product':
        return cls._templates[key].clone()

class Product:
    __slots__ = ('_id', 'name', 'specs', '_mutable')

    def __init__(self, name: str, specs: Dict[str, Any], mutable: bool = True):
        self._id = uuid.uuid4()
        self.name = name
        self.specs = specs
        self._mutable = mutable

    def clone(self, deep: bool = True) -> 'Product':
        new_obj = copy.deepcopy(self) if deep else copy.copy(self)
        new_obj._id = uuid.uuid4()
        return new_obj

    def __repr__(self) -> str:
        return f"{self.name}(id={self._id})"

class Assembler:
    @staticmethod
    def build_standard() -> Product:
        return Product("Standard", {"cores": 4, "ram": 8})

    @staticmethod
    def build_performance() -> Product:
        return Product("Performance", {"cores": 16, "ram": 64})

if __name__ == "__main__":
    Registry.add("standard", Assembler.build_standard())
    Registry.add("performance", Assembler.build_performance())

    base = Registry.get("standard")
    custom = base.clone()
    custom.specs["ram"] = 32

    perf = Registry.get("performance")
    perf_copy = perf.clone(deep=False)
    perf_copy.specs["gpu"] = "RTX4090"

    print(base)
    print(custom)
    print(perf)
    print(perf_copy)