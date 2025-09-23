import threading
from abc import ABC, abstractmethod
from typing import Optional


class TransitionError(Exception):
    pass


class TransitionInProgressError(TransitionError):
    pass


class InvalidTransitionError(TransitionError):
    pass


class BaseMode(ABC):
    @abstractmethod
    def enter_mode(self, context: "ModeContext"):
        pass

    @abstractmethod
    def exit_mode(self, context: "ModeContext"):
        pass

    @abstractmethod
    def handle_event(self, context: "ModeContext", event: str):
        pass

    def can_enter_from(self, previous: Optional["BaseMode"]) -> bool:
        return True


class IdleMode(BaseMode):
    def enter_mode(self, context: "ModeContext"):
        context._log("Entering Idle")

    def exit_mode(self, context: "ModeContext"):
        context._log("Exiting Idle")

    def handle_event(self, context: "ModeContext", event: str):
        if event == "start":
            context.change_mode(ActiveMode())
            return "started"
        return "ignored"


class ActiveMode(BaseMode):
    def enter_mode(self, context: "ModeContext"):
        context._log("Entering Active")
        context._work_count = 0

    def exit_mode(self, context: "ModeContext"):
        context._log("Exiting Active")

    def handle_event(self, context: "ModeContext", event: str):
        if event == "pause":
            context.change_mode(PausedMode())
            return "paused"
        if event == "stop":
            context.change_mode(IdleMode())
            return "stopped"
        if event == "work":
            context._work_count += 1
            return f"worked:{context._work_count}"
        return "unknown"


class PausedMode(BaseMode):
    def enter_mode(self, context: "ModeContext"):
        context._log("Entering Paused")

    def exit_mode(self, context: "ModeContext"):
        context._log("Exiting Paused")

    def handle_event(self, context: "ModeContext", event: str):
        if event == "resume":
            context.restore_previous_mode()
            return "resumed"
        if event == "stop":
            context.change_mode(IdleMode())
            return "stopped"
        return "ignored"

    def can_enter_from(self, previous: Optional["BaseMode"]) -> bool:
        return isinstance(previous, ActiveMode)


class ModeContext:
    def __init__(self, initial: BaseMode):
        self._lock = threading.RLock()
        self._current: BaseMode = initial
        self._previous: Optional[BaseMode] = None
        self._in_transition = False
        self._work_count = 0
        self._current.enter_mode(self)

    def _log(self, message: str):
        print(f"[Context] {message}")

    def change_mode(self, new_mode: BaseMode):
        with self._lock:
            if self._in_transition:
                raise TransitionInProgressError("Transition already in progress")
            if new_mode is None:
                raise InvalidTransitionError("Target mode is None")
            if type(new_mode) is type(self._current):
                self._log("No transition: already in requested mode")
                return
            if not new_mode.can_enter_from(self._current):
                raise InvalidTransitionError("Transition not allowed from current mode")
            self._in_transition = True
            try:
                self._current.exit_mode(self)
                self._previous = self._current
                self._current = new_mode
                self._current.enter_mode(self)
            finally:
                self._in_transition = False

    def restore_previous_mode(self):
        with self._lock:
            if self._previous is None:
                raise InvalidTransitionError("No previous mode to restore")
            self.change_mode(self._previous)

    def handle(self, event: str):
        with self._lock:
            if self._in_transition:
                raise TransitionInProgressError("Cannot handle events during transition")
            try:
                return self._current.handle_event(self, event)
            except TransitionError:
                raise
            except Exception as exc:
                raise TransitionError(f"Unhandled exception in handler: {exc}") from exc


if __name__ == "__main__":
    ctx = ModeContext(IdleMode())
    print(ctx.handle("start"))
    print(ctx.handle("work"))
    print(ctx.handle("work"))
    print(ctx.handle("pause"))
    print(ctx.handle("work"))
    print(ctx.handle("resume"))
    print(ctx.handle("work"))
    print(ctx.handle("stop"))
    try:
        ctx.restore_previous_mode()
    except TransitionError as e:
        print("Expected error:", e)