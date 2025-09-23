from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional
import threading
import copy

@dataclass(frozen=True)
class Product:
    name: str
    components: Tuple[str, ...]
    options: Tuple[Tuple[str, Any], ...]
    version: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "components": list(self.components),
            "options": dict(self.options),
            "version": self.version,
        }

class Configurator:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.reset()

    def reset(self) -> "Configurator":
        with self._lock:
            self._name: Optional[str] = None
            self._components: list[str] = []
            self._options: dict[str, Any] = {}
            self._version: int = 1
            self._built: bool = False
            return self

    def set_name(self, name: str) -> "Configurator":
        with self._lock:
            if self._built:
                raise RuntimeError("Instance has been built; call reset() to modify.")
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Name must be a non-empty string.")
            self._name = name.strip()
            return self

    def add_component(self, component: str) -> "Configurator":
        with self._lock:
            if self._built:
                raise RuntimeError("Instance has been built; call reset() to modify.")
            if not isinstance(component, str) or not component.strip():
                raise ValueError("Component must be a non-empty string.")
            comp = component.strip()
            if comp not in self._components:
                self._components.append(comp)
            return self

    def set_option(self, key: str, value: Any) -> "Configurator":
        with self._lock:
            if self._built:
                raise RuntimeError("Instance has been built; call reset() to modify.")
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Option key must be a non-empty string.")
            self._options[key.strip()] = copy.deepcopy(value)
            return self

    def set_version(self, version: int) -> "Configurator":
        with self._lock:
            if self._built:
                raise RuntimeError("Instance has been built; call reset() to modify.")
            if not isinstance(version, int) or version <= 0:
                raise ValueError("Version must be a positive integer.")
            self._version = version
            return self

    def apply_template(self, product: Product) -> "Configurator":
        with self._lock:
            if self._built:
                raise RuntimeError("Instance has been built; call reset() to modify.")
            if not isinstance(product, Product):
                raise ValueError("Template must be a Product instance.")
            self._name = product.name
            self._components = list(product.components)
            self._options = dict(product.options)
            self._version = product.version
            return self

    def build(self, allow_repeat: bool = False) -> Product:
        with self._lock:
            if self._built and not allow_repeat:
                raise RuntimeError("Product already built; call reset() or set allow_repeat=True.")
            if not self._name:
                raise ValueError("Name is required.")
            if not self._components:
                raise ValueError("At least one component is required.")
            components_tuple = tuple(self._components)
            options_tuple = tuple(sorted(self._options.items()))
            if self._version <= 0:
                raise ValueError("Version must be positive.")
            product = Product(
                name=self._name,
                components=components_tuple,
                options=options_tuple,
                version=self._version,
            )
            self._built = True
            return product

class Engineer:
    def __init__(self) -> None:
        self._configurator = Configurator()

    def create_minimal(self, name: str) -> Product:
        cfg = self._configurator.reset().set_name(name).add_component("core")
        return cfg.build()

    def create_full(self, name: str, extras: list[str]) -> Product:
        cfg = self._configurator.reset().set_name(name).set_version(2).set_option("mode", "full")
        for e in extras:
            cfg.add_component(e)
        cfg.add_component("core")
        return cfg.build()

if __name__ == "__main__":
    eng = Engineer()
    p1 = eng.create_minimal("Alpha")
    print(p1.to_dict())

    eng2 = Engineer()
    p2 = eng2.create_full("Beta", ["ui", "network"])
    print(p2.to_dict())

    cfg = Configurator()
    product_template = cfg.set_name("TemplateX").add_component("core").set_option("debug", True).set_version(3).build()
    cfg.reset().apply_template(product_template).set_option("debug", False)
    cloned = cfg.build(allow_repeat=True)
    print(cloned.to_dict())

    try:
        cfg.set_name("ShouldFail")
    except RuntimeError as e:
        print("Expected error:", str(e))