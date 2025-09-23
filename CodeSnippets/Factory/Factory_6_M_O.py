from abc import ABC, abstractmethod
from typing import Callable, Dict, Any, Optional


class DataHandler(ABC):
    @abstractmethod
    def handle(self, data: str) -> str:
        pass


class JSONHandler(DataHandler):
    def __init__(self, indent: int = 2):
        self.indent = indent

    def handle(self, data: str) -> str:
        return f"JSON handled with indent={self.indent}: {data}"


class XMLHandler(DataHandler):
    def __init__(self, validate: bool = False):
        self.validate = validate

    def handle(self, data: str) -> str:
        return f"XML handled (validate={self.validate}): {data}"


class CSVHandler(DataHandler):
    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    def handle(self, data: str) -> str:
        return f"CSV handled (delimiter='{self.delimiter}'): {data}"


class HandlerRegistry:
    def __init__(self):
        self._creators: Dict[str, Callable[..., DataHandler]] = {}
        self._cache: Dict[str, DataHandler] = {}
        self.register("json", lambda **kw: JSONHandler(**kw))
        self.register("xml", lambda **kw: XMLHandler(**kw))
        self.register("csv", lambda **kw: CSVHandler(**kw))

    def register(self, key: str, builder: Callable[..., DataHandler]) -> None:
        if not callable(builder):
            raise TypeError("builder must be callable")
        self._creators[key.lower()] = builder

    def create(self, key: str, *, reuse: bool = False, cache_key: Optional[str] = None, **kwargs) -> DataHandler:
        lookup = key.lower()
        if lookup not in self._creators:
            raise ValueError(f"Unknown handler type: {key}")
        if reuse:
            ck = cache_key or f"{lookup}:{sorted(kwargs.items())}"
            if ck in self._cache:
                return self._cache[ck]
            instance = self._creators[lookup](**kwargs)
            self._cache[ck] = instance
            return instance
        return self._creators[lookup](**kwargs)


if __name__ == "__main__":
    registry = HandlerRegistry()

    json_handler = registry.create("json", indent=4)
    print(json_handler.handle('{"key":"value"}'))

    xml_handler = registry.create("xml", validate=True)
    print(xml_handler.handle("<root/>"))

    csv_handler = registry.create("csv", delimiter=";")
    print(csv_handler.handle("a;b;c"))

    # Demonstrate reuse feature
    pooled1 = registry.create("json", reuse=True, indent=2)
    pooled2 = registry.create("json", reuse=True, indent=2)
    print("pooled same object:", pooled1 is pooled2)

    # Dynamically register a new type
    class TXTHandler(DataHandler):
        def __init__(self, prefix: str = ""):
            self.prefix = prefix

        def handle(self, data: str) -> str:
            return f"{self.prefix}{data}"

    registry.register("txt", lambda **kw: TXTHandler(**kw))
    txt = registry.create("txt", prefix="[TXT] ")
    print(txt.handle("plain text"))