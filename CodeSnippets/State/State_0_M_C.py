class Context:
    def __init__(self):
        self._current_mode = OffMode()
    
    def set_mode(self, mode):
        self._current_mode = mode
    
    def press_button(self):
        try:
            self._current_mode.handle_press(self)
        except AttributeError:
            raise ValueError("Invalid mode configured")
    
    def get_status(self):
        return self._current_mode.__class__.__name__.replace('Mode', '')

class OffMode:
    def handle_press(self, context):
        print("Turning on - Low brightness")
        context.set_mode(LowMode())

class LowMode:
    def handle_press(self, context):
        print("Switching to medium brightness")
        context.set_mode(MediumMode())

class MediumMode:
    def handle_press(self, context):
        print("Switching to high brightness")
        context.set_mode(HighMode())

class HighMode:
    def handle_press(self, context):
        print("Turning off")
        context.set_mode(OffMode())

if __name__ == "__main__":
    lamp = Context()
    
    for i in range(6):
        print(f"Press {i+1}: Status = {lamp.get_status()}")
        lamp.press_button()
        print()