from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import RLock
from typing import Any, Callable, Dict, Optional
import inspect
import sys


class CreationError(Exception):
    pass


class UnknownProductError(Exception):
    pass


class InvalidParamsError(Exception):
    pass


class Component(ABC):
    @abstractmethod
    def operate(self) -> str:
        pass


@dataclass
class ConsoleLogger(Component):
    level: str
    fmt: str = "{level}: {msg}"

    def operate(self) -> str:
        return self.fmt.format(level=self.level, msg="console_log")


@dataclass
class FileStorage(Component):
    path: str
    mode: str = "r"

    def operate(self) -> str:
        return f"storage at {self.path} mode={self.mode}"


class CreatorRegistry:
    def __init__(self) -> None:
        self._creators: Dict[str, Callable[..., Component]] = {}
        self._validators: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self._singletons: Dict[str, Component] = {}
        self._singleton_flags: Dict[str, bool] = {}
        self._lock = RLock()

    def register(self, name: str, constructor: Callable[..., Component], *, singleton: bool = False,
                 validator: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None) -> None:
        if not callable(constructor):
            raise CreationError("constructor must be callable")
        with self._lock:
            self._creators[name] = constructor
            self._singleton_flags[name] = bool(singleton)
            if validator:
                self._validators[name] = validator

    def create(self, name: str, **params: Any) -> Component:
        with self._lock:
            if name not in self._creators:
                raise UnknownProductError(f"Unknown product '{name}'")
            if self._singleton_flags.get(name) and name in self._singletons:
                return self._singletons[name]
            validator = self._validators.get(name)
            if validator:
                try:
                    params = validator(dict(params))
                except Exception as e:
                    raise InvalidParamsError(str(e))
            constructor = self._creators[name]
        try:
            result = self._invoke(constructor, params)
        except TypeError as e:
            raise CreationError(f"Parameter mismatch for '{name}': {e}") from e
        except Exception as e:
            raise CreationError(f"Error creating '{name}': {e}") from e
        with self._lock:
            if self._singleton_flags.get(name):
                self._singletons[name] = result
        return result

    @staticmethod
    def _invoke(constructor: Callable[..., Component], params: Dict[str, Any]) -> Component:
        sig = inspect.signature(constructor)
        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()):
            return constructor(**params)
        allowed = {k: v for k, v in params.items() if k in sig.parameters}
        return constructor(**allowed)


def validate_logger(params: Dict[str, Any]) -> Dict[str, Any]:
    level = params.get("level")
    if level not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
        raise ValueError("level must be one of DEBUG, INFO, WARNING, ERROR")
    fmt = params.get("fmt", "{level}: {msg}")
    return {"level": level, "fmt": fmt}


def validate_storage(params: Dict[str, Any]) -> Dict[str, Any]:
    path = params.get("path")
    if not path or not isinstance(path, str):
        raise ValueError("path is required and must be a string")
    mode = params.get("mode", "r")
    if mode not in {"r", "w", "a", "rb", "wb"}:
        raise ValueError("invalid mode")
    return {"path": path, "mode": mode}


if __name__ == "__main__":
    registry = CreatorRegistry()
    registry.register("console_logger", ConsoleLogger, singleton=False, validator=validate_logger)
    registry.register("file_storage", FileStorage, singleton=True, validator=validate_storage)

    logger = registry.create("console_logger", level="INFO")
    print(logger.operate())

    storage1 = registry.create("file_storage", path="/tmp/data.db", mode="wb")
    storage2 = registry.create("file_storage", path="/tmp/other.db", mode="wb")
    print(storage1.operate())
    print(storage1 is storage2)

    try:
        registry.create("console_logger", level="VERBOSE")
    except InvalidParamsError as e:
        print("Validation failed:", e, file=sys.stderr)

    def custom_component(**kwargs):
        return ConsoleLogger(level=kwargs.get("level", "INFO"), fmt=kwargs.get("fmt", "[{level}]{msg}"))

    registry.register("custom", custom_component, singleton=False)
    custom = registry.create("custom", level="DEBUG", fmt="[{level}] {msg}")
    print(custom.operate())