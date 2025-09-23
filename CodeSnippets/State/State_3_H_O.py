import threading
import time
from abc import ABC, abstractmethod
from typing import List, Optional


class InvalidTransitionError(RuntimeError):
    pass


class ModeBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def on_enter(self, context: "Machine", **kwargs) -> None:
        return None

    def on_exit(self, context: "Machine") -> None:
        return None

    @abstractmethod
    def handle(self, context: "Machine", event: str) -> None:
        pass


class IdleMode(ModeBase):
    @property
    def name(self) -> str:
        return "idle"

    def handle(self, context: "Machine", event: str) -> None:
        if event == "start":
            context.change_mode(ActiveMode())
        else:
            raise InvalidTransitionError(f"'{event}' not allowed from idle")


class ActiveMode(ModeBase):
    @property
    def name(self) -> str:
        return "active"

    def on_enter(self, context: "Machine", **kwargs) -> None:
        context.schedule_transition(PausedMode(), delay=2.0)

    def on_exit(self, context: "Machine") -> None:
        context.cancel_scheduled()

    def handle(self, context: "Machine", event: str) -> None:
        if event == "pause":
            context.change_mode(PausedMode())
        elif event == "stop":
            context.change_mode(IdleMode())
        else:
            raise InvalidTransitionError(f"'{event}' not allowed from active")


class PausedMode(ModeBase):
    @property
    def name(self) -> str:
        return "paused"

    def handle(self, context: "Machine", event: str) -> None:
        if event == "resume":
            context.change_mode(ActiveMode())
        elif event == "stop":
            context.change_mode(IdleMode())
        else:
            raise InvalidTransitionError(f"'{event}' not allowed from paused")


class Machine:
    def __init__(self, initial: ModeBase) -> None:
        self._lock = threading.RLock()
        self._current: ModeBase = initial
        self._history: List[ModeBase] = []
        self._timer: Optional[threading.Timer] = None
        self._current.on_enter(self)

    def get_mode(self) -> str:
        with self._lock:
            return self._current.name

    def change_mode(self, new_mode: ModeBase, record_history: bool = True, force: bool = False) -> None:
        with self._lock:
            if not force and type(new_mode) is type(self._current):
                return
            prev = self._current
            prev.on_exit(self)
            if record_history:
                self._history.append(prev)
            self.cancel_scheduled()
            self._current = new_mode
            self._current.on_enter(self)

    def trigger(self, event: str) -> None:
        with self._lock:
            try:
                self._current.handle(self, event)
            except InvalidTransitionError:
                raise

    def revert(self) -> None:
        with self._lock:
            if not self._history:
                raise InvalidTransitionError("No previous mode to revert to")
            previous = self._history.pop()
            self.change_mode(previous, record_history=False, force=True)

    def schedule_transition(self, mode: ModeBase, delay: float) -> None:
        def _switch():
            try:
                self.change_mode(mode)
            except Exception:
                pass

        with self._lock:
            self.cancel_scheduled()
            timer = threading.Timer(delay, _switch)
            self._timer = timer
            timer.daemon = True
            timer.start()

    def cancel_scheduled(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "current": self._current.name,
                "history": [m.name for m in self._history],
                "timer_active": self._timer is not None
            }


if __name__ == "__main__":
    m = Machine(IdleMode())
    print("initial:", m.get_mode())
    m.trigger("start")
    print("after start:", m.get_mode())
    time.sleep(0.1)
    print("waiting for auto pause...")
    time.sleep(2.2)
    print("after auto:", m.get_mode())
    try:
        m.trigger("start")
    except InvalidTransitionError as e:
        print("invalid:", e)
    m.trigger("resume")
    print("after resume:", m.get_mode())
    m.trigger("stop")
    print("after stop:", m.get_mode())
    try:
        m.revert()
        print("after revert:", m.get_mode())
    except InvalidTransitionError as e:
        print("revert failed:", e)
    print("snapshot:", m.snapshot())