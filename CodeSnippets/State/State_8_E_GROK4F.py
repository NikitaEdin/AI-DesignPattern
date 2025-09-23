class Device:
    def __init__(self):
        self._current_mode = OffMode()

    def set_mode(self, mode):
        self._current_mode = mode

    def press_button(self):
        self._current_mode.press(self)

    def get_status(self):
        return self._current_mode.get_status()

class Mode:
    def press(self, device):
        pass

    def get_status(self):
        return "Unknown"

class OffMode(Mode):
    def press(self, device):
        device.set_mode(OnMode())

    def get_status(self):
        return "Off"

class OnMode(Mode):
    def press(self, device):
        device.set_mode(OffMode())

    def get_status(self):
        return "On"

if __name__ == "__main__":
    dev = Device()
    print(dev.get_status())
    dev.press_button()
    print(dev.get_status())
    dev.press_button()
    print(dev.get_status())