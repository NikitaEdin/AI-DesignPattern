import threading
import time
from abc import ABC, abstractmethod
from typing import Optional, Type, Any


class TransitionError(Exception):
    pass


class ModeBase(ABC):
    def __init__(self, controller: "ModeController"):
        self.controller = controller

    @property
    @abstractmethod
    def label(self) -> str:
        pass

    def enter(self, **meta: Any) -> None:
        pass

    def exit(self) -> None:
        pass

    @abstractmethod
    def handle(self, event: str, **payload: Any) -> Optional[object]:
        """
        Return values:
         - None: consume event, remain in current mode
         - Mode subclass: switch to that mode
         - ("revert",): go back to previous mode
         - ("switch", Mode subclass, record_history: bool)
        """
        pass


class IdleMode(ModeBase):
    @property
    def label(self) -> str:
        return "idle"

    def enter(self, **meta: Any) -> None:
        pass

    def handle(self, event: str, **payload: Any) -> Optional[object]:
        if event == "activate":
            if payload.get("token") == "open":
                return ActiveMode
            return LockedMode
        if event == "status":
            return None
        raise TransitionError(f"Idle cannot handle '{event}'")


class ActiveMode(ModeBase):
    @property
    def label(self) -> str:
        return "active"

    def enter(self, **meta: Any) -> None:
        pass

    def handle(self, event: str, **payload: Any) -> Optional[object]:
        if event == "pause":
            return ("switch", PausedMode, True)
        if event == "stop":
            return IdleMode
        if event == "timeout":
            return LockedMode
        if event == "status":
            return None
        raise TransitionError(f"Active cannot handle '{event}'")


class PausedMode(ModeBase):
    @property
    def label(self) -> str:
        return "paused"

    def enter(self, **meta: Any) -> None:
        pass

    def handle(self, event: str, **payload: Any) -> Optional[object]:
        if event == "resume":
            return ("revert",)
        if event == "stop":
            return IdleMode
        raise TransitionError(f"Paused cannot handle '{event}'")


class LockedMode(ModeBase):
    @property
    def label(self) -> str:
        return "locked"

    def enter(self, **meta: Any) -> None:
        pass

    def handle(self, event: str, **payload: Any) -> Optional[object]:
        if event == "unlock" and payload.get("key") == "letme":
            return ("revert",)
        if event == "force":
            return IdleMode
        raise TransitionError(f"Locked cannot handle '{event}'")


class ModeController:
    def __init__(self, initial: Type[ModeBase]):
        self._lock = threading.RLock()
        self._current: ModeBase = initial(self)
        self._previous: Optional[ModeBase] = None
        self._current.enter()
        self._log = []

    @property
    def current_label(self) -> str:
        with self._lock:
            return self._current.label

    def switch_mode(self, target: Type[ModeBase], record_history: bool = True, reason: Optional[str] = None) -> None:
        with self._lock:
            if isinstance(self._current, target):
                return
            old = self._current
            try:
                old.exit()
            except Exception:
                pass
            if record_history:
                self._previous = old
            else:
                self._previous = None
            self._current = target(self)
            try:
                self._current.enter(reason=reason)
            except Exception:
                pass
            self._log.append((time.time(), old.label, self._current.label, reason))

    def revert_mode(self) -> None:
        with self._lock:
            if not self._previous:
                raise TransitionError("No previous mode to revert to")
            target = type(self._previous)
            self.switch_mode(target, record_history=False, reason="revert")

    def trigger(self, event: str, **payload: Any) -> None:
        with self._lock:
            res = self._current.handle(event, **payload)
            if res is None:
                return
            if isinstance(res, tuple):
                if res[0] == "revert":
                    self.revert_mode()
                    return
                if res[0] == "switch":
                    _, target_cls, record_history = res
                    if not issubclass(target_cls, ModeBase):
                        raise TransitionError("Invalid target for switch")
                    self.switch_mode(target_cls, record_history=bool(record_history), reason=event)
                    return
            if isinstance(res, type) and issubclass(res, ModeBase):
                self.switch_mode(res, record_history=True, reason=event)
                return
            raise TransitionError("Unhandled transition result")

    def dump_log(self) -> list:
        with self._lock:
            return list(self._log)


if __name__ == "__main__":
    ctrl = ModeController(IdleMode)
    print("Initial:", ctrl.current_label)
    try:
        ctrl.trigger("activate", token="wrong")
    except TransitionError as e:
        print("Error:", e)
    print("After failed activate:", ctrl.current_label)
    ctrl.trigger("unlock", key="letme")
    print("After unlock attempt:", ctrl.current_label)
    ctrl.trigger("activate", token="open")
    print("After activate:", ctrl.current_label)
    ctrl.trigger("pause")
    print("After pause:", ctrl.current_label)
    ctrl.trigger("resume")
    print("After resume:", ctrl.current_label)
    ctrl.trigger("timeout")
    print("After timeout:", ctrl.current_label)
    try:
        ctrl.revert_mode()
    except TransitionError as e:
        print("Revert error:", e)
    ctrl.trigger("force")
    print("After force:", ctrl.current_label)
    print("Log:", ctrl.dump_log())