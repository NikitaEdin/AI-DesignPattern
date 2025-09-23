class LightOnCommand(object):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

class LightOffCommand(object):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()

class RemoteControl(object):
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def add_command(self, command):
        self.undo_stack.append(command)

    def undo(self):
        if len(self.undo_stack) > 0:
            command = self.undo_stack.pop()
            command.execute()
            self.redo_stack.append(command)

    def redo(self):
        if len(self.redo_stack) > 0:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)