from abc import ABC, abstractmethod

class LightBehavior(ABC):
    @abstractmethod
    def display(self, controller):
        pass

    @abstractmethod
    def transition(self, controller):
        pass

class RedBehavior(LightBehavior):
    def display(self, controller):
        print("Red light: Stop")

    def transition(self, controller):
        controller.current_behavior = YellowBehavior()

class YellowBehavior(LightBehavior):
    def display(self, controller):
        print("Yellow light: Caution")

    def transition(self, controller):
        controller.current_behavior = GreenBehavior()

class GreenBehavior(LightBehavior):
    def display(self, controller):
        print("Green light: Go")

    def transition(self, controller):
        controller.current_behavior = RedBehavior()

class TrafficController:
    def __init__(self):
        self.current_behavior = RedBehavior()

    def show_signal(self):
        if self.current_behavior is None:
            raise ValueError("No behavior assigned")
        self.current_behavior.display(self)

    def change_light(self):
        if self.current_behavior is None:
            raise ValueError("No behavior assigned")
        self.current_behavior.transition(self)

if __name__ == "__main__":
    light = TrafficController()
    for _ in range(6):
        light.show_signal()
        light.change_light()