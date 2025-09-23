from abc import ABC, abstractmethod
from typing import Dict, Tuple, Type, Optional, List
import threading
import time

class TransitionError(Exception):
    pass

class ModeError(Exception):
    pass

class ModeBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def enter(self, controller: "Controller", payload=None):
        return None

    def exit(self, controller: "Controller"):
        return None

    @abstractmethod
    def handle(self, controller: "Controller", event: str, payload=None):
        pass

class Controller:
    def __init__(self):
        self._lock = threading.RLock()
        self._modes: Dict[str, Type[ModeBase]] = {}
        self._transitions: Dict[Tuple[str, str], str] = {}
        self._current: Optional[ModeBase] = None
        self._history: List[str] = []

    def register_mode(self, mode_cls: Type[ModeBase]):
        if not issubclass(mode_cls, ModeBase):
            raise ModeError("Only ModeBase subclasses may be registered")
        self._modes[mode_cls().name] = mode_cls

    def register_transition(self, from_mode: str, event: str, to_mode: str):
        if from_mode == to_mode:
            raise TransitionError("Refusing no-op transition")
        self._transitions[(from_mode, event)] = to_mode

    def set_initial(self, mode_name: str, payload=None):
        with self._lock:
            if mode_name not in self._modes:
                raise ModeError("Unknown mode")
            mode_cls = self._modes[mode_name]
            new = mode_cls()
            self._current = new
            new.enter(self, payload)

    def trigger(self, event: str, payload=None):
        with self._lock:
            if self._current is None:
                raise ModeError("No initial mode set")
            current_name = self._current.name
            key = (current_name, event)
            if key in self._transitions:
                target_name = self._transitions[key]
                if target_name not in self._modes:
                    raise TransitionError("Target mode not registered")
                if target_name == current_name:
                    return False
                target_cls = self._modes[target_name]
                self._current.exit(self)
                self._history.append(current_name)
                self._current = target_cls()
                self._current.enter(self, payload)
                return True
            else:
                return self._current.handle(self, event, payload)

    def request_change(self, mode_name: str, payload=None):
        with self._lock:
            if mode_name not in self._modes:
                raise ModeError("Unknown mode requested")
            if self._current and self._current.name == mode_name:
                return False
            if self._current:
                self._current.exit(self)
                self._history.append(self._current.name)
            self._current = self._modes[mode_name]()
            self._current.enter(self, payload)
            return True

    def revert(self, payload=None):
        with self._lock:
            if not self._history:
                raise TransitionError("No history to revert to")
            previous = self._history.pop()
            return self.request_change(previous, payload)

    @property
    def current_name(self) -> Optional[str]:
        return self._current.name if self._current else None

class IdleMode(ModeBase):
    @property
    def name(self) -> str:
        return "idle"

    def enter(self, controller: Controller, payload=None):
        pass

    def exit(self, controller: Controller):
        pass

    def handle(self, controller: Controller, event: str, payload=None):
        if event == "status":
            return "idle"
        return False

class RunningMode(ModeBase):
    @property
    def name(self) -> str:
        return "running"

    def enter(self, controller: Controller, payload=None):
        pass

    def exit(self, controller: Controller):
        pass

    def handle(self, controller: Controller, event: str, payload=None):
        if event == "status":
            return "running"
        if event == "suspend":
            controller.trigger("pause")
            return "suspended requested"
        return False

class PausedMode(ModeBase):
    @property
    def name(self) -> str:
        return "paused"

    def enter(self, controller: Controller, payload=None):
        pass

    def exit(self, controller: Controller):
        pass

    def handle(self, controller: Controller, event: str, payload=None):
        if event == "status":
            return "paused"
        return False

if __name__ == "__main__":
    ctrl = Controller()
    ctrl.register_mode(IdleMode)
    ctrl.register_mode(RunningMode)
    ctrl.register_mode(PausedMode)

    ctrl.register_transition("idle", "start", "running")
    ctrl.register_transition("running", "pause", "paused")
    ctrl.register_transition("paused", "resume", "running")
    ctrl.register_transition("running", "stop", "idle")

    ctrl.set_initial("idle")
    print(ctrl.current_name, ctrl.trigger("status"))

    print("start->", ctrl.trigger("start"))
    print(ctrl.current_name, ctrl.trigger("status"))

    print("pause via event->", ctrl.trigger("pause"))
    print(ctrl.current_name, ctrl.trigger("status"))

    print("resume->", ctrl.trigger("resume"))
    print(ctrl.current_name, ctrl.trigger("status"))

    print("stop->", ctrl.trigger("stop"))
    print(ctrl.current_name, ctrl.trigger("status"))

    try:
        ctrl.revert()
    except Exception as e:
        print("revert error:", e)

    ctrl.trigger("start")
    print("before revert:", ctrl.current_name)
    ctrl.revert()
    print("after revert:", ctrl.current_name)

    def concurrent_actions(c: Controller):
        for ev in ("start", "pause", "resume", "stop"):
            try:
                res = c.trigger(ev)
                print("thread:", ev, "->", res, "current:", c.current_name)
            except Exception as exc:
                print("thread error:", exc)
            time.sleep(0.01)

    t = threading.Thread(target=concurrent_actions, args=(ctrl,))
    t.start()
    t.join()