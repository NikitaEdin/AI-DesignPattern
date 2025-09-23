class Fan:
    def __init__(self):
        self.speed = 0

    def speed_up(self):
        self.speed = min(self.speed + 1, 10)
        print(f"Fan speed increased to {self.speed}")

    def speed_down(self):
        self.speed = max(self.speed - 1, 0)
        print(f"Fan speed decreased to {self.speed}")

class Action:
    def execute(self):
        pass

    def undo(self):
        pass

class SpeedUpAction(Action):
    def __init__(self, fan):
        self.fan = fan

    def execute(self):
        self.prev_speed = self.fan.speed
        self.fan.speed_up()

    def undo(self):
        self.fan.speed = self.prev_speed
        print(f"Fan speed reverted to {self.prev_speed}")

class SpeedDownAction(Action):
    def __init__(self, fan):
        self.fan = fan

    def execute(self):
        self.prev_speed = self.fan.speed
        self.fan.speed_down()

    def undo(self):
        self.fan.speed = self.prev_speed
        print(f"Fan speed reverted to {self.prev_speed}")

class Remote:
    def __init__(self):
        self.current_action = None

    def set_action(self, action):
        self.current_action = action

    def press(self):
        if self.current_action is None:
            raise ValueError("No action set")
        self.current_action.execute()

    def undo_last(self):
        if self.current_action is None:
            raise ValueError("No action to undo")
        self.current_action.undo()

if __name__ == "__main__":
    fan = Fan()
    print(f"Initial speed: {fan.speed}")
    remote = Remote()
    up_action = SpeedUpAction(fan)
    remote.set_action(up_action)
    remote.press()
    print(f"After press: {fan.speed}")
    remote.undo_last()
    print(f"After undo: {fan.speed}")