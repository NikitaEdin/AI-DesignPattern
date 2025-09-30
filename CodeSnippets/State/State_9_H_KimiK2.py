from abc import ABC, abstractmethod
import time

class TrafficLightContext:
    def __init__(self):
        self._current = GreenPhase()
        self._last_switch = time.time()
    def change(self):
        self._current = self._current.next()
        self._last_switch = time.time()
    def report(self):
        return self._current.info()
    def urgent_override(self):
        self._current = BlinkingRedPhase()
    def _raw_elapsed(self):
        return time.time() - self._last_switch

class PhaseInterface(ABC):
    @abstractmethod
    def next(self): ...
    @abstractmethod
    def info(self): ...

class GreenPhase(PhaseInterface):
    def next(self):
        return YellowPhase()
    def info(self):
        return "GREEN - vehicles may proceed"

class YellowPhase(PhaseInterface):
    def next(self):
        return RedPhase()
    def info(self):
        return "YELLOW - prepare to stop"

class RedPhase(PhaseInterface):
    def next(self):
        return GreenPhase()
    def info(self):
        return "RED - vehicles must stop"

class BlinkingRedPhase(PhaseInterface):
    def __init__(self):
        self._ticks = 0
    def next(self):
        self._ticks += 1
        return self if self._ticks < 5 else GreenPhase()
    def info(self):
        return "BLINKING RED - emergency mode"

if __name__ == "__main__":
    controller = TrafficLightContext()
    for _ in range(7):
        print(controller.report())
        controller.change()
    controller.urgent_override()
    while True:
        print(controller.report())
        controller.change()
        if isinstance(controller._current, GreenPhase):
            break