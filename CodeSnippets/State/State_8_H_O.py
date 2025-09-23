import threading
import time
from abc import ABC, abstractmethod
from typing import Optional, List, Union, Type


class ModeBase(ABC):
    timeout_seconds: Optional[float] = None

    def enter(self, ctx: "ModeContext"):
        print(f"> Entering {self}")
        if self.timeout_seconds:
            self._start_timer(ctx)

    def exit(self, ctx: "ModeContext"):
        if hasattr(self, "_timer") and self._timer:
            self._timer.cancel()
            self._timer = None
        print(f"< Exiting {self}")

    def _start_timer(self, ctx: "ModeContext"):
        if hasattr(self, "_timer") and self._timer:
            self._timer.cancel()

        def _on_timeout():
            try:
                tgt = self.timeout_target(ctx)
                if tgt:
                    ctx.switch_mode(tgt, record_history=True)
            except Exception as exc:
                print("Timeout handler error:", exc)

        self._timer = threading.Timer(self.timeout_seconds, _on_timeout)
        self._timer.daemon = True
        self._timer.start()

    @abstractmethod
    def on_event(self, ctx: "ModeContext", event: str) -> Optional["ModeBase"]:
        pass

    def timeout_target(self, ctx: "ModeContext") -> Optional["ModeBase"]:
        return None

    def __repr__(self):
        return self.__class__.__name__


class IdleMode(ModeBase):
    def on_event(self, ctx: "ModeContext", event: str) -> Optional[ModeBase]:
        if event == "start":
            return ActiveMode()
        if event == "error":
            return ErrorMode()
        return None


class ActiveMode(ModeBase):
    timeout_seconds = 3.0

    def on_event(self, ctx: "ModeContext", event: str) -> Optional[ModeBase]:
        if event == "stop":
            return IdleMode()
        if event == "error":
            return ErrorMode()
        if event == "suspend":
            return SuspendedMode()
        return None

    def timeout_target(self, ctx: "ModeContext") -> Optional[ModeBase]:
        return IdleMode()


class SuspendedMode(ModeBase):
    timeout_seconds = 5.0

    def on_event(self, ctx: "ModeContext", event: str) -> Optional[ModeBase]:
        if event == "resume":
            return ActiveMode()
        if event == "error":
            return ErrorMode()
        return None

    def timeout_target(self, ctx: "ModeContext") -> Optional[ModeBase]:
        return IdleMode()


class ErrorMode(ModeBase):
    def on_event(self, ctx: "ModeContext", event: str) -> Optional[ModeBase]:
        if event == "reset":
            return IdleMode()
        if event == "rollback":
            try:
                ctx.rollback()
            except RuntimeError as exc:
                print("Rollback failed:", exc)
        return None


class ModeContext:
    def __init__(self, initial: Union[ModeBase, Type[ModeBase]]):
        self._lock = threading.RLock()
        self._history: List[ModeBase] = []
        self._max_history = 10
        self._current = self._ensure_instance(initial)
        self._current.enter(self)

    def _ensure_instance(self, candidate: Union[ModeBase, Type[ModeBase]]) -> ModeBase:
        if isinstance(candidate, ModeBase):
            return candidate
        if isinstance(candidate, type) and issubclass(candidate, ModeBase):
            return candidate()
        raise TypeError("Invalid mode")

    def switch_mode(self, new: Union[ModeBase, Type[ModeBase]], record_history: bool = True):
        with self._lock:
            new_inst = self._ensure_instance(new)
            if record_history:
                self._history.append(self._current)
                if len(self._history) > self._max_history:
                    self._history.pop(0)
            try:
                self._current.exit(self)
            except Exception as exc:
                print("Exit handler error:", exc)
            self._current = new_inst
            try:
                self._current.enter(self)
            except Exception as exc:
                print("Enter handler error:", exc)

    def handle_event(self, event: str):
        with self._lock:
            try:
                result = self._current.on_event(self, event)
            except Exception as exc:
                print("Event handler error:", exc)
                result = None
            if isinstance(result, ModeBase) or (isinstance(result, type) and issubclass(result, ModeBase)):
                self.switch_mode(result)
            else:
                print(f"No transition from {self._current} on '{event}'")

    def rollback(self):
        with self._lock:
            if not self._history:
                raise RuntimeError("No history to rollback to")
            target = self._history.pop()
            try:
                self._current.exit(self)
            except Exception:
                pass
            self._current = target
            self._current.enter(self)

    def current(self) -> ModeBase:
        with self._lock:
            return self._current


if __name__ == "__main__":
    ctx = ModeContext(IdleMode)
    ctx.handle_event("start")
    time.sleep(1)
    ctx.handle_event("suspend")
    time.sleep(2)
    ctx.handle_event("resume")
    time.sleep(4)
    ctx.handle_event("error")
    ctx.handle_event("rollback")
    ctx.handle_event("reset")
    time.sleep(1)
    ctx.handle_event("start")
    time.sleep(4)
    ctx.handle_event("stop")
    print("Final:", ctx.current())