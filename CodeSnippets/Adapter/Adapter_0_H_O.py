from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Tuple


class OperationNotSupported(Exception):
    pass


class ServiceInterface(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


class LegacyPrinter:
    def print_text(self, text: str) -> None:
        print(f"[LegacyPrinter] {text}")

    def meta(self) -> str:
        return "Printer v1.0"


class LegacyCalculator:
    def compute(self, x: float, y: float) -> float:
        return x + y

    def details(self) -> str:
        return "Calculator v2.3"


class ServiceTranslator(ServiceInterface):
    def __init__(
        self,
        legacy_obj: object,
        mapping: Optional[Dict[str, Any]] = None,
        fallback: Optional[Callable[..., Any]] = None,
    ):
        self._legacy = legacy_obj
        self._mapping = mapping or {}
        self._fallback = fallback
        self._validate_mapping()

    def _validate_mapping(self) -> None:
        if "execute" not in self._mapping:
            raise ValueError("Mapping must provide an implementation for 'execute'")
        if not callable(self._mapping["execute"]) and not isinstance(self._mapping["execute"], str):
            raise TypeError("Mapping for 'execute' must be a method name or callable")

    def _resolve(self, key: str) -> Callable[..., Any]:
        entry = self._mapping.get(key)
        if entry is None:
            if self._fallback:
                return lambda *a, **k: self._fallback(key, *a, **k)
            raise OperationNotSupported(f"No mapping for operation '{key}'")

        if callable(entry):
            return lambda *a, **k: entry(self._legacy, *a, **k)

        if isinstance(entry, str):
            if not hasattr(self._legacy, entry):
                raise OperationNotSupported(f"Legacy object missing method '{entry}'")
            method = getattr(self._legacy, entry)
            if not callable(method):
                raise OperationNotSupported(f"Attribute '{entry}' is not callable")
            return method

        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and callable(entry[1]):
            name, transformer = entry
            if not hasattr(self._legacy, name):
                raise OperationNotSupported(f"Legacy object missing method '{name}'")
            method = getattr(self._legacy, name)
            if not callable(method):
                raise OperationNotSupported(f"Attribute '{name}' is not callable")
            return lambda *a, **k: transformer(method(*a, **k))

        raise TypeError("Unsupported mapping entry type")

    def execute(self, *args, **kwargs) -> Any:
        func = self._resolve("execute")
        return func(*args, **kwargs)

    def describe(self) -> str:
        try:
            func = self._resolve("describe")
            return func()
        except OperationNotSupported:
            if hasattr(self._legacy, "meta"):
                meta = getattr(self._legacy, "meta")
                if callable(meta):
                    return meta()
            if hasattr(self._legacy, "details"):
                details = getattr(self._legacy, "details")
                if callable(details):
                    return details()
            return "No description available"

    def __getattr__(self, item: str) -> Any:
        if hasattr(self._legacy, item):
            return getattr(self._legacy, item)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")


def _sum_transform(result: Any) -> float:
    return float(result)


def _fallback_handler(operation: str, *args, **kwargs) -> Any:
    if operation == "describe":
        return "Fallback description"
    raise OperationNotSupported(f"Fallback cannot handle operation '{operation}'")


if __name__ == "__main__":
    printer = LegacyPrinter()
    printer_map = {
        "execute": "print_text",
        "describe": "meta",
    }
    printer_service = ServiceTranslator(printer, mapping=printer_map)

    calculator = LegacyCalculator()
    calculator_map = {
        "execute": ("compute", _sum_transform),
    }
    calculator_service = ServiceTranslator(calculator, mapping=calculator_map, fallback=_fallback_handler)

    printer_service.execute("Hello from unified interface")
    print(printer_service.describe())

    result = calculator_service.execute(3, 4)
    print("Calculation result:", result)
    print("Calculator description:", calculator_service.describe())

    try:
        bad_service = ServiceTranslator(printer, mapping={"describe": "meta"})
    except Exception as e:
        print("Expected error creating translator without execute mapping:", e)