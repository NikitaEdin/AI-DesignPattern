from abc import ABC, abstractmethod

class ActionBase(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Light:
    def __init__(self, name):
        self.name = name
        self.is_on = False

    def turn_on(self):
        if self.is_on:
            raise RuntimeError(f"{self.name} is already on")
        self.is_on = True
        print(f"{self.name} turned on")

    def turn_off(self):
        if not self.is_on:
            raise RuntimeError(f"{self.name} is already off")
        self.is_on = False
        print(f"{self.name} turned off")

class TurnOn(ActionBase):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_on()

    def undo(self):
        self.device.turn_off()

class TurnOff(ActionBase):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_off()

    def undo(self):
        self.device.turn_on()

class Sequence(ActionBase):
    def __init__(self, actions):
        self.actions = list(actions)
        self._executed = []

    def execute(self):
        self._executed = []
        for act in self.actions:
            try:
                act.execute()
                self._executed.append(act)
            except Exception as e:
                print(f"Error during sequence: {e}")
                break

    def undo(self):
        for act in reversed(self._executed):
            try:
                act.undo()
            except Exception as e:
                print(f"Error undoing sequence: {e}")

class Controller:
    def __init__(self):
        self.slots = {}
        self.history = []

    def assign(self, slot_name, action):
        if not isinstance(action, ActionBase):
            raise TypeError("Assigned object must implement ActionBase")
        self.slots[slot_name] = action

    def trigger(self, slot_name):
        action = self.slots.get(slot_name)
        if action is None:
            print(f"No action assigned to slot '{slot_name}'")
            return
        try:
            action.execute()
            self.history.append(action)
        except Exception as e:
            print(f"Execution failed: {e}")

    def undo_last(self):
        if not self.history:
            print("No actions to undo")
            return
        action = self.history.pop()
        try:
            action.undo()
        except Exception as e:
            print(f"Undo failed: {e}")

if __name__ == "__main__":
    living = Light("Living Room")
    kitchen = Light("Kitchen")

    on_living = TurnOn(living)
    off_living = TurnOff(living)
    on_kitchen = TurnOn(kitchen)

    evening_sequence = Sequence([on_living, on_kitchen])

    remote = Controller()
    remote.assign("living_on", on_living)
    remote.assign("living_off", off_living)
    remote.assign("evening", evening_sequence)

    remote.trigger("living_on")
    remote.trigger("living_on")
    remote.undo_last()
    remote.trigger("evening")
    remote.undo_last()
    remote.trigger("unknown_slot")