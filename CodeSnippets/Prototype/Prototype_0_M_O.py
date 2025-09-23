import copy
from abc import ABC, abstractmethod


class ItemBase(ABC):
    @abstractmethod
    def clone(self, **overrides):
        pass


class ConfigItem(ItemBase):
    def __init__(self, name: str, settings: dict, version: int = 1):
        if not isinstance(name, str) or not isinstance(settings, dict) or not isinstance(version, int):
            raise TypeError("Invalid types for ConfigItem")
        if version < 0:
            raise ValueError("Version must be non-negative")
        self.name = name
        self.settings = settings
        self.version = version

    def clone(self, **overrides):
        new_obj = copy.deepcopy(self)
        for key, val in overrides.items():
            if key not in {"name", "settings", "version"}:
                raise KeyError(f"Cannot override unknown attribute '{key}'")
            if key == "name":
                if not isinstance(val, str):
                    raise TypeError("name must be a string")
            if key == "settings":
                if not isinstance(val, dict):
                    raise TypeError("settings must be a dict")
            if key == "version":
                if not isinstance(val, int) or val < 0:
                    raise ValueError("version must be a non-negative int")
            setattr(new_obj, key, val)
        return new_obj

    def __repr__(self):
        return f"ConfigItem(name={self.name!r}, settings={self.settings!r}, version={self.version})"


class TemplateRegistry:
    def __init__(self):
        self._store = {}

    def register(self, key: str, item: ItemBase):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not isinstance(item, ItemBase):
            raise TypeError("Item must implement ItemBase")
        self._store[key] = item

    def unregister(self, key: str):
        self._store.pop(key, None)

    def create(self, key: str, **overrides):
        try:
            template = self._store[key]
        except KeyError:
            raise KeyError(f"No template registered under key '{key}'")
        return template.clone(**overrides)


if __name__ == "__main__":
    registry = TemplateRegistry()
    base_config = ConfigItem("default", {"timeout": 30, "retry": 3}, version=1)
    registry.register("service_default", base_config)

    cloned_a = registry.create("service_default", name="service_a", settings={"timeout": 10, "retry": 5}, version=2)
    cloned_b = registry.create("service_default", name="service_b")

    print("Original:", base_config)
    print("Cloned A:", cloned_a)
    print("Cloned B:", cloned_b)

    try:
        registry.create("service_default", settings="invalid")
    except Exception as e:
        print("Caught error as expected:", e)

    try:
        registry.create("missing_key")
    except Exception as e:
        print("Caught missing template error:", e)