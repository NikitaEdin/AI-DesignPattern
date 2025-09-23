from abc import ABC, abstractmethod
from threading import RLock
from typing import Optional, List


class InvalidTransitionError(Exception):
    pass


class ModeBase(ABC):
    def __init__(self, machine: "Machine"):
        self.machine = machine

    def enter(self, previous: Optional["ModeBase"]) -> None:
        pass

    def exit(self, next_mode: Optional["ModeBase"]) -> None:
        pass

    def start(self) -> None:
        raise InvalidTransitionError(f"start not allowed in {self.__class__.__name__}")

    def pause(self) -> None:
        raise InvalidTransitionError(f"pause not allowed in {self.__class__.__name__}")

    def resume(self) -> None:
        raise InvalidTransitionError(f"resume not allowed in {self.__class__.__name__}")

    def stop(self) -> None:
        raise InvalidTransitionError(f"stop not allowed in {self.__class__.__name__}")

    def handle_event(self, event: str, **kwargs) -> None:
        raise InvalidTransitionError(f"event handling not allowed in {self.__class__.__name__}")


class IdleMode(ModeBase):
    def enter(self, previous: Optional["ModeBase"]) -> None:
        print("Entering Idle")

    def start(self) -> None:
        print("Idle: start requested")
        self.machine.change_mode(RunningMode(self.machine))


class RunningMode(ModeBase):
    def enter(self, previous: Optional["ModeBase"]) -> None:
        print("Entering Running")

    def pause(self) -> None:
        print("Running: pause requested")
        self.machine.change_mode(PausedMode(self.machine))

    def stop(self) -> None:
        print("Running: stop requested")
        self.machine.change_mode(IdleMode(self.machine))

    def handle_event(self, event: str, **kwargs) -> None:
        print(f"Running handling event '{event}' with {kwargs}")
        if event == "error":
            self.machine.push_mode(ErrorMode(self.machine, reason=kwargs.get("reason")))


class PausedMode(ModeBase):
    def enter(self, previous: Optional["ModeBase"]) -> None:
        print("Entering Paused")

    def resume(self) -> None:
        print("Paused: resume requested")
        self.machine.change_mode(RunningMode(self.machine))

    def stop(self) -> None:
        print("Paused: stop requested")
        self.machine.change_mode(IdleMode(self.machine))


class ErrorMode(ModeBase):
    def __init__(self, machine: "Machine", reason: Optional[str] = None):
        super().__init__(machine)
        self.reason = reason

    def enter(self, previous: Optional["ModeBase"]) -> None:
        print(f"Entering Error: {self.reason}")

    def stop(self) -> None:
        print("Error: acknowledged, returning to previous mode if any")
        self.machine.pop_mode()

    def handle_event(self, event: str, **kwargs) -> None:
        print(f"Error mode ignoring event '{event}'")


class Machine:
    def __init__(self, initial: ModeBase):
        self._lock = RLock()
        self._current: ModeBase = initial
        self._history: List[ModeBase] = []
        self._current.enter(None)

    def current_name(self) -> str:
        with self._lock:
            return self._current.__class__.__name__

    def change_mode(self, new_mode: ModeBase) -> None:
        with self._lock:
            if new_mode is self._current:
                return
            old = self._current
            old.exit(new_mode)
            self._current = new_mode
            new_mode.enter(old)

    def push_mode(self, new_mode: ModeBase) -> None:
        with self._lock:
            print(f"Pushing {new_mode.__class__.__name__} (saving {self._current.__class__.__name__})")
            self._history.append(self._current)
            old = self._current
            old.exit(new_mode)
            self._current = new_mode
            new_mode.enter(old)

    def pop_mode(self) -> None:
        with self._lock:
            if not self._history:
                raise InvalidTransitionError("No previous mode to return to")
            previous = self._history.pop()
            old = self._current
            old.exit(previous)
            self._current = previous
            previous.enter(old)

    def start(self) -> None:
        with self._lock:
            self._current.start()

    def pause(self) -> None:
        with self._lock:
            self._current.pause()

    def resume(self) -> None:
        with self._lock:
            self._current.resume()

    def stop(self) -> None:
        with self._lock:
            self._current.stop()

    def handle_event(self, event: str, **kwargs) -> None:
        with self._lock:
            self._current.handle_event(event, **kwargs)


if __name__ == "__main__":
    m = Machine(IdleMode(None))
    m._current.machine = m
    try:
        m.start()
        m.handle_event("tick", value=1)
        m.pause()
        m.resume()
        m.handle_event("error", reason="overflow")
        m.stop()
        m.stop()
    except InvalidTransitionError as e:
        print("Caught transition error:", e)