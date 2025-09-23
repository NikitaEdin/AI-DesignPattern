from abc import ABC, abstractmethod
from typing import Callable, Dict, Type, Any, Optional
from threading import Lock
import json
import pickle

class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        pass

class JSONSerializer(Serializer):
    def __init__(self, indent: Optional[int] = None):
        self.indent = indent

    def serialize(self, data: Any) -> bytes:
        return json.dumps(data, indent=self.indent, separators=(",", ":")).encode("utf-8")

class XMLSerializer(Serializer):
    def __init__(self, root_name: str = "root"):
        self.root_name = root_name

    def _to_xml(self, key: str, value: Any) -> str:
        if isinstance(value, dict):
            inner = "".join(self._to_xml(k, v) for k, v in value.items())
            return f"<{key}>{inner}</{key}>"
        if isinstance(value, list):
            inner = "".join(self._to_xml(key, v) for v in value)
            return inner
        return f"<{key}>{str(value)}</{key}>"

    def serialize(self, data: Any) -> bytes:
        body = self._to_xml(self.root_name, data)
        return body.encode("utf-8")

class BinarySerializer(Serializer):
    def __init__(self, protocol: int = pickle.HIGHEST_PROTOCOL):
        self.protocol = protocol

    def serialize(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self.protocol)

class UnknownProductError(Exception):
    pass

class RegistrationError(Exception):
    pass

class ProducerRegistry:
    def __init__(self):
        self._creators: Dict[str, Callable[..., Serializer]] = {}
        self._singletons: Dict[str, Serializer] = {}
        self._lock = Lock()

    def register(self, key: str, creator: Callable[..., Serializer], override: bool = False) -> None:
        if not callable(creator):
            raise RegistrationError("creator must be callable")
        with self._lock:
            if key in self._creators and not override:
                raise RegistrationError(f"{key} already registered")
            self._creators[key] = creator
            if key in self._singletons:
                del self._singletons[key]

    def unregister(self, key: str) -> None:
        with self._lock:
            if key in self._creators:
                del self._creators[key]
            if key in self._singletons:
                del self._singletons[key]

    def produce(self, key: str, *args, singleton: bool = False, **kwargs) -> Serializer:
        with self._lock:
            creator = self._creators.get(key)
            if creator is None:
                raise UnknownProductError(f"Unknown product key: {key}")
            if singleton:
                instance = self._singletons.get(key)
                if instance is not None:
                    return instance
                instance = creator(*args, **kwargs)
                self._singletons[key] = instance
                return instance
        return creator(*args, **kwargs)

if __name__ == "__main__":
    registry = ProducerRegistry()
    registry.register("json", lambda indent=None: JSONSerializer(indent=indent))
    registry.register("xml", lambda root_name="root": XMLSerializer(root_name=root_name))
    registry.register("binary", lambda protocol=pickle.HIGHEST_PROTOCOL: BinarySerializer(protocol=protocol))

    payload = {"name": "Alice", "age": 30, "items": ["book", "pen"]}

    j = registry.produce("json", indent=2)
    print(j.serialize(payload).decode())

    x = registry.produce("xml", root_name="person")
    print(x.serialize(payload).decode())

    b1 = registry.produce("binary", singleton=True)
    b2 = registry.produce("binary", singleton=True)
    assert b1 is b2
    print(len(b1.serialize(payload)))

    try:
        registry.produce("yaml")
    except UnknownProductError as e:
        print("Error:", e)

    try:
        registry.register("json", lambda: JSONSerializer(), override=False)
    except RegistrationError as e:
        print("Registration error:", e)