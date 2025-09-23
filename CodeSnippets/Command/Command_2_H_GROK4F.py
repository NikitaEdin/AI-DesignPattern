from abc import ABC, abstractmethod
import sys

class Action(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

class GarageDoor:
    def __init__(self):
        self.is_open = False

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

class TurnOnAction(Action):
    def __init__(self, light):
        self.light = light
        self.saved_state = None

    def execute(self):
        self.saved_state = self.light.is_on
        self.light.turn_on()
        if not self.saved_state:
            print("Light turned on")

    def undo(self):
        if self.saved_state is not None:
            previous = self.light.is_on
            self.light.is_on = self.saved_state
            if previous != self.saved_state:
                status = "on" if self.saved_state else "off"
                print(f"Light turned {status} (undo)")

class TurnOffAction(Action):
    def __init__(self, light):
        self.light = light
        self.saved_state = None

    def execute(self):
        self.saved_state = self.light.is_on
        self.light.turn_off()
        if self.saved_state:
            print("Light turned off")

    def undo(self):
        if self.saved_state is not None:
            previous = self.light.is_on
            self.light.is_on = self.saved_state
            if previous != self.saved_state:
                status = "on" if self.saved_state else "off"
                print(f"Light turned {status} (undo)")

class OpenGarageAction(Action):
    def __init__(self, garage):
        self.garage = garage
        self.saved_state = None

    def execute(self):
        self.saved_state = self.garage.is_open
        self.garage.open()
        if not self.saved_state:
            print("Garage door opened")

    def undo(self):
        if self.saved_state is not None:
            previous = self.garage.is_open
            self.garage.is_open = self.saved_state
            if previous != self.saved_state:
                status = "opened" if self.saved_state else "closed"
                print(f"Garage door {status} (undo)")

class SequenceAction(Action):
    def __init__(self, actions):
        self.actions = actions

    def execute(self):
        for action in self.actions:
            action.execute()

    def undo(self):
        for action in reversed(self.actions):
            action.undo()

class Remote:
    def __init__(self):
        self.current_action = None
        self.history = []

    def assign_action(self, action):
        self.current_action = action

    def trigger(self):
        if self.current_action is None:
            print("No action assigned")
            return
        self.current_action.execute()
        self.history.append(self.current_action)

    def revert_last(self):
        if not self.history:
            print("No actions to revert")
            return
        last_action = self.history.pop()
        last_action.undo()

if __name__ == "__main__":
    light = Light()
    garage = GarageDoor()
    remote = Remote()

    turn_on = TurnOnAction(light)
    remote.assign_action(turn_on)
    remote.trigger()
    remote.revert_last()

    remote.revert_last()

    open_garage = OpenGarageAction(garage)
    sequence = SequenceAction([turn_on, open_garage])
    remote.assign_action(sequence)
    remote.trigger()
    remote.revert_last()

    remote.trigger()