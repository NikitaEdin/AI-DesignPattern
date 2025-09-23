class Command:
    def execute(self):
        pass

class ConcreteCommandA(Command):
    def execute(self):
        print("Executing command A")

class ConcreteCommandB(Command):
    def execute(self):
        print("Executing command B")

class Invoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def remove_command(self, command):
        self.commands.remove(command)

    def execute_commands(self):
        for command in self.commands:
            command.execute()

if __name__ == "__main__":
    invoker = Invoker()
    command_a = ConcreteCommandA()
    command_b = ConcreteCommandB()
    invoker.add_command(command_a)
    invoker.add_command(command_b)
    invoker.execute_commands()