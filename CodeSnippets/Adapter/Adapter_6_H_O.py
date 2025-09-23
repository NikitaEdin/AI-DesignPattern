from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class Printer(ABC):
    @abstractmethod
    def print(self, text: str) -> str:
        raise NotImplementedError


class LegacyUpperPrinter:
    def print_upper(self, message: str) -> str:
        return f"[LegacyUpperPrinter] {message.upper()}"


class LegacyByteSender:
    def send(self, data: bytes) -> int:
        return len(data)


class ModernWriter:
    def write_line(self, line: str) -> str:
        return f"[ModernWriter] {line}"


class UnifiedPrinter(Printer):
    def __init__(self, service: Any, method_map: Optional[Dict[str, str]] = None):
        self._service = service
        self._method_map = method_map or {}
        self._callable: Callable[[str], str] = self._resolve_target()

    def _resolve_target(self) -> Callable[[str], str]:
        mapped = self._method_map.get("print")
        if mapped:
            target = getattr(self._service, mapped, None)
            if callable(target):
                return lambda text: self._invoke(target, text)
            raise TypeError("Mapped target method not callable")

        if hasattr(self._service, "print_upper") and callable(getattr(self._service, "print_upper")):
            return lambda text: self._invoke(getattr(self._service, "print_upper"), text)

        if hasattr(self._service, "send") and callable(getattr(self._service, "send")):
            return lambda text: self._invoke(getattr(self._service, "send"), text.encode("utf-8"))

        if hasattr(self._service, "write_line") and callable(getattr(self._service, "write_line")):
            return lambda text: self._invoke(getattr(self._service, "write_line"), text)

        if callable(self._service):
            return lambda text: self._invoke(self._service, text)

        raise TypeError("Service cannot be adapted to Printer")

    def _invoke(self, func: Callable[..., Any], payload: Any) -> str:
        try:
            result = func(payload)
        except Exception as exc:
            return f"[error] {exc!s}"

        if isinstance(result, bytes):
            try:
                return result.decode("utf-8")
            except Exception:
                return result.decode("utf-8", errors="ignore")
        if isinstance(result, int):
            return f"[sent_bytes:{result}]"
        if result is None:
            return "[ok]"
        return str(result)

    def print(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return self._callable(text)


if __name__ == "__main__":
    legacy_a = LegacyUpperPrinter()
    legacy_b = LegacyByteSender()
    modern = ModernWriter()

    unified_a = UnifiedPrinter(legacy_a)
    unified_b = UnifiedPrinter(legacy_b)
    unified_mod = UnifiedPrinter(modern)
    unified_custom = UnifiedPrinter(modern, method_map={"print": "write_line"})

    examples = [
        ("A", unified_a, "hello world"),
        ("B", unified_b, "hello bytes"),
        ("M", unified_mod, "modern write"),
        ("C", unified_custom, "custom mapping"),
    ]

    for label, printer, text in examples:
        out = printer.print(text)
        print(f"{label} -> {out}")