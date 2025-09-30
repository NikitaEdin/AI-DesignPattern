import time

class Light:
    def __init__(self, room):
        self.room = room
        self.is_on = False

    def on(self):
        self.is_on = True
        print(f"{self.room} light is on")

    def off(self):
        self.is_on = False
        print(f"{self.room} light is off")


class Switch:
    def __init__(self):
        self.history = []

    def record(self, request):
        self.history.append(request)

    def execute(self, request):
        request.execute()
        self.record(request)

    def replay_last(self):
        if self.history:
            self.history[-1].execute()


class LightRequest:
    def __init__(self, light, action):
        self.light = light
        self.action = action

    def execute(self):
        if self.action == "on":
            self.light.on()
        elif self.action == "off":
            self.light.off()

    def undo(self):
        if self.action == "on":
            self.light.off()
        elif self.action == "off":
            self.light.on()


if __name__ == "__main__":
    living_room = Light("Living Room")
    switch = Switch()

    switch.execute(LightRequest(living_room, "on"))
    time.sleep(1)
    switch.execute(LightRequest(living_room, "off"))
    switch.replay_last()