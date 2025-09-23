from abc import ABC, abstractmethod
from typing import List

class ModeBase(ABC):
    @abstractmethod
    def handle_insert(self, controller):
        pass

    @abstractmethod
    def handle_push(self, controller):
        pass

    @abstractmethod
    def handle_fix(self, controller):
        pass

class LockedMode(ModeBase):
    def handle_insert(self, controller):
        controller._set_mode(UnlockedMode())
        return "Key accepted. Unlocked."

    def handle_push(self, controller):
        return "Door is locked. Cannot open."

    def handle_fix(self, controller):
        return "No repair needed while locked."

class UnlockedMode(ModeBase):
    def handle_insert(self, controller):
        controller._set_mode(LockedMode())
        return "Key turned. Locked."

    def handle_push(self, controller):
        controller._set_mode(LockedMode())
        return "Door opened and closed, then auto-locked."

    def handle_fix(self, controller):
        return "No repair needed while unlocked."

class JammedMode(ModeBase):
    def handle_insert(self, controller):
        raise RuntimeError("Mechanism jammed. Cannot insert key.")

    def handle_push(self, controller):
        raise RuntimeError("Door is jammed. Cannot push.")

    def handle_fix(self, controller):
        controller._set_mode(LockedMode())
        return "Mechanism repaired. Locked."

class DoorController:
    def __init__(self):
        self._mode: ModeBase = LockedMode()
        self._history: List[str] = ["Locked"]

    def _set_mode(self, new_mode: ModeBase):
        name = new_mode.__class__.__name__.replace("Mode", "")
        self._mode = new_mode
        self._history.append(name)

    def insert_key(self):
        try:
            return self._mode.handle_insert(self)
        except Exception as e:
            return f"Error: {e}"

    def push(self):
        try:
            return self._mode.handle_push(self)
        except Exception as e:
            return f"Error: {e}"

    def fix_mechanism(self):
        try:
            return self._mode.handle_fix(self)
        except Exception as e:
            return f"Error: {e}"

    def report(self):
        return {"current": self._mode.__class__.__name__.replace("Mode", ""), "history": list(self._history)}

if __name__ == "__main__":
    door = DoorController()
    print(door.report())
    print(door.insert_key())
    print(door.report())
    print(door.push())
    print(door.report())
    door._set_mode(JammedMode())
    print(door.report())
    print(door.push())
    print(door.insert_key())
    print(door.fix_mechanism())
    print(door.report())