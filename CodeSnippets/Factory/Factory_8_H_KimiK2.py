import threading
import weakref
from typing import Dict, Type, Optional, Any

class Product:
    def __init__(self, name: str):
        self.name = name

    def produce(self) -> str:
        return f"Produced {self.name}"

class ProductA(Product):
    def __init__(self):
        super().__init__("ProductA")

    def produce(self) -> str:
        return f"Produced {self.name} with special handling"

class ProductB(Product):
    def __init__(self):
        super().__init__("ProductB")

    def produce(self) -> str:
        return f"Produced {self.name} with advanced features"

class Registry:
    _instance: Optional['Registry'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'Registry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._products: Dict[str, Type[Product]] = {}
                    cls._instance._lazy_loaders: Dict[str, Any] = {}
        return cls._instance

    def register(self, key: str, product_class: Type[Product]) -> None:
        with self._lock:
            self._products[key] = product_class

    def register_lazy(self, key: str, loader: Any) -> None:
        with self._lock:
            self._lazy_loaders[key] = loader

    def create(self, key: str) -> Product:
        with self._lock:
            if key in self._lazy_loaders:
                product_class = self._lazy_loaders[key]()
                self._products[key] = product_class
                del self._lazy_loaders[key]
            if key not in self._products:
                raise ValueError(f"Unknown product: {key}")
            return self._products[key]()

class Creator:
    def __init__(self):
        self.registry = Registry()

    def register_product(self, key: str, product_class: Type[Product]) -> None:
        self.registry.register(key, product_class)

    def register_lazy_product(self, key: str, loader: Any) -> None:
        self.registry.register_lazy(key, loader)

    def manufacture(self, key: str) -> Product:
        return self.registry.create(key)

if __name__ == "__main__":
    creator = Creator()
    creator.register_product("A", ProductA)
    creator.register_lazy_product("B", lambda: ProductB)

    product1 = creator.manufacture("A")
    print(product1.produce())

    product2 = creator.manufacture("B")
    print(product2.produce())