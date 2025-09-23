import threading
import time
from typing import Callable, Dict, List

class InvalidTransitionError(Exception):
    pass

class ModeBase:
    name: str

    def enter(self, ctx: "Context"):
        pass

    def exit(self, ctx: "Context"):
        pass

    def handle_event(self, ctx: "Context", event: str):
        raise InvalidTransitionError(f"Event '{event}' not handled in mode '{self.name}'")

class IdleMode(ModeBase):
    name = "idle"

    def handle_event(self, ctx: "Context", event: str):
        if event == "start":
            ctx.switch_mode("running")
        elif event == "reset":
            ctx.switch_mode("idle")
        else:
            super().handle_event(ctx, event)

class RunningMode(ModeBase):
    name = "running"

    def __init__(self, auto_pause_seconds: float = 3.0):
        self.auto_pause_seconds = auto_pause_seconds
        self._timer: threading.Timer | None = None

    def enter(self, ctx: "Context"):
        self._start_timer(ctx)

    def exit(self, ctx: "Context"):
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _start_timer(self, ctx: "Context"):
        def _auto_pause():
            try:
                ctx.switch_mode("paused")
            except Exception:
                pass
        self._timer = threading.Timer(self.auto_pause_seconds, _auto_pause)
        self._timer.daemon = True
        self._timer.start()

    def handle_event(self, ctx: "Context", event: str):
        if event == "pause":
            ctx.switch_mode("paused")
        elif event == "stop":
            ctx.switch_mode("idle")
        else:
            super().handle_event(ctx, event)

class PausedMode(ModeBase):
    name = "paused"

    def handle_event(self, ctx: "Context", event: str):
        if event == "resume":
            ctx.switch_mode("running")
        elif event == "stop":
            ctx.switch_mode("idle")
        elif event == "reset":
            ctx.switch_mode("idle")
        else:
            super().handle_event(ctx, event)

class Context:
    def __init__(self):
        self._modes: Dict[str, ModeBase] = {
            "idle": IdleMode(),
            "running": RunningMode(auto_pause_seconds=2.0),
            "paused": PausedMode(),
        }
        self._lock = threading.RLock()
        self._history: List[str] = []
        self._current: str = "idle"
        self._listeners: List[Callable[[str, str], None]] = []
        self._modes[self._current].enter(self)

    def add_listener(self, fn: Callable[[str, str], None]):
        with self._lock:
            self._listeners.append(fn)

    def handle(self, event: str):
        with self._lock:
            mode = self._modes[self._current]
            mode.handle_event(self, event)

    def switch_mode(self, new_name: str, record_history: bool = True):
        with self._lock:
            if new_name not in self._modes:
                raise InvalidTransitionError(f"Unknown target '{new_name}'")
            if new_name == self._current:
                return
            prev = self._current
            self._modes[prev].exit(self)
            if record_history:
                self._history.append(prev)
            self._current = new_name
            self._modes[new_name].enter(self)
            for fn in list(self._listeners):
                try:
                    fn(prev, new_name)
                except Exception:
                    pass

    def revert(self):
        with self._lock:
            if not self._history:
                raise InvalidTransitionError("No previous mode to revert to")
            prev = self._history.pop()
            self.switch_mode(prev, record_history=False)

    def current(self) -> str:
        with self._lock:
            return self._current

if __name__ == "__main__":
    ctx = Context()
    ctx.add_listener(lambda old, new: print(f"Transition: {old} -> {new}"))

    print("Initial:", ctx.current())
    ctx.handle("start")
    print("After start:", ctx.current())

    time.sleep(1)
    ctx.handle("pause")
    print("After pause:", ctx.current())

    try:
        ctx.handle("invalid_event")
    except InvalidTransitionError as e:
        print("Caught invalid event:", e)

    ctx.handle("resume")
    print("After resume:", ctx.current())

    print("Waiting for auto-pause (2s)...")
    time.sleep(3)
    print("After auto transition:", ctx.current())

    ctx.revert()
    print("After revert:", ctx.current())

    ctx.handle("stop")
    print("Final:", ctx.current())