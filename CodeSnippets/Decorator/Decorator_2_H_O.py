import abc
from typing import Any, Callable, Optional, Type


class ComponentBase(abc.ABC):
    @abc.abstractmethod
    def operate(self, payload: str) -> str:
        pass


class ConcreteService(ComponentBase):
    def __init__(self, name: str, state: str = ""):
        self.name = name
        self.state = state

    def operate(self, payload: str) -> str:
        return f"{self.name}|{payload}|{self.state}"

    def update_state(self, new_state: str) -> None:
        self.state = new_state

    def __repr__(self) -> str:
        return f"<Service {self.name} state={self.state!r}>"


class LayerBase(ComponentBase):
    def __init__(self, component: ComponentBase):
        if not isinstance(component, ComponentBase):
            raise TypeError("Wrapped object must implement ComponentBase")
        self._component = component

    def operate(self, payload: str) -> str:
        return self._component.operate(payload)

    def __getattr__(self, item: str) -> Any:
        return getattr(self._component, item)

    def find_first(self, target_type: Type[ComponentBase]) -> Optional[ComponentBase]:
        current = self
        visited = set()
        while True:
            if id(current) in visited:
                raise RuntimeError("Cycle detected in layer chain")
            visited.add(id(current))
            if isinstance(current, target_type):
                return current
            comp = getattr(current, "_component", None)
            if comp is None:
                return None
            if isinstance(comp, target_type):
                return comp
            if isinstance(comp, LayerBase):
                current = comp
                continue
            return comp if isinstance(comp, target_type) else None

    def unwrap_all(self) -> list:
        items = []
        current = self
        visited = set()
        while True:
            if id(current) in visited:
                raise RuntimeError("Cycle detected in layer chain")
            visited.add(id(current))
            items.append(current)
            comp = getattr(current, "_component", None)
            if comp is None:
                break
            if isinstance(comp, LayerBase):
                current = comp
                continue
            items.append(comp)
            break
        return items

    def __repr__(self) -> str:
        return f"<Layer wrapping {self._component!r}>"


class LoggingLayer(LayerBase):
    def __init__(self, component: ComponentBase):
        super().__init__(component)
        self.events: list[str] = []

    def operate(self, payload: str) -> str:
        self.events.append(f"enter:{payload}")
        try:
            result = self._component.operate(payload)
            self.events.append(f"exit:{result}")
            return result
        except Exception as exc:
            self.events.append(f"error:{exc}")
            raise

    def get_events(self) -> list[str]:
        return list(self.events)

    def __repr__(self) -> str:
        return f"<LoggingLayer events={len(self.events)} wrapping {self._component!r}>"


class TransformLayer(LayerBase):
    def __init__(self, component: ComponentBase, transform: Optional[Callable[[str], str]] = None):
        super().__init__(component)
        self.transform = transform or (lambda s: s)

    def operate(self, payload: str) -> str:
        result = self._component.operate(payload)
        try:
            transformed = self.transform(result)
            if not isinstance(transformed, str):
                raise TypeError("Transform must return a string")
            return transformed
        except Exception as exc:
            raise RuntimeError(f"Transformation failed: {exc}") from exc

    def __repr__(self) -> str:
        return f"<TransformLayer wrapping {self._component!r}>"


if __name__ == "__main__":
    svc = ConcreteService("svcA", "initial")
    log1 = LoggingLayer(svc)
    transform = TransformLayer(log1, transform=lambda s: s.upper())
    log2 = LoggingLayer(transform)

    out = log2.operate("input")
    print("Output:", out)

    log_layer = log2.find_first(LoggingLayer)
    print("Found logging layer:", repr(log_layer))
    if isinstance(log_layer, LoggingLayer):
        print("Events:", log_layer.get_events())

    service_found = log2.find_first(ConcreteService)
    print("Original service:", service_found)
    if isinstance(service_found, ConcreteService):
        service_found.update_state("updated")
        print("Service after update:", service_found.operate("check"))

    chain = log2.unwrap_all()
    print("Chain:", " -> ".join(repr(x) for x in chain))