class RemoteControl:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        if not isinstance(command, Command):
            raise ValueError("Command must be an instance of the Command class")
        self.commands.append(command)

    def remove_command(self, command):
        if not isinstance(command, Command):
            raise ValueError("Command must be an instance of the Command class")
        self.commands.remove(command)

    def execute_all(self):
        for command in self.commands:
            command.execute()

class Command:
    def __init__(self, receiver, action):
        self.receiver = receiver
        self.action = action

    def execute(self):
        getattr(self.receiver, self.action)()