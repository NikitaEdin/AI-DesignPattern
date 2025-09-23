import threading
from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional, List

class TransitionError(Exception):
    pass

class ModeBase(ABC):
    def __init__(self, name: str):
        self.name = name
        self.event_handlers: Dict[str, Callable[..., Optional[str]]] = {}
        self.transition_guards: Dict[str, Callable[..., bool]] = {}

    def set_event_handler(self, event: str, handler: Callable[..., Optional[str]]):
        self.event_handlers[event] = handler

    def set_guard(self, target: str, guard: Callable[..., bool]):
        self.transition_guards[target] = guard

    def handle_event(self, event: str, context: "ContextEngine", **kwargs) -> Optional[str]:
        handler = self.event_handlers.get(event)
        if not handler:
            raise TransitionError(f"No handler for event '{event}' in mode '{self.name}'")
        return handler(context, **kwargs)

    def can_transition(self, target: str, **kwargs) -> bool:
        guard = self.transition_guards.get(target)
        return True if guard is None else bool(guard(**kwargs))

    def on_enter(self, context: "ContextEngine", **kwargs):
        pass

    def on_exit(self, context: "ContextEngine"):
        pass

class OffMode(ModeBase):
    def __init__(self):
        super().__init__("off")
        self.set_event_handler("power", lambda ctx, **k: "standby")

class StandbyMode(ModeBase):
    def __init__(self):
        super().__init__("standby")
        self.set_event_handler("start", lambda ctx, **k: "running")
        self.set_event_handler("power", lambda ctx, **k: "off")
        self.set_guard("running", lambda **k: k.get("allowed", True))
    def on_enter(self, context, **kwargs):
        pass

class RunningMode(ModeBase):
    def __init__(self):
        super().__init__("running")
        self.set_event_handler("stop", lambda ctx, **k: "standby")
        self.set_event_handler("fail", lambda ctx, **k: "off")
        self.set_guard("standby", lambda **k: True)
    def on_enter(self, context, **kwargs):
        pass

class ContextEngine:
    def __init__(self, history_limit: int = 10):
        self._modes: Dict[str, ModeBase] = {}
        self._lock = threading.RLock()
        self.current: Optional[ModeBase] = None
        self._history: List[str] = []
        self._history_limit = max(0, history_limit)

    def register(self, mode: ModeBase):
        with self._lock:
            self._modes[mode.name] = mode

    def start(self, mode_name: str, **kwargs):
        with self._lock:
            if mode_name not in self._modes:
                raise TransitionError(f"Unknown mode '{mode_name}'")
            if self.current and self.current.name == mode_name:
                return
            new_mode = self._modes[mode_name]
            if self.current:
                self.current.on_exit(self)
                if self._history_limit != 0:
                    self._history.append(self.current.name)
                    if len(self._history) > self._history_limit:
                        self._history.pop(0)
            self.current = new_mode
            self.current.on_enter(self, **kwargs)

    def trigger(self, event: str, **kwargs):
        with self._lock:
            if not self.current:
                raise TransitionError("No active mode to handle events")
            target = self.current.handle_event(event, self, **kwargs)
            if not target:
                return
            if target not in self._modes:
                raise TransitionError(f"Target '{target}' not registered")
            if not self.current.can_transition(target, **kwargs):
                raise TransitionError(f"Transition from '{self.current.name}' to '{target}' blocked by guard")
            if self.current.name == target:
                return
            self.current.on_exit(self)
            if self._history_limit != 0:
                self._history.append(self.current.name)
                if len(self._history) > self._history_limit:
                    self._history.pop(0)
            self.current = self._modes[target]
            self.current.on_enter(self, **kwargs)

    def revert(self):
        with self._lock:
            if not self._history:
                raise TransitionError("No history to revert to")
            previous = self._history.pop()
            if previous not in self._modes:
                raise TransitionError(f"Previous mode '{previous}' not available")
            if self.current:
                self.current.on_exit(self)
            self.current = self._modes[previous]
            self.current.on_enter(self)

if __name__ == "__main__":
    engine = ContextEngine(history_limit=5)
    off = OffMode()
    standby = StandbyMode()
    running = RunningMode()
    engine.register(off)
    engine.register(standby)
    engine.register(running)
    engine.start("off")
    print("Current:", engine.current.name)
    engine.trigger("power")
    print("Current:", engine.current.name)
    try:
        engine.trigger("start", allowed=False)
    except TransitionError as e:
        print("Blocked:", e)
    engine.trigger("start", allowed=True)
    print("Current:", engine.current.name)
    engine.trigger("fail")
    print("Current:", engine.current.name)
    try:
        engine.revert()
        print("Reverted to:", engine.current.name)
    except TransitionError as e:
        print("Revert failed:", e)