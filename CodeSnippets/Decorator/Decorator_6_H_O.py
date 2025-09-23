from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time

class Component(ABC):
    @abstractmethod
    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def chain(self) -> List["Component"]:
        return [self]

class CoreService(Component):
    def __init__(self, name: str):
        self.name = name

    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(data)
        processed = out.get("processed", [])
        processed = list(processed) + [self.name]
        out["processed"] = processed
        out.setdefault("result", {}).update({"service": self.name})
        return out

    def __repr__(self):
        return f"<CoreService {self.name}>"

class WrapperBase(Component):
    def __init__(self, component: Component):
        if not isinstance(component, Component):
            raise TypeError("Wrapped object must implement Component")
        self._component: Optional[Component] = component

    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self._component is None:
            raise RuntimeError("No component attached")
        if not hasattr(self._component, "handle"):
            raise AttributeError("Wrapped component lacks handle method")
        return self._component.handle(data)

    def attach(self, component: Component):
        if not isinstance(component, Component):
            raise TypeError("Can only attach Component instances")
        self._component = component

    def detach(self) -> Component:
        if self._component is None:
            raise RuntimeError("Nothing to detach")
        old = self._component
        self._component = None
        return old

    def chain(self) -> List[Component]:
        if self._component is None:
            return [self]
        rest = self._component.chain()
        return [self] + rest

    def __getattr__(self, item):
        if "_component" in self.__dict__ and self._component is not None:
            return getattr(self._component, item)
        raise AttributeError(item)

    def __repr__(self):
        inner = repr(self._component) if self._component is not None else "None"
        return f"<{self.__class__.__name__} wrapping={inner}>"

class LoggerWrap(WrapperBase):
    def __init__(self, component: Component, prefix: str = "LOG"):
        super().__init__(component)
        self.prefix = prefix

    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"{self.prefix} - entering: {self._component!r} with {data}")
        result = super().handle(data)
        print(f"{self.prefix} - exiting: {self._component!r} produced {result}")
        return result

class TimerWrap(WrapperBase):
    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        start = time.perf_counter()
        result = super().handle(data)
        elapsed = time.perf_counter() - start
        meta = result.setdefault("meta", {})
        timings = meta.setdefault("timings", [])
        timings.append({"wrapper": self.__class__.__name__, "elapsed": elapsed})
        return result

class ValidatorWrap(WrapperBase):
    def __init__(self, component: Component, required_keys: Optional[List[str]] = None):
        super().__init__(component)
        self.required_keys = required_keys or []

    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        missing = [k for k in self.required_keys if k not in data]
        if missing:
            raise ValueError(f"Missing required keys: {missing}")
        return super().handle(data)

if __name__ == "__main__":
    core = CoreService("Alpha")
    validated = ValidatorWrap(core, required_keys=["value"])
    logger = LoggerWrap(validated, prefix="TRACE")
    timed = TimerWrap(logger)

    payload = {"value": 42}
    print("Chain before call:", timed.chain())
    result = timed.handle(payload)
    print("Final result:", result)

    detached = timed.detach()
    print("Detached component:", detached)
    print("Chain after detach:", timed.chain())

    new_core = CoreService("Beta")
    timed.attach(LoggerWrap(new_core, prefix="NEWLOG"))
    print("Chain after attach:", timed.chain())
    try:
        print(timed.handle({"wrong": "data"}))
    except Exception as e:
        print("Handled error:", e)

    print("Transparent attribute access:", getattr(timed, "name", "no-name"))