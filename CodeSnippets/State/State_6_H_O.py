from abc import ABC, abstractmethod
from threading import RLock, Thread
from typing import Optional, List, Type
import time


class TransitionError(RuntimeError):
    pass


class ModeBase(ABC):
    @abstractmethod
    def on_enter(self, context: "Machine"):
        pass

    @abstractmethod
    def on_exit(self, context: "Machine"):
        pass

    @abstractmethod
    def handle(self, context: "Machine", event: str, **kwargs) -> Optional["ModeBase"]:
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


class IdleMode(ModeBase):
    def on_enter(self, context):
        context.log.append("entered idle")

    def on_exit(self, context):
        context.log.append("exited idle")

    def handle(self, context, event, **kwargs):
        if event == "start":
            return ProcessingMode()
        if event == "error":
            return ErrorMode("error occurred before start")
        return None


class ProcessingMode(ModeBase):
    def on_enter(self, context):
        context.log.append("entered processing")
        context.processing_started_at = time.time()

    def on_exit(self, context):
        duration = time.time() - getattr(context, "processing_started_at", time.time())
        context.log.append(f"exited processing after {duration:.2f}s")

    def handle(self, context, event, **kwargs):
        if event == "pause":
            return PausedMode()
        if event == "stop":
            return IdleMode()
        if event == "error":
            return ErrorMode(kwargs.get("message", "processing error"))
        return None


class PausedMode(ModeBase):
    def on_enter(self, context):
        context.log.append("entered paused")

    def on_exit(self, context):
        context.log.append("exited paused")

    def handle(self, context, event, **kwargs):
        if event == "resume":
            return ProcessingMode()
        if event == "stop":
            return IdleMode()
        if event == "error":
            return ErrorMode(kwargs.get("message", "paused error"))
        return None


class ErrorMode(ModeBase):
    def __init__(self, reason: str = ""):
        self.reason = reason

    def on_enter(self, context):
        context.log.append(f"entered error: {self.reason}")

    def on_exit(self, context):
        context.log.append("exited error")

    def handle(self, context, event, **kwargs):
        if event == "reset":
            return IdleMode()
        return None


class Machine:
    def __init__(self, initial: ModeBase):
        self._lock = RLock()
        self.current_mode: ModeBase = initial
        self.history: List[ModeBase] = []
        self.log: List[str] = []
        try:
            self.current_mode.on_enter(self)
        except Exception as exc:
            raise TransitionError("initial enter failed") from exc

    def trigger(self, event: str, **kwargs):
        with self._lock:
            result = self.current_mode.handle(self, event, **kwargs)
            if result is None:
                raise TransitionError(f"event '{event}' not allowed from {self.current_mode}")
            self._transition_to(result)

    def _transition_to(self, new_mode: ModeBase):
        old = self.current_mode
        self.history.append(old)
        try:
            old.on_exit(self)
            self.current_mode = new_mode
            new_mode.on_enter(self)
        except Exception as exc:
            self.current_mode = old
            try:
                old.on_enter(self)
            except Exception:
                pass
            raise TransitionError("transition failed and was rolled back") from exc

    def undo(self, steps: int = 1):
        with self._lock:
            if steps < 1 or steps > len(self.history):
                raise TransitionError("invalid undo steps")
            target = self.history[-steps]
            self.history = self.history[:-steps]
            try:
                self.current_mode.on_exit(self)
            except Exception:
                pass
            self.current_mode = target
            try:
                self.current_mode.on_enter(self)
            except Exception as exc:
                raise TransitionError("undo enter failed") from exc

    def snapshot(self):
        with self._lock:
            return (repr(self.current_mode), list(self.log))


if __name__ == "__main__":
    m = Machine(IdleMode())

    def worker(name, events):
        for ev in events:
            try:
                m.trigger(ev)
            except TransitionError as e:
                m.log.append(f"{name} failed {ev}: {e}")
            time.sleep(0.05)

    t1 = Thread(target=worker, args=("T1", ["start", "pause", "resume", "stop"]))
    t2 = Thread(target=worker, args=("T2", ["start", "error", "reset"]))
    t1.start(); t2.start()
    t1.join(); t2.join()

    try:
        m.trigger("start")
        m.trigger("error", message="fatal")
    except TransitionError:
        pass

    print("current:", m.snapshot()[0])
    for entry in m.log:
        print(entry)