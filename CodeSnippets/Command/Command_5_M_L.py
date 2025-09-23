class RemoteControlSystem:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def remove_command(self, command):
        if command in self.commands:
            self.commands.remove(command)

    def execute_all(self):
        for command in self.commands:
            command.execute()

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()