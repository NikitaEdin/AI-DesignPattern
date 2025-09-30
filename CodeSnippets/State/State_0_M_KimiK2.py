from abc import ABC, abstractmethod
import itertools
import time

class Phase(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def next(self, light):
        pass
    def __str__(self):
        return self.name

class GreenPhase(Phase):
    def __init__(self):
        super().__init__("Green")
    def next(self, light):
        light.phase = YellowPhase()

class YellowPhase(Phase):
    def __init__(self):
        super().__init__("Yellow")
    def next(self, light):
        light.phase = RedPhase()

class RedPhase(Phase):
    def __init__(self):
        super().__init__("Red")
    def next(self, light):
        light.phase = GreenPhase()

class TrafficLight:
    def __init__(self):
        self.phase = GreenPhase()
    def switch(self):
        self.phase.next(self)
    def __str__(self):
        return str(self.phase)

def main():
    light = TrafficLight()
    try:
        for _ in itertools.count():
            print(light)
            time.sleep(1)
            light.switch()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()