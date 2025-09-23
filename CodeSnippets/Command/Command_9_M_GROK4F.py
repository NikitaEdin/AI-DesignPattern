import abc

class Light:
    def turn_on(self):
        print("Light is on")

    def turn_off(self):
        print("Light is off")

class Action(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass

class TurnOn(Action):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()

class TurnOff(Action):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()

class Remote:
    def __init__(self):
        self.current_action = None
        self.last_action = None

    def set_action(self, action):
        if isinstance(action, Action):
            self.current_action = action
        else:
            raise ValueError("Invalid action provided")

    def press_button(self):
        if self.current_action:
            self.current_action.execute()
            self.last_action = self.current_action
        else:
            print("No action set")

    def press_undo(self):
        if self.last_action:
            self.last_action.undo()
        else:
            print("No last action to undo")

if __name__ == "__main__":
    light = Light()
    turn_on_action = TurnOn(light)
    turn_off_action = TurnOff(light)
    remote = Remote()
    remote.set_action(turn_on_action)
    remote.press_button()
    remote.set_action(turn_off_action)
    remote.press_button()
    remote.press_undo()