class Light:
    def on(self):
        print("Light is on")

    def off(self):
        print("Light is off")

class Action:
    def execute(self):
        pass

    def undo(self):
        pass

class LightOnAction(Action):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

class LightOffAction(Action):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()

class RemoteControl:
    def __init__(self):
        self.current_action = None
        self.last_action = None

    def set_action(self, action):
        if not isinstance(action, Action):
            raise ValueError("Invalid action provided")
        self.current_action = action

    def press_button(self):
        if self.current_action is None:
            print("No action set")
            return
        self.current_action.execute()
        self.last_action = self.current_action

    def press_undo(self):
        if self.last_action is None:
            print("No action to undo")
            return
        self.last_action.undo()

if __name__ == "__main__":
    light = Light()
    on_action = LightOnAction(light)
    off_action = LightOffAction(light)
    remote = RemoteControl()
    remote.set_action(on_action)
    remote.press_button()
    remote.press_undo()
    remote.set_action(off_action)
    remote.press_button()
    remote.press_undo()