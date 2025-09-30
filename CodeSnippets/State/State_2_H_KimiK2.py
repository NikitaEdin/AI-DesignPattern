import random

class TrafficLight:
    def __init__(self):
        self._phase = RedPhase(self)
    def switch(self):
        self._phase = self._phase.next()
    def report(self):
        return self._phase.status()
    def __str__(self):
        return self.report()

class Phase:
    def __init__(self, light):
        self.light = light
    def next(self):
        raise NotImplementedError
    def status(self):
        raise NotImplementedError

class RedPhase(Phase):
    def next(self):
        return GreenPhase(self.light)
    def status(self):
        return "🔴 RED"

class GreenPhase(Phase):
    def next(self):
        return YellowPhase(self.light)
    def status(self):
        return "🟢 GREEN"

class YellowPhase(Phase):
    def next(self):
        return RedPhase(self.light)
    def status(self):
        return "🟡 YELLOW"

class BrokenPhase(Phase):
    def next(self):
        return random.choice([RedPhase, GreenPhase, YellowPhase])(self.light) if random.random() > 0.1 else self
    def status(self):
        return "⚠️  MALFUNCTION"

class AdaptiveTrafficLight(TrafficLight):
    def __init__(self):
        super().__init__()
        self._phase = RedPhase(self)
        self._faulty = False
    def break_light(self):
        self._faulty = True
        self._phase = BrokenPhase(self)
    def fix(self):
        self._faulty = False
        self._phase = RedPhase(self)

if __name__ == "__main__":
    tl = AdaptiveTrafficLight()
    for _ in range(10):
        print(tl)
        tl.switch()
    tl.break_light()
    for _ in range(5):
        print(tl)
        tl.switch()
    tl.fix()
    print(tl)