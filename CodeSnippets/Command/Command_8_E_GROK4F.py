class Device:
    def __init__(self):
        self.state = "off"

    def turn_on(self):
        self.state = "on"
        print("Device is on")

    def turn_off(self):
        self.state = "off"
        print("Device is off")

class Operation:
    def execute(self):
        pass

class TurnOn(Operation):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_on()

class TurnOff(Operation):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.turn_off()

class Remote:
    def __init__(self):
        self.current_operation = None

    def set_operation(self, operation):
        self.current_operation = operation

    def press_button(self):
        if self.current_operation:
            self.current_operation.execute()

if __name__ == "__main__":
    device = Device()
    remote = Remote()
    remote.set_operation(TurnOn(device))
    remote.press_button()
    remote.set_operation(TurnOff(device))
    remote.press_button()