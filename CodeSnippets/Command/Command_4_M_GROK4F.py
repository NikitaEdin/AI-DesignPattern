import abc

class Device(abc.ABC):
    @abc.abstractmethod
    def activate(self):
        pass

    @abc.abstractmethod
    def deactivate(self):
        pass

class Light(Device):
    def __init__(self):
        self.is_on = False

    def activate(self):
        if not self.is_on:
            self.is_on = True
            print("Light turned on")
        else:
            print("Light is already on")

    def deactivate(self):
        if self.is_on:
            self.is_on = False
            print("Light turned off")
        else:
            print("Light is already off")

class Action(abc.ABC):
    @abc.abstractmethod
    def perform(self):
        pass

    @abc.abstractmethod
    def reverse(self):
        pass

class LightOnAction(Action):
    def __init__(self, light):
        self.light = light

    def perform(self):
        try:
            self.light.activate()
        except Exception as e:
            print(f"Error activating light: {e}")

    def reverse(self):
        try:
            self.light.deactivate()
        except Exception as e:
            print(f"Error reversing light activation: {e}")

class LightOffAction(Action):
    def __init__(self, light):
        self.light = light

    def perform(self):
        try:
            self.light.deactivate()
        except Exception as e:
            print(f"Error deactivating light: {e}")

    def reverse(self):
        try:
            self.light.activate()
        except Exception as e:
            print(f"Error reversing light deactivation: {e}")

class Remote:
    def __init__(self):
        self.current_action = None

    def set_action(self, action):
        self.current_action = action

    def press(self):
        if self.current_action:
            self.current_action.perform()
        else:
            print("No action set")

    def undo(self):
        if self.current_action:
            self.current_action.reverse()
        else:
            print("No action to undo")

if __name__ == "__main__":
    light = Light()
    on_action = LightOnAction(light)
    off_action = LightOffAction(light)

    remote = Remote()
    remote.set_action(on_action)
    remote.press()
    remote.undo()

    remote.set_action(off_action)
    remote.press()
    remote.undo()