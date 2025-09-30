import time

class Light:
    def __init__(self, location):
        self.location = location
        self.on = False

    def turn_on(self):
        if self.on:
            raise RuntimeError("Light already on")
        self.on = True
        print(f"{self.location} light is on")

    def turn_off(self):
        if not self.on:
            raise RuntimeError("Light already off")
        self.on = False
        print(f"{self.location} light is off")


class Action:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


class LightOnAction(Action):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()


class LightOffAction(Action):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()


class RemoteControl:
    def __init__(self):
        self.history = []

    def press(self, action):
        action.execute()
        self.history.append(action)

    def undo_last(self):
        if not self.history:
            raise IndexError("No actions to undo")
        last_action = self.history.pop()
        last_action.undo()


if __name__ == "__main__":
    living_room_light = Light("Living Room")
    remote = RemoteControl()

    on = LightOnAction(living_room_light)
    off = LightOffAction(living_room_light)

    remote.press(on)
    time.sleep(0.1)
    remote.press(off)
    time.sleep(0.1)
    remote.undo_last()
    remote.undo_last()