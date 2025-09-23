from abc import ABC, abstractmethod

class LightBehavior(ABC):
    @abstractmethod
    def display(self, controller):
        pass

    @abstractmethod
    def transition(self, controller):
        pass

class GreenLight(LightBehavior):
    def display(self, controller):
        print("Green light: Proceed")

    def transition(self, controller):
        controller.current_handler = YellowLight()

class YellowLight(LightBehavior):
    def display(self, controller):
        print("Yellow light: Prepare to stop")

    def transition(self, controller):
        controller.current_handler = RedLight()

class RedLight(LightBehavior):
    def display(self, controller):
        print("Red light: Stop")

    def transition(self, controller):
        controller.current_handler = GreenLight()

class TrafficController:
    def __init__(self):
        self.current_handler = RedLight()

    def show_status(self):
        self.current_handler.display(self)

    def change_signal(self):
        try:
            self.current_handler.transition(self)
        except Exception:
            print("Invalid transition attempted")

if __name__ == "__main__":
    controller = TrafficController()
    for _ in range(6):
        controller.show_status()
        controller.change_signal()