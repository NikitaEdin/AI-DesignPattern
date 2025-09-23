from abc import ABC, abstractmethod

class ModeBase(ABC):
    @abstractmethod
    def on_enter(self, controller):
        pass

    @abstractmethod
    def handle(self, controller, event):
        pass

class IdleMode(ModeBase):
    def on_enter(self, controller):
        print("Entering idle mode")

    def handle(self, controller, event):
        if event == "start":
            controller.change_mode(ProcessingMode())
        elif event == "error":
            controller.change_mode(ErrorMode("unexpected_start_error"))
        else:
            print(f"Idle: unrecognized event '{event}'")

class ProcessingMode(ModeBase):
    def on_enter(self, controller):
        print("Processing started")

    def handle(self, controller, event):
        if event == "complete":
            controller.change_mode(IdleMode())
        elif event == "fail":
            controller.change_mode(ErrorMode("processing_failed"))
        else:
            print(f"Processing: unrecognized event '{event}'")

class ErrorMode(ModeBase):
    def __init__(self, reason):
        self.reason = reason

    def on_enter(self, controller):
        print(f"Entered error mode: {self.reason}")

    def handle(self, controller, event):
        if event == "reset":
            controller.revert_mode()
        elif event == "clear":
            controller.change_mode(IdleMode())
        else:
            print(f"Error: unrecognized event '{event}'")

class Controller:
    def __init__(self, initial_mode, max_history=5):
        if not isinstance(initial_mode, ModeBase):
            raise ValueError("initial_mode must implement ModeBase")
        self.current = initial_mode
        self.history = []
        self.max_history = max_history
        self.current.on_enter(self)

    def change_mode(self, new_mode):
        if not isinstance(new_mode, ModeBase):
            raise ValueError("new_mode must implement ModeBase")
        if self.current is not None:
            self.history.append(self.current)
            if len(self.history) > self.max_history:
                self.history.pop(0)
        self.current = new_mode
        self.current.on_enter(self)

    def revert_mode(self):
        if not self.history:
            print("No previous mode to revert to")
            return
        self.current = self.history.pop()
        self.current.on_enter(self)

    def handle_event(self, event):
        try:
            self.current.handle(self, event)
        except Exception as exc:
            print("Exception during handling:", exc)
            self.change_mode(ErrorMode(str(exc)))

if __name__ == "__main__":
    controller = Controller(IdleMode())
    controller.handle_event("start")
    controller.handle_event("unknown")
    controller.handle_event("fail")
    controller.handle_event("reset")
    controller.handle_event("complete")
    controller.handle_event("start")
    controller.handle_event("fail")
    controller.handle_event("clear")