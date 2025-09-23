from abc import ABC, abstractmethod

class SignalPhase(ABC):
    def __init__(self, controller):
        self.controller = controller

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def transition(self):
        pass

class RedPhase(SignalPhase):
    def display(self):
        return "Stop"

    def transition(self):
        self.controller.current_phase = YellowPhase(self.controller)

class YellowPhase(SignalPhase):
    def display(self):
        return "Caution"

    def transition(self):
        self.controller.current_phase = GreenPhase(self.controller)

class GreenPhase(SignalPhase):
    def display(self):
        return "Go"

    def transition(self):
        self.controller.current_phase = RedPhase(self.controller)

class IntersectionManager:
    def __init__(self):
        self.current_phase = RedPhase(self)

    def change_phase(self):
        try:
            self.current_phase.transition()
        except AttributeError:
            raise ValueError("Invalid phase transition")

    def get_status(self):
        return self.current_phase.display()

if __name__ == "__main__":
    manager = IntersectionManager()
    print(manager.get_status())  # Stop
    manager.change_phase()
    print(manager.get_status())  # Caution
    manager.change_phase()
    print(manager.get_status())  # Go
    manager.change_phase()
    print(manager.get_status())  # Stop