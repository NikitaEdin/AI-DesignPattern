class LightReceiver:
    def turn_on(self):
        print("Light turned on")

    def turn_off(self):
        print("Light turned off")

class LightOnCommand:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.turn_on()

class LightOffCommand:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.turn_off()

# Usage example in a main section
if __name__ == "__main__":
    light_receiver = LightReceiver()
    light_on_command = LightOnCommand(light_receiver)
    light_off_command = LightOffCommand(light_receiver)

    light_on_command.execute()
    light_off_command.execute()