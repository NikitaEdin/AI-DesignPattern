class Command(object):
    def __init__(self, receiver):
        self._receiver = receiver
    
    def execute(self):
        raise NotImplementedError()

class LightOnCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)
    
    def execute(self):
        self._receiver.turn_on()

class LightOffCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)
    
    def execute(self):
        self._receiver.turn_off()

class RemoteControl(object):
    def __init__(self, command):
        self._command = command
    
    def press_button(self):
        self._command.execute()

class Light(object):
    def turn_on(self):
        print("Light is on")
    
    def turn_off(self):
        print("Light is off")

if __name__ == "__main__":
    light = Light()
    remote_control = RemoteControl(LightOnCommand(light))
    remote_control.press_button()