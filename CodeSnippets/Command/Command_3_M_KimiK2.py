class Light:
    def __init__(self):
        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on


class Fan:
    def __init__(self):
        self.speed = 0

    def set_speed(self, value):
        self.speed = value


class LightToggle:
    def __init__(self, light):
        self.light = light
        self.prev_state = None

    def execute(self):
        self.prev_state = self.light.is_on
        self.light.toggle()

    def undo(self):
        self.light.is_on = self.prev_state


class FanCycle:
    def __init__(self, fan):
        self.fan = fan
        self.prev_speed = None

    def execute(self):
        self.prev_speed = self.fan.speed
        self.fan.set_speed((self.fan.speed + 1) % 4)

    def undo(self):
        self.fan.set_speed(self.prev_speed)


class Remote:
    def __init__(self):
        self.history = []

    def invoke(self, task):
        task.execute()
        self.history.append(task)

    def revert(self):
        if self.history:
            self.history.pop().undo()


if __name__ == "__main__":
    light = Light()
    fan = Fan()
    remote = Remote()

    light_task = LightToggle(light)
    fan_task = FanCycle(fan)

    remote.invoke(light_task)
    remote.invoke(fan_task)
    remote.revert()
    remote.revert()