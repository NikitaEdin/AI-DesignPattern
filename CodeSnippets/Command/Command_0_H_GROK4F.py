from abc import ABC, abstractmethod
from typing import List

class Light:
    def __init__(self, name: str):
        self.name = name
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} is turned on")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} is turned off")

class Operation(ABC):
    def __init__(self, light: Light):
        self.light = light

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class LightOn(Operation):
    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()

class LightOff(Operation):
    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()

class MacroOperation(Operation):
    def __init__(self, light: Light):
        super().__init__(light)
        self.sub_operations: List[Operation] = []

    def add(self, op: Operation):
        if op:
            self.sub_operations.append(op)

    def execute(self):
        for op in self.sub_operations:
            op.execute()

    def undo(self):
        for op in reversed(self.sub_operations):
            op.undo()

class RemoteControl:
    def __init__(self):
        self.current_operation = None
        self.history: List[Operation] = []
        self.redo_stack: List[Operation] = []

    def set_operation(self, op: Operation):
        if op:
            self.current_operation = op
            self.redo_stack.clear()

    def press_button(self):
        if self.current_operation:
            self.current_operation.execute()
            self.history.append(self.current_operation)
            self.current_operation = None

    def undo_last(self):
        if self.history:
            last_op = self.history.pop()
            last_op.undo()
            self.redo_stack.append(last_op)

    def redo_last(self):
        if self.redo_stack:
            redo_op = self.redo_stack.pop()
            redo_op.execute()
            self.history.append(redo_op)

if __name__ == "__main__":
    living_room_light = Light("Living Room Light")
    remote = RemoteControl()

    on_op = LightOn(living_room_light)
    off_op = LightOff(living_room_light)

    remote.set_operation(on_op)
    remote.press_button()
    remote.undo_last()
    remote.redo_last()

    macro = MacroOperation(living_room_light)
    macro.add(LightOn(living_room_light))
    macro.add(LightOff(living_room_light))

    remote.set_operation(macro)
    remote.press_button()
    remote.undo_last()