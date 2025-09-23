from abc import ABC, abstractmethod

class ModeBase(ABC):
    @abstractmethod
    def handle(self, controller, action):
        pass

class IdleMode(ModeBase):
    def handle(self, controller, action):
        if action == "start":
            controller.switch_to(WorkingMode())
            return "Started working"
        raise ValueError(f"Unsupported action '{action}' in idle")

class WorkingMode(ModeBase):
    def handle(self, controller, action):
        if action == "work":
            return "Working... progress made"
        if action == "pause":
            controller.switch_to(PausedMode())
            return "Paused"
        if action == "stop":
            controller.switch_to(IdleMode())
            return "Stopped and idle"
        raise ValueError(f"Unsupported action '{action}' while working")

class PausedMode(ModeBase):
    def handle(self, controller, action):
        if action == "resume":
            controller.switch_to(WorkingMode())
            return "Resumed work"
        if action == "stop":
            controller.switch_to(IdleMode())
            return "Stopped from pause"
        raise ValueError(f"Unsupported action '{action}' while paused")

class Controller:
    def __init__(self, initial_mode):
        if not isinstance(initial_mode, ModeBase):
            raise TypeError("Initial mode must implement ModeBase")
        self.current = initial_mode
        self.history = []

    def switch_to(self, new_mode):
        if not isinstance(new_mode, ModeBase):
            raise TypeError("New mode must implement ModeBase")
        self.history.append(self.current)
        self.current = new_mode

    def execute(self, action):
        try:
            return self.current.handle(self, action)
        except Exception as exc:
            raise

    def undo_mode(self):
        if not self.history:
            raise RuntimeError("No previous mode to revert to")
        self.current = self.history.pop()
        return f"Reverted to {self.current.__class__.__name__}"

if __name__ == "__main__":
    controller = Controller(IdleMode())
    print(controller.execute("start"))
    print(controller.execute("work"))
    print(controller.execute("pause"))
    print(controller.execute("resume"))
    print(controller.execute("stop"))
    print(controller.undo_mode())
    try:
        print(controller.execute("invalid"))
    except Exception as e:
        print("Error caught:", type(e).__name__, str(e))
    try:
        controller.switch_to("not a mode")
    except Exception as e:
        print("Error caught:", type(e).__name__, str(e))