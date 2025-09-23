from abc import ABC, abstractmethod

class MathEngine:
    def __init__(self):
        self.value = 0

    def add(self, num):
        if not isinstance(num, (int, float)):
            raise ValueError("Number must be an integer or float")
        self.value += num

    def subtract(self, num):
        if not isinstance(num, (int, float)):
            raise ValueError("Number must be an integer or float")
        self.value -= num

class Action(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddAction(Action):
    def __init__(self, engine, num):
        self.engine = engine
        self.num = num
        self.prev_value = None

    def execute(self):
        self.prev_value = self.engine.value
        self.engine.add(self.num)

    def undo(self):
        if self.prev_value is not None:
            self.engine.value = self.prev_value

class SubtractAction(Action):
    def __init__(self, engine, num):
        self.engine = engine
        self.num = num
        self.prev_value = None

    def execute(self):
        self.prev_value = self.engine.value
        self.engine.subtract(self.num)

    def undo(self):
        if self.prev_value is not None:
            self.engine.value = self.prev_value

class ActionRunner:
    def __init__(self):
        self.actions = []

    def perform(self, action):
        action.execute()
        self.actions.append(action)

    def undo_last(self):
        if self.actions:
            last_action = self.actions.pop()
            last_action.undo()

if __name__ == "__main__":
    engine = MathEngine()
    runner = ActionRunner()

    add_op = AddAction(engine, 5)
    runner.perform(add_op)
    print(f"After add: {engine.value}")

    subtract_op = SubtractAction(engine, 3)
    runner.perform(subtract_op)
    print(f"After subtract: {engine.value}")

    runner.undo_last()
    print(f"After undo subtract: {engine.value}")

    runner.undo_last()
    print(f"After undo add: {engine.value}")