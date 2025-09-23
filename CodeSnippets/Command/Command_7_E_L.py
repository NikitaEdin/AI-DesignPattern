class Invoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_all_commands(self):
        for command in self.commands:
            command.execute()

class Receiver:
    def __init__(self):
        self.status = "Idle"

    def do_something(self):
        print("Receiver: Something")
        self.status = "Busy"

    def get_status(self):
        return self.status

class Command:
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.do_something()

if __name__ == "__main__":
    # Create a new instance of the Receiver class
    r = Receiver()

    # Create a new instance of the Command class with the receiver as an argument
    c1 = Command(r)
    c2 = Command(r)

    # Create a new instance of the Invoker class and add both commands to it
    i = Invoker()
    i.add_command(c1)
    i.add_command(c2)

    # Execute all commands in the invoker
    i.execute_all_commands()