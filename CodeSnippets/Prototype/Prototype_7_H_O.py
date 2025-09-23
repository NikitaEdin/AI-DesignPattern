import copy
import threading
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict


class Creatable(ABC):
    @abstractmethod
    def duplicate(self, deep: bool = True, **overrides) -> "Creatable":
        pass


class ConfigItem(Creatable):
    def __init__(self, name: str, config: Dict[str, Any], data: list):
        self.id = str(uuid.uuid4())
        self.name = name
        self.config = config
        self.data = data
        self._self_ref = self  # circular reference to test deep copy handling

    def duplicate(self, deep: bool = True, **overrides) -> "ConfigItem":
        copier = copy.deepcopy if deep else copy.copy
        new_obj = copier(self)
        if not deep:
            # ensure a new top-level object identity but keep circular ref consistent
            new_obj._self_ref = new_obj
        new_obj._after_duplicate(overrides)
        return new_obj

    def _after_duplicate(self, overrides: Dict[str, Any]) -> None:
        if "id" in overrides:
            self.id = overrides.pop("id")
        else:
            self.id = str(uuid.uuid4())
        if "name" in overrides:
            self.name = overrides.pop("name")
        if "config" in overrides and isinstance(overrides["config"], dict):
            self.config.update(overrides.pop("config"))
        if "data" in overrides and isinstance(overrides["data"], list):
            self.data = list(overrides.pop("data"))
        for k, v in overrides.items():
            setattr(self, k, v)

    def __repr__(self) -> str:
        return f"<ConfigItem id={self.id[:8]} name={self.name!r} config={self.config} data={self.data}>"


class RegistryError(Exception):
    pass


class ItemRegistry:
    def __init__(self):
        self._lock = threading.RLock()
        self._items: Dict[str, Creatable] = {}

    def register(self, key: str, item: Creatable) -> None:
        if not isinstance(item, Creatable):
            raise RegistryError("Only Creatable instances can be registered")
        with self._lock:
            self._items[key] = item

    def unregister(self, key: str) -> None:
        with self._lock:
            if key in self._items:
                del self._items[key]
            else:
                raise RegistryError(f"No item registered under key: {key}")

    def create(self, key: str, deep: bool = True, **overrides) -> Creatable:
        with self._lock:
            if key not in self._items:
                raise RegistryError(f"No item registered under key: {key}")
            prototype = self._items[key]
        return prototype.duplicate(deep=deep, **overrides)

    def keys(self):
        with self._lock:
            return list(self._items.keys())


if __name__ == "__main__":
    registry = ItemRegistry()

    base_config = {"retries": 3, "timeout": 30}
    base_data = [1, 2, 3]

    original = ConfigItem("base", config=base_config, data=base_data)
    registry.register("base_item", original)

    shallow_copy = registry.create("base_item", deep=False, name="shallow_copy")
    deep_copy = registry.create("base_item", deep=True, name="deep_copy", config={"timeout": 60})

    shallow_copy.data.append(99)
    shallow_copy.config["retries"] = 9

    deep_copy.data.append(42)
    deep_copy.config["new_key"] = "value"

    print("Original:", original)
    print("Shallow:", shallow_copy)
    print("Deep   :", deep_copy)

    # Demonstrate independence for deep copy and shared state for shallow copy
    print("Original data object is shallow_copy.data same?", original.data is shallow_copy.data)
    print("Original data object is deep_copy.data same?", original.data is deep_copy.data)

    # Demonstrate circular reference maintained
    print("Original self ref ok?", original._self_ref is original)
    print("Deep self ref ok?", deep_copy._self_ref is deep_copy)
    print("Shallow self ref ok?", shallow_copy._self_ref is shallow_copy)