from abc import ABC, abstractmethod
import time
import weakref
import threading
import traceback


class ModeContext:
    def __init__(self):
        self._mode = OffMode(self)
        self._history = []
        self._lock = threading.Lock()

    def transition(self, mode_cls):
        with self._lock:
            old = self._mode
            self._history.append(type(old).__name__)
            self._mode = mode_cls(self)
            self._mode.enter()

    def signal(self, s):
        with self._lock:
            try:
                self._mode.handle(s)
            except Exception as e:
                self.transition(FailMode)

    def __repr__(self):
        return f"ModeContext({type(self._mode).__name__})"


class BaseMode(ABC):
    def __init__(self, ctx):
        self._ctx_ref = weakref.ref(ctx)

    @property
    def ctx(self):
        return self._ctx_ref()

    @abstractmethod
    def enter(self): ...

    @abstractmethod
    def handle(self, s): ...


class OffMode(BaseMode):
    def enter(self):
        self.log("enter")

    def handle(self, s):
        if s == "ON":
            self.ctx.transition(OnMode)
        else:
            self.mode_error(s)

    def log(self, msg):
        print(f"OffMode {msg}")

    def mode_error(self, s):
        print(f"OffMode: unexpected signal {s}")
        self.ctx.transition(FailMode)


class OnMode(BaseMode):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.count = 0

    def enter(self):
        self.log("enter")

    def handle(self, s):
        if s == "OFF":
            self.ctx.transition(OffMode)
        elif s == "STANDBY":
            self.ctx.transition(StandbyMode)
        elif s == "ON":
            self.count += 1
            self.log("duplicate ON")
            if self.count > 1:
                self.ctx.transition(FailMode)
        else:
            self.mode_error(s)

    def log(self, msg):
        print(f"OnMode {msg}")

    def mode_error(self, s):
        print(f"OnMode: unexpected signal {s}")
        self.ctx.transition(FailMode)


class StandbyMode(BaseMode):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.t0 = None

    def enter(self):
        self.t0 = time.time()
        self.log("enter")

    def handle(self, s):
        if s == "ON":
            if time.time() - self.t0 > 0.1:
                self.ctx.transition(OnMode)
            else:
                self.log("too fast - ignored")
        elif s == "OFF":
            self.ctx.transition(OffMode)
        else:
            self.mode_error(s)

    def log(self, msg):
        print(f"StandbyMode {msg}")

    def mode_error(self, wip):
        self.ctx.transition(FailMode)


class FailMode(BaseMode):
    def enter(self):
        print("FAILURE: transition to fail-safe")

    def handle(self, s):
        print("FailMode: ignoring all signals")


def main():
    c = ModeContext()
    c.signal("ON")
    c.signal("STANDBY")
    c.signal("ON")
    c.signal("JUNK")
    print("HISTORY:", c._history)


if __name__ == "__main__":
    main()