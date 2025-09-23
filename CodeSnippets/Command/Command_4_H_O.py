from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class Operation(ABC):
    @abstractmethod
    def perform(self) -> Any:
        pass

    @abstractmethod
    def revert(self) -> None:
        pass


class Light:
    def __init__(self) -> None:
        self._on: bool = False
        self._brightness: int = 100

    def set_state(self, on: bool, brightness: Optional[int] = None) -> Tuple[bool, int]:
        prev = (self._on, self._brightness)
        self._on = bool(on)
        if brightness is not None:
            self._brightness = max(0, min(100, int(brightness)))
        return prev

    def get_state(self) -> Tuple[bool, int]:
        return self._on, self._brightness

    def __repr__(self) -> str:
        return f"Light(on={self._on}, brightness={self._brightness})"


class ToggleLight(Operation):
    def __init__(self, receiver: Light, target_on: Optional[bool] = None) -> None:
        self.receiver = receiver
        self.target_on = target_on
        self._prev: Optional[Tuple[bool, int]] = None

    def perform(self) -> Tuple[bool, int]:
        current_on, current_brightness = self.receiver.get_state()
        new_on = self.target_on if self.target_on is not None else not current_on
        self._prev = self.receiver.set_state(new_on)
        return self.receiver.get_state()

    def revert(self) -> None:
        if self._prev is None:
            raise RuntimeError("Nothing to revert")
        self.receiver.set_state(*self._prev)
        self._prev = None


class AdjustBrightness(Operation):
    def __init__(self, receiver: Light, brightness: int) -> None:
        if not isinstance(brightness, int):
            raise TypeError("brightness must be int")
        self.receiver = receiver
        self.brightness = max(0, min(100, brightness))
        self._prev: Optional[Tuple[bool, int]] = None

    def perform(self) -> Tuple[bool, int]:
        self._prev = self.receiver.set_state(self.receiver.get_state()[0], self.brightness)
        return self.receiver.get_state()

    def revert(self) -> None:
        if self._prev is None:
            raise RuntimeError("Nothing to revert")
        self.receiver.set_state(*self._prev)
        self._prev = None


class MacroOperation(Operation):
    def __init__(self, operations: List[Operation]) -> None:
        if not isinstance(operations, list):
            raise TypeError("operations must be a list")
        self.operations = operations
        self._executed: List[Operation] = []

    def perform(self) -> List[Any]:
        results: List[Any] = []
        self._executed = []
        for op in self.operations:
            try:
                res = op.perform()
                self._executed.append(op)
                results.append(res)
            except Exception as exc:
                for done in reversed(self._executed):
                    try:
                        done.revert()
                    except Exception:
                        pass
                self._executed = []
                raise RuntimeError(f"Macro failed and rolled back: {exc}") from exc
        return results

    def revert(self) -> None:
        for op in reversed(self._executed):
            try:
                op.revert()
            except Exception:
                pass
        self._executed = []


class Controller:
    def __init__(self) -> None:
        self._slots: Dict[str, Operation] = {}
        self._history: List[Operation] = []
        self._redo_stack: List[Operation] = []

    def register(self, name: str, operation: Operation) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("slot name must be a non-empty string")
        if not isinstance(operation, Operation):
            raise TypeError("operation must derive from Operation")
        self._slots[name] = operation

    def run(self, name: str) -> Any:
        if name not in self._slots:
            raise KeyError(f"No operation registered under '{name}'")
        op = self._slots[name]
        result = op.perform()
        self._history.append(op)
        self._redo_stack.clear()
        return result

    def undo_last(self) -> None:
        if not self._history:
            raise RuntimeError("No operation to undo")
        op = self._history.pop()
        op.revert()
        self._redo_stack.append(op)

    def redo_last(self) -> Any:
        if not self._redo_stack:
            raise RuntimeError("No operation to redo")
        op = self._redo_stack.pop()
        result = op.perform()
        self._history.append(op)
        return result


if __name__ == "__main__":
    lamp = Light()
    toggle = ToggleLight(lamp)
    brighten = AdjustBrightness(lamp, 75)
    dim = AdjustBrightness(lamp, 20)
    macro = MacroOperation([toggle, brighten])
    ctrl = Controller()
    ctrl.register("toggle", toggle)
    ctrl.register("brighten", brighten)
    ctrl.register("evening", macro)

    print("Initial:", lamp)
    print("Run toggle ->", ctrl.run("toggle"))
    print("Run brighten ->", ctrl.run("brighten"))
    print("Undo last")
    ctrl.undo_last()
    print("State after undo:", lamp)
    print("Run evening macro ->", ctrl.run("evening"))
    print("State after macro:", lamp)
    print("Undo macro")
    ctrl.undo_last()
    print("State after undo macro:", lamp)
    try:
        ctrl.run("nonexistent")
    except Exception as e:
        print("Handled error:", e)