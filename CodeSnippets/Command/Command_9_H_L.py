class Receiver:
    def do_something(self):
        print("Receiver: Doing something")

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

class SimpleCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

class ComplexCommand(Command):
    def __init__(self, receiver):
        super().__init__(receiver)

    def add_subcommand(self, subcommand):
        self.subcommands.append(subcommand)

    def execute(self):
        for subcommand in self.subcommands:
            subcommand.execute()

class Invoker:
    def __init__(self):
        self.stack = []

    def store_and_execute(self, command):
        self.stack.append(command)
        command.execute()

# Usage example
receiver = Receiver()
invoker = Invoker()

simple_command = SimpleCommand(receiver)
complex_command = ComplexCommand(receiver)

invoker.store_and_execute(simple_command)  # Output: "Receiver: Doing something"
invoker.store_and_execute(complex_command)  # Output: "Receiver: Doing something"