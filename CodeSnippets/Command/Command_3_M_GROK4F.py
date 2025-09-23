class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print("Light is on")
        else:
            print("Light is already on")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print("Light is off")
        else:
            print("Light is already off")

    def undo(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

class ExecutableAction:
    def execute(self):
        pass

    def undo(self):
        pass

class TurnLightOnAction(ExecutableAction):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()

class TurnLightOffAction(ExecutableAction):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()

class ControlPanel:
    def __init__(self):
        self.current_action = None
        self.last_action = None

    def set_action(self, action):
        if isinstance(action, ExecutableAction):
            self.current_action = action
        else:
            raise ValueError("Invalid action provided")

    def press_button(self):
        if self.current_action:
            self.current_action.execute()
            self.last_action = self.current_action
        else:
            print("No action set")

    def undo_last(self):
        if self.last_action:
            self.last_action.undo()
        else:
            print("No action to undo")

if __name__ == "__main__":
    light = Light()
    panel = ControlPanel()

    on_action = TurnLightOnAction(light)
    off_action = TurnLightOffAction(light)

    panel.set_action(on_action)
    panel.press_button()
    panel.undo_last()

    panel.set_action(off_action)
    panel.press_button()
    panel.undo_last()