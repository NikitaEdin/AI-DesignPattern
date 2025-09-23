import threading
import logging
from abc import ABC, abstractmethod
from typing import Callable, List, Optional

logging.basicConfig(level=logging.INFO)


class TransitionError(Exception):
    pass


class HandlerError(Exception):
    pass


class ModeBase(ABC):
    name: str

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__

    def can_enter(self, previous: "ModeBase") -> bool:
        return True

    def enter(self, manager: "ModeManager"):
        return None

    def exit(self, manager: "ModeManager"):
        return None

    def handle(self, manager: "ModeManager", event):
        raise NotImplementedError


class IdleMode(ModeBase):
    def handle(self, manager, event):
        if event == "start":
            manager.transition_to(RunningMode())
        else:
            raise NotImplementedError


class RunningMode(ModeBase):
    def can_enter(self, previous: ModeBase) -> bool:
        return isinstance(previous, (IdleMode, SuspendedMode))

    def handle(self, manager, event):
        if event == "pause":
            manager.transition_to(SuspendedMode())
        elif event == "stop":
            manager.transition_to(IdleMode())
        else:
            raise NotImplementedError


class SuspendedMode(ModeBase):
    def can_enter(self, previous: ModeBase) -> bool:
        return isinstance(previous, RunningMode)

    def handle(self, manager, event):
        if event == "resume":
            manager.transition_to(RunningMode())
        elif event == "stop":
            manager.transition_to(IdleMode())
        else:
            raise NotImplementedError


class ModeManager:
    def __init__(self, initial: ModeBase):
        self._lock = threading.RLock()
        self._current: ModeBase = initial
        self._history: List[ModeBase] = []
        self._listeners: List[Callable[[ModeBase, ModeBase], None]] = []

    @property
    def current(self) -> ModeBase:
        with self._lock:
            return self._current

    def add_listener(self, fn: Callable[[ModeBase, ModeBase], None]):
        with self._lock:
            self._listeners.append(fn)

    def remove_listener(self, fn: Callable[[ModeBase, ModeBase], None]):
        with self._lock:
            self._listeners.remove(fn)

    def transition_to(self, new_mode: ModeBase, force: bool = False, skip_if_same: bool = False):
        previous = None
        listeners = []
        with self._lock:
            previous = self._current
            if skip_if_same and type(previous) is type(new_mode):
                return
            if not force and not new_mode.can_enter(previous):
                raise TransitionError(f"cannot enter {new_mode.name} from {previous.name}")
            try:
                previous.exit(self)
                new_mode.enter(self)
            except Exception as exc:
                # Attempt rollback
                try:
                    previous.enter(self)
                except Exception as rollback_exc:
                    raise TransitionError(f"transition failed and rollback failed: {exc!r}, {rollback_exc!r}")
                raise TransitionError(f"transition failed but rolled back: {exc!r}")
            # successful
            self._current = new_mode
            self._history.append(previous)
            listeners = list(self._listeners)
        # notify outside lock
        for fn in listeners:
            try:
                fn(previous, new_mode)
            except Exception:
                logging.exception("listener raised")

    def undo_last(self):
        with self._lock:
            if not self._history:
                raise TransitionError("no history to undo")
            target = self._history.pop()
        # use force to allow returning to previous even if can_enter rejects
        self.transition_to(target, force=True)

    def dispatch(self, event):
        try:
            handler = None
            with self._lock:
                handler = self._current.handle
            return handler(self, event)
        except NotImplementedError:
            raise HandlerError(f"handler not implemented for {self.current.name} and event {event!r}")
        except Exception as exc:
            raise HandlerError(f"handler error: {exc!r}")


if __name__ == "__main__":
    mgr = ModeManager(IdleMode())

    def print_transition(prev, cur):
        print(f"Transitioned from {prev.name} to {cur.name}")

    mgr.add_listener(print_transition)

    # Normal flow
    mgr.dispatch("start")   # Idle -> Running
    mgr.dispatch("pause")   # Running -> Suspended
    mgr.dispatch("resume")  # Suspended -> Running
    mgr.dispatch("stop")    # Running -> Idle

    # Undo last (should go back to Running)
    mgr.undo_last()
    print("Current after undo:", mgr.current.name)