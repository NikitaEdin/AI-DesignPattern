from abc import ABC, abstractmethod

class ModeBase(ABC):
    @property
    @abstractmethod
    def label(self) -> str:
        pass

    @abstractmethod
    def on_coin(self, context):
        pass

    @abstractmethod
    def on_push(self, context):
        pass

class LockedMode(ModeBase):
    @property
    def label(self) -> str:
        return "locked"

    def on_coin(self, context):
        context._set_mode(UnlockedMode())
        return "Coin accepted, gate unlocked."

    def on_push(self, context):
        raise RuntimeError("Gate locked. Insert coin first.")

class UnlockedMode(ModeBase):
    @property
    def label(self) -> str:
        return "unlocked"

    def on_coin(self, context):
        return "Already unlocked. Coin returned."

    def on_push(self, context):
        context._set_mode(LockedMode())
        return "Passed through, gate locked again."

class Turnstile:
    def __init__(self, initial: ModeBase = None):
        self.history = []
        self.current_mode = initial or LockedMode()

    def _set_mode(self, new_mode: ModeBase):
        if not isinstance(new_mode, ModeBase):
            raise TypeError("Invalid mode object.")
        prev = self.current_mode.label if self.current_mode else None
        self.current_mode = new_mode
        self.history.append((prev, new_mode.label))

    def insert_coin(self):
        try:
            result = self.current_mode.on_coin(self)
            return result
        except Exception as e:
            return f"Error: {e}"

    def push_through(self):
        try:
            result = self.current_mode.on_push(self)
            return result
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    gate = Turnstile()
    actions = [
        ("coin", gate.insert_coin),
        ("push", gate.push_through),
        ("push", gate.push_through),
        ("coin", gate.insert_coin),
        ("coin", gate.insert_coin),
        ("push", gate.push_through),
    ]
    for name, action in actions:
        print(f"Action: {name} -> {action()}")
    print("Transition history:", gate.history)