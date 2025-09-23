from abc import ABC, abstractmethod

class Bulb:
    def __init__(self, name):
        self.name = name
        self.is_on = False
        self.brightness = 0

    def activate(self):
        self.is_on = True
        print(f"{self.name} activated")

    def deactivate(self):
        self.is_on = False
        self.brightness = 0
        print(f"{self.name} deactivated")

    def adjust_brightness(self, level):
        if self.is_on:
            self.brightness = max(0, min(100, level))
            print(f"{self.name} brightness set to {self.brightness}")

    def get_brightness(self):
        return self.brightness

class Operation(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Activate(Operation):
    def __init__(self, bulb):
        self.bulb = bulb
        self.prev_on = self.bulb.is_on
        self.prev_bright = self.bulb.get_brightness()

    def execute(self):
        if not self.bulb.is_on:
            self.bulb.activate()

    def undo(self):
        if self.prev_on:
            self.bulb.activate()
            self.bulb.brightness = self.prev_bright
            print(f"{self.bulb.name} restored: on, brightness {self.prev_bright}")
        else:
            self.bulb.deactivate()

class AdjustBrightness(Operation):
    def __init__(self, bulb, level):
        self.bulb = bulb
        self.level = level
        self.prev_on = self.bulb.is_on
        self.prev_bright = self.bulb.get_brightness()

    def execute(self):
        self.bulb.adjust_brightness(self.level)

    def undo(self):
        if self.prev_on:
            self.bulb.activate()
            self.bulb.brightness = self.prev_bright
            print(f"{self.bulb.name} restored: on, brightness {self.prev_bright}")
        else:
            self.bulb.deactivate()
            print(f"{self.bulb.name} restored: off")

class CompositeOperation(Operation):
    def __init__(self, operations):
        self.operations = operations[:]

    def execute(self):
        for op in self.operations:
            op.execute()

    def undo(self):
        for op in reversed(self.operations):
            op.undo()

class TaskHandler:
    def __init__(self):
        self.executed_tasks = []

    def perform(self, task):
        task.execute()
        self.executed_tasks.append(task)

    def rollback(self):
        if self.executed_tasks:
            last_task = self.executed_tasks.pop()
            last_task.undo()

if __name__ == "__main__":
    bulb = Bulb("Desk Lamp")
    handler = TaskHandler()

    act = Activate(bulb)
    handler.perform(act)
    handler.rollback()

    adj = AdjustBrightness(bulb, 50)
    handler.perform(adj)
    print(f"After adjust when off: on={bulb.is_on}, bright={bulb.brightness}")
    handler.rollback()
    print(f"After rollback: on={bulb.is_on}, bright={bulb.brightness}")

    act2 = Activate(bulb)
    adj2 = AdjustBrightness(bulb, 80)
    combo = CompositeOperation([act2, adj2])
    handler.perform(combo)
    print(f"After macro: on={bulb.is_on}, bright={bulb.brightness}")
    handler.rollback()
    print(f"After macro rollback: on={bulb.is_on}, bright={bulb.brightness}")