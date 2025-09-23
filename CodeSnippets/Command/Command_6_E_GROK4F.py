class Device:
    def __init__(self):
        self.state = "off"

    def turn_on(self):
        self.state = "on"
        print("Device is on")

    def turn_off(self):
        self.state = "off"
        print("Device is off")

class TurnOn:
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_on()

class TurnOff:
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_off()

class Button:
    def __init__(self, operation):
        self.operation = operation

    def press(self):
        self.operation.execute()

if __name__ == "__main__":
    device = Device()
    on_op = TurnOn(device)
    off_op = TurnOff(device)
    button = Button(on_op)
    button.press()
    button.operation = off_op
    button.press()