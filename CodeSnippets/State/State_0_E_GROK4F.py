from abc import ABC, abstractmethod

class Switch:
    def __init__(self):
        self._current_mode = OffMode(self)

    def toggle(self):
        self._current_mode.handle_toggle()

    def set_mode(self, mode):
        self._current_mode = mode

    def get_mode(self):
        return self._current_mode.__class__.__name__

class Mode(ABC):
    def __init__(self, switch):
        self._switch = switch

    @abstractmethod
    def handle_toggle(self):
        pass

class OffMode(Mode):
    def handle_toggle(self):
        print("Switching on.")
        self._switch.set_mode(OnMode(self._switch))

class OnMode(Mode):
    def handle_toggle(self):
        print("Switching off.")
        self._switch.set_mode(OffMode(self._switch))

if __name__ == "__main__":
    s = Switch()
    print(f"Initial: {s.get_mode()}")
    s.toggle()
    print(f"After toggle: {s.get_mode()}")
    s.toggle()
    print(f"After toggle: {s.get_mode()}")