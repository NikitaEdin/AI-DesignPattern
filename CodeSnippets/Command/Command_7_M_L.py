class Light:
    def __init__(self, is_on):
        self._is_on = is_on
    
    @property
    def is_on(self):
        return self._is_on
    
    @is_on.setter
    def is_on(self, value):
        self._is_on = value
    
    def turn_on(self):
        if not self._is_on:
            self._is_on = True
    
    def turn_off(self):
        if self._is_on:
            self._is_on = False
    
    def toggle(self):
        self._is_on = not self._is_on

class LightCommand:
    def __init__(self, light):
        self._light = light
    
    def execute(self):
        if self._light.is_on:
            self._light.turn_off()
        else:
            self._light.turn_on()

class RemoteControl:
    def __init__(self, light):
        self._light = light
    
    def set_command(self, command):
        self._command = command
    
    def press_button(self):
        self._command.execute()

if __name__ == "__main__":
    light = Light(False)
    remote = RemoteControl(light)
    remote.set_command(LightCommand(light))
    print("Initial state:", light.is_on)
    remote.press_button()
    print("After pressing button once:", light.is_on)
    remote.press_button()
    print("After pressing button twice:", light.is_on)