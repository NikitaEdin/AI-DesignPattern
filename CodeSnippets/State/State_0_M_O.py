from abc import ABC, abstractmethod
from datetime import datetime

class ModeBase(ABC):
    @abstractmethod
    def on_enter(self, controller):
        pass

    @abstractmethod
    def on_exit(self, controller):
        pass

    @abstractmethod
    def handle_event(self, controller, event):
        pass

class LockedMode(ModeBase):
    def on_enter(self, controller):
        controller.status = "locked"

    def on_exit(self, controller):
        pass

    def handle_event(self, controller, event):
        if event == "insert_key":
            controller.set_mode(UnlockedMode())
        elif event == "force_open":
            controller.set_mode(AlarmedMode())
        else:
            raise ValueError(f"LockedMode cannot handle '{event}'")

class UnlockedMode(ModeBase):
    def on_enter(self, controller):
        controller.status = "unlocked"
        controller.last_unlocked = datetime.utcnow()

    def on_exit(self, controller):
        pass

    def handle_event(self, controller, event):
        if event in ("close", "timeout"):
            controller.set_mode(LockedMode())
        elif event == "force_open":
            controller.set_mode(AlarmedMode())
        else:
            raise ValueError(f"UnlockedMode cannot handle '{event}'")

class AlarmedMode(ModeBase):
    def on_enter(self, controller):
        controller.status = "alarmed"
        controller.alerts += 1

    def on_exit(self, controller):
        pass

    def handle_event(self, controller, event):
        if event == "reset":
            controller.set_mode(LockedMode())
        else:
            raise ValueError(f"AlarmedMode cannot handle '{event}'")

class DoorController:
    def __init__(self, initial_mode):
        self.history = []
        self.status = None
        self.last_unlocked = None
        self.alerts = 0
        self.current = None
        self.set_mode(initial_mode)

    def set_mode(self, new_mode):
        if not all(hasattr(new_mode, m) for m in ("on_enter", "on_exit", "handle_event")):
            raise TypeError("Invalid mode object")
        old = self.current
        if old:
            old.on_exit(self)
        self.current = new_mode
        self.history.append((type(new_mode).__name__, datetime.utcnow()))
        new_mode.on_enter(self)

    def request(self, event):
        if not self.current:
            raise RuntimeError("No active mode")
        try:
            self.current.handle_event(self, event)
        except Exception as exc:
            return f"error: {exc}"
        return f"ok: {self.status}"

if __name__ == "__main__":
    controller = DoorController(LockedMode())
    sequence = ["insert_key", "force_open", "reset", "insert_key", "timeout"]
    for ev in sequence:
        result = controller.request(ev)
        print(ev, "->", result, "| current:", controller.status, "| alerts:", controller.alerts)
    print("History:", controller.history)