from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class ComponentBase(ABC):
    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def set_text(self, value: str) -> None:
        pass

    @abstractmethod
    def send(self) -> None:
        pass


class SimpleMessage(ComponentBase):
    def __init__(self, text: str = ""):
        self._text = str(text)

    def get_text(self) -> str:
        return self._text

    def set_text(self, value: str) -> None:
        self._text = str(value)

    def send(self) -> None:
        print(self._text)

    def __repr__(self) -> str:
        return f"<SimpleMessage text={self._text!r}>"


class BaseWrapper(ComponentBase):
    def __init__(self, target: ComponentBase):
        if target is None:
            raise ValueError("target cannot be None")
        if self._contains_cycle(target):
            raise ValueError("Wrapping would create a cycle")
        self._target = target
        self.enabled = True

    def _contains_cycle(self, target: ComponentBase) -> bool:
        visited = set()
        current = target
        while True:
            if id(current) in visited:
                return True
            visited.add(id(current))
            if not isinstance(current, BaseWrapper):
                return False
            current = current._target

    def get_text(self) -> str:
        text = self._target.get_text()
        return self._apply_on_get(text) if self.enabled else text

    def set_text(self, value: str) -> None:
        value = self._apply_on_set(value) if self.enabled else value
        self._target.set_text(value)

    def send(self) -> None:
        if self.enabled:
            self._pre_send()
        self._target.send()
        if self.enabled:
            self._post_send()

    def _apply_on_get(self, text: str) -> str:
        return text

    def _apply_on_set(self, text: str) -> str:
        return text

    def _pre_send(self) -> None:
        pass

    def _post_send(self) -> None:
        pass

    def unwrap(self) -> ComponentBase:
        current = self
        while isinstance(current, BaseWrapper):
            current = current._target
        return current

    def __getattr__(self, name: str) -> Any:
        return getattr(self._target, name)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} enabled={self.enabled} target={self._target!r}>"


class UpperCaseTransform(BaseWrapper):
    def _apply_on_get(self, text: str) -> str:
        return text.upper()

    def _apply_on_set(self, text: str) -> str:
        return text.upper()


class ShiftCipherTransform(BaseWrapper):
    def __init__(self, target: ComponentBase, shift: int = 3):
        super().__init__(target)
        self.shift = int(shift) % 26

    def _rotate_char(self, ch: str, shift: int) -> str:
        if "a" <= ch <= "z":
            return chr((ord(ch) - 97 + shift) % 26 + 97)
        if "A" <= ch <= "Z":
            return chr((ord(ch) - 65 + shift) % 26 + 65)
        return ch

    def _apply_on_get(self, text: str) -> str:
        return "".join(self._rotate_char(c, -self.shift) for c in text)

    def _apply_on_set(self, text: str) -> str:
        return "".join(self._rotate_char(c, self.shift) for c in text)


class TimestampPrefixTransform(BaseWrapper):
    def __init__(self, target: ComponentBase, fmt: str = "%Y-%m-%d %H:%M:%S"):
        super().__init__(target)
        self.fmt = fmt

    def _apply_on_get(self, text: str) -> str:
        prefix = datetime.utcnow().strftime(self.fmt)
        return f"{prefix} {text}"

    def _pre_send(self) -> None:
        if hasattr(self._target, "set_text"):
            self._target.set_text(self.get_text())


if __name__ == "__main__":
    base = SimpleMessage("Hello, World!")
    shifted = ShiftCipherTransform(base, shift=5)
    upper = UpperCaseTransform(shifted)
    stamped = TimestampPrefixTransform(upper)

    print("Original:", base.get_text())
    print("Wrapped get_text:", stamped.get_text())
    print("Send through stack:")
    stamped.send()

    print("\nModify via top wrapper (set_text):")
    stamped.set_text("Secret Message")
    print("Base stored (encrypted):", base.get_text())
    print("Top view:", stamped.get_text())

    print("\nDisable uppercase layer temporarily:")
    upper.enabled = False
    print("Top view without uppercase:", stamped.get_text())
    upper.enabled = True

    print("\nUnwrapped original object:", stamped.unwrap())
    print("Repr chain:", stamped)