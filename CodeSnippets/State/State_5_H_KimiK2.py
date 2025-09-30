import random
from abc import ABC, abstractmethod


class Mode(ABC):
    @abstractmethod
    def engage(self, ctx):
        pass

    @abstractmethod
    def update(self, ctx):
        pass


class ConcreteModeA(Mode):
    __slots__ = ()

    def engage(self, ctx):
        ctx.counter += 1
        ctx.energy = max(0, ctx.energy - 3)
        if ctx.energy < 5:
            return ConcreteModeC()
        return self

    def update(self, ctx):
        if ctx.counter > 10:
            return ConcreteModeB()
        return self


class ConcreteModeB(Mode):
    __slots__ = ("_ticks",)

    def __init__(self):
        self._ticks = 0

    def engage(self, ctx):
        ctx.counter += 2
        ctx.energy = max(0, ctx.energy - 1)
        self._ticks += 1
        if self._ticks >= 3:
            return ConcreteModeC()
        return self

    def update(self, ctx):
        if ctx.energy < 2:
            return ConcreteModeA()
        return self


class ConcreteModeC(Mode):
    __slots__ = ("_cycles",)

    def __init__(self):
        self._cycles = 0

    def engage(self, ctx):
        ctx.counter += 1
        ctx.energy = min(100, ctx.energy + 5)
        self._cycles += 1
        if self._cycles >= 2 and ctx.counter > 5:
            return ConcreteModeA()
        return self

    def update(self, ctx):
        if ctx.energy > 90:
            return ConcreteModeB()
        return self


class Context:
    __slots__ = ("_mode", "counter", "energy", "log")

    def __init__(self):
        self._mode = ConcreteModeA()
        self.counter = 0
        self.energy = 20
        self.log = []

    def trigger(self):
        prev = self._mode.__class__.__name__
        self._mode = self._mode.engage(self)
        nxt = self._mode.__class__.__name__
        self.log.append((prev, nxt))

    def refresh(self):
        prev = self._mode.__class__.__name__
        self._mode = self._mode.update(self)
        nxt = self._mode.__class__.__name__
        self.log.append((prev, nxt))


if __name__ == "__main__":
    ctx = Context()
    for _ in range(30):
        ctx.trigger()
        ctx.refresh()
    print("Transitions:", ctx.log)