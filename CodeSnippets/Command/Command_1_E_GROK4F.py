class Light:
    def turn_on(self):
        print("Light is on")

    def turn_off(self):
        print("Light is off")

class Instruction:
    def execute(self):
        pass

class TurnOnInstruction(Instruction):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

class TurnOffInstruction(Instruction):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

class RemoteControl:
    def __init__(self):
        self.current_instruction = None

    def set_instruction(self, instruction):
        self.current_instruction = instruction

    def press_button(self):
        self.current_instruction.execute()

if __name__ == "__main__":
    light = Light()
    turn_on = TurnOnInstruction(light)
    turn_off = TurnOffInstruction(light)
    remote = RemoteControl()
    remote.set_instruction(turn_on)
    remote.press_button()
    remote.set_instruction(turn_off)
    remote.press_button()